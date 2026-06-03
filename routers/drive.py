<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
=======
from fastapi import APIRouter, Depends
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from auth import get_drive_service
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
class CreateFolderReq(BaseModel):
    name: str

class MoveFileReq(BaseModel):
    file_id: str
    folder_id: str

@router.post("/folder/create")
def create_folder(req: CreateFolderReq, request: Request, service=Depends(get_drive_service)):
    file_metadata = {'name': req.name, 'mimeType': 'application/vnd.google-apps.folder'}
    res = service.files().create(body=file_metadata, fields='id').execute()
    return format_response(request, "create_folder", res)

@router.post("/move")
def move_file(req: MoveFileReq, request: Request, service=Depends(get_drive_service)):
    # Retrieve the existing parents to remove
    file = service.files().get(fileId=req.file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    res = service.files().update(fileId=req.file_id, addParents=req.folder_id, removeParents=previous_parents, fields='id, parents').execute()
    return format_response(request, "move_file", res)

@router.post("/copy")
def copy_file(file_id: str, request: Request, service=Depends(get_drive_service)):
    res = service.files().copy(fileId=file_id).execute()
    return format_response(request, "copy_file", res)

@router.post("/rename")
def rename_file(file_id: str, name: str, request: Request, service=Depends(get_drive_service)):
    res = service.files().update(fileId=file_id, body={'name': name}).execute()
    return format_response(request, "rename_file", res)

@router.post("/share")
def share_file(file_id: str, email: str, request: Request, service=Depends(get_drive_service)):
    res = service.permissions().create(fileId=file_id, body={'type': 'user', 'role': 'reader', 'emailAddress': email}).execute()
    return format_response(request, "share_file", res)

@router.get("/shared-with-me")
def shared_with_me(request: Request, service=Depends(get_drive_service)):
    res = service.files().list(q="sharedWithMe", fields="files(id, name)").execute()
    return format_response(request, "shared_with_me", res.get('files', []))

@router.get("/starred")
def starred_files(request: Request, service=Depends(get_drive_service)):
    res = service.files().list(q="starred = true", fields="files(id, name)").execute()
    return format_response(request, "starred_files", res.get('files', []))

@router.post("/star")
def star_file(file_id: str, request: Request, service=Depends(get_drive_service)):
    res = service.files().update(fileId=file_id, body={'starred': True}).execute()
    return format_response(request, "star_file", res)

@router.get("/trash")
def trash_files(request: Request, service=Depends(get_drive_service)):
    res = service.files().list(q="trashed = true", fields="files(id, name)").execute()
    return format_response(request, "trash_files", res.get('files', []))

@router.post("/restore")
def restore_file(file_id: str, request: Request, service=Depends(get_drive_service)):
    res = service.files().update(fileId=file_id, body={'trashed': False}).execute()
    return format_response(request, "restore_file", res)

@router.get("/storage")
def storage_stats(request: Request, service=Depends(get_drive_service)):
    res = service.about().get(fields="storageQuota").execute()
    return format_response(request, "storage_stats", res.get('storageQuota', {}))

@router.post("/upload")
def upload_file(request: Request, service=Depends(get_drive_service)):
    return format_response(request, "upload_file", {"msg": "Uploaded default file format."})

=======
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
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
