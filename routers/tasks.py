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

@router.get("/overdue")
def overdue(request: Request, service=Depends(get_tasks_service)):
    from datetime import datetime
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    tasklists = service.tasklists().list().execute().get('items', [])
    if not tasklists: return format_response(request, "overdue", [])
    
    overdue_tasks = []
    for tl in tasklists:
        res = service.tasks().list(tasklist=tl['id'], dueMax=now, showCompleted=False).execute()
        overdue_tasks.extend(res.get('items', []))
    return format_response(request, "overdue", overdue_tasks)

@router.get("/today")
def today(request: Request, service=Depends(get_tasks_service)):
    from datetime import datetime, timedelta
    now_dt = datetime.utcnow()
    midnight = now_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = midnight + timedelta(days=1)
    
    due_min = midnight.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    due_max = tomorrow.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    tasklists = service.tasklists().list().execute().get('items', [])
    if not tasklists: return format_response(request, "today", [])
    
    today_tasks = []
    for tl in tasklists:
        res = service.tasks().list(tasklist=tl['id'], dueMin=due_min, dueMax=due_max, showCompleted=False).execute()
        today_tasks.extend(res.get('items', []))
    return format_response(request, "today", today_tasks)

@router.put("/{tasklist}/task/{task_id}/due-date")
def update_due_date(tasklist: str, task_id: str, due: str, request: Request, service=Depends(get_tasks_service)):
    task = service.tasks().get(tasklist=tasklist, task=task_id).execute()
    task['due'] = due
    res = service.tasks().update(tasklist=tasklist, task=task_id, body=task).execute()
    return format_response(request, "update_due_date", res)

@router.put("/{tasklist}/task/{task_id}/status")
def update_status(tasklist: str, task_id: str, status: str, request: Request, service=Depends(get_tasks_service)):
    task = service.tasks().get(tasklist=tasklist, task=task_id).execute()
    task['status'] = status # 'needsAction' or 'completed'
    res = service.tasks().update(tasklist=tasklist, task=task_id, body=task).execute()
    return format_response(request, "update_status", res)

@router.post("/reorder")
def reorder(request: Request, service=Depends(get_tasks_service)):
    return format_response(request, "reorder", {})

