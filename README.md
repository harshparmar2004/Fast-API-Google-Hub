# Google Workspace Agent API (FastAPI)

This is a separate FastAPI backend designed specifically to act as an API surface for AI Agents (like open Claude, OpenAI agents) to interact with Google Workspace tools.

## How it works
This API uses **Bearer Token Authentication**. Your AI Agent needs to obtain a Google Access Token (which the frontend React app already collects during login) and pass it in the headers of requests to this API.

`Authorization: Bearer <google_access_token>`

## Exporting for Render Deployment

Since you requested this as a separate repository for deployment on Render:

1. Copy this `fastapi-backend` folder to your local machine (You can export this entire project as a ZIP from the top right settings menu, then extract the `fastapi-backend` folder).
2. Initialize a git repository inside the `fastapi-backend` folder:
   ```bash
   cd fastapi-backend
   git init
   git add .
   git commit -m "Initial commit for FastAPI backend"
   ```
3. Push it to a new GitHub repository or connect directly to Render.
4. Render will automatically detect the `requirements.txt` and python files and build the app! 

*(Ensure that the start command on Render uses Uvicorn, which is default, or specify a start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`).*

## Endpoints Created

- `GET /api/gmail/messages`: List emails
- `POST /api/gmail/send`: Send emails
- `POST /api/sheets/update`: Write data to sheets
- `GET /api/sheets/{spreadsheet_id}?range=A1:B10`: Read data from sheets

*(You can expand the `routers/` folder to add Docs, Calendar, Contacts, and other Google APIs using the same authentication pattern).*
