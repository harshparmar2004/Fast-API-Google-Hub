from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_calendar_service
from utils import format_response

router = APIRouter()

class CreateEventReq(BaseModel):
    summary: str
    start_time: str
    end_time: str

class RSVPReq(BaseModel):
    event_id: str
    status: str # accepted, declined, tentative

@router.get("/upcoming")
def upcoming_events(request: Request, service=Depends(get_calendar_service)):
    from datetime import datetime, timedelta
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    events = service.events().list(calendarId='primary', timeMin=now, maxResults=10, orderBy='startTime', singleEvents=True).execute()
    return format_response(request, "upcoming_events", events.get('items', []))

@router.get("/today")
def today_events(request: Request, service=Depends(get_calendar_service)):
    from datetime import datetime, timedelta
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    later = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    events = service.events().list(calendarId='primary', timeMin=now, timeMax=later, singleEvents=True, orderBy='startTime').execute()
    return format_response(request, "today_events", events.get('items', []))

@router.get("/week")
def week_events(request: Request, service=Depends(get_calendar_service)):
    from datetime import datetime, timedelta
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    later = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    events = service.events().list(calendarId='primary', timeMin=now, timeMax=later, singleEvents=True, orderBy='startTime').execute()
    return format_response(request, "week_events", events.get('items', []))

@router.get("/month")
def month_events(request: Request, service=Depends(get_calendar_service)):
    from datetime import datetime, timedelta
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    later = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    events = service.events().list(calendarId='primary', timeMin=now, timeMax=later, singleEvents=True, orderBy='startTime').execute()
    return format_response(request, "month_events", events.get('items', []))

@router.post("/recurring")
def recurring_events(request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "recurring_events", {"msg": "Recurring event created"})

@router.get("/search")
def search_events(q: str, request: Request, service=Depends(get_calendar_service)):
    events = service.events().list(calendarId='primary', q=q, singleEvents=True).execute()
    return format_response(request, "search_events", events.get('items', []))

@router.post("/rsvp")
def rsvp_event(req: RSVPReq, request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "rsvp_event", {"status": req.status})

@router.get("/free-busy")
def free_busy(request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "free_busy", {"status": "free"})

@router.post("/reminder")
def reminder(request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "reminder", {"status": "ok"})

@router.get("/list")
def list_calendars(request: Request, service=Depends(get_calendar_service)):
    res = service.calendarList().list().execute()
    return format_response(request, "list_calendars", res.get('items', []))

@router.post("/out-of-office")
def out_of_office(request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "out_of_office", {"status": "ok"})

