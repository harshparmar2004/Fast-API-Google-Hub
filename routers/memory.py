from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_google_credentials
from utils import format_response

router = APIRouter()

@router.post("/save")
def _16(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "save_memory", {})
@router.get("/get")
def _17(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "get_memory", {})
@router.delete("/clear")
def _18(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "clear_memory", {})
@router.post("/preference")
def _19(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "memory_preference", {})
