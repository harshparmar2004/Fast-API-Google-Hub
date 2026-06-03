from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_google_credentials
from utils import format_response

router = APIRouter()

class AgentReq(BaseModel):
    prompt: str

@router.post("/run")
def run_agent(req: AgentReq, request: Request, creds=Depends(get_google_credentials)):
    system_prompt = """You are a highly capable AI Agent with full access to the user's Google Workspace via an extensive set of tools.
You have tools ranging from reading emails and calendar events to making subtasks, creating meet URLs, drafting emails, managing labels, setting filters, creating spreadsheets, updating docs, formatting slides, sharing files, extracting memories, running workflow macros (such as morning-brief, meeting-prep, email-to-task) and building automatic automations.
You can perform complex multi-step routines.
If the user asks to 'Handle my morning', you should call workflow/morning-brief, check gmail/starred, calendar/today, tasks/today.
If the user asks 'Prepare for my 3pm meeting', search calendar, run workflow/meeting-prep, search docs, search gmail.
You have the following categories of endpoints available to you:
- Gmail (Threads, Labels, Forward, Drafts, Star, Archive, Filter out...)
- Drive (Move, Copy, Rename, Share, Trash...)
- Docs (Share, Comment, Revisions...)
- Sheets (Formula, Filter, Range, Share, Sort...)
- Tasks (Lists, Reorder, Subtasks...)
- And many more for Workflow, Dashboard, Automations, Memory!
"""
    return format_response(request, "run_agent", {"agent_response": "Agent executed", "system_prompt": system_prompt})
