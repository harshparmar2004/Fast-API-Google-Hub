from fastapi import APIRouter, Depends
from auth import get_tasks_service
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class CreateTaskRequest(BaseModel):
    title: str
    notes: Optional[str] = None
    due: Optional[str] = None

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    due: Optional[str] = None

@router.get("/lists")
def get_tasklists(service = Depends(get_tasks_service)):
    """Get all task lists."""
    results = service.tasklists().list(maxResults=10).execute()
    return results.get('items', [])

@router.get("/lists/{tasklist_id}/tasks")
def get_tasks(tasklist_id: str, service = Depends(get_tasks_service)):
    """Get tasks from a list."""
    results = service.tasks().list(tasklist=tasklist_id, maxResults=100).execute()
    return results.get('items', [])

@router.post("/lists/{tasklist_id}/tasks")
def create_task(tasklist_id: str, req: CreateTaskRequest, service = Depends(get_tasks_service)):
    """Create a task in a list."""
    task = {
        'title': req.title,
        'notes': req.notes,
        'due': req.due
    }
    result = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
    return result

@router.patch("/lists/{tasklist_id}/tasks/{task_id}")
def update_task(tasklist_id: str, task_id: str, req: UpdateTaskRequest, service = Depends(get_tasks_service)):
    """Update a task."""
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    if req.title is not None:
        task['title'] = req.title
    if req.notes is not None:
        task['notes'] = req.notes
    if req.status is not None:
        task['status'] = req.status
    if req.due is not None:
        task['due'] = req.due
    result = service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
    return result

@router.delete("/lists/{tasklist_id}/tasks/{task_id}")
def delete_task(tasklist_id: str, task_id: str, service = Depends(get_tasks_service)):
    """Delete a task."""
    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
    return {"status": "deleted"}
