from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_google_credentials
from utils import format_response

router = APIRouter()

@router.post("/email-to-task")
def _1(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "email-to-task", {})
@router.post("/email-to-event")
def _2(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "email-to-event", {})
@router.post("/email-to-sheet")
def _3(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "email-to-sheet", {})
@router.post("/morning-brief")
def _4(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "morning-brief", {})
@router.post("/meeting-prep")
def _5(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "meeting-prep", {})
@router.post("/follow-up")
def _6(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "follow-up", {})
@router.post("/weekly-summary")
def _7(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "weekly-summary", {})
@router.post("/smart-reply")
def _8(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "smart-reply", {})
@router.post("/organize-inbox")
def _9(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "organize-inbox", {})
@router.post("/project-status")
def _10(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "project-status", {})
