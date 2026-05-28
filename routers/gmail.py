from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_gmail_service
from typing import List, Optional
import base64
from email.message import EmailMessage

router = APIRouter()

class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str

@router.get("/messages")
def list_messages(service = Depends(get_gmail_service), max_results: int = 10, q: str = ""):
    """List recent emails from the inbox."""
    results = service.users().messages().list(userId='me', maxResults=max_results, q=q).execute()
    return results.get('messages', [])

@router.get("/messages/{message_id}")
def get_message(message_id: str, service = Depends(get_gmail_service)):
    """Get full details of a specific email."""
    message = service.users().messages().get(userId='me', id=message_id).execute()
    return message

@router.post("/send")
def send_email(req: SendEmailRequest, service = Depends(get_gmail_service)):
    """Send an email on behalf of the user."""
    message = EmailMessage()
    message.set_content(req.body)
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = req.subject
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    
    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    return {"status": "success", "id": send_message["id"]}
