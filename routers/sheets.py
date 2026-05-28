from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_sheets_service
from typing import List

router = APIRouter()

class UpdateSheetRequest(BaseModel):
    spreadsheet_id: str
    range: str
    values: List[List[str]]

@router.post("/update")
def update_sheet(req: UpdateSheetRequest, service = Depends(get_sheets_service)):
    """Update a range in a Google Sheet."""
    body = {
        'values': req.values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=req.spreadsheet_id, range=req.range,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

@router.get("/{spreadsheet_id}")
def read_sheet(spreadsheet_id: str, range: str, service = Depends(get_sheets_service)):
    """Read data from a Google Sheet."""
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range).execute()
    return result.get('values', [])
