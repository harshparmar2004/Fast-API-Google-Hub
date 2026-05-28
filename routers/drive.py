from fastapi import APIRouter, Depends
from auth import get_drive_service
import json

router = APIRouter()

@router.get("/files")
def list_files(service = Depends(get_drive_service), q: str = "trashed=false"):
    """List out drive files."""
    results = service.files().list(q=q, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

@router.delete("/{file_id}")
def delete_file(file_id: str, service = Depends(get_drive_service)):
    """Delete a specific file."""
    service.files().delete(fileId=file_id).execute()
    return {"status": "deleted"}
