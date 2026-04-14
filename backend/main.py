from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import pandas as pd
from ML.data_loader import DataLoader
from ML.preprocessor import Preprocessor
from ML.eda_engine import EDAEngine
from ML.models.classification import ClassificationModels
from ML.models.regression import RegressionModels
from ML.tuner import MLTuner
from backend.auth import init_db, get_db, save_db, AuthHandler, get_current_user
import hashlib
import joblib
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="MLSuite API")
init_db()

# Mount static files to serve plots
if not os.path.exists("static/plots"):
    os.makedirs("static/plots")
app.mount("/static", StaticFiles(directory="static"), name="static")

class UserAuth(BaseModel):
    email: str
    password: str
    role: Optional[str] = "user"

@app.post("/register")
async def register(user: UserAuth):
    db = get_db()
    if user.email in db["users"]:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Store user data as a dict now instead of just password hash if we want roles
    # But to maintain compatibility with existing hashes, I'll check if it's a dict or string
    db["users"][user.email] = {
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
        "role": user.role if user.role in ["user", "admin"] else "user"
    }
    save_db(db)
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserAuth):
    db = get_db()
    user_data = db["users"].get(user.email)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Handle both old (string) and new (dict) storage formats
    if isinstance(user_data, str):
        pwd_hash = user_data
        role = "user"
    else:
        pwd_hash = user_data["password"]
        role = user_data["role"]

    if pwd_hash != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    token = AuthHandler.create_access_token(user.email, role)
    return {"token": token, "role": role}

