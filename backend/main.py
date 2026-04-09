import re
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Banking Chatbot API",
    description="FastAPI backend for Demo Bank chatbot",
    version="1.0.0",
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Data Models ====================


class Transaction(BaseModel):
    date: str
    desc: str
    amount: float


class Account(BaseModel):
    balance: float
    accountNumber: str
    transactions: List[Transaction]


class User(BaseModel):
    name: str
    accounts: Dict[str, Account]


class WebhookRequest(BaseModel):
    session: str
    queryResult: Dict
    originalDetectIntentRequest: Optional[Dict] = None


class WebhookResponse(BaseModel):
    fulfillmentText: str
    fulfillmentMessages: List[Dict]
    outputContexts: List[Dict] = []


# ==================== Mock Database ====================

MOCK_DATABASE = {
    "user-123": {
        "name": "John Demo",
        "accounts": {
            "checking": {
                "balance": 2547.83,
                "accountNumber": "****4532",
                "transactions": [
                    {"date": "2026-04-08", "desc": "Grocery Store", "amount": -87.43},
                    {"date": "2026-04-07", "desc": "Salary Deposit", "amount": 3200.00},
                    {"date": "2026-04-06", "desc": "Electric Bill", "amount": -124.50},
                    {"date": "2026-04-05", "desc": "Coffee Shop", "amount": -5.60},
                    {
                        "date": "2026-04-04",
                        "desc": "Transfer from Savings",
                        "amount": 500.00,
                    },
                ],
            },
            "savings": {
                "balance": 12750.00,
                "accountNumber": "****7891",
                "transactions": [
                    {"date": "2026-04-01", "desc": "Interest Credit", "amount": 12.50},
                    {
                        "date": "2026-03-15",
                        "desc": "Transfer to Checking",
                        "amount": -500.00,
                    },
                    {"date": "2026-03-01", "desc": "Deposit", "amount": 1000.00},
                ],
            },
        },
    }
}

# Session storage for pending transfers
PENDING_TRANSFERS = {}

# ==================== Helper Functions ====================


def format_currency(amount: float) -> str:
    """Format amount as currency string"""
    return f"${amount:.2f}"


def get_user(user_id: str = "user-123") -> Optional[Dict[str, Any]]:
    """Get user from mock database"""
    return MOCK_DATABASE.get(user_id)


def extract_intent(result: Dict) -> str:
    """Extract intent name from query result"""
    return result.get("intent", {}).get("displayName", "Default Fallback Intent")


def extract_parameters(result: Dict) -> Dict:
    """Extract parameters from query result"""
    return result.get("parameters", {})


# ==================== Intent Handlers ====================


def welcome_handler(user: Dict) -> tuple[str, List[Dict]]:
    """Handle welcome intent"""
    text = (
        f"Welcome to Demo Bank! 🏦\n\n"
        f"Hello {user['name']}, I can help you with:\n"
        f"• Check account balances\n"
        f"• Transfer money between accounts\n"
        f"• View recent transactions\n\n"
        f"What would you like to do?"
    )
    suggestions = [
        {"title": "Check Balance"},
        {"title": "Transfer Money"},
        {"title": "Transactions"},
    ]
    return text, suggestions


def check_balance_handler(user: Dict, params: Dict) -> tuple[str, List[Dict]]:
    """Handle check balance intent"""
    account_type = params.get("account-type", "").lower()

    if account_type:
        account = user["accounts"].get(account_type)
        if account:
            text = (
                f"Your {account_type} account ({account['accountNumber']}) balance is:\n\n"
                f"💰 **${account['balance']:,.2f}**"
            )
            suggestions = [{"title": "Transfer Money"}, {"title": "View Transactions"}]
            return text, suggestions
        else:
            text = (
                f"I couldn't find your {account_type} account. You have:\n"
                f"• Checking: ${user['accounts']['checking']['balance']:,.2f}\n"
                f"• Savings: ${user['accounts']['savings']['balance']:,.2f}"
            )
            suggestions = [{"title": "Check Balance"}, {"title": "Transfer Money"}]
            return text, suggestions
    else:
        # Show all balances
        checking = user["accounts"]["checking"]
        savings = user["accounts"]["savings"]
        total = checking["balance"] + savings["balance"]
        text = (
            f"Here are your account balances:\n\n"
            f"🏦 **Checking** ({checking['accountNumber']}): ${checking['balance']:,.2f}\n"
            f"💎 **Savings** ({savings['accountNumber']}): ${savings['balance']:,.2f}\n\n"
            f"Total: ${total:,.2f}"
        )
        suggestions = [{"title": "Transfer Money"}, {"title": "Transaction History"}]
        return text, suggestions


