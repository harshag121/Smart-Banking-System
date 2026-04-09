# Smart Banking System - FastAPI Backend

A complete banking chatbot system with FastAPI backend and HTML frontend, replacing the original Node.js Firebase Functions implementation.

## Project Structure

```
Smart-Banking-System/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   ├── requirements.txt      # Python dependencies
│   └── .env                 # Environment configuration
├── frontend/
│   └── index.html           # Chat UI (updated for FastAPI)
├── banking_agent/           # Original Dialogflow configuration
│   ├── agent.json          # Agent config
│   ├── firebase.json       # Firebase config (reference only)
│   ├── functions/          # Original Node.js code (reference only)
│   └── public/             # Original HTML (legacy)
└── README_FASTAPI.md        # This file
```

## Features

✅ **Check Balance** - View checking and savings account balances
✅ **Transfer Money** - Transfer funds between accounts with confirmation
✅ **Transaction History** - View recent transactions
✅ **Session Management** - Track pending transfers per session
✅ **User Management** - Demo user with mock data
✅ **Dialogflow Integration** - Webhook support for Dialogflow fulfillment
✅ **Direct API** - Alternative chat endpoint without Dialogflow
✅ **CORS Enabled** - Works with any frontend
✅ **Health Checks** - Kubernetes/LB ready

## Installation

### Backend Setup

1. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment**
The `.env` file is already configured with defaults:
```
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
PROJECT_NAME=Banking Chatbot API
```

3. **Run the FastAPI server**
```bash
python main.py
# OR
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### Frontend Setup

1. **Open the frontend**
Simply open `frontend/index.html` in a browser, or serve it with a local web server:
```bash
cd frontend
python -m http.server 8080
```

Then visit: `http://localhost:8080`

## API Endpoints

### Health Check
```
GET /
GET /health
GET /ui
```

### Dialogflow Webhook (for Dialogflow integration)
```
POST /webhook
```
Request body (Dialogflow format):
```json
{
  "session": "projects/PROJECT_ID/agent/sessions/SESSION_ID",
  "queryResult": {
    "intent": {
      "displayName": "Check Balance"
    },
    "parameters": {
      "account-type": "checking"
    }
  }
}
```

### Direct Chat API (recommended for testing)
```
POST /api/chat
```
Request body:
```json
{
  "message": "Check my balance",
  "session_id": "demo-session-12345"
}
```

Response:
```json
{
  "text": "Your checking account (****4532) balance is:\n\n💰 **$2,547.83**",
  "suggestions": ["Transfer Money", "View Transactions"]
}
```

### User Information
```
GET /api/user?user_id=user-123
```

Response:
```json
{
  "name": "John Demo",
  "accounts": {
    "checking": {
      "balance": 2547.83,
      "accountNumber": "****4532"
    },
    "savings": {
      "balance": 12750.00,
      "accountNumber": "****7891"
    }
  }
}
```

### Transaction History
```
GET /api/user/transactions?account=checking&user_id=user-123
```

Response:
```json
{
  "account": "checking",
  "transactions": [
    {
      "date": "2026-04-08",
      "desc": "Grocery Store",
      "amount": -87.43
    }
  ]
}
```

## Intent Handlers

The system automatically routes to the appropriate handler based on intent:

### 1. Default Welcome Intent
Shows welcome message and available actions.

### 2. Check Balance
Shows account balances. Supports:
- All accounts: "What's my balance?"
- Specific account: "Check my savings"

### 3. Transfer Money
Initiates a transfer. Requires:
- Amount
- From account (checking/savings)
- To account (checking/savings)

Example: "Transfer $100 from checking to savings"

### 4. Confirm Transfer
Executes the pending transfer after confirmation.
- "Yes, confirm" - Execute transfer
- "No, cancel" - Cancel transfer

### 5. Transaction History
Shows recent transactions for an account.
- Checking by default
- "Show my savings transactions" for savings

### 6. Help
Shows available commands and examples.

### 7. Default Fallback
Handles unrecognized intents.

## Mock Database

The system uses an in-memory mock database with demo user:

```python
User: John Demo (user-123)
Checking Account: $2,547.83 (****4532)
Savings Account: $12,750.00 (****7891)
```

Sample transactions are included for demonstration.

## Features Implementation

### Session Management
Pending transfers are stored in memory:
```python
PENDING_TRANSFERS = {
    'session-id': {
        'amount': 100.00,
        'from': 'checking',
        'to': 'savings',
        'timestamp': '2026-04-09T10:30:00'
    }
}
```

### Data Persistence
Currently uses in-memory storage. For production:
- Replace `MOCK_DATABASE` with database client (PostgreSQL, MongoDB, etc.)
- Add proper authentication and authorization
- Implement transaction logging for compliance
- Add encryption for sensitive data

## Configuration