@app.get("/admin/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db = get_db()
    return {"users": [{"email": email, "role": (data["role"] if isinstance(data, dict) else "user")} for email, data in db["users"].items()]}

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
STATIC_DIR = "static/plots"
MODELS_DIR = "static/models"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

class Config(BaseModel):
    task_type: str # 'classification' or 'regression'
    target_column: str
    data_source: str = 'file' # 'file', 'sql', 'mongodb'
    connection_string: str = ''
    table_name: str = ''
    db_name: str = ''
    collection_name: str = ''
    tune_hyperparameters: bool = True

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.get("/columns")
async def get_columns(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    if filename.endswith(('.xlsx', '.xls')):
        df = DataLoader.load_excel(file_path)
    else:
        df = DataLoader.load_csv(file_path)
    
    return {"columns": list(df.columns)}

def _get_df_from_params(
    data_source: str,
    filename: str = None,
    connection_string: str = None,
    table_name: str = None,
    connection_uri: str = None,
    db_name: str = None,
    collection_name: str = None
):
    """Helper to load data based on source type and provided params."""
    try:
        if data_source == 'file':
            if not filename:
                raise HTTPException(status_code=400, detail="Filename required for file source")
            file_path = os.path.join(UPLOAD_DIR, filename)
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail=f"File {filename} not found")
            return DataLoader.load_data('file', file_path=file_path)
        
        elif data_source == 'sql':
            if not connection_string or not table_name:
                raise HTTPException(status_code=400, detail="Connection string and table name required for SQL source")
            return DataLoader.load_data('sql', connection_string=connection_string, table_name=table_name)
        
        elif data_source == 'mongodb':
            if not connection_uri or not db_name or not collection_name:
                raise HTTPException(status_code=400, detail="URI, DB name, and Collection name required for MongoDB source")
            return DataLoader.load_data('mongodb', connection_uri=connection_uri, db_name=db_name, collection_name=collection_name)
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported data source: {data_source}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data loading failed: {str(e)}")

@app.get("/analyze")
async def analyze_data(
    filename: str = None,
    data_source: str = 'file',
    connection_string: str = None,
    table_name: str = None,
    connection_uri: str = None,
    db_name: str = None,
    collection_name: str = None
):
    """Performs immediate EDA and returns data insights from any source."""
    df = _get_df_from_params(data_source, filename, connection_string, table_name, connection_uri, db_name, collection_name)
    
    if df.empty:
        raise HTTPException(status_code=400, detail="Loaded dataset is empty")

    # 1. Clear previous plots
    eda = EDAEngine(df, STATIC_DIR)
    eda.clear_plots()
    
    # 2. Generate EDA
    all_plots = eda.generate_all()
    stats = eda.get_data_stats()
    
    return {
        "plots": all_plots,
        "stats": stats,
        "columns": list(df.columns)
    }

@app.get("/models")
async def list_models(task_type: str):
    """Returns available models for classification or regression."""
    if task_type == 'classification':
        return {"models": ClassificationModels().get_model_list()}
    elif task_type == 'regression':
        return {"models": RegressionModels().get_model_list()}
    else:
        raise HTTPException(status_code=400, detail="Invalid task type")

@app.post("/train")
async def train_model(
    task_type: str,
    target_column: str,
    model_name: str,
    filename: str = None,
    data_source: str = 'file',
    connection_string: str = None,
    table_name: str = None,
    connection_uri: str = None,
    db_name: str = None,
    collection_name: str = None,
    tune: bool = False
):
    """Trains a specific model on the dataset from any source."""
    df = _get_df_from_params(data_source, filename, connection_string, table_name, connection_uri, db_name, collection_name)
    
    if df.empty:
        raise HTTPException(status_code=400, detail="Loaded dataset is empty")

    # Preprocess
    preprocessor = Preprocessor(df)
    df = preprocessor.process_all()

    if target_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target '{target_column}' not found")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    results = {}
    tuning_result = None

    # Clear old model plots before training
    for f in os.listdir(STATIC_DIR):
        if f.startswith('model_'):
            os.remove(os.path.join(STATIC_DIR, f))

    if tune:
        # Automated Comparison Mode
        tuning_result = MLTuner.run_automated_comparison(X_train, y_train, X_test, y_test, task_type)
        winner_name = tuning_result['winner_name']
        model_to_save = tuning_result['best_model']
        
        # Extract tuned metrics for the winner from leaderboard
        winner_entry = next(item for item in tuning_result['leaderboard'] if item['model_name'] == winner_name)
        results = {winner_name: {winner_entry['metric_name']: winner_entry['score']}}
        
        # Generate visualizations using the TUNED model
        if task_type == 'classification':
            clf = ClassificationModels()
            clf.generate_visualizations(winner_name, X_test, y_test, STATIC_DIR, trained_model=model_to_save)
        else:
            reg = RegressionModels()
            reg.generate_visualizations(winner_name, X_test, y_test, STATIC_DIR, trained_model=model_to_save)
    else:
        # Single Model Mode
        if task_type == 'classification':
            if model_name == 'auto':
                model_name = ClassificationModels().get_model_list()[0]
            clf = ClassificationModels()
            results = clf.train_and_eval(X_train, X_test, y_train, y_test, selected_model=model_name)
            model_to_save = clf.models[model_name]
            clf.generate_visualizations(model_name, X_test, y_test, STATIC_DIR)
        else:
            if model_name == 'auto':
                model_name = RegressionModels().get_model_list()[0]
            reg = RegressionModels()
            results = reg.train_and_eval(X_train, X_test, y_train, y_test, selected_model=model_name)
            model_to_save = reg.models[model_name]
            reg.generate_visualizations(model_name, X_test, y_test, STATIC_DIR)

    # Save best model
    model_path = os.path.join(MODELS_DIR, "best_model.pkl")
    joblib.dump(model_to_save, model_path)

    # Remove non-serializable scikit-learn model object from response
    if tuning_result and 'best_model' in tuning_result:
        del tuning_result['best_model']

    # Collect only the new model-specific performance plots
    perf_plots = [f for f in os.listdir(STATIC_DIR) if f.startswith('model_')]

    return {
        "results": results,
        "tuning_result": tuning_result,
        "performance_plots": perf_plots,
        "model_url": "/static/models/best_model.pkl",
        "is_auto_selected": tune
    }

@app.post("/process")
async def process_data(filename: str, config: Config):
    # Keep for backward compatibility but implement via new logic
    # (Optional, but let's just keep it for now or return a message)
    return await train_model(filename, config.task_type, config.target_column, "Logistic Regression" if config.task_type == 'classification' else "Linear Regression", config.tune_hyperparameters)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
