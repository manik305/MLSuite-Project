import requests
import json

BASE_URL = "http://localhost:8001"

def test_columns():
    # Attempt to get columns for MYDF.csv
    filename = "MYDF.csv"
    response = requests.get(f"{BASE_URL}/columns", params={"filename": filename})
    print(f"Columns for {filename}:")
    print(json.dumps(response.json(), indent=2))
    
    # Attempt to get columns for Akkodis enterprise_response (1).xlsx
    filename = "Akkodis enterprise_response (1).xlsx"
    response = requests.get(f"{BASE_URL}/columns", params={"filename": filename})
    print(f"\nColumns for {filename}:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    try:
        test_columns()
    except Exception as e:
        print(f"Error: {e}")