def transfer_money_handler(
    user: Dict, params: Dict, session_id: str
) -> tuple[str, List[Dict]]:
    """Handle transfer money intent"""
    amount_obj = params.get("amount", {})
    from_account = params.get("from-account", "").lower()
    to_account = params.get("to-account", "").lower()

    # Extract numeric amount
    if isinstance(amount_obj, dict):
        transfer_amount = amount_obj.get("amount")
    else:
        transfer_amount = float(amount_obj) if amount_obj else 0

    # Validate accounts
    if from_account not in user["accounts"] or to_account not in user["accounts"]:
        text = (
            "I couldn't find one of those accounts for your transfer. You have:\n"
            "• Checking\n"
            "• Savings\n\n"
            "Please specify both accounts (for example: transfer $100 from checking to savings)."
        )
        suggestions = [{"title": "Transfer Money"}, {"title": "Check Balance"}]
        return text, suggestions

    if from_account == to_account:
        text = "You can't transfer money to the same account. Please choose different accounts."
        suggestions = [{"title": "Transfer Money"}, {"title": "Check Balance"}]
        return text, suggestions

    if not transfer_amount or transfer_amount <= 0:
        text = "Please specify a valid amount to transfer."
        suggestions = [{"title": "Transfer Money"}, {"title": "Check Balance"}]
        return text, suggestions

    # Check sufficient funds
    if user["accounts"][from_account]["balance"] < transfer_amount:
        text = (
            f"❌ Insufficient funds in your {from_account} account.\n"
            f"Available: ${user['accounts'][from_account]['balance']:,.2f}\n"
            f"Requested: ${transfer_amount:,.2f}"
        )
        suggestions = [{"title": "Check Balance"}, {"title": "Transfer Money"}]
        return text, suggestions

    # Store pending transfer
    PENDING_TRANSFERS[session_id] = {
        "amount": transfer_amount,
        "from": from_account,
        "to": to_account,
        "timestamp": datetime.now().isoformat(),
    }

    from_cap = from_account.capitalize()
    to_cap = to_account.capitalize()
    text = (
        f"Please confirm your transfer:\n\n"
        f"💸 **${transfer_amount:.2f}**\n"
        f"From: {from_cap}\n"
        f"To: {to_cap}\n\n"
        f"Do you want to proceed?"
    )
    suggestions = [{"title": "Yes, confirm"}, {"title": "No, cancel"}]
    return text, suggestions


def confirm_transfer_handler(user: Dict, session_id: str) -> tuple[str, List[Dict]]:
    """Handle transfer confirmation"""
    transfer = PENDING_TRANSFERS.get(session_id)

    if not transfer:
        text = (
            "I don't see any pending transfer. Would you like to start a new transfer?"
        )
        suggestions = [{"title": "Transfer Money"}, {"title": "Check Balance"}]
        return text, suggestions

    # Execute transfer
    amount = transfer["amount"]
    from_acc = transfer["from"]
    to_acc = transfer["to"]

    user["accounts"][from_acc]["balance"] -= amount
    user["accounts"][to_acc]["balance"] += amount

    # Add transaction records
    today = datetime.now().strftime("%Y-%m-%d")
    user["accounts"][from_acc]["transactions"].insert(
        0, {"date": today, "desc": f"Transfer to {to_acc}", "amount": -amount}
    )
    user["accounts"][to_acc]["transactions"].insert(
        0, {"date": today, "desc": f"Transfer from {from_acc}", "amount": amount}
    )

    # Clear pending
    del PENDING_TRANSFERS[session_id]

    text = (
        f"✅ **Transfer Successful!**\n\n"
        f"${amount:.2f} has been transferred from your {from_acc} to your {to_acc} account.\n\n"
        f"New Balances:\n"
        f"• {from_acc}: ${user['accounts'][from_acc]['balance']:.2f}\n"
        f"• {to_acc}: ${user['accounts'][to_acc]['balance']:.2f}"
    )
    suggestions = [{"title": "Check Balance"}, {"title": "Another Transfer"}]
    return text, suggestions


