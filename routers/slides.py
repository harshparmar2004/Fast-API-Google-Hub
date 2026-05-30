from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_slides_service, get_drive_service
from utils import format_response

router = APIRouter()

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
