import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CRED_FILE = "c:/Users/manik/Downloads/antigravitysheet-cf53fdaf06c1.json"

def list_spreadsheets():
    try:
        creds = service_account.Credentials.from_service_account_file(
            CRED_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('drive', 'v3', credentials=creds)
        
        # Search for spreadsheets
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            fields="files(id, name)"
        ).execute()
        
        files = results.get('files', [])
        if not files:
            print("No spreadsheets found.")
        else:
            print("Spreadsheets found:")
            for file in files:
                print(f"{file['name']} (ID: {file['id']})")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    list_spreadsheets()
