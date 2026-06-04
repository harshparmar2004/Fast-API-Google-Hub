from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_people_service
from utils import format_response

router = APIRouter()

@router.get("/groups")
def groups(request: Request, service=Depends(get_people_service)):
    res = service.contactGroups().list().execute()
    return format_response(request, "groups", res.get('contactGroups', []))

@router.post("/group/create")
def create_group(name: str, request: Request, service=Depends(get_people_service)):
    res = service.contactGroups().create(body={'contactGroup': {'name': name}}).execute()
    return format_response(request, "create_group", res)

@router.post("/{id}/group/add")
def add_to_group(id: str, group_id: str, request: Request, service=Depends(get_people_service)):
    return format_response(request, "add_to_group", {"msg": "Added"})

@router.get("/recent")
def recent(request: Request, service=Depends(get_people_service)):
    return format_response(request, "recent", [])

@router.get("/starred")
def starred(request: Request, service=Depends(get_people_service)):
    return format_response(request, "starred", [])

@router.post("/import")
def import_csv(request: Request, service=Depends(get_people_service)):
    return format_response(request, "import", {})

