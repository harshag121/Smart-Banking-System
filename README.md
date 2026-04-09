# Smart Banking System

A full-stack banking chatbot built with **FastAPI** and a responsive web UI, designed for demo and interview presentation.

This project supports **Dialogflow-first chat**, plus webhook fulfillment and local fallback logic.

---

## Project Highlights

- FastAPI backend with clean API routes
- Banking chatbot features: balance, transfer, transactions, help
- Dialogflow `detectIntent` integration via `/api/chat`
- Dialogflow webhook fulfillment endpoint (`/webhook`)
- Mobile-friendly frontend chat experience
- Docker + Render deployment support
- Automated tests with `pytest`

---

## Does this use Dialogflow?

**Yes.**  
When `DIALOGFLOW_ENABLED=true`, the backend forwards user chat messages to Dialogflow using `detectIntent`, then returns Dialogflow responses to the UI.

This gives you a true Dialogflow-powered flow for evaluation.

The app also includes:
- `/webhook` for Dialogflow fulfillment callbacks
- local fallback mode (`DIALOGFLOW_ENABLED=false`) for offline demo/testing

---

## Architecture

```text
Frontend (frontend/index.html)
        |
        | POST /api/chat
        v
FastAPI (backend/main.py)
  - Dialogflow detectIntent client (when enabled)
  - fallback local handlers (when disabled)
  - transfer session tracking
  - mock banking data
        |
        +--> Dialogflow webhook route: POST /webhook
```

---

## Features Implemented

### 1) Check Balance
- Returns checking and savings balances
- Supports all-account and account-specific queries

### 2) Transfer Money
- Parses amount/from/to accounts
- Validates accounts and available funds
- Uses confirmation step before execution
- Updates balances and transaction records

### 3) Transaction History
- Returns recent account transactions

### 4) Help + Fallback
- Provides supported commands and guidance

---

## API Endpoints

- `GET /` - service status
- `GET /health` - health endpoint
- `GET /ui` - serves chat UI
- `POST /api/chat` - main chat endpoint (Dialogflow-first when enabled)
- `POST /webhook` - Dialogflow fulfillment webhook
- `GET /api/user` - demo user/account information
- `GET /api/user/transactions?account=checking` - transaction history

---

## Dialogflow-first Setup (Step-by-step)

### 1) Google Cloud setup
1. Create/select a Google Cloud project.
2. Enable:
   - Dialogflow API
   - IAM Service Account Credentials API

### 2) Service account
1. Create a service account.
2. Grant role: **Dialogflow API Client**.
3. Create/download JSON key.

### 3) Dialogflow agent
1. Create/select Dialogflow ES agent in same project.
2. Configure intents (example):
   - Welcome
   - Check Balance
   - Transfer Money
   - Confirm Transfer
   - Transaction History
   - Help

### 4) Backend environment
Edit `backend/.env`:

```env
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
PROJECT_NAME=Banking Chatbot API

DIALOGFLOW_ENABLED=true
DIALOGFLOW_PROJECT_ID=your-gcp-project-id
DIALOGFLOW_LANGUAGE_CODE=en
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
```

### 5) Run backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 6) Quick verification
```bash
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"message\":\"check my balance\",\"session_id\":\"demo1\"}"
```

---

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
Open:
- `frontend/index.html`, or
- serve frontend with a local web server.

Backend default URL: `http://localhost:8000`

---

## Testing

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

Current test coverage includes:
- health and root endpoints
- chat behavior
- user and transaction endpoints
- Dialogflow webhook endpoint behavior

---

## Free Deployment (Render)

This repo includes `render.yaml`.

1. Push repository to GitHub.
2. In Render: **New + -> Blueprint**
3. Select this repository.
4. Deploy.

After deployment:
- API: `https://<your-service>.onrender.com/`
- UI: `https://<your-service>.onrender.com/ui`

### Render env vars for Dialogflow

Set in Render service settings:

- `DIALOGFLOW_ENABLED=true`
- `DIALOGFLOW_PROJECT_ID=<your-project-id>`
- `DIALOGFLOW_LANGUAGE_CODE=en`
- `GOOGLE_APPLICATION_CREDENTIALS=<path to mounted secret file>`

If file path mounting is not available in your plan, use Render secret-file strategy and point this variable to that mounted path.

---

## Cost / Free Tier Notes

For demo-level traffic this is usually free:

- **Render Free tier** (with sleep/cold starts)
- **Dialogflow ES free quota**
- **GCP project + service account creation is free**

Charges may apply only when usage exceeds free quotas.

Recommended safety:
- Set GCP budget + billing alerts
- Keep demo traffic low
- Turn off unused services

---

## Tech Stack

- Backend: FastAPI, Uvicorn, Pydantic
- NLP: Google Dialogflow ES (`detectIntent` + webhook protocol)
- Frontend: HTML, CSS, JavaScript
- Testing: Pytest, FastAPI TestClient
- Deployment: Docker, docker-compose, Render

---

## Repository Structure

```text
Smart-Banking-System/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── test_main.py
│   └── ...
├── frontend/
│   └── index.html
├── banking_agent/      # legacy/reference artifacts
├── docker-compose.yml
├── render.yaml
└── README.md
```

---

## Demo Disclaimer

This is a demonstration application:
- Uses mock in-memory data
- No real banking integration
- No production-grade auth/compliance hardening by default

---

## Summary

This project is a complete, demo-ready banking chatbot that:
- runs on FastAPI
- supports Dialogflow-first chat behavior
- includes webhook fulfillment
- is easy to test, deploy, and present.
