<<<<<<< HEAD
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

=======
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_calendar_service
from utils import format_response
from datetime import datetime
import uuid

router = APIRouter()

class CreateMeetEventReq(BaseModel):
    summary: str
    start_time: str
    end_time: str

@router.get("/list")
def list_meet_links(service=Depends(get_calendar_service)):
    # 45. List upcoming Meet links
    now = datetime.utcnow().isoformat() + 'Z'
    res = service.events().list(calendarId='primary', timeMin=now, maxResults=50, singleEvents=True, orderBy='startTime').execute()
    events = res.get('items', [])
    meet_events = [e for e in events if 'conferenceData' in e or 'hangoutLink' in e]
    return format_response(meet_events)

@router.post("/create_link")
def create_meet_link(service=Depends(get_calendar_service)):
    # 46. Create new Meet link (by creating an event right now)
    now = datetime.utcnow()
    start_time = now.isoformat() + 'Z'
    end_time = (now + dict(hours=1)).isoformat() + 'Z' # Wait, dictionary is not correct
    from datetime import timedelta
    end_time = (now + timedelta(hours=1)).isoformat() + 'Z'
    
    event = {
        'summary': 'Instant Meet Session',
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }
    res = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return format_response({
        "meet_link": res.get("hangoutLink"),
        "event_id": res.get("id")
    })

@router.post("/create_event")
def create_meet_with_event(req: CreateMeetEventReq, service=Depends(get_calendar_service)):
    # 47. Create Meet with calendar event
    event = {
        'summary': req.summary,
        'start': {'dateTime': req.start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': req.end_time, 'timeZone': 'UTC'},
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }
    res = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return format_response(res)
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
