from fastapi import APIRouter, Depends
from auth import get_drive_service
from utils import format_response

router = APIRouter()

@router.get("/list")
def list_files(service=Depends(get_drive_service)):
    # 10. List all files
    res = service.files().list(pageSize=20, fields="nextPageToken, files(id, name)").execute()
    return format_response(res.get('files', []))

@router.get("/search")
def search_files(q: str, service=Depends(get_drive_service)):
    # 11. Search files by name
    query = f"name contains '{q}'"
    res = service.files().list(q=query, pageSize=20, fields="nextPageToken, files(id, name)").execute()
    return format_response(res.get('files', []))

@router.get("/{file_id}")
def file_details(file_id: str, service=Depends(get_drive_service)):
    # 12. Get file details
    res = service.files().get(fileId=file_id, fields="id, name, mimeType, webViewLink").execute()
    return format_response(res)

@router.delete("/{file_id}")
def delete_file(file_id: str, service=Depends(get_drive_service)):
    # 13. Delete a file
    service.files().delete(fileId=file_id).execute()
    return format_response({"file_id": file_id, "deleted": True})

@router.get("/recent/files")
def recent_files(service=Depends(get_drive_service)):
    # 14. List recent files
    res = service.files().list(orderBy="modifiedTime desc", pageSize=10, fields="files(id, name)").execute()
    return format_response(res.get('files', []))
