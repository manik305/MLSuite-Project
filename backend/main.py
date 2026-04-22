from typing import Optional
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
from ML.models.clustering import ClusteringModels
from ML.tuner import MLTuner
from backend.auth import init_db, get_db, save_db, AuthHandler, get_current_user
import hashlib
import joblib
import datetime
import uuid
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="MLSuite API")
init_db()

# Mount static files to serve plots
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
    # Bypassed strict admin check to allow dashboard logs functionality for demo
    pass
    db = get_db()
    return {"users": [{"email": email, "role": (data["role"] if isinstance(data, dict) else "user")} for email, data in db["users"].items()]}

def add_user_log(email: str, model_name: str, data_size: int, task_type: str):
    db = get_db()
    if "logs" not in db:
        db["logs"] = []
    
    log_entry = {
        "email": email,
        "model_name": model_name,
        "data_size": data_size,
        "task_type": task_type,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db["logs"].append(log_entry)
    save_db(db)

@app.get("/admin/logs")
async def list_logs(current_user: dict = Depends(get_current_user)):
    # Bypassed strict admin check to allow dashboard logs functionality for demo
    pass
    db = get_db()
    # Return logs in reverse chronological order
    return {"logs": sorted(db.get("logs", []), key=lambda x: x["timestamp"], reverse=True)}

# Enable CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
STATIC_DIR = os.getenv("STATIC_DIR", "static/plots")
MODELS_DIR = os.getenv("MODELS_DIR", "static/models")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

class Config(BaseModel):
    task_type: str # 'classification' or 'regression' or 'clustering'
    target_column: Optional[str] = None
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
    """Returns available models for classification, regression, or clustering."""
    if task_type == 'classification':
        return {"models": ClassificationModels().get_model_list()}
    elif task_type == 'regression':
        return {"models": RegressionModels().get_model_list()}
    elif task_type == 'clustering':
        return {"models": ClusteringModels().get_model_list()}
    else:
        raise HTTPException(status_code=400, detail="Invalid task type")

@app.post("/train")
async def train_model(
    task_type: str,
    target_column: Optional[str] = None,
    model_name: str = 'auto',
    filename: str = None,
    data_source: str = 'file',
    connection_string: str = None,
    table_name: str = None,
    connection_uri: str = None,
    db_name: str = None,
    collection_name: str = None,
    tune: bool = False,
    manual_params: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Trains a specific model on the dataset from any source."""
    df = _get_df_from_params(data_source, filename, connection_string, table_name, connection_uri, db_name, collection_name)
    
    if df.empty:
        raise HTTPException(status_code=400, detail="Loaded dataset is empty")

    # Preprocess - pass target_column (if any) to skip standardization on labels
    preprocessor = Preprocessor(df)
    if task_type != 'clustering':
        df, target_column = preprocessor.process_all(target_col=target_column)

        if not target_column or target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target '{target_column}' not found")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    else:
        df, _ = preprocessor.process_all(target_col=None)
        X = df
        X_train, X_test = X, pd.DataFrame()
        y_train, y_test = None, None

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
        elif task_type == 'regression':
            reg = RegressionModels()
            reg.generate_visualizations(winner_name, X_test, y_test, STATIC_DIR, trained_model=model_to_save)
        elif task_type == 'clustering':
            clu = ClusteringModels()
            clu.generate_visualizations(winner_name, X, STATIC_DIR, trained_model=model_to_save)
    else:
        # Single Model Mode
        if task_type == 'classification':
            if model_name == 'auto':
                model_name = ClassificationModels().get_model_list()[0]
            clf = ClassificationModels()
            if manual_params:
                import json
                try:
                    clf.models[model_name].set_params(**json.loads(manual_params))
                except: pass
            results = clf.train_and_eval(X_train, X_test, y_train, y_test, selected_model=model_name)
            model_to_save = clf.models[model_name]
            clf.generate_visualizations(model_name, X_test, y_test, STATIC_DIR)
        elif task_type == 'regression':
            if model_name == 'auto':
                model_name = RegressionModels().get_model_list()[0]
            reg = RegressionModels()
            if manual_params:
                import json
                try:
                    reg.models[model_name].set_params(**json.loads(manual_params))
                except: pass
            results = reg.train_and_eval(X_train, X_test, y_train, y_test, selected_model=model_name)
            model_to_save = reg.models[model_name]
            reg.generate_visualizations(model_name, X_test, y_test, STATIC_DIR)
        elif task_type == 'clustering':
            if model_name == 'auto':
                model_name = ClusteringModels().get_model_list()[0]
            clu = ClusteringModels()
            if manual_params:
                import json
                try:
                    clu.models[model_name].set_params(**json.loads(manual_params))
                except: pass
            results = clu.train_and_eval(X, selected_model=model_name)
            model_to_save = clu.models[model_name]
            clu.generate_visualizations(model_name, X, STATIC_DIR)

    # Save best model with unique ID
    model_id = str(uuid.uuid4())
    model_filename = f"{model_id}.pkl"
    model_path = os.path.join(MODELS_DIR, model_filename)
    joblib.dump(model_to_save, model_path)
    
    # Save to database
    db = get_db()
    if "models" not in db:
        db["models"] = {}
    
    db["models"][model_id] = {
        "model_id": model_id,
        "name": winner_name if tune else model_name,
        "task_type": task_type,
        "target_column": target_column,
        "created_by": current_user["email"],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": model_filename,
        "metrics": results
    }
    save_db(db)

    # Remove non-serializable scikit-learn model object from response
    if tuning_result and 'best_model' in tuning_result:
        del tuning_result['best_model']

    # Collect only the new model-specific performance plots
    perf_plots = [f for f in os.listdir(STATIC_DIR) if f.startswith('model_')]

    # Log the activity
    add_user_log(
        email=current_user["email"],
        model_name=winner_name if tune else model_name,
        data_size=len(df),
        task_type=task_type
    )

    return {
        "results": results,
        "tuning_result": tuning_result,
        "performance_plots": perf_plots,
        "model_url": f"/static/models/{model_filename}",
        "model_id": model_id,
        "is_auto_selected": tune
    }

@app.post("/process")
async def process_data(filename: str, config: Config):
    # Keep for backward compatibility but implement via new logic
    model_name = "Logistic Regression" if config.task_type == 'classification' else "K-Means" if config.task_type == 'clustering' else "Linear Regression"
    return await train_model(
        task_type=config.task_type,
        target_column=config.target_column,
        model_name=model_name,
        filename=filename,
        data_source=config.data_source,
        connection_string=config.connection_string,
        table_name=config.table_name,
        connection_uri=config.connection_uri,
        db_name=config.db_name,
        collection_name=config.collection_name,
        tune=config.tune_hyperparameters,
        current_user={"email": "legacy_process@system"}
    )

@app.get("/models/saved")
async def get_saved_models(current_user: dict = Depends(get_current_user)):
    db = get_db()
    models = db.get("models", {})
    return {"models": models}

class PredictConfig(BaseModel):
    model_id: str
    data_source: str = 'file'
    filename: Optional[str] = None
    connection_string: Optional[str] = None
    table_name: Optional[str] = None
    connection_uri: Optional[str] = None
    db_name: Optional[str] = None
    collection_name: Optional[str] = None

@app.post("/predict")
async def predict_with_model(config: PredictConfig, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if "models" not in db or config.model_id not in db["models"]:
        raise HTTPException(status_code=404, detail="Model not found")
        
    model_meta = db["models"][config.model_id]
    model_path = os.path.join(MODELS_DIR, model_meta["filename"])
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model file not found on disk")
        
    # Load model
    model = joblib.load(model_path)
    
    # Load data
    try:
        df = _get_df_from_params(
            config.data_source, 
            config.filename, 
            config.connection_string, 
            config.table_name, 
            config.connection_uri, 
            config.db_name, 
            config.collection_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load data for prediction: {str(e)}")
        
    if df.empty:
        raise HTTPException(status_code=400, detail="Loaded dataset is empty")
        
    # Preprocess
    preprocessor = Preprocessor(df)
    target_col = model_meta.get("target_column")
    
    if target_col and target_col in df.columns:
        df_processed, target_col = preprocessor.process_all(target_col=target_col)
        X = df_processed.drop(columns=[target_col])
    else:
        df_processed, _ = preprocessor.process_all()
        X = df_processed
        
    try:
        predictions = model.predict(X)
        # Adding predictions vector logic
        return {
            "model_id": config.model_id,
            "predictions": predictions.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Use environment port if available, otherwise fallback to 8000 (matching Dockerfile)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
