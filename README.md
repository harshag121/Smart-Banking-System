# Smart Banking System

A full-stack banking chatbot demo built with **FastAPI (Python)** and a responsive **HTML/CSS/JS frontend**.

It supports:
- balance checks
- transaction history
- money transfer with confirmation
- Dialogflow detectIntent + webhook integration

---

## What you built

You migrated the backend flow from legacy Node/Firebase-style fulfillment to a modern FastAPI service and added:

- A direct chat API (`POST /api/chat`) that can run in **Dialogflow-first mode**
- A Dialogflow-compatible webhook (`POST /webhook`) for fulfillment
- Demo banking data with checking/savings accounts and transaction history
- Session-based pending transfer confirmation flow
- Frontend chat interface for user interaction
- Docker and Render deployment support
- Automated backend tests (`pytest`)

---

## Is chat using Dialogflow?

**Short answer: yes, when Dialogflow mode is enabled.**

This project supports **two modes**:

1. **Dialogflow-first mode (recommended for evaluation):**  
   Frontend still calls `POST /api/chat`, but backend forwards the text to Dialogflow `detectIntent` and returns Dialogflow response.
   Enable it with:
   - `DIALOGFLOW_ENABLED=true`
   - `DIALOGFLOW_PROJECT_ID=<your-project-id>`
   - `GOOGLE_APPLICATION_CREDENTIALS=<service-account-json-path>`

2. **Webhook mode:**  
   Dialogflow sends requests to `POST /webhook`.  
   FastAPI handles intents and returns Dialogflow-formatted fulfillment responses.

There is also a local fallback mode (when `DIALOGFLOW_ENABLED=false`) for offline demo/testing.

---

## Architecture overview

```text
Browser UI (frontend/index.html)
        |
        |  POST /api/chat
        v
FastAPI backend (backend/main.py)
  - Dialogflow detectIntent client (if enabled)
  - fallback local intent handlers
  - session transfer state
  - mock user/account data
        |
        +--> Dialogflow webhook path: POST /webhook
```

---

## Core features

### 1) Balance check
- Returns checking + savings balances
- Can respond to specific account requests

### 2) Transfer money
- Parses amount/from/to accounts
- Validates accounts and sufficient funds
- Asks for confirmation
- On confirmation, updates balances + transaction history

### 3) Transaction history
- Returns recent transactions by account

### 4) Help + fallback
- Guides users with example commands

---

## API endpoints

- `GET /` - service status
- `GET /health` - health check
- `GET /ui` - serves chat UI file
- `POST /api/chat` - chat endpoint (Dialogflow detectIntent when enabled)
- `POST /webhook` - Dialogflow fulfillment endpoint
- `GET /api/user` - demo user/account info
- `GET /api/user/transactions?account=checking` - account transactions

---

## Local run

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on: `http://localhost:8000`

### Enable Dialogflow-first mode

Edit `backend/.env`:

```env
DIALOGFLOW_ENABLED=true
DIALOGFLOW_PROJECT_ID=your-gcp-project-id
DIALOGFLOW_LANGUAGE_CODE=en
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
```

Then restart backend.

### Dialogflow setup (step-by-step)

1. Create/select a Google Cloud project.
2. Enable APIs:
   - Dialogflow API
   - IAM Service Account Credentials API
3. Create a service account and grant **Dialogflow API Client** role.
4. Create and download JSON key for that service account.
5. Put JSON path into `GOOGLE_APPLICATION_CREDENTIALS` in `.env`.
6. In Dialogflow ES, create intents (Welcome, Check Balance, Transfer, Confirm, Transactions, Help).
7. Start backend and test with:

```bash
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"message\":\"check my balance\",\"session_id\":\"demo1\"}"
```

### Frontend
Open:
- `frontend/index.html` directly, or
- serve frontend folder and open in browser.

If using direct file open, frontend points to local API URL in script config.

---

## Run tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

Current test suite validates:
- health endpoints
- chat endpoint behavior
- user and transactions endpoints
- Dialogflow webhook behavior

---

## Deploy (free) - Render

This repo includes `render.yaml`.

1. Push repository to GitHub
2. In Render: **New + -> Blueprint**
3. Select this repo
4. Deploy

After deployment:
- API root: `https://<your-service>.onrender.com/`
- UI: `https://<your-service>.onrender.com/ui`

### Render environment variables for Dialogflow

Set these in Render service settings:

- `DIALOGFLOW_ENABLED=true`
- `DIALOGFLOW_PROJECT_ID=<your-project-id>`
- `DIALOGFLOW_LANGUAGE_CODE=en`
- `GOOGLE_APPLICATION_CREDENTIALS=<path in container OR use secret-file strategy>`

If you cannot mount a file path on Render, use a secret file approach (recommended) and point `GOOGLE_APPLICATION_CREDENTIALS` to that mounted file path.

---

## Free tier / cost notes

For demo and interview traffic, this setup is typically free:

- **Render**: free web service tier (sleeps when idle, cold starts).
- **Dialogflow ES**: free quota available.
- **Google Cloud project/service account**: free to create.

You may be charged only if usage exceeds free limits.

Recommended safety:

- Set GCP billing budget + alert.
- Keep app on demo-level traffic.
- Disable service when not in use.

---

## Tech stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **NLP:** Google Dialogflow CX/ES via detectIntent + webhook protocol
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Testing:** Pytest, FastAPI TestClient
- **Containerization:** Docker + docker-compose

---

## Important demo notes

This is a demo project (not production banking):
- Uses mock in-memory data
- No real authentication/authorization
- No persistent database by default
- No PCI/security hardening for real financial use

---

## Repository structure

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
├── banking_agent/      # legacy/agent reference artifacts
├── docker-compose.yml
├── render.yaml
└── README.md
```

---

## Summary

You now have a clean, demo-ready banking assistant that:
- runs through FastAPI with Dialogflow-first chat support
- supports Dialogflow webhook fulfillment integration
- is testable, deployable, and easy to showcase.
