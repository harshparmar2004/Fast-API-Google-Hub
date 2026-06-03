from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_google_credentials
from utils import format_response

router = APIRouter()

@router.post("/create")
def _20(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "create_automation", {})
@router.get("/list")
def _21(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "list_automations", {})
@router.put("/toggle")
def _22(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "toggle_automation", {})
@router.delete("/delete")
def _23(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "delete_automation", {})
@router.post("/run")
def _24(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "run_automation", {})
@router.get("/logs")
def _25(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "automation_logs", {})
