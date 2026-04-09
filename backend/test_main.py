"""
Unit Tests for Banking Chatbot API
Run with: pytest
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure backend dir is in path for imports
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert "Banking Chatbot API" in response.json()["service"]

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestChatEndpoint:
    """Test chat endpoint"""

    def test_balance_query(self):
        """Test balance query"""
        response = client.post(
            "/api/chat", json={"message": "Check my balance", "session_id": "test-123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "balance" in data["text"].lower() or "checking" in data["text"].lower()
        assert "suggestions" in data

    def test_transfer_query(self):
        """Test transfer query"""
        response = client.post(
            "/api/chat", json={"message": "Transfer money", "session_id": "test-123"}
        )
        assert response.status_code == 200
        data = response.json()
        # Transfer handler requires parsed parameters; without them it shows account selection message
        assert "account" in data["text"].lower() or "specify" in data["text"].lower()

    def test_transaction_history_query(self):
        """Test transaction history query"""
        response = client.post(
            "/api/chat",
            json={"message": "Show my transactions", "session_id": "test-123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "transaction" in data["text"].lower()

    def test_help_query(self):
        """Test help query"""
        response = client.post(
            "/api/chat", json={"message": "Help", "session_id": "test-123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "help" in data["text"].lower() or "can help" in data["text"].lower()

    def test_fallback_query(self):
        """Test fallback for unknown message"""
        response = client.post(
            "/api/chat", json={"message": "xyz123abc", "session_id": "test-123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert (
            "not sure" in data["text"].lower() or "understand" in data["text"].lower()
        )


class TestUserEndpoint:
    """Test user endpoint"""

    def test_get_user_info(self):
        """Test getting user information"""
        response = client.get("/api/user")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "John Demo" in data["name"]
        assert "accounts" in data
        assert "checking" in data["accounts"]
        assert "savings" in data["accounts"]

    def test_user_has_balances(self):
        """Test user has account balances"""
        response = client.get("/api/user")
        data = response.json()
        assert data["accounts"]["checking"]["balance"] > 0
        assert data["accounts"]["savings"]["balance"] > 0


class TestTransactionEndpoint:
    """Test transaction endpoint"""

    def test_get_checking_transactions(self):
        """Test getting checking account transactions"""
        response = client.get("/api/user/transactions?account=checking")
        assert response.status_code == 200
        data = response.json()
        assert data["account"] == "checking"
        assert "transactions" in data
        assert len(data["transactions"]) > 0

    def test_get_savings_transactions(self):
        """Test getting savings account transactions"""
        response = client.get("/api/user/transactions?account=savings")
        assert response.status_code == 200
        data = response.json()
        assert data["account"] == "savings"
        assert "transactions" in data

    def test_invalid_account_type(self):
        """Test invalid account type"""
        response = client.get("/api/user/transactions?account=invalid")
        assert response.status_code == 400


class TestWebhookEndpoint:
    """Test Dialogflow webhook endpoint"""

    def test_webhook_check_balance(self):
        """Test webhook with check balance intent"""
        response = client.post(
            "/webhook",
            json={
                "session": "projects/test/agent/sessions/test-123",
                "queryResult": {
                    "intent": {"displayName": "Check Balance"},
                    "parameters": {},
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "fulfillmentText" in data
        assert "fulfillmentMessages" in data

    def test_webhook_help_intent(self):
        """Test webhook with help intent"""
        response = client.post(
            "/webhook",
            json={
                "session": "projects/test/agent/sessions/test-123",
                "queryResult": {"intent": {"displayName": "Help"}, "parameters": {}},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "fulfillmentText" in data

    def test_webhook_fallback(self):
        """Test webhook with unknown intent"""
        response = client.post(
            "/webhook",
            json={
                "session": "projects/test/agent/sessions/test-123",
                "queryResult": {
                    "intent": {"displayName": "Unknown Intent"},
                    "parameters": {},
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "fulfillmentText" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
