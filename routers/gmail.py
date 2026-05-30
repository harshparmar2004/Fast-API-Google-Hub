from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_gmail_service
from utils import format_response
import base64
from email.message import EmailMessage

router = APIRouter()

class SendEmailReq(BaseModel):
    to: str
    subject: str
    body: str

class ReplyEmailReq(BaseModel):
    to: str
    subject: str
    body: str
    thread_id: str
    message_id: str

@router.get("/list")
def list_emails(service=Depends(get_gmail_service)):
    # 1. List all emails
    results = service.users().messages().list(userId='me', maxResults=20).execute()
    return format_response(results.get('messages', []))

@router.get("/unread")
def unread_emails(service=Depends(get_gmail_service)):
    # 2. List unread emails only
    results = service.users().messages().list(userId='me', q="is:unread", maxResults=20).execute()
    return format_response(results.get('messages', []))

@router.get("/search")
def search_emails(q: str, service=Depends(get_gmail_service)):
    # 3. Search emails by keyword
    results = service.users().messages().list(userId='me', q=q, maxResults=20).execute()
    return format_response(results.get('messages', []))

@router.get("/read/{message_id}")
def read_email(message_id: str, service=Depends(get_gmail_service)):
    # 4. Read one specific email content
    message = service.users().messages().get(userId='me', id=message_id).execute()
    return format_response(message)

@router.post("/send")
def send_email(req: SendEmailReq, service=Depends(get_gmail_service)):
    # 5. Send a new email
    message = EmailMessage()
    message.set_content(req.body)
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = req.subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    res = service.users().messages().send(userId="me", body={'raw': encoded_message}).execute()
    return format_response(res)

@router.post("/reply")
def reply_email(req: ReplyEmailReq, service=Depends(get_gmail_service)):
    # 6. Reply to an email
    message = EmailMessage()
    message.set_content(req.body)
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = req.subject
    message['In-Reply-To'] = req.message_id
    message['References'] = req.message_id
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    res = service.users().messages().send(userId="me", body={'raw': encoded_message, 'threadId': req.thread_id}).execute()
    return format_response(res)

@router.delete("/{message_id}")
def delete_email(message_id: str, service=Depends(get_gmail_service)):
    # 7. Delete an email
    service.users().messages().trash(userId='me', id=message_id).execute()
    return format_response({"message_id": message_id, "deleted": True})

@router.post("/{message_id}/read")
def mark_read(message_id: str, service=Depends(get_gmail_service)):
    # 8. Mark email as read
    res = service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    return format_response(res)

@router.get("/count/unread")
def unread_count(service=Depends(get_gmail_service)):
    # 9. Get unread count
    res = service.users().messages().list(userId='me', q="is:unread", maxResults=1).execute()
    return format_response({"unread_count": res.get('resultSizeEstimate', 0)})