def transaction_history_handler(user: Dict, params: Dict) -> tuple[str, List[Dict]]:
    """Handle transaction history intent"""
    account_type = params.get("account-type", "checking").lower()
    account = user["accounts"].get(account_type)

    if not account:
        account = user["accounts"]["checking"]
        account_type = "checking"

    text = f"📊 **Recent {account_type.capitalize()} Transactions:**\n\n"

    for tx in account["transactions"][:5]:
        emoji = "💵" if tx["amount"] > 0 else "💸"
        amount_str = (
            f"+${tx['amount']:.2f}"
            if tx["amount"] > 0
            else f"-${abs(tx['amount']):.2f}"
        )
        text += f"{emoji} {tx['date']} - {tx['desc']}\n   {amount_str}\n\n"

    text += f"Current Balance: ${account['balance']:.2f}"

    suggestions = [
        (
            {"title": "Check Savings"}
            if account_type == "checking"
            else {"title": "Check Checking"}
        ),
        {"title": "Transfer Money"},
    ]
    return text, suggestions


def help_handler(user: Dict) -> tuple[str, List[Dict]]:
    """Handle help intent"""
    text = (
        "Here's what I can help you with:\n\n"
        "💰 **Check Balance** - Say 'What's my balance?' or 'Check my savings'\n"
        "💸 **Transfer Money** - Say 'Transfer $100 from checking to savings'\n"
        "📊 **Transaction History** - Say 'Show my recent transactions'\n"
        "❓ **Help** - Show this message\n\n"
        "What would you like to do?"
    )
    suggestions = [
        {"title": "Check Balance"},
        {"title": "Transfer Money"},
        {"title": "Transactions"},
    ]
    return text, suggestions


def fallback_handler(user: Dict) -> tuple[str, List[Dict]]:
    """Handle fallback intent"""
    text = (
        "I'm not sure I understand. Try saying:\n"
        "• 'Check my balance'\n"
        "• 'Transfer $100 to savings'\n"
        "• 'Show my transactions'\n"
        "• 'Help'"
    )
    suggestions = [
        {"title": "Help"},
        {"title": "Check Balance"},
        {"title": "Transfer Money"},
    ]
    return text, suggestions


def parse_transfer_message(message: str) -> Dict:
    """Extract transfer parameters from plain text chat message."""
    amount_match = re.search(r"\$?\s*(\d+(?:\.\d{1,2})?)", message)
    amount = float(amount_match.group(1)) if amount_match else None

    from_match = re.search(r"from\s+(checking|savings)", message)
    to_match = re.search(r"to\s+(checking|savings)", message)

    return {
        "amount": {"amount": amount} if amount is not None else {},
        "from-account": from_match.group(1) if from_match else "",
        "to-account": to_match.group(1) if to_match else "",
    }


def is_dialogflow_enabled() -> bool:
    """Check if Dialogflow detectIntent mode is enabled."""
    return os.getenv("DIALOGFLOW_ENABLED", "false").strip().lower() == "true"


def call_dialogflow_detect_intent(message: str, session_id: str) -> Dict[str, Any]:
    """
    Send user text to Dialogflow detectIntent and return normalized chat payload.
    Requires DIALOGFLOW_PROJECT_ID and valid Google credentials.
    """
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID", "").strip()
    language_code = os.getenv("DIALOGFLOW_LANGUAGE_CODE", "en").strip() or "en"

    if not project_id:
        raise HTTPException(
            status_code=500,
            detail="Dialogflow is enabled but DIALOGFLOW_PROJECT_ID is not configured.",
        )

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()

    try:
        from google.cloud import dialogflow_v2 as dialogflow
        from google.oauth2 import service_account
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="Dialogflow SDK is not installed. Install dependencies from requirements.txt.",
        ) from exc

    try:
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            sessions_client = dialogflow.SessionsClient(credentials=credentials)
        else:
            sessions_client = dialogflow.SessionsClient()

        session = sessions_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=message, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = sessions_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Dialogflow detectIntent failed: {str(exc)}",
        ) from exc

    result = response.query_result
    fulfillment_text = result.fulfillment_text or "I processed your request."
    suggestions: List[str] = []

    for message_obj in result.fulfillment_messages:
        if message_obj.quick_replies and message_obj.quick_replies.quick_replies:
            suggestions.extend(list(message_obj.quick_replies.quick_replies))

    return {
        "text": fulfillment_text,
        "suggestions": suggestions,
        "session_id": session_id,
        "intent": result.intent.display_name if result.intent else "",
    }


# ==================== API Endpoints ====================


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "Banking Chatbot API", "version": "1.0.0"}


@app.get("/ui")
async def ui():
    """Serve built-in chat UI from frontend/index.html"""
    ui_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    if not ui_path.exists():
        raise HTTPException(status_code=404, detail="Frontend UI not found")
    return FileResponse(ui_path)


