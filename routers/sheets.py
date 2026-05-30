from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_sheets_service, get_drive_service
from utils import format_response

router = APIRouter()

class CreateSheetReq(BaseModel):
    title: str

class AppendRowReq(BaseModel):
    values: list

class UpdateRowReq(BaseModel):
    range: str
    values: list

@router.get("/list")
def list_sheets(service=Depends(get_drive_service)):
    # 20. List all spreadsheets
    query = "mimeType='application/vnd.google-apps.spreadsheet'"
    res = service.files().list(q=query, pageSize=20, fields="files(id, name)").execute()
    return format_response(res.get('files', []))

@router.get("/{sheet_id}/read")
def read_sheet(sheet_id: str, range: str = "A1:Z100", service=Depends(get_sheets_service)):
    # 21. Read sheet data
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range).execute()
    return format_response(res.get('values', []))

@router.put("/{sheet_id}/update")
def update_row(sheet_id: str, req: UpdateRowReq, service=Depends(get_sheets_service)):
    # 22. Update a specific row
    body = {"values": [req.values]}
    res = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=req.range, valueInputOption="USER_ENTERED", body=body).execute()
    return format_response(res)

@router.post("/{sheet_id}/append")
def append_row(sheet_id: str, req: AppendRowReq, range: str = "A1:A", service=Depends(get_sheets_service)):
    # 23. Append new row
    body = {"values": [req.values]}
    res = service.spreadsheets().values().append(spreadsheetId=sheet_id, range=range, valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body=body).execute()
    return format_response(res)

@router.post("/create")
def create_sheet(req: CreateSheetReq, service=Depends(get_sheets_service)):
    # 24. Create new spreadsheet
    spreadsheet = {"properties": {"title": req.title}}
    res = service.spreadsheets().create(body=spreadsheet).execute()
    return format_response(res)

@router.get("/{sheet_id}/search")
def search_sheet(sheet_id: str, q: str, range: str = "A1:Z100", service=Depends(get_sheets_service)):
    # 25. Search within sheet
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range).execute()
    values = res.get('values', [])
    found = [row for row in values if any(q.lower() in str(cell).lower() for cell in row)]
    return format_response(found)
