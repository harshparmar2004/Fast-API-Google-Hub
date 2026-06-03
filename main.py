from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import gmail, sheets, drive, calendar, docs, slides, tasks, contacts, auth_backend, meet, agent, workflow, dashboard, memory, automation
import uvicorn
import os
from database import init_db

app = FastAPI(
    title="Google Workspace Agent API",
    description="A FastAPI backend for Claude/OpenAI agents to manipulate Google Workspace apps.",
    version="1.1.0"
)

# Initialize Token Database
@app.on_event("startup")
def startup_event():
    init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the routers for different Google services
app.include_router(auth_backend.router, prefix="/api/auth", tags=["Backend Auth"])
app.include_router(gmail.router, prefix="/api/gmail", tags=["Gmail"])
app.include_router(sheets.router, prefix="/api/sheets", tags=["Sheets"])
app.include_router(drive.router, prefix="/api/drive", tags=["Drive"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(docs.router, prefix="/api/docs", tags=["Docs"])
app.include_router(slides.router, prefix="/api/slides", tags=["Slides"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(meet.router, prefix="/api/meet", tags=["Meet"])
app.include_router(agent.router, prefix="/api/agent", tags=["Agent"])\n
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(memory.router, prefix="/api/memory", tags=["Memory"])
app.include_router(automation.router, prefix="/api/automation", tags=["Automation"])


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Google Workspace Agent API is running."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
