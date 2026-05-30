from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_calendar_service
from utils import format_response
from datetime import datetime, timedelta
import uuid

router = APIRouter()

class EventReq(BaseModel):
    summary: str
    description: str = ""
    start_time: str
    end_time: str

class UpdateEventReq(EventReq):
    pass

@router.get("/list")
def list_events(service=Depends(get_calendar_service)):
    # 29. List all upcoming events
    now = datetime.utcnow().isoformat() + 'Z'
    res = service.events().list(calendarId='primary', timeMin=now, maxResults=20, singleEvents=True, orderBy='startTime').execute()
    return format_response(res.get('items', []))

@router.get("/today")
def list_today_events(service=Depends(get_calendar_service)):
    # 30. List today's events only
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'
    res = service.events().list(calendarId='primary', timeMin=start_of_day, timeMax=end_of_day, singleEvents=True, orderBy='startTime').execute()
    return format_response(res.get('items', []))

@router.post("/create")
def create_event(req: EventReq, service=Depends(get_calendar_service)):
    # 31. Create new event
    event = {
        'summary': req.summary,
        'description': req.description,
        'start': {'dateTime': req.start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': req.end_time, 'timeZone': 'UTC'},
    }
    res = service.events().insert(calendarId='primary', body=event).execute()
    return format_response(res)

@router.put("/{event_id}")
def update_event(event_id: str, req: UpdateEventReq, service=Depends(get_calendar_service)):
    # 32. Update existing event
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['summary'] = req.summary
    event['description'] = req.description
    event['start'] = {'dateTime': req.start_time, 'timeZone': 'UTC'}
    event['end'] = {'dateTime': req.end_time, 'timeZone': 'UTC'}
    res = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return format_response(res)

@router.delete("/{event_id}")
def delete_event(event_id: str, service=Depends(get_calendar_service)):
    # 33. Delete an event
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    return format_response({"event_id": event_id, "deleted": True})

@router.post("/create_with_meet")
def create_event_with_meet(req: EventReq, service=Depends(get_calendar_service)):
    # 34. Create event with Meet link
    event = {
        'summary': req.summary,
        'description': req.description,
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
