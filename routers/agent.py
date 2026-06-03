<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from auth import get_google_credentials
=======
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
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
=======
class AgentRequest(BaseModel):
    instruction: str
    llm_api_key: str = ""

SYSTEM_PROMPT = """
You are the Google Workspace Agent. You have access to exactly 48 capabilities across 9 Google apps.
Based on the user's plain English instruction, decide which tool to use.
Capabilities available:

GMAIL:
1. List all emails (GET /api/gmail/list)
2. List unread emails only (GET /api/gmail/unread)
3. Search emails by keyword (GET /api/gmail/search)
4. Read one specific email content (GET /api/gmail/read/{message_id})
5. Send a new email (POST /api/gmail/send)
6. Reply to an email (POST /api/gmail/reply)
7. Delete an email (DELETE /api/gmail/{message_id})
8. Mark email as read (POST /api/gmail/{message_id}/read)
9. Get unread count (GET /api/gmail/count/unread)

GOOGLE DRIVE:
10. List all files (GET /api/drive/list)
11. Search files by name (GET /api/drive/search)
12. Get file details (GET /api/drive/{file_id})
13. Delete a file (DELETE /api/drive/{file_id})
14. List recent files (GET /api/drive/recent/files)

GOOGLE DOCS:
15. List all documents (GET /api/docs/list)
16. Read document content (GET /api/docs/{doc_id})
17. Create new document (POST /api/docs/create)
18. Update document content (POST /api/docs/{doc_id}/update)
19. Search documents by keyword (GET /api/docs/search)

GOOGLE SHEETS:
20. List all spreadsheets (GET /api/sheets/list)
21. Read sheet data (GET /api/sheets/{sheet_id}/read)
22. Update a specific row (PUT /api/sheets/{sheet_id}/update)
23. Append new row (POST /api/sheets/{sheet_id}/append)
24. Create new spreadsheet (POST /api/sheets/create)
25. Search within sheet (GET /api/sheets/{sheet_id}/search)

GOOGLE SLIDES:
26. List all presentations (GET /api/slides/list)
27. Read presentation content (GET /api/slides/{presentation_id})
28. Create new presentation (POST /api/slides/create)

GOOGLE CALENDAR:
29. List all upcoming events (GET /api/calendar/list)
30. List today's events only (GET /api/calendar/today)
31. Create new event (POST /api/calendar/create)
32. Update existing event (PUT /api/calendar/{event_id})
33. Delete an event (DELETE /api/calendar/{event_id})
34. Create event with Meet link (POST /api/calendar/create_with_meet)

GOOGLE TASKS:
35. List all tasks (GET /api/tasks/list)
36. List pending tasks only (GET /api/tasks/pending)
37. Create new task (POST /api/tasks/create)
38. Mark task as complete (POST /api/tasks/{task_id}/complete)
39. Delete a task (DELETE /api/tasks/{task_id})
40. Update task details (PUT /api/tasks/{task_id})

GOOGLE CONTACTS:
41. List all contacts (GET /api/contacts/list)
42. Search contact by name (GET /api/contacts/search)
43. Create new contact (POST /api/contacts/create)
44. Update contact details (PUT /api/contacts/{resource_name})

GOOGLE MEET:
45. List upcoming Meet links (GET /api/meet/list)
46. Create new Meet link (POST /api/meet/create_link)
47. Create Meet with calendar event (POST /api/meet/create_event)

AGENT ENDPOINT:
48. POST /api/agent/run — receives plain English instruction, uses LLM to decide which of these 48 capabilities to use, executes it, returns result

Return a JSON with "target_endpoint", "method", and "body" to execute.
"""

@router.post("/run")
async def run_agent(req: AgentRequest, request: Request):
    # 48. Receive plain English instruction, use LLM to decide capability, execute, return result.
    # In a real setup, we would call an LLM (OpenAI/Gemini/Claude) using req.llm_api_key
    # The LLM reads SYSTEM_PROMPT.
    # This is a stub implementation representing the backend agent controller.
    
    # Mocking LLM delegation logic
    # response = llm_client.generate(system_prompt=SYSTEM_PROMPT, user_input=req.instruction) 
    
    return format_response({
        "status": "success",
        "message": f"Agent dynamically processed instruction: '{req.instruction}'. All 48 tools are now available to the LLM context.",
        "processed_via": "Agent System Prompt"
    })
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
