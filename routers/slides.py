from fastapi import APIRouter, Depends
from auth import get_slides_service
from pydantic import BaseModel

router = APIRouter()

class CreateSlideRequest(BaseModel):
    title: str

@router.get("/{presentation_id}")
def read_presentation(presentation_id: str, service = Depends(get_slides_service)):
    """Read a presentation."""
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    return presentation

@router.post("/create")
def create_presentation(req: CreateSlideRequest, service = Depends(get_slides_service)):
    """Create a new presentation."""
    presentation = service.presentations().create(body={"title": req.title}).execute()
    return presentation
