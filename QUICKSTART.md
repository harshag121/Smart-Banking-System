# 🚀 Quick Start Guide - Banking Chatbot with FastAPI

## What's New?

✅ **FastAPI Backend** - Modern, fast Python web framework replacing Node.js
✅ **Production Ready** - Includes Docker, Nginx, health checks
✅ **Full Integration** - Works with Dialogflow or standalone
✅ **Complete Feature Set** - Balance, transfers, transactions, session management

---

## 📋 Prerequisites

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** (optional) - For version control

---

## ⚡ Quick Start (5 minutes)

### Step 1: Install Backend

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start API Server

**On Mac/Linux:**
```bash
bash run.sh
```

**On Windows:**
```bash
run.bat
```

**Or directly:**
```bash
python main.py
```

✅ Server running at: `http://localhost:8000`

### Step 3: Open Frontend

Open `frontend/index.html` in your browser or serve it:

```bash
cd frontend
python -m http.server 8080
```

Then visit: `http://localhost:8080`

---

## 🧪 Test the API

### Using Browser
1. Open `http://localhost:8000/docs` - Interactive API documentation
2. Try the endpoints in the Swagger UI

### Using cURL
```bash
# Check if API is running
curl http://localhost:8000/

# Chat request
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Check my balance","session_id":"test"}'

# Get user info
curl http://localhost:8000/api/user

# Get transactions
curl http://localhost:8000/api/user/transactions?account=checking
```

---

## 📁 Project Structure

```
Smart-Banking-System/
├── backend/
│   ├── main.py              ← Main FastAPI app
│   ├── requirements.txt      ← Dependencies
│   ├── .env                 ← Config
│   ├── Dockerfile           ← Container setup
│   ├── run.sh              ← Linux/Mac startup
│   └── run.bat             ← Windows startup
├── frontend/
│   └── index.html          ← Chat UI
├── docker-compose.yml       ← Full stack setup
├── nginx.conf              ← Web server config
└── README_FASTAPI.md        ← Full documentation
```

---

## 🎯 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send chat message |
| GET | `/api/user` | Get user information |
| GET | `/api/user/transactions` | Get transaction history |
| POST | `/webhook` | Dialogflow webhook |
| GET | `/health` | Health check |
| GET | `/docs` | API documentation |

---

## 💬 Chat Examples

```
User: "Check my balance"
Bot: Shows checking and savings balance

User: "Transfer $100 from checking to savings"
Bot: Asks for confirmation

User: "Yes, confirm"
Bot: Executes transfer and shows new balances

User: "Show my transactions"
Bot: Shows recent transaction history

User: "Help"
Bot: Shows available commands
```

---

## 🐳 Docker Deployment (Optional)

### Single Container
```bash
cd backend
docker build -t banking-chatbot .
docker run -p 8000:8000 banking-chatbot
```

### Full Stack (API + Frontend + Web Server)
```bash
docker-compose up -d
```

Then visit: `http://localhost`

---

## 🔧 Configuration

Edit `backend/.env`:
```
DEBUG=True              # Debug mode
API_HOST=0.0.0.0      # Bind address
API_PORT=8000         # Port number
PROJECT_NAME=...      # App name
```

---

## 🧠 How It Works

### Request Flow
```
Client Request → Frontend (index.html)
                  ↓
                FastAPI Backend (main.py)
                  ↓
              Intent Handler Function
                  ↓
              Mock Database Lookup
                  ↓
              Generate Response
                  ↓
                API Response
                  ↓
              Display in Chat UI
```

### Intent Routing
```
Message → Keyword Detection → Intent Handler
  │
  ├─ "balance" → check_balance_handler()
  ├─ "transfer" → transfer_money_handler()
  ├─ "transaction" → transaction_history_handler()
  ├─ "help" → help_handler()
  └─ (default) → fallback_handler()
```

---

## 📊 Demo User

```
Name: John Demo
User ID: user-123

Checking Account:
  Balance: $2,547.83
  Number: ****4532

Savings Account:
  Balance: $12,750.00
  Number: ****7891
```

Sample transactions are included in the database.

---

## ⚠️ Important Notes

### For Development
✅ Perfect as-is for testing and learning
✅ In-memory session storage (resets on restart)
✅ Mock data only (no real banking)

### For Production
⚠️ Add authentication
⚠️ Use real database (PostgreSQL, MongoDB, etc.)
⚠️ Enable SSL/TLS
⚠️ Implement logging and monitoring
⚠️ Add rate limiting
⚠️ Secure Dialogflow integration
⚠️ Follow PCI-DSS compliance

See `README_FASTAPI.md` for detailed security recommendations.

---

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### CORS error in browser
Check `frontend/index.html` API URL:
```javascript
const API_CONFIG = {
    apiUrl: 'http://localhost:8000'  // Update if needed
};
```

### Module not found error
```bash
cd backend
pip install -r requirements.txt
```

### Can't connect to API
1. Make sure backend is running: `python main.py`
2. Check port is correct: `http://localhost:8000`
3. Check firewall settings
4. Try: `curl http://localhost:8000/health`

---

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Uvicorn Docs**: https://www.uvicorn.org
- **Dialogflow Docs**: https://cloud.google.com/dialogflow/docs
- **Interactive Docs**: `http://localhost:8000/docs` (when running)

---

## 🚀 Next Steps

1. ✅ Backend running
2. ✅ Frontend working
3. 📌 (Optional) Integrate with Dialogflow
4. 📌 (Optional) Connect to real database
5. 📌 (Optional) Deploy to cloud

---

## 📞 Support

- Check `README_FASTAPI.md` for detailed documentation
- Review API docs at `http://localhost:8000/docs`
- Check browser console for frontend errors
- Check terminal for backend errors

---

**Happy Banking! 🏦**
