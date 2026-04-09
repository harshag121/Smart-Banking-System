"""
Pytest configuration and fixtures for Banking Chatbot API
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def sample_message():
    """Sample chat message"""
    return {"message": "Check my balance", "session_id": "test-session-123"}


@pytest.fixture
def sample_webhook_request():
    """Sample Dialogflow webhook request"""
    return {
        "session": "projects/test-project/agent/sessions/test-session",
        "queryResult": {"intent": {"displayName": "Check Balance"}, "parameters": {"account-type": "checking"}},
    }
