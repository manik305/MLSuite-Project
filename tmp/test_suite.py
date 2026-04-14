import requests
import json
import time
import os

BASE_URL = "http://localhost:8001"
TOKEN = None

def setup_auth():
    global TOKEN
    print("--- [1] Setting up Authentication ---")
    try:
        # Give the backend a moment to settle
        time.sleep(2)
        # Register if not exists, then login
        # For testing purposes, we'll just try to login with a fixed credential
        res = requests.post(f"{BASE_URL}/login", json={"email": "test@mlsuite.com", "password": "password123"})
        if res.status_code != 200:
            print("Registering new test user...")
            requests.post(f"{BASE_URL}/register", json={"email": "test@mlsuite.com", "password": "password123"})
            res = requests.post(f"{BASE_URL}/login", json={"email": "test@mlsuite.com", "password": "password123"})
        
        TOKEN = res.json().get("access_token")
        if TOKEN:
            print("Successfully authenticated.")
        return TOKEN
    except Exception as e:
        print(f"Auth setup failed with exception: {e}")
        return None

def test_auto_ml_cycle():
    if not TOKEN: return
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    print("\n--- [2] Testing Automated ML Lifecycle ---")
    
    # 1. Upload sample data (MYDF.csv if it exists)
    sample_file = r"c:\Users\manik\Downloads\MLProcess\uploads\MYDF.csv"
    if not os.path.exists(sample_file):
        print(f"Sample file {sample_file} not found. Please ensure it exists.")
        return

    print(f"Uploading {os.path.basename(sample_file)}...")
    with open(sample_file, 'rb') as f:
        files = {'file': f}
        up_res = requests.post(f"{BASE_URL}/upload", headers=headers, files=files)
        if up_res.status_code != 200:
            print(f"Upload failed: {up_res.text}")
            return

    # 2. Trigger automated comparison (tune=True)
    # We'll use 'legit' vs 'fruad' from MYDF.csv as classification
    print("Triggering Automated Neural Optimization (tune=True)...")
    train_params = {
        "data_source": "file",
        "filename": "MYDF.csv",
        "task_type": "classification",
        "target_column": "Label", # MYDF.csv target column is 'Label'
        "tune": "true"
    }
    
    start_time = time.time()
    train_res = requests.post(f"{BASE_URL}/train", headers=headers, params=train_params)
    duration = time.time() - start_time
    
    if train_res.status_code == 200:
        results = train_res.json()
        print(f"Success! AutoML cycle completed in {duration:.2f} seconds.")
        print(f"Winner: {results.get('model_name')}")
        print(f"Overall Accuracy: {results.get('score')}")
        
        leaderboard = results.get('leaderboard', [])
        if leaderboard:
            print("\n--- Neural Leaderboard ---")
            for entry in leaderboard:
                winner_star = "[WINNER]" if entry.get('is_winner') else "        "
                print(f"{winner_star} {entry['model_name']}: Score={entry['score']}, Error={entry['error_rate']}")
        else:
            print("Error: Leaderboard is empty. Check tuner.py logic.")
    else:
        print(f"Automated training failed: {train_res.text}")

if __name__ == "__main__":
    # Note: Backend MUST be running on port 8001
    if setup_auth():
        test_auto_ml_cycle()
    else:
        print("Test aborted due to auth failure. Is the backend running on port 8001?")
