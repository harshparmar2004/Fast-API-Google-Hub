from fastapi import APIRouter, Depends
from auth import get_docs_service
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CreateDocRequest(BaseModel):
    title: str

class InsertTextRequest(BaseModel):
    document_id: str
    text: str
    index: int = 1

@router.get("/{document_id}")
def read_document(document_id: str, service = Depends(get_docs_service)):
    """Read a document."""
    doc = service.documents().get(documentId=document_id).execute()
    return doc

@router.post("/create")
def create_document(req: CreateDocRequest, service = Depends(get_docs_service)):
    """Create a new document."""
    doc = service.documents().create(body={"title": req.title}).execute()
    return doc

@router.post("/insert_text")
def insert_text(req: InsertTextRequest, service = Depends(get_docs_service)):
    """Insert text into a document."""
    requests = [
        {
            'insertText': {
                'location': {
                    'index': req.index,
                },
                'text': req.text
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=req.document_id, body={'requests': requests}).execute()
    return result
