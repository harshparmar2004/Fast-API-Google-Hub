from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import Request

# If not initialized, initialize with default creds
if not firebase_admin._apps:
    try:
        firebase_admin.initialize_app()
    except Exception:
        pass

def get_firestore_db():
    try:
        return firestore.client(database="ai-studio-76ff7b07-f37f-4cef-aed2-581810e5acd3")
    except Exception:
        # Fallback to default if somehow the specific database ID is invalid
        try:
            return firestore.client()
        except:
            return None

def format_response(request: Request, action_name: str, data=None, success=True):
    user_email = getattr(request.state, "user_email", "unknown@user")
    ts = datetime.utcnow().isoformat() + "Z"
    
    # Log to Firestore
    db = get_firestore_db()
    if db:
        try:
            db.collection("api_logs").add({
                "user": user_email,
                "action": action_name,
                "timestamp": ts,
                "success": success
            })
        except Exception:
            pass
            
    return {
        "success": success,
        "user": user_email,
        "data": data,
        "timestamp": ts,
        "action": action_name
    }
