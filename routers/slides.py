from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_slides_service
from utils import format_response

router = APIRouter()

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

