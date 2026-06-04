from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_calendar_service
from utils import format_response

router = APIRouter()

@router.post("/instant")
def instant(request: Request, service=Depends(get_calendar_service)):
    from datetime import datetime, timedelta
    now_str = datetime.utcnow().isoformat() + "Z"
    end_str = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    event = {
        'summary': 'Instant Meet',
        'start': {'dateTime': now_str},
        'end': {'dateTime': end_str},
        'conferenceData': {'createRequest': {'requestId': "instant_meet_123"}}
    }
    res = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return format_response(request, "instant", res)

@router.get("/recordings")
def recordings(request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "recordings", [])

@router.post("/invite")
def invite(request: Request, service=Depends(get_calendar_service)):
    return format_response(request, "invite", {})

