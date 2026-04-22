import os
import pandas as pd
import joblib
from ML.data_loader import DataLoader
from ML.preprocessor import Preprocessor
from ML.models.regression import RegressionModels
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def run_benchmark():
    print("Starting ML Model Performance Benchmark...")
    
    # 1. Load a sample dataset (or create dummy data if none exists)
    data_path = "uploads/sample_data.csv"
    if not os.path.exists(data_path):
        print("No sample data found, creating dummy dataset...")
        df = pd.DataFrame({
            'feature1': range(100),
            'feature2': [x * 2 for x in range(100)],
            'target': [x * 1.5 + 5 for x in range(100)]
        })
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    # 2. Preprocess
    print("Preprocessing data...")
    preprocessor = Preprocessor(df)
    df_processed = preprocessor.process_all(target_col='target')
    
    X = df_processed.drop(columns=['target'])
    y = df_processed['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Train and Eval
    print("Training Linear Regression...")
    reg = RegressionModels()
    # reg.train_and_eval returns {model_name: {metric: value}}
    results = reg.train_and_eval(X_train, X_test, y_train, y_test, selected_model="Linear Regression")
    
    r2 = results["Linear Regression"]["R2 Score"]
    print(f"Benchmark Result -> R2 Score: {r2:.4f}")
    
    # 4. Validation
    THRESHOLD = 0.8
    if r2 >= THRESHOLD:
        print(f"SUCCESS: Model performance ({r2:.4f}) meets threshold ({THRESHOLD})")
        return True
    else:
        print(f"FAILURE: Model performance ({r2:.4f}) is below threshold ({THRESHOLD})")
        return False

if __name__ == "__main__":
    success = run_benchmark()
    if not success:
        exit(1)
