from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_docs_service
from utils import format_response

router = APIRouter()

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

