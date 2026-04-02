import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    from db.init_db import initialize_database
    initialize_database()
    yield


def test_chat_trade_execute_and_history():
    # Send a chat command to buy AAPL via the agent route
    response = client.post("/api/chat/", json={"message": "mua AAPL 1"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "trade_executed" in data
    assert data["trade_executed"]["trade"]["action"] == "buy"
    assert data["trade_executed"]["trade"]["ticker"] == "AAPL"

    # Validate trade history includes this trade
    history_resp = client.get("/api/trades/history?limit=10")
    assert history_resp.status_code == 200
    trades = history_resp.json().get("trades", [])
    assert any(t["action"] == "buy" and t["ticker"] == "AAPL" for t in trades)

    # Validate chat history records entry
    chat_history_resp = client.get("/api/chat/history")
    assert chat_history_resp.status_code == 200
    chat_messages = chat_history_resp.json().get("history", [])
    assert any(m["role"] == "user" and "mua AAPL" in m["content"] for m in chat_messages)
    assert any(m["role"] == "assistant" for m in chat_messages)