### Environment Variables
```
DEBUG=True              # Enable debug mode
API_HOST=0.0.0.0      # API host
API_PORT=8000         # API port
PROJECT_NAME=...      # Application name
```

### CORS Configuration
Currently allows all origins for demo. For production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],               # Only needed methods
    allow_headers=["Content-Type"],              # Only needed headers
)
```

## Security Considerations

⚠️ **Demo Features (for development only):**
- Static user ID (no authentication)
- In-memory session storage
- No data encryption
- CORS allows all origins

🔒 **For Production:**

1. **Authentication**
   - Implement OAuth 2.0 or JWT
   - Add user authentication before processing requests

2. **Database**
   - Use proper database (PostgreSQL, MongoDB, etc.)
   - Add connection pooling
   - Implement transaction logging

3. **Security**
   - Add SSL/TLS
   - Implement rate limiting
   - Add request validation and sanitization
   - Encrypt sensitive data in transit and at rest

4. **Compliance**
   - Implement audit logging
   - Add data encryption
   - Follow PCI-DSS for financial data
   - Add proper error handling (don't expose internal errors)

## Testing

### Test with cURL
```bash
# Check health
curl http://localhost:8000/

# Chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Check my balance","session_id":"test-123"}'

# Get user info
curl http://localhost:8000/api/user

# Get transactions
curl http://localhost:8000/api/user/transactions?account=checking
```

### Test with Python
```python
import requests

url = "http://localhost:8000/api/chat"
data = {
    "message": "What is my balance?",
    "session_id": "test-123"
}
response = requests.post(url, json=data)
print(response.json())
```

## Dialogflow Integration

If integrating with Dialogflow:

1. **Update webhook URL in Dialogflow:**
   - Go to Fulfillment section
   - Set webhook URL to: `https://your-domain/webhook`

2. **Update frontend configuration:**
   Edit `frontend/index.html`:
   ```javascript
   const API_CONFIG = {
       apiUrl: 'https://your-domain',
       chatEndpoint: '/api/chat',
       webhookEndpoint: '/webhook'
   };
   ```

3. **Use Dialogflow intents:**
   - Intent names must match handler names
   - Parameters must match parameter names in requests

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Options
- **Heroku**: Add `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Google Cloud Run**: Container deployment
- **AWS Lambda**: Requires Lambda wrapper
- **Azure App Service**: Container or direct Python deployment

### Free deployment (recommended)

This repo includes `render.yaml` for one-click deployment on Render Free plan.

1. Push this repository to GitHub.
2. In Render, choose **New +** -> **Blueprint** and select your repo.
3. Render will detect `render.yaml`, build from `backend/`, and run:
   - Build: `pip install -r requirements-dev.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. After deploy, open:
   - API docs: `https://<your-app>.onrender.com/docs`
   - Mobile UI: `https://<your-app>.onrender.com/ui`

Notes:
- `/ui` is now served by FastAPI, so frontend and backend are on the same domain (no CORS issues for demo usage).
- The standalone `frontend/index.html` still works locally.

### Mobile UX notes

- Updated UI is phone-first and optimized for touch:
  - Full-height layout on mobile
  - Larger touch targets for quick actions and send button
  - Better spacing/typography/readability
  - Inline connection error banner
- If frontend is hosted separately, pass backend URL with query string:
  - `index.html?api=https://<your-backend-url>`

## Troubleshooting

### CORS Errors
If frontend can't reach backend:
1. Check API_CONFIG.apiUrl in frontend/index.html
2. Ensure backend is running on correct port
3. Check browser console for specific error

### "User not found"
- Backend returns user-123 by default
- Modify front-end to pass user_id if using different user

### Port Already in Use
```bash
# Find process on port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

## File Modifications from Original

### Changes from Node.js version:
1. **Backend**: Replaced Firebase Functions (Node.js) with FastAPI (Python)
2. **Frontend**: Updated API endpoints and configuration
3. **Database**: Mock data structure remains same
4. **Response Format**: Dialogflow-compatible JSON responses
5. **Webhooks**: FastAPI webhook implements Dialogflow fulfillment protocol

### Original Files (kept for reference):
- `banking_agent/functions/index.js` - Original Node.js code
- `banking_agent/agent.json` - Dialogflow agent config
- `banking_agent/public/index.html` - Original HTML (superseded)

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication (OAuth 2.0/JWT)
- [ ] Real banking API integration
- [ ] Logging and analytics
- [ ] Admin dashboard
- [ ] Mobile app support
- [ ] Multi-language support
- [ ] Advanced NLP with custom models
- [ ] Transaction encryption
- [ ] WebSocket for real-time updates

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review endpoint examples
3. Check FastAPI docs: http://localhost:8000/docs (when running)

## License

This project is provided as-is for demonstration purposes.

---

**Built with FastAPI** | Banking Demo Application | v1.0.0
