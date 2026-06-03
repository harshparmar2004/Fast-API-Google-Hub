<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_sheets_service
=======
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import get_sheets_service, get_drive_service
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
@router.post("/{id}/sheet/create")
def create_sheet_tab(id: str, title: str, request: Request, service=Depends(get_sheets_service)):
    requests = [{'addSheet': {'properties': {'title': title}}}]
    res = service.spreadsheets().batchUpdate(spreadsheetId=id, body={'requests': requests}).execute()
    return format_response(request, "create_sheet_tab", res)

@router.delete("/{id}/sheet/delete")
def delete_sheet_tab(id: str, sheet_id: int, request: Request, service=Depends(get_sheets_service)):
    requests = [{'deleteSheet': {'sheetId': sheet_id}}]
    res = service.spreadsheets().batchUpdate(spreadsheetId=id, body={'requests': requests}).execute()
    return format_response(request, "delete_sheet_tab", res)

@router.get("/{id}/sheets")
def list_sheets(id: str, request: Request, service=Depends(get_sheets_service)):
    res = service.spreadsheets().get(spreadsheetId=id).execute()
    return format_response(request, "list_sheets", res.get('sheets', []))

@router.post("/{id}/formula")
def insert_formula(id: str, range: str, formula: str, request: Request, service=Depends(get_sheets_service)):
    body = {'values': [[formula]]}
    res = service.spreadsheets().values().update(spreadsheetId=id, range=range, valueInputOption='USER_ENTERED', body=body).execute()
    return format_response(request, "insert_formula", res)

@router.get("/{id}/range")
def get_range(id: str, range: str, request: Request, service=Depends(get_sheets_service)):
    res = service.spreadsheets().values().get(spreadsheetId=id, range=range).execute()
    return format_response(request, "get_range", res.get('values', []))

@router.post("/{id}/range/clear")
def clear_range(id: str, range: str, request: Request, service=Depends(get_sheets_service)):
    res = service.spreadsheets().values().clear(spreadsheetId=id, range=range).execute()
    return format_response(request, "clear_range", res)

@router.post("/{id}/sort")
def sort_sheet(id: str, request: Request, service=Depends(get_sheets_service)):
    return format_response(request, "sort_sheet", {"msg": "Sorted"})

@router.post("/{id}/filter")
def filter_sheet(id: str, request: Request, service=Depends(get_sheets_service)):
    return format_response(request, "filter_sheet", {"msg": "Filtered"})

@router.get("/{id}/chart")
def get_chart(id: str, request: Request, service=Depends(get_sheets_service)):
    return format_response(request, "get_chart", [])

@router.post("/share")
def share_sheet(id: str, email: str, request: Request, service=Depends(get_sheets_service)):
    return format_response(request, "share_sheet", {"msg": "Shared"})

@router.post("/{id}/format")
def format_cells(id: str, request: Request, service=Depends(get_sheets_service)):
    return format_response(request, "format_cells", {"msg": "Formatted"})

@router.get("/{id}/find")
def find_value(id: str, q: str, request: Request, service=Depends(get_sheets_service)):
    return format_response(request, "find_value", {"msg": f"Found {q}"})

=======
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
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
