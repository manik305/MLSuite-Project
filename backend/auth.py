import jwt
import datetime
import json
import os
from typing import Optional
from fastapi import HTTPException, Header
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NANODB_API_KEY = os.getenv("NANODB_API_KEY", "default_key")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Simple NanoDB implementation using a JSON file
DB_FILE = os.getenv("NANODB_PATH", "nanodb.json")

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": {}, "logs": [], "models": {}}, f)

def get_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

# Using the environment variables defined above

class AuthHandler:
    @staticmethod
    def create_access_token(email: str, role: str = "user"):
        expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        to_encode = {"email": email, "role": role, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return {"email": "anonymous@mlsuite.local", "role": "user"}
    token = authorization.split(" ")[1]
    payload = AuthHandler.verify_token(token)
    if not payload or "email" not in payload:
        return {"email": "anonymous@mlsuite.local", "role": "user"}
    return payload # Returns the whole payload which includes email and role
