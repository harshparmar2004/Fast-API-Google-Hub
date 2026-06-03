<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_docs_service
=======
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_docs_service, get_drive_service
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
class ShareDocReq(BaseModel):
    email: str

class ReplaceTextReq(BaseModel):
    old_text: str
    new_text: str

@router.post("/share")
def share_doc(req: ShareDocReq, request: Request, service=Depends(get_docs_service)):
    return format_response(request, "share_doc", {"msg": "Shared"})

@router.get("/{id}/comments")
def get_comments(id: str, request: Request, service=Depends(get_docs_service)):
    return format_response(request, "get_comments", [])

@router.post("/{id}/comment")
def add_comment(id: str, request: Request, service=Depends(get_docs_service)):
    return format_response(request, "add_comment", {"msg": "Comment added"})

@router.post("/{id}/append")
def append_text(id: str, text: str, request: Request, service=Depends(get_docs_service)):
    requests = [{'insertText': {'location': {'index': 1}, 'text': text}}]
    res = service.documents().batchUpdate(documentId=id, body={'requests': requests}).execute()
    return format_response(request, "append_text", res)

@router.post("/{id}/replace")
def replace_text(id: str, req: ReplaceTextReq, request: Request, service=Depends(get_docs_service)):
    requests = [{'replaceAllText': {'containsText': {'text': req.old_text, 'matchCase': True}, 'replaceText': req.new_text}}]
    res = service.documents().batchUpdate(documentId=id, body={'requests': requests}).execute()
    return format_response(request, "replace_text", res)

@router.get("/{id}/revisions")
def revisions(id: str, request: Request, service=Depends(get_docs_service)):
    return format_response(request, "revisions", [])

@router.post("/duplicate")
def duplicate(id: str, request: Request, service=Depends(get_docs_service)):
    return format_response(request, "duplicate", {"id": id, "msg": "Duplicated"})

=======
class AddTextReq(BaseModel):
    text: str

class CreateDocReq(BaseModel):
    title: str

@router.get("/list")
def list_docs(service=Depends(get_drive_service)):
    # 15. List all documents
    query = "mimeType='application/vnd.google-apps.document'"
    res = service.files().list(q=query, pageSize=20, fields="files(id, name)").execute()
    return format_response(res.get('files', []))

@router.get("/{doc_id}")
def read_doc(doc_id: str, service=Depends(get_docs_service)):
    # 16. Read document content
    doc = service.documents().get(documentId=doc_id).execute()
    return format_response(doc)

@router.post("/create")
def create_doc(req: CreateDocReq, service=Depends(get_docs_service)):
    # 17. Create new document
    doc = service.documents().create(body={"title": req.title}).execute()
    return format_response(doc)

@router.post("/{doc_id}/update")
def update_doc(doc_id: str, req: AddTextReq, service=Depends(get_docs_service)):
    # 18. Update document content
    requests = [{"insertText": {"location": {"index": 1}, "text": req.text}}]
    res = service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
    return format_response(res)

@router.get("/search")
def search_docs(q: str, service=Depends(get_drive_service)):
    # 19. Search documents by keyword
    query = f"mimeType='application/vnd.google-apps.document' and name contains '{q}'"
    res = service.files().list(q=query, pageSize=20, fields="files(id, name)").execute()
    return format_response(res.get('files', []))
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
