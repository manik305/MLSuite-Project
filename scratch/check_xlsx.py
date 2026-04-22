import pandas as pd
import re

try:
    df = pd.read_excel('uploads/regression.xlsx')
    print("Original Columns:")
    print(df.columns.tolist())
    
    def sanitize(col):
        return re.sub(r'[\[\]<>\s,]', '_', str(col))
    
    print("\nSanitized Columns:")
    print([sanitize(c) for c in df.columns])
    
except Exception as e:
    print(f"Error: {e}")
