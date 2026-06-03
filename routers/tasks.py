<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
=======
from fastapi import APIRouter, Depends
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from pydantic import BaseModel
from auth import get_tasks_service
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
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

=======
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
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
