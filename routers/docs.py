from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_docs_service, get_drive_service
from utils import format_response

router = APIRouter()

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
