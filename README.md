# Smart Banking System

A full-stack banking chatbot demo built with **FastAPI (Python)** and a responsive **HTML/CSS/JS frontend**.

It supports:
- balance checks
- transaction history
- money transfer with confirmation
- Dialogflow webhook integration (optional)

---

## What you built

You migrated the backend flow from legacy Node/Firebase-style fulfillment to a modern FastAPI service and added:

- A direct chat API (`POST /api/chat`) that works **without Dialogflow**
- A Dialogflow-compatible webhook (`POST /webhook`)
- Demo banking data with checking/savings accounts and transaction history
- Session-based pending transfer confirmation flow
- Frontend chat interface for user interaction
- Docker and Render deployment support
- Automated backend tests (`pytest`)

---

## Is chat using Dialogflow?

**Short answer: it can, but it does not have to.**

This project supports **two modes**:

1. **Direct mode (current frontend path):**  
   Frontend calls `POST /api/chat` directly.  
   This mode does **not require Dialogflow**.

2. **Dialogflow mode (optional):**  
   Dialogflow sends requests to `POST /webhook`.  
   FastAPI handles intents and returns Dialogflow-formatted fulfillment responses.

So your deployed app can run fully even if Dialogflow is not connected.

---

## Architecture overview

```text
Browser UI (frontend/index.html)
        |
        |  POST /api/chat
        v
FastAPI backend (backend/main.py)
  - intent detection / routing
  - business handlers
  - session transfer state
  - mock user/account data
        |
        +--> optional Dialogflow webhook path: POST /webhook
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
- `POST /api/chat` - direct chatbot endpoint
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

---

## Tech stack

- **Backend:** FastAPI, Uvicorn, Pydantic
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
- works directly through FastAPI
- optionally supports Dialogflow webhook integration
- is testable, deployable, and easy to showcase.
