from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_tasks_service
from utils import format_response

router = APIRouter()

@router.get("/lists")
def task_lists(request: Request, service=Depends(get_tasks_service)):
    res = service.tasklists().list().execute()
    return format_response(request, "task_lists", res.get('items', []))

@router.post("/list/create")
def create_task_list(title: str, request: Request, service=Depends(get_tasks_service)):
    res = service.tasklists().insert(body={'title': title}).execute()
    return format_response(request, "create_task_list", res)

@router.post("/{id}/subtask")
def add_subtask(id: str, title: str, request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "add_subtask", {"msg": "Subtask added"})

@router.put("/{id}/due-date")
def update_due_date(id: str, request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "update_due_date", {"msg": "Due date updated"})

@router.put("/{id}/priority")
def update_priority(id: str, request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "update_priority", {"msg": "Priority updated"})

@router.get("/overdue")
def overdue(request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "overdue", [])

@router.get("/today")
def today(request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "today", [])

@router.post("/reorder")
def reorder(request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "reorder", {})

