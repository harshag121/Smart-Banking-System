# Banking Chatbot - Complete Application

## 🎯 What Was Built

A **complete FastAPI banking chatbot system** replacing the original Node.js Firebase Functions backend with a modern Python framework.

### ✅ Includes:
- **FastAPI Backend** - RESTful API with Dialogflow webhook support
- **HTML Frontend** - Interactive chat interface
- **Docker Support** - Easy containerization and deployment
- **Comprehensive Docs** - Full API documentation
- **Test Suite** - Unit tests for all endpoints
- **Production Ready** - CORS, error handling, health checks

---

## 📦 Complete File Structure

```
Smart-Banking-System/
│
├── QUICKSTART.md                  ← Start here! (5-minute setup)
├── README_FASTAPI.md             ← Full documentation
├── README.md                       ← Project info
│
├── backend/                        ← FastAPI Application
│   ├── main.py                    ← Main API (400+ lines)
│   ├── config.py                  ← Configuration management
│   ├── test_main.py               ← Unit tests
│   ├── conftest.py                ← Test fixtures
│   │
│   ├── requirements.txt            ← Core dependencies
│   ├── requirements-dev.txt        ← Dev dependencies
│   │
│   ├── .env                        ← Environment config
│   ├── Dockerfile                  ← Container image
│   │
│   ├── run.sh                      ← Linux/Mac startup
│   └── run.bat                     ← Windows startup
│
├── frontend/                       ← Web UI
│   └── index.html                 ← Chat interface (500+ lines)
│
├── banking_agent/                  ← Reference only
│   ├── agent.json                 ← Dialogflow config
│   ├── functions/                 ← Original Node.js code
│   └── public/                    ← Original HTML
│
├── docker-compose.yml              ← Full stack (API + Frontend + Nginx)
├── nginx.conf                      ← Web server configuration
│
└── .git/                           ← Version control
```

---

## 🚀 Getting Started (Choose One)

### Option 1: Quick Start (Recommended)
```bash
cd backend
python main.py
```
Then open `frontend/index.html` in your browser.

See `QUICKSTART.md` for detailed steps.

### Option 2: Full Stack with Docker
```bash
docker-compose up -d
```
Then visit: `http://localhost`

### Option 3: Development with Auto-reload
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🎮 Features Implemented

✅ **Check Balance** - View checking/savings account balances
✅ **Transfer Money** - Transfer between accounts with confirmation
✅ **Transaction History** - View recent transactions
✅ **Session Management** - Track pending transfers per session
✅ **Dialogflow Integration** - Full webhook support
✅ **Direct Chat API** - Works without Dialogflow
✅ **User Management** - Demo user with mock data
✅ **Error Handling** - Proper error responses
✅ **CORS Support** - Works with any frontend
✅ **Health Checks** - Kubernetes/LB ready

---

## 📡 API Endpoints

### Core Endpoints
```
POST   /api/chat                    Chat with the bot
GET    /api/user                    Get user information
GET    /api/user/transactions       Get transaction history
POST   /webhook                     Dialogflow webhook
GET    /health                      Health check
GET    /docs                        Interactive Swagger UI
```

### Examples

**Chat Request:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Check my balance","session_id":"test"}'
```

**Response:**
```json
{
  "text": "Here are your account balances:\n\n🏦 **Checking** (****4532): $2,547.83\n💎 **Savings** (****7891): $12,750.00",
  "suggestions": ["Transfer Money", "Transaction History"]
}
```

---

## 🧪 Testing

### Run Tests
```bash
cd backend
pip install -r requirements-dev.txt
pytest test_main.py -v
```

### Run Single Test
```bash
pytest test_main.py::TestChatEndpoint::test_balance_query -v
```

### Test with cURL
```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

---

## 🔐 Demo Data

**User:** John Demo
**ID:** user-123

**Checking Account:**
- Balance: $2,547.83
- Number: ****4532

**Savings Account:**
- Balance: $12,750.00
- Number: ****7891

Sample transactions included for both accounts.

---

## 🛠 Configuration

Edit `backend/.env`:
```ini
DEBUG=True              # Debug mode
API_HOST=0.0.0.0      # Server address
API_PORT=8000         # Server port
PROJECT_NAME=Banking Chatbot API
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | 5-minute startup guide |
| `README_FASTAPI.md` | Complete documentation |
| `backend/test_main.py` | Unit tests with examples |
| `http://localhost:8000/docs` | Interactive API docs |

---

## 🐳 Docker Deployment

### Single Container
```bash
cd backend
docker build -t banking-api .
docker run -p 8000:8000 banking-api
```

### Full Stack (API + Frontend + Nginx)
```bash
docker-compose up -d
# Visit http://localhost
```

---

## 🔍 What Changed from Original

| Feature | Original (Node.js) | New (FastAPI) |
|---------|-------------------|---------------|
| Backend | Firebase Functions | FastAPI |
| Language | JavaScript | Python |
| Setup | Firebase CLI + config | Simple pip install |
| Documentation | Minimal | Comprehensive |
| Testing | Not included | Full test suite |
| Docker | Not included | Included |
| Database | Firestore (cloud) | In-memory (can add) |
| Performance | Cold starts | Fast startup |
| Development | Complex setup | Simple setup |

**Original files kept for reference:**
- `banking_agent/` - Dialogflow configuration
- `banking_agent/functions/index.js` - Original Node.js code
- `README.md` - Original project info

---

## 💡 Next Steps

1. **Run the app** - Follow QUICKSTART.md
2. **Test endpoints** - Use `/docs` endpoint
3. **Explore code** - Read comments in `backend/main.py`
4. **Add features** - Extend handlers in main.py
5. **Deploy** - Use docker-compose for production

---

## 🌟 Highlights

- **Modern Python** - FastAPI, Pydantic, async/await
- **FastAPI Features** - Auto OpenAPI/Swagger docs
- **Production Ready** - Docker, Nginx, health checks
- **Well Documented** - Inline comments, README, guides
- **Fully Tested** - 15+ unit tests included
- **Easy Development** - Simple structure, quick changes
- **Scalable** - Can add database, auth, logging

---

## ⚙️ Technology Stack

**Backend:**
- Python 3.11+
- FastAPI 0.104+
- Uvicorn (ASGI server)
- Pydantic (validation)

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript
- No frameworks/dependencies

**Deployment:**
- Docker & Docker Compose
- Nginx web server
- Python environment

**Testing:**
- Pytest
- TestClient (FastAPI testing)
- Http fixtures

---

## 🎓 Learning Resources

- **Quick Setup** - Read QUICKSTART.md (5 min)
- **API Docs** - Visit http://localhost:8000/docs
- **Full Docs** - Read README_FASTAPI.md (30 min)
- **Code Comments** - See inline docs in main.py
- **Tests** - See examples in test_main.py

---

## 📞 Quick Help

**Q: How do I start?**
A: Run `QUICKSTART.md` - it's 5 minutes!

**Q: How do I test?**
A: Visit `http://localhost:8000/docs` - interactive testing

**Q: How do I deploy?**
A: Use `docker-compose up -d` or the Dockerfile

**Q: How do I add features?**
A: Edit the handler functions in `backend/main.py`

**Q: How do I use a database?**
A: See production section in README_FASTAPI.md

---

## ✨ Ready to Go!

Everything is set up and ready to use. No additional configuration needed for basic usage.

→ **Start with:** `QUICKSTART.md` or `backend/run.bat` (Windows) / `backend/run.sh` (Mac/Linux)

---

**Built with FastAPI • Full Stack • Production Ready** 🚀
