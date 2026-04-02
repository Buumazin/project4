# Market Data Discovery & API Research

## Current Status
Market data simulator has been completed. See `planning/MARKET_DATA_SUMMARY.md` for details.

## Polygon.io (Massive) API Investigation

### Account & Pricing (As of 2026)
- **Free Tier**: 5 API calls/minute
  - Real-time stock quotes available
  - 15-minute delayed data
  - Basic market data
  - Suitable for demo/learning

- **Starter Tier**: Higher rate limits
  - Professional market data
  - Current market conditions
  - Historical data access

### API Endpoints (for implementation)
```
GET /v1/quote/{ticker}
- Returns: latest price, bid/ask, previous close, etc.
- Used for: Real-time price updates and watchlist
- Rate: 5 calls/min (free tier)

GET /v1/universal-snapshot/metadata
- Returns: All available tickers and metadata
- Used for: Watchlist population

GET /v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}
- Returns: Historical OHLCV data
- Used for: Price charts and analysis
- Useful for building value from history
```

### Alternative Providers
- **IEX Cloud**: $349+/month, excellent data quality
- **Alpha Vantage**: Generous free tier, CSV format
- **Yahoo Finance**: Free, unofficial API
- **Finnhub**: Free tier with 60 API calls/min

### Recommendation for Finally
- **Development**: Use built-in simulator (no API key needed)
- **Production**: Add Polygon.io as optional premium feature
- **Users**: Can work without real market data via simulator
- **Implementation**: Abstracted interface allows easy switching

## Environment Variables for Market Data
```bash
# Optional: Leave empty or omit for simulator
MASSIVE_API_KEY=

# If provided:
MASSIVE_API_KEY=pk_... (Polygon.io key)

# Backend automatically switches:
- Empty/None → Use simulator
- Provided → Use Polygon.io API
```

## Market Data in Application

### SSE Streaming Endpoint
```
GET /api/stream/prices
- Sends: Price updates for all tickers
- Interval: ~500ms (matches simulator update rate)
- Format: Server-Sent Events (plain text)
- Client: Uses native EventSource API
```

### Data Points Streamed
```json
{
  "ticker": "AAPL",
  "price": 185.42,
  "previous_price": 185.38,
  "timestamp": "2026-04-02T14:30:00Z",
  "change_direction": "up"
}
```

### Simulator Pricing Model
GBM (Geometric Brownian Motion) with:
- Realistic seed prices  
- Daily volatility 1-3%
- Sector correlations
- Occasional "events" (2-5% swings)
- Continuous background task updating cache

## Integration Points in Application

1. **Frontend**:
   - Connect to `/api/stream/prices`
   - Display live updates in PriceGrid
   - Show price highlights (green/red flashes)
   - Build sparkline charts progressively

2. **Backend**:
   - Market data service (simulator OR Polygon.io)
   - Price cache (in-memory)
   - SSE endpoint marshals cache to clients
   - No direct connection from frontend to market data

3. **Database**:
   - Can store historical prices (optional)
   - Trade execution prices recorded
   - Historical analysis available

## Implementation Checklist for Day 2-3

- ✅ Understand market data architecture
- ✅ Confirm simulator is sufficient for demo
- ✅ Document Polygon.io as optional upgrade
- ✅ Note environment variable setup
- ✅ Plan SSE endpoint in backend
- ✅ Design price cache structure

## For Agent Teams (Day 4)

**Backend Engineer**:
- Implement both market data providers
- Abstract interface in `backend/src/market_data/`
- SSE endpoint at `/api/stream/prices`

**Frontend Engineer**:
- Use `EventSource` API to connect to SSE
- Update components on price changes
- Show connection status indicator

**DevOps Engineer**:
- Document MASSIVE_API_KEY in .env.example
- Ensure price cache survives container restarts (in-memory is ok for demo)
