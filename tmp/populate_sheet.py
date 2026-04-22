import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CRED_FILE = "c:/Users/manik/Downloads/antigravitysheet-cf53fdaf06c1.json"
SPREADSHEET_ID = "17735uZEs0gB7x8XN6Ycy_JCWhMN4DS3ez8xAkXzKSVo"

def populate():
    try:
        creds = service_account.Credentials.from_service_account_file(
            CRED_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=creds)
        
        # Define the data
        values = [
            ["MLSUITE PROJECT BREAKTHROUGH & SPRINT PLAN"],
            [""],
            ["1. TECHNOLOGY STACK GATHERING"],
            ["Layer", "Technology", "Purpose / Context"],
            ["Frontend", "Vite + React 18", "Core framework for high-speed UI"],
            ["Frontend", "TypeScript", "Type-safe development and scalability"],
            ["Frontend", "Tailwind CSS", "Premium 'Digital Nebula' glassmorphism design"],
            ["Backend", "FastAPI", "Async high-performance API Gateway"],
            ["Backend", "Python 3.10+", "Core logic & Model orchestration"],
            ["Backend", "PyJWT / bcrypt", "Security, RBAC, and Token management"],
            ["ML Engine", "Scikit-Learn", "Regression & Classification pipelines"],
            ["ML Engine", "MLTuner", "Automated hyperparameter optimization"],
            ["Database", "NanoDB (JSON)", "Lightweight persistent operator storage"],
            [""],
            ["2. KEY FUNCTIONALITIES"],
            ["Module", "Feature", "Description"],
            ["ML Flow", "Auto-Tuning", "Automated model selection & parameter search"],
            ["ML Flow", "Visualization", "Neural flow discovery & residual analytics"],
            ["Identity", "RBAC", "Admin vs User portal segmentation"],
            ["Identity", "Vault", "Admin console for operator management"],
            ["Logging", "Activity Audit", "Real-time logging of operator activity & model scaling"],
            ["Ingestion", "Multi-Source", "Support for Files, SQL, and MongoDB"],
            [""],
            ["3. RESOURCES REQUIRED"],
            ["Type", "Requirement", "Status"],
            ["Infra", "Docker Orchestration", "Implemented"],
            ["Infra", "Cloud Provider Quota", "Pending Integration"],
            ["Data", "High-Integrity Datasets", "Ready for Discovery"],
            [""],
            ["4. SCREEN PLAN / SITEMAP"],
            ["Route", "Access Level", "Purpose"],
            ["/login", "Public", "Neural protocol entry"],
            ["/dashboard", "User", "Standard ML implementation flow"],
            ["/admin", "Admin", "Unified Console (Flow + Vault + Audit Log)"]
        ]
        
        body = {
            'values': values
        }
        
        # Clear the sheet first if needed, or just overwrite
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="A1",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        
        # Add some formatting (Bold headers)
        requests = [
            {
                "repeatCell": {
                    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 1},
                    "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 14}}},
                    "fields": "userEnteredFormat.textFormat"
                }
            },
            {
                "repeatCell": {
                    "range": {"sheetId": 0, "startRowIndex": 2, "endRowIndex": 3},
                    "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.8, "green": 0.9, "blue": 1.0}, "textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            },
             {
                "repeatCell": {
                    "range": {"sheetId": 0, "startRowIndex": 14, "endRowIndex": 15},
                    "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.8, "green": 0.9, "blue": 1.0}, "textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            },
            {
                "repeatCell": {
                    "range": {"sheetId": 0, "startRowIndex": 23, "endRowIndex": 24},
                    "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.8, "green": 0.9, "blue": 1.0}, "textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            },
            {
                "repeatCell": {
                    "range": {"sheetId": 0, "startRowIndex": 29, "endRowIndex": 30},
                    "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.8, "green": 0.9, "blue": 1.0}, "textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            }
        ]
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': requests}
        ).execute()
        
        print("Success: MLsuit Sprintplan populated successfully.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    populate()
