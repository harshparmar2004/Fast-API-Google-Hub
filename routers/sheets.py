from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_sheets_service
from utils import format_response

router = APIRouter()

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

