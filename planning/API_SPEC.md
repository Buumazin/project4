# API Specification for FinAlly Trading Platform

## Base URL
- Local development: `http://localhost:8000`

## Endpoints

### Health
- `GET /api/health`
- Response: 200
  ```json
  {
    "status": "healthy",
    "message": "FinAlly trading platform is running",
    "market_data": "active" | "inactive"
  }
  ```

### Portfolio
- `GET /api/portfolio/`
- `GET /api/portfolio/positions`
- `GET /api/portfolio/pnl`

Portfolio response:
```json
{
  "cash_balance": 10000.0,
  "total_value": 12600.0,
  "positions": [
    {
      "ticker": "AAPL",
      "quantity": 10,
      "avg_cost": 180.0,
      "current_price": 188.65,
      "market_value": 1886.5,
      "unrealized_pnl": 86.5,
      "unrealized_pnl_pct": 4.80
    }
  ],
  "total_positions_value": 2600.0
}
```

### Trades
- `POST /api/trades/buy`
  - Body: `{ "ticker": "AAPL", "quantity": 1, "price": 100.0 }`
  - Response: `{ "success": true, "trade": {...}, "remaining_cash": 9900 }`

- `POST /api/trades/sell`
  - Body: `{ "ticker": "AAPL", "quantity": 1, "price": 100.0 }`

- `GET /api/trades/history`
  - Query: `limit` and `offset`
  - Response: `{ "trades": [...], "total": 10, "limit": 50, "offset": 0 }`

### Watchlist
- `GET /api/watchlist/`
- `POST /api/watchlist/` body: `{ "ticker": "TSLA" }`
- `DELETE /api/watchlist/{ticker}`

### Prices
- `GET /api/prices/{ticker}`
  - Response: `{ "ticker": "AAPL", "price": 182.98, "timestamp": ... }`

- `GET /api/prices/` returns current prices for all tickers.

- `GET /api/stream/prices`
  - SSE stream with events containing JSON `{ "prices": {...}, "timestamp": ... }`

### Chat
- `POST /api/chat` body: `{ "message": "What should I do?" }`
- `GET /api/chat/history`

Response:
```json
{
  "response": "Simulated assistant response...",
  "timestamp": "2026-04-02T...Z",
  "status": "ok"
}
```

## Error Handling
- `400` for invalid inputs
- `404` for not found (ticker not listed, position not in watchlist)
- `503` for unavailable market simulation
- `500` for internal errors
