from fastapi import Security, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from database import get_refresh_token

security = HTTPBearer(auto_error=False)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

def get_google_credentials(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    1. Check for Agent API Key; if valid, use backend stored auth (Refresh Token).
    2. Fallback to extracting the Google Access Token sent via the Authorization: Bearer header.
    """
    req_api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
    
    # Authenticate via Backend Refresh Token (for AI Agents)
    if req_api_key:
        refresh_token = get_refresh_token(req_api_key)
        
        if refresh_token:
            if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
                raise HTTPException(status_code=500, detail="Backend missing Google Client ID/Secret")
            
            from database import get_email_by_api_key
            request.state.user_email = get_email_by_api_key(req_api_key) or "agent@hub"
            
            return Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid Agent API Key.")

    # Authenticate via Frontend Bearer token (for UI / short-lived tasks)
    if credentials:
        token = credentials.credentials
        request.state.user_email = "ui_user@hub" # We can fetch real email later if needed
        return Credentials(token)
        
    raise HTTPException(status_code=401, detail="Not authenticated. Provide X-API-Key for bots, or Bearer token for UI.")

def get_gmail_service(creds: Credentials = Depends(get_google_credentials)):
    return build('gmail', 'v1', credentials=creds)

def get_sheets_service(creds: Credentials = Depends(get_google_credentials)):
    return build('sheets', 'v4', credentials=creds)

def get_drive_service(creds: Credentials = Depends(get_google_credentials)):
    return build('drive', 'v3', credentials=creds)

def get_calendar_service(creds: Credentials = Depends(get_google_credentials)):
    return build('calendar', 'v3', credentials=creds)

def get_docs_service(creds: Credentials = Depends(get_google_credentials)):
    return build('docs', 'v1', credentials=creds)

def get_slides_service(creds: Credentials = Depends(get_google_credentials)):
    return build('slides', 'v1', credentials=creds)

def get_tasks_service(creds: Credentials = Depends(get_google_credentials)):
    return build('tasks', 'v1', credentials=creds)

def get_people_service(creds: Credentials = Depends(get_google_credentials)):
    return build('people', 'v1', credentials=creds)
