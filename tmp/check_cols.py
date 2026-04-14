import pandas as pd
import os

uploads_dir = r'c:\Users\manik\Downloads\MLProcess\uploads'
for filename in os.listdir(uploads_dir):
    if filename.endswith(('.csv', '.xlsx', '.xls')):
        file_path = os.path.join(uploads_dir, filename)
        print(f"\nFILE: {filename}")
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            print("COLUMNS:", df.columns.tolist())
        except Exception as e:
            print(f"ERROR: {e}")
