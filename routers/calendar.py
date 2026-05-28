from fastapi import APIRouter, Depends
from auth import get_calendar_service
from pydantic import BaseModel
import datetime
from typing import Optional

router = APIRouter()

class CreateEventRequest(BaseModel):
    summary: str
    location: Optional[str] = None
    description: Optional[str] = None
    start_date_time: str # ISO 8601 string
    end_date_time: str # ISO 8601 string

@router.get("/events")
def list_events(service = Depends(get_calendar_service), max_results: int = 10):
    """List upcoming events."""
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=max_results, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])

@router.post("/events")
def create_event(req: CreateEventRequest, service = Depends(get_calendar_service)):
    """Create a new event in the primary calendar."""
    event = {
        'summary': req.summary,
        'location': req.location,
        'description': req.description,
        'start': {
            'dateTime': req.start_date_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': req.end_date_time,
            'timeZone': 'UTC',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event

@router.delete("/events/{event_id}")
def delete_event(event_id: str, service = Depends(get_calendar_service)):
    """Delete an event by ID."""
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    return {"status": "deleted"}
