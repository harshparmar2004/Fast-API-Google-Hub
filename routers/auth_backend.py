from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import requests
from database import save_user_auth, get_refresh_token
import urllib.parse
from urllib.parse import urlencode
import os
import secrets

router = APIRouter()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

@router.get("/login")
def login(request: Request):
    """Initiates Google OAuth 2.0 flow for backend."""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return HTMLResponse("<html><body><h3>Backend Not Configured</h3><p>Server admin must set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables on their Render deployment.</p></body></html>", status_code=500)

    # Generate a new random API key for this user immediately and pass it through 'state'
    agent_api_key = "sk_" + secrets.token_hex(16)
    
    redirect_uri = str(request.base_url).rstrip("/") + "/api/auth/callback"
    scopes = " ".join([
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/presentations",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/tasks",
        "https://www.googleapis.com/auth/contacts"
    ])
    
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode({
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scopes,
        "access_type": "offline",
        "prompt": "consent",
        "state": agent_api_key # pass the api key safely through state
    })
    return RedirectResponse(auth_url)

@router.get("/callback")
def auth_callback(request: Request, code: str, state: str):
    """Handles Google OAuth callback and sets permanent tokens."""
    agent_api_key = state
    redirect_uri = str(request.base_url).rstrip("/") + "/api/auth/callback"
    
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    res = r.json()
    
    if 'refresh_token' in res:
        save_user_auth(api_key=agent_api_key, refresh_token=res['refresh_token'], email="")
        
        # Display the generated API Key to the user
        html_content = f"""
        <html>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h2>Authorization Successful!</h2>
                <p>Google tools connected securely.</p>
                <div style="background: #f0f0f0; border-radius: 8px; padding: 20px; display: inline-block; margin-top: 20px;">
                    <p style="margin-bottom: 5px; color: #555;">Your Agent API Key:</p>
                    <h3 style="margin: 0; color: #333; font-family: monospace;">{agent_api_key}</h3>
                </div>
                <p style="margin-top: 20px; font-size: 14px; color: #777;">
                    Please copy this API Key and provide it to your AI Agent (like OpenClaw or Clawbot).<br/>
                    The Agent will send this as <code style="background: #eee; padding: 2px 4px; border-radius: 4px;">X-API-Key</code> in Request headers.
                </p>
                <button onclick="window.close()" style="margin-top: 30px; padding: 10px 20px; cursor: pointer; border: none; background: #000; color: #fff; border-radius: 5px;">Close Tab</button>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
        
    return HTMLResponse(f"<html><body><h3>Authentication failed.</h3><p>Did not receive a refresh token from Google. Make sure you don't already have an active authorization, or revoke the app from your Google account and try again.</p><p><small>{res}</small></p></body></html>", status_code=400)

