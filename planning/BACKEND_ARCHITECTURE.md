# Backend Architecture & API Specification

## Technology Stack
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Database**: SQLite (development), PostgreSQL (production)
- **Server**: Uvicorn
- **Project Manager**: uv (modern Python dependency management)

## Project Structure
```
backend/
├── pyproject.toml         # Dependencies and project config
├── src/
│   ├── main.py           # FastAPI application entry point
│   ├── api/              # API route modules
│   │   ├── trades.py     # Trade execution endpoints
│   │   ├── portfolio.py  # Portfolio management endpoints
│   │   ├── watchlist.py  # Watchlist management endpoints
│   │   └── chat.py       # AI chat endpoint
│   ├── db/               # Database related
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schema.py     # Database creation
│   │   ├── seed.py       # Seed data
│   │   └── init_db.py    # Initialization
│   ├── market_data/      # Market data providers
│   │   ├── base.py       # Abstract interface
│   │   ├── simulator.py  # GBM simulator
│   │   └── polygon.py    # Polygon.io client
│   └── llm/              # LLM integration
│       ├── cerebras_client.py  # Cerebras API client
│       ├── prompts.py          # Prompt templates
│       └── tools.py            # Trading tools
└── tests/                # Test suite
```

## Core API Endpoints

### Authentication (Future)
Currently single-user, no auth required.

### Portfolio Endpoints
```
GET /api/portfolio
- Returns: Cash balance, positions, total value, P&L
- Response: {
    "cash_balance": 10000.0,
    "total_value": 12500.0,
    "positions": [...],
    "unrealized_pnl": 2500.0
  }

GET /api/portfolio/positions
- Returns: Array of current positions
- Response: [{
    "ticker": "AAPL",
    "quantity": 10,
    "avg_cost": 150.00,
    "current_price": 185.42,
    "unrealized_pnl": 354.20,
    "pct_change": 23.6
  }]

GET /api/portfolio/pnl
- Returns: Historical P&L data for charting
- Response: [{
    "timestamp": "2026-04-02T14:00:00Z",
    "total_value": 12000.00
  }]
```

### Trade Endpoints
```
POST /api/trades/buy
- Executes market buy order
- Body: {"ticker": "AAPL", "quantity": 10}
- Response: {
    "order_id": "ord_123",
    "status": "filled",
    "ticker": "AAPL",
    "quantity": 10,
    "filled_price": 185.42,
    "timestamp": "2026-04-02T14:30:00Z"
  }

POST /api/trades/sell
- Executes market sell order
- Body: {"ticker": "AAPL", "quantity": 5}
- Response: Same as buy

GET /api/trades/history
- Returns: All trades for this session
- Response: [trade objects from above]
```

### Watchlist Endpoints
```
GET /api/watchlist
- Returns: Array of watched tickers
- Response: ["AAPL", "GOOGL", "MSFT", ...]

POST /api/watchlist
- Adds ticker to watchlist
- Body: {"ticker": "TSLA"}
- Response: {"watchlist": [...]}

DELETE /api/watchlist/{ticker}
- Removes ticker from watchlist
- Response: {"watchlist": [...]}
```

### Market Data Endpoints
```
GET /api/prices/{ticker}
- Returns: Latest price for ticker
- Response: {
    "ticker": "AAPL",
    "price": 185.42,
    "previous_price": 185.38,
    "change": 0.04,
    "change_pct": 0.02,
    "timestamp": "2026-04-02T14:30:00Z"
  }

GET /api/stream/prices
- Server-Sent Events endpoint
- Streams price updates at ~500ms intervals
- Response: stream of price objects
```

### Chat Endpoints
```
POST /api/chat
- Sends message to AI assistant
- Body: {"message": "What should I do with my AAPL position?"}
- Response: {
    "response": "Based on your holdings...",
    "trades": [
      {"action": "buy", "ticker": "MSFT", "quantity": 5}
    ],
    "confidence": 0.85
  }

GET /api/chat/history
- Returns: Chat message history
- Response: [{
    "role": "user|assistant",
    "content": "...",
    "timestamp": "..."
  }]
```

## Database Schema

### Users Table
```sql
CREATE TABLE users_profile (
  id TEXT PRIMARY KEY DEFAULT 'default',
  cash_balance REAL DEFAULT 10000.0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Positions Table
```sql
CREATE TABLE positions (
  id INTEGER PRIMARY KEY,
  user_id TEXT DEFAULT 'default',
  ticker TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  avg_cost REAL NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users_profile(id)
)
```

### Trades Table
```sql
CREATE TABLE trades (
  id INTEGER PRIMARY KEY,
  user_id TEXT DEFAULT 'default',
  ticker TEXT NOT NULL,
  action TEXT NOT NULL, -- 'buy' or 'sell'
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  total_value REAL NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users_profile(id)
)
```

### Watchlist Table
```sql
CREATE TABLE watchlist (
  id INTEGER PRIMARY KEY,
  user_id TEXT DEFAULT 'default',
  ticker TEXT NOT NULL,
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, ticker),
  FOREIGN KEY(user_id) REFERENCES users_profile(id)
)
```

### Chat History Table
```sql
CREATE TABLE chat_history (
  id INTEGER PRIMARY KEY,
  user_id TEXT DEFAULT 'default',
  role TEXT NOT NULL, -- 'user' or 'assistant'
  content TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users_profile(id)
)
```

## Error Handling

All endpoints should return appropriate HTTP status codes:
- 200: Success
- 400: Bad request (invalid parameters)
- 404: Not found (ticker not in watchlist, etc.)
- 500: Server error

Error response format:
```json
{
  "error": "Insufficient cash balance",
  "detail": "Trying to buy 1000 shares but only have $500"
}
```

## Testing Strategy

Target: 121+ passing unit tests
- Test utilities: pytest
- Mock data: Factory Boy
- Coverage: Aim for >80% code coverage

Test categories:
1. API endpoint tests (~30 tests)
2. Database model tests (~20 tests)
3. Market data provider tests (~15 tests)
4. Trade execution logic tests (~20 tests)
5. Portfolio calculation tests (~15 tests)
6. LLM integration tests (~15 tests)
7. E2E integration tests (~10 tests)

## Development Notes

- Start server with: `python -m uvicorn src.main:app --reload`
- API will be at `http://localhost:8000`
- Auto-reload enabled for development
- API docs at `http://localhost:8000/docs`
- Schema at `http://localhost:8000/openapi.json`

## Production Considerations

- Use PostgreSQL for production (not SQLite)
- Add authentication (JWT tokens)
- Implement rate limiting
- Add request logging
- Monitor API usage and errors
- Use environment variables for configuration
- Run migrations on deployment
- Scale Uvicorn with multiple workers
