<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_slides_service
=======
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_slides_service, get_drive_service
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
@router.post("/{id}/slide/add")
def add_slide(id: str, request: Request, service=Depends(get_slides_service)):
    requests = [{'createSlide': {}}]
    res = service.presentations().batchUpdate(presentationId=id, body={'requests': requests}).execute()
    return format_response(request, "add_slide", res)

@router.delete("/{id}/slide/delete")
def delete_slide(id: str, slide_id: str, request: Request, service=Depends(get_slides_service)):
    requests = [{'deleteObject': {'objectId': slide_id}}]
    res = service.presentations().batchUpdate(presentationId=id, body={'requests': requests}).execute()
    return format_response(request, "delete_slide", res)

@router.post("/{id}/text/add")
def add_text_box(id: str, page_id: str, request: Request, service=Depends(get_slides_service)):
    requests = [{'createShape': {'shapeType': 'TEXT_BOX', 'elementProperties': {'pageObjectId': page_id}}}]
    res = service.presentations().batchUpdate(presentationId=id, body={'requests': requests}).execute()
    return format_response(request, "add_text_box", res)

@router.post("/{id}/duplicate")
def dup(id: str, request: Request, service=Depends(get_slides_service)):
    return format_response(request, "duplicate", {"msg": "Duplicated"})

@router.post("/share")
def shar(id: str, request: Request, service=Depends(get_slides_service)):
    return format_response(request, "share", {"msg": "Shared"})

@router.get("/{id}/thumbnail")
def thumb(id: str, request: Request, service=Depends(get_slides_service)):
    return format_response(request, "thumbnail", {"url": "http"})

=======
class CreateSlideReq(BaseModel):
    title: str

@router.get("/list")
def list_presentations(service=Depends(get_drive_service)):
    # 26. List all presentations
    query = "mimeType='application/vnd.google-apps.presentation'"
    res = service.files().list(q=query, pageSize=20, fields="files(id, name)").execute()
    return format_response(res.get('files', []))

@router.get("/{presentation_id}")
def read_presentation(presentation_id: str, service=Depends(get_slides_service)):
    # 27. Read presentation content
    res = service.presentations().get(presentationId=presentation_id).execute()
    return format_response(res)

@router.post("/create")
def create_presentation(req: CreateSlideReq, service=Depends(get_slides_service)):
    # 28. Create new presentation
    presentation = {"title": req.title}
    res = service.presentations().create(body=presentation).execute()
    return format_response(res)
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
