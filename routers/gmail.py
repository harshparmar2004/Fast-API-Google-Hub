from fastapi import APIRouter, Depends, Request
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

class LabelApplyReq(BaseModel):
    message_id: str
    label_ids: list[str]

class LabelCreateReq(BaseModel):
    name: str

class ForwardEmailReq(BaseModel):
    message_id: str
    to: str

class FilterCreateReq(BaseModel):
    from_address: str
    label_id: str

@router.get("/list")
def list_emails(request: Request, service=Depends(get_gmail_service)):
    results = service.users().messages().list(userId='me', maxResults=20).execute()
    return format_response(request, "list_emails", results.get('messages', []))

@router.get("/unread")
def unread_emails(request: Request, service=Depends(get_gmail_service)):
    results = service.users().messages().list(userId='me', q="is:unread", maxResults=20).execute()
    return format_response(request, "unread_emails", results.get('messages', []))

@router.get("/search")
def search_emails(q: str, request: Request, service=Depends(get_gmail_service)):
    results = service.users().messages().list(userId='me', q=q, maxResults=20).execute()
    return format_response(request, "search_emails", results.get('messages', []))

@router.get("/read/{message_id}")
def read_email(message_id: str, request: Request, service=Depends(get_gmail_service)):
    message = service.users().messages().get(userId='me', id=message_id).execute()
    return format_response(request, "read_email", message)

@router.post("/send")
def send_email(req: SendEmailReq, request: Request, service=Depends(get_gmail_service)):
    message = EmailMessage()
    message.set_content(req.body)
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = req.subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    res = service.users().messages().send(userId="me", body={'raw': encoded_message}).execute()
    return format_response(request, "send_email", res)

@router.post("/reply")
def reply_email(req: ReplyEmailReq, request: Request, service=Depends(get_gmail_service)):
    message = EmailMessage()
    message.set_content(req.body)
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = req.subject
    message['In-Reply-To'] = req.message_id
    message['References'] = req.message_id
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    res = service.users().messages().send(userId="me", body={'raw': encoded_message, 'threadId': req.thread_id}).execute()
    return format_response(request, "reply_email", res)

@router.delete("/{message_id}")
def delete_email(message_id: str, request: Request, service=Depends(get_gmail_service)):
    service.users().messages().trash(userId='me', id=message_id).execute()
    return format_response(request, "delete_email", {"message_id": message_id, "deleted": True})

@router.post("/{message_id}/read")
def mark_read(message_id: str, request: Request, service=Depends(get_gmail_service)):
    res = service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    return format_response(request, "mark_read", res)

@router.get("/count/unread")
def unread_count(request: Request, service=Depends(get_gmail_service)):
    res = service.users().messages().list(userId='me', q="is:unread", maxResults=1).execute()
    return format_response(request, "unread_count", {"unread_count": res.get('resultSizeEstimate', 0)})

# NEW ENDPOINTS

@router.get("/threads")
def get_threads(request: Request, service=Depends(get_gmail_service)):
    results = service.users().threads().list(userId='me', maxResults=10).execute()
    return format_response(request, "get_threads", results.get("threads", []))

@router.get("/labels")
def get_labels(request: Request, service=Depends(get_gmail_service)):
    results = service.users().labels().list(userId='me').execute()
    return format_response(request, "get_labels", results.get("labels", []))

@router.post("/label/apply")
def apply_label(req: LabelApplyReq, request: Request, service=Depends(get_gmail_service)):
    res = service.users().messages().modify(userId='me', id=req.message_id, body={'addLabelIds': req.label_ids}).execute()
    return format_response(request, "apply_label", res)

@router.post("/label/create")
def create_label(req: LabelCreateReq, request: Request, service=Depends(get_gmail_service)):
    label = {"name": req.name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    res = service.users().labels().create(userId='me', body=label).execute()
    return format_response(request, "create_label", res)

@router.post("/forward")
def forward_email(req: ForwardEmailReq, request: Request, service=Depends(get_gmail_service)):
    original = service.users().messages().get(userId='me', id=req.message_id, format='raw').execute()
    raw_msg = original['raw']
    message = EmailMessage()
    message.set_content(f"Fwd: ...
")
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = "Fwd"
    # Actually just sending a raw constructed msg for simplicity
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    res = service.users().messages().send(userId='me', body={'raw': encoded_message}).execute()
    return format_response(request, "forward_email", res)

@router.post("/draft/create")
def create_draft(req: SendEmailReq, request: Request, service=Depends(get_gmail_service)):
    message = EmailMessage()
    message.set_content(req.body)
    message['To'] = req.to
    message['From'] = "me"
    message['Subject'] = req.subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    res = service.users().drafts().create(userId='me', body={'message': {'raw': encoded_message}}).execute()
    return format_response(request, "create_draft", res)

@router.get("/drafts")
def list_drafts(request: Request, service=Depends(get_gmail_service)):
    results = service.users().drafts().list(userId='me').execute()
    return format_response(request, "list_drafts", results.get("drafts", []))

@router.post("/draft/send")
def send_draft(draft_id: str, request: Request, service=Depends(get_gmail_service)):
    res = service.users().drafts().send(userId='me', body={'id': draft_id}).execute()
    return format_response(request, "send_draft", res)

@router.post("/star")
def star_email(message_id: str, request: Request, service=Depends(get_gmail_service)):
    res = service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': ['STARRED']}).execute()
    return format_response(request, "star_email", res)

@router.post("/unstar")
def unstar_email(message_id: str, request: Request, service=Depends(get_gmail_service)):
    res = service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['STARRED']}).execute()
    return format_response(request, "unstar_email", res)

@router.get("/starred")
def get_starred_emails(request: Request, service=Depends(get_gmail_service)):
    results = service.users().messages().list(userId='me', q="is:starred", maxResults=20).execute()
    return format_response(request, "get_starred_emails", results.get('messages', []))

@router.post("/archive")
def archive_email(message_id: str, request: Request, service=Depends(get_gmail_service)):
    res = service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['INBOX']}).execute()
    return format_response(request, "archive_email", res)

@router.get("/attachments/{id}")
def get_attachment(id: str, message_id: str, request: Request, service=Depends(get_gmail_service)):
    att = service.users().messages().attachments().get(userId='me', messageId=message_id, id=id).execute()
    return format_response(request, "get_attachment", att)

@router.post("/filter/create")
def create_filter(req: FilterCreateReq, request: Request, service=Depends(get_gmail_service)):
    filter_body = {
        "criteria": {"from": req.from_address},
        "action": {"addLabelIds": [req.label_id]}
    }
    res = service.users().settings().filters().create(userId='me', body=filter_body).execute()
    return format_response(request, "create_filter", res)
