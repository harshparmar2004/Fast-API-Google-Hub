from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_google_credentials
from utils import format_response

router = APIRouter()

@router.get("/overview")
def _11(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "overview", {})
@router.get("/notifications")
def _12(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "notifications", {})
@router.get("/recent-activity")
def _13(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "recent-activity", {})
@router.post("/search")
def _14(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "search", {})
@router.get("/stats")
def _15(request: Request, creds=Depends(get_google_credentials)): return format_response(request, "stats", {})
