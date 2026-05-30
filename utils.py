from datetime import datetime

def format_response(data=None, success=True):
    return {
        "success": success,
        "user": "authenticated_user",
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
