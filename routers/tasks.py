from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_tasks_service
from utils import format_response

router = APIRouter()

class TaskReq(BaseModel):
    title: str
    notes: str = ""

@router.get("/list")
def list_tasks(tasklist_id: str = "@default", service=Depends(get_tasks_service)):
    # 35. List all tasks
    res = service.tasks().list(tasklist=tasklist_id, maxResults=50).execute()
    return format_response(res.get('items', []))

@router.get("/pending")
def list_pending_tasks(tasklist_id: str = "@default", service=Depends(get_tasks_service)):
    # 36. List pending tasks only
    res = service.tasks().list(tasklist=tasklist_id, maxResults=50, showHidden=False).execute()
    items = res.get('items', [])
    pending = [t for t in items if t.get('status') != 'completed']
    return format_response(pending)

@router.post("/create")
def create_task(req: TaskReq, tasklist_id: str = "@default", service=Depends(get_tasks_service)):
    # 37. Create new task
    task = {"title": req.title, "notes": req.notes}
    res = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
    return format_response(res)

@router.post("/{task_id}/complete")
def mark_complete(task_id: str, tasklist_id: str = "@default", service=Depends(get_tasks_service)):
    # 38. Mark task as complete
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    task['status'] = 'completed'
    res = service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
    return format_response(res)

@router.delete("/{task_id}")
def delete_task(task_id: str, tasklist_id: str = "@default", service=Depends(get_tasks_service)):
    # 39. Delete a task
    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
    return format_response({"task_id": task_id, "deleted": True})

@router.put("/{task_id}")
def update_task(task_id: str, req: TaskReq, tasklist_id: str = "@default", service=Depends(get_tasks_service)):
    # 40. Update task details
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    task['title'] = req.title
    task['notes'] = req.notes
    res = service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
    return format_response(res)
