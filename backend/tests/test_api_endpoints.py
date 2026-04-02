import pytest
from fastapi.testclient import TestClient

# ensure tests run with backend src path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Ensure DB is initialized before each test
    from db.init_db import initialize_database
    initialize_database()
    yield


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "market_data" in data


def test_portfolio_endpoint():
    response = client.get("/api/portfolio/")
    assert response.status_code == 200
    data = response.json()
    assert "cash_balance" in data
    assert "positions" in data


def test_price_endpoint_aapl():
    response = client.get("/api/prices/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert "price" in data


def test_watchlist_get_and_add_remove():
    # Read watchlist
    response = client.get("/api/watchlist/")
    assert response.status_code == 200
    initial_watchlist = response.json()

    new_ticker = "TEST"
    # Add ticker
    response = client.post("/api/watchlist/", json={"ticker": new_ticker})
    assert response.status_code == 200
    assert response.json()["success"] is True

    response = client.delete(f"/api/watchlist/{new_ticker}")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_trade_buy_and_sell():
    # buy order
    response = client.post("/api/trades/buy", json={"ticker": "AAPL", "quantity": 1, "price": 100.0})
    assert response.status_code == 200
    assert response.json()["success"] is True

    # sell order
    response = client.post("/api/trades/sell", json={"ticker": "AAPL", "quantity": 1, "price": 100.0})
    assert response.status_code == 200
    assert response.json()["success"] is True

    # insufficient funds/supply check not exactly
