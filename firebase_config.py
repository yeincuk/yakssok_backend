import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

_db = None

def get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            firebase_env = os.getenv("FIREBASE_CREDENTIALS_JSON")
            if firebase_env:
                import json
                cred = credentials.Certificate(json.loads(firebase_env))
            else:
                cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH", "firebase-key.json"))
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db