@app.post("/webhook")
async def webhook(request: Request):
    """
    Main webhook endpoint for Dialogflow fulfillment
    Handles all intents and returns appropriate responses
    """
    try:
        body = await request.json()

        # Extract session and query result
        session_id = body.get("session", "demo-session").split("/")[-1]
        query_result = body.get("queryResult", {})
        intent_name = extract_intent(query_result)
        params = extract_parameters(query_result)

        # Get user (using static user for demo)
        user = get_user("user-123")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Route to appropriate handler
        suggestions: List[Dict[str, str]] = []

        if intent_name == "Default Welcome Intent":
            text, suggestions = welcome_handler(user)
        elif intent_name == "Check Balance":
            text, suggestions = check_balance_handler(user, params)
        elif intent_name == "Transfer Money":
            text, suggestions = transfer_money_handler(user, params, session_id)
        elif intent_name == "Confirm Transfer - yes":
            text, suggestions = confirm_transfer_handler(user, session_id)
        elif intent_name == "Transaction History":
            text, suggestions = transaction_history_handler(user, params)
        elif intent_name == "Help":
            text, suggestions = help_handler(user)
        else:
            text, suggestions = fallback_handler(user)

        # Format response for Dialogflow
        message_obj: Dict[str, Any] = {"text": {"text": [text]}}

        if suggestions:
            message_obj["suggestions"] = {"suggestions": suggestions}

        response = {
            "fulfillmentText": text,
            "fulfillmentMessages": [message_obj],
            "source": "banking-api",
        }

        return response

    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        error_response = {
            "fulfillmentText": "Sorry, I encountered an error. Please try again.",
            "fulfillmentMessages": [
                {"text": {"text": ["Sorry, I encountered an error. Please try again."]}}
            ],
            "source": "banking-api",
        }
        return error_response


@app.post("/api/chat")
async def chat(request: Request):
    """
    Direct chat endpoint (alternative to webhook)
    Can be used if not using Dialogflow
    """
    try:
        body = await request.json()
        raw_message = body.get("message", "")
        message = raw_message.lower()
        session_id = body.get("session_id", "demo-session")

        if is_dialogflow_enabled():
            return call_dialogflow_detect_intent(raw_message, session_id)

        user = get_user("user-123")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Simple intent detection based on keywords
        if "balance" in message or "how much" in message:
            text, suggestions = check_balance_handler(user, {})
        elif any(
            keyword in message
            for keyword in ("yes", "confirm", "proceed", "approve", "ok", "okay")
        ):
            text, suggestions = confirm_transfer_handler(user, session_id)
        elif any(keyword in message for keyword in ("cancel", "no", "stop")):
            if session_id in PENDING_TRANSFERS:
                del PENDING_TRANSFERS[session_id]
                text = "Transfer cancelled. No money was moved."
                suggestions = [{"title": "Check Balance"}, {"title": "Transfer Money"}]
            else:
                text = "There is no pending transfer to cancel."
                suggestions = [{"title": "Transfer Money"}, {"title": "Check Balance"}]
        elif "transfer" in message or "send" in message:
            transfer_params = parse_transfer_message(message)
            text, suggestions = transfer_money_handler(user, transfer_params, session_id)
        elif "transaction" in message or "history" in message or "spent" in message:
            text, suggestions = transaction_history_handler(user, {})
        elif "help" in message or "what can you do" in message:
            text, suggestions = help_handler(user)
        else:
            text, suggestions = fallback_handler(user)

        return {
            "text": text,
            "suggestions": [s.get("title", "") for s in suggestions],
            "session_id": session_id,
        }

    except Exception as e:
        print(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user")
async def get_user_info(user_id: str = "user-123"):
    """Get user information"""
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": user["name"],
        "accounts": {
            "checking": {
                "balance": user["accounts"]["checking"]["balance"],
                "accountNumber": user["accounts"]["checking"]["accountNumber"],
            },
            "savings": {
                "balance": user["accounts"]["savings"]["balance"],
                "accountNumber": user["accounts"]["savings"]["accountNumber"],
            },
        },
    }


@app.get("/api/user/transactions")
async def get_transactions(account: str = "checking", user_id: str = "user-123"):
    """Get transaction history for an account"""
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if account not in user["accounts"]:
        raise HTTPException(status_code=400, detail="Invalid account type")

    return {
        "account": account,
        "transactions": user["accounts"][account]["transactions"],
    }


@app.get("/health")
async def health_check():
    """Kubernetes/load balancer health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
