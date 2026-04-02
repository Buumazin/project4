# Day 4 Agent Teams Orchestration Guide

## Overview

This is the main build phase where Agent Teams will construct the entire FinAlly trading workstation. The team lead agent coordinates 6 specialist agents to build in parallel where possible, with proper sequencing for dependencies.

## Start Here

When you're ready to begin Day 4 build:

1. **Read this entire document** - Understand the build strategy
2. **Read CLAUDE_EXTENDED.md** - Understand agent roles
3. **Read planning/PLAN.md** - Understand full requirements
4. **Enable Agent Teams in Claude Code** - Use experimental feature flag
5. **Follow the Team Structure below** - Execute in recommended sequence

---

## Team Structure & Agent Definitions

### Team Lead (You / Lead Opus Agent)
**Role**: Orchestrates all agents, makes decisions, resolves conflicts

**Prompt**:
```
You are the team lead orchestrating the build of FinAlly, an AI-powered trading platform.

Your team consists of 6 specialist agents:
- Backend Engineer: Builds FastAPI backend with all APIs
- Frontend Engineer: Builds React/Next.js UI
- Database Engineer: Creates database schema and migrations
- DevOps Engineer: Sets up Docker containerization
- LLM Engineer: Integrates Cerebras for chat
- Integration Tester: Validates everything works end-to-end

Your responsibilities:
1. Assign tasks in the recommended sequence (see below)
2. Ensure agents communicate and handle dependencies
3. Resolve any blockers or conflicts
4. Validate deliverables are complete before moving to next phase
5. Request status updates via /agent-status command

Build strategy:
- Phase 1 (2 hours): Database + Backend foundation
- Phase 2 (2 hours): API implementation + tests
- Phase 3 (2 hours): Frontend development
- Phase 4 (2 hours): Integration + DevOps + LLM
- Phase 5 (1 hour): Final testing and validation

Success = All tests passing, Docker running, feature-complete application
```

---

## Build Phases & Sequence

### PHASE 1: Foundation & Setup (Hours 1-2)

#### Task 1.1: Database Engineer Setup
**Agent**: Database Engineer
**Time**: 30 minutes

**Instructions**:
```
Create database schema and models for FinAlly.

Tasks:
1. Create backend/src/db/
   - models.py (SQLAlchemy models)
   - schema.py (database initialization)
   - seed.py (test data)

2. Define these models in SQLAlchemy:
   - UserProfile (id, cash_balance, created_at, updated_at)
   - Position (ticker, quantity, avg_cost, user_id, timestamps)
   - Trade (ticker, action, quantity, price, total_value, user_id, timestamp)
   - WatchlistItem (ticker, user_id, added_at)
   - ChatMessage (role, content, user_id, timestamp)

3. Include:
   - Primary keys and foreign keys
   - Proper indexes on frequently queried columns
   - Default user_id = "default" (single user for demo)
   - Timestamps with defaults

4. Create seed.py to populate:
   - Default user with $10,000 cash
   - 3-5 default positions for testing
   - 10 default watchlist tickers

5. Document in planning/DB_SCHEMA.md what was created

Success criteria:
- All models compile without errors
- Tables can be created fresh
- Seed data loads successfully
- Database can be queried via SQLAlchemy
```

#### Task 1.2: Backend Engineer Setup
**Agent**: Backend Engineer
**Time**: 30 minutes (parallel with Database Engineer)

**Instructions**:
```
Set up FastAPI project and integrate database.

Tasks:
1. Create backend/pyproject.toml with dependencies:
   - fastapi, uvicorn
   - sqlalchemy, alembic
   - pytest, pytest-asyncio
   - python-dotenv
   - requests
   - litellm (for LLM integration)

2. Create backend/src/main.py with:
   - FastAPI app initialization
   - CORS configuration
   - Database connection setup
   - Health check endpoint: GET /api/health
   - Documentation endpoint: GET /docs

3. Create backend/src/db/init.py:
   - Database session management
   - Lazy database initialization on first request
   - Migration runner

4. Test:
   - Start server: python -m uvicorn src.main:app --reload
   - Access: http://localhost:8000/docs
   - Verify: GET /api/health returns 200

5. Create planning/BACKEND_INIT.md documenting setup

Success criteria:
- FastAPI server starts and runs on port 8000
- /api/health endpoint responds
- Swagger docs accessible
- Database session management working
```

#### Task 1.3: DevOps Engineer Foundation
**Agent**: DevOps Engineer
**Time**: 30 minutes (parallel, will complete in Phase 4)

**Instructions**:
```
Start Dockerfile and environment setup.

Tasks:
1. Create Dockerfile (multi-stage):
   - Stage 1: Node 18+ to build Next.js frontend
   - Stage 2: Python 3.11+ for FastAPI backend
   - Final: Both frontend (static) and backend in single image

2. Create .dockerignore:
   - node_modules, venv, __pycache__
   - .git, .env (local only)
   - build artifacts

3. Create .env.example:
   - OPENROUTER_API_KEY=
   - MASSIVE_API_KEY=
   - DATABASE_URL=sqlite:///db/finally.db
   - LLM_MOCK=false

4. Create docker-compose.yml for development:
   - One service: finally-app
   - Port: 8000
   - Volume: ./db for persistence
   - Environment: read from .env

5. Create scripts/start_windows.ps1 and start_mac.sh

Success criteria:
- Dockerfile exists (don't build yet, will do after all components ready)
- Environment template complete
- Scripts are executable
```

---

### PHASE 2: API Implementation (Hours 2-4)

#### Task 2.1: Backend API Implementation
**Agent**: Backend Engineer
**Time**: 2 hours

**Prerequisites**: Database schema complete

**Instructions**:
```
Implement all API endpoints for FinAlly.

Files to create:
- backend/src/api/portfolio.py
- backend/src/api/trades.py
- backend/src/api/watchlist.py
- backend/src/api/prices.py (market data)

Endpoints to implement (details in planning/BACKEND_ARCHITECTURE.md):

Portfolio:
- GET /api/portfolio - Get cash, positions, total value, P&L
- GET /api/portfolio/positions - Get list of positions
- GET /api/portfolio/pnl - Get P&L history for charting

Trades:
- POST /api/trades/buy - Execute buy order
- POST /api/trades/sell - Execute sell order
- GET /api/trades/history - Get trade history

Watchlist:
- GET /api/watchlist - Get watched tickers
- POST /api/watchlist - Add ticker
- DELETE /api/watchlist/{ticker} - Remove ticker

Prices:
- GET /api/prices/{ticker} - Get current price
- GET /api/stream/prices - SSE stream for all prices (complex, see market data task)

Basics for each endpoint:
1. Proper request/response validation using Pydantic
2. Error handling with appropriate HTTP status codes
3. Database transactions where needed
4. Logging of operations
5. Docstrings

Market Data Integration (simplified for Phase 2):
1. Create backend/src/market_data/base.py - Abstract interface
2. Create backend/src/market_data/simulator.py - GBM price simulator
   - Generate realistic seed prices
   - Simulate price movements using GBM
   - Update price cache every ~500ms
   - Handle watchlist tickers

3. Integrate into main.py:
   - Start market data background task on startup
   - Seed default prices
   - Make prices available to /api/prices endpoints

4. Simple SSE endpoint:
   - GET /api/stream/prices
   - Sends price updates at ~500ms intervals to connected clients
   - Format: Server-Sent Events (plain text event stream)

Success criteria:
- All endpoints return correct response structure
- Trade execution updates portfolio correctly
- Prices update in real-time
- Market data simulator generates plausible prices
- All endpoints tested and working
```

#### Task 2.2: Backend Unit Tests
**Agent**: Backend Engineer
**Time**: 1 hour (interleaved with implementation)

**Instructions**:
```
Write unit tests for all backend functionality.

Target: 121+ passing tests

Test structure (backend/tests/):
- test_api_portfolio.py - Portfolio calculations
- test_api_trades.py - Buy/sell logic
- test_api_watchlist.py - Watchlist operations
- test_api_prices.py - Price data endpoints
- test_models.py - Database model tests
- test_market_data.py - Simulator tests
- test_integration_e2e.py - End-to-end flows

Each test module should cover:
- Happy path (valid inputs)
- Error cases (invalid inputs, edge cases)
- Database state changes
- Calculation accuracy

Run tests:
- cd backend
- pytest tests/ -v
- pytest tests/ --cov=src (coverage report)

Success criteria:
- 121+ tests passing
- 80%+ code coverage
- No flaky tests
- All tests run in < 30 seconds
```

#### Task 2.3: API Specification Document
**Agent**: Backend Engineer
**Time**: 30 minutes

**Instructions**:
```
Document all API endpoints for Frontend Engineer.

Create planning/API_SPEC.md with:
1. All endpoint URLs
2. Request/response formats (JSON schema)
3. Status codes
4. Example cURLs for testing
5. Authentication (none for demo)
6. Rate limits (none for demo)
7. Error responses

Format:
```
### GET /api/portfolio
Returns portfolio summary.

Request: No body
Response:
{
  "cash_balance": 10000.0,
  "total_value": 12500.0,
  "unrealized_pnl": 2500.0,
  "positions": [...]
}
Status: 200
```

Include examples for all endpoints listed in planning/BACKEND_ARCHITECTURE.md

Success criteria:
- All endpoints documented
- Clear request/response examples
- Frontend Engineer can implement without asking questions
```

---

### PHASE 3: Frontend Development (Hours 4-6)

#### Task 3.1: Frontend Project Setup
**Agent**: Frontend Engineer
**Time**: 30 minutes

**Prerequisites**: API Specification available

**Instructions**:
```
Initialize Next.js project with static export.

Tasks:
1. Create frontend/ directory with:
   - package.json (Next.js 14+, TypeScript, Tailwind CSS, Redux)
   - next.config.js with: output: 'export' (static export)
   - tsconfig.json
   - tailwind.config.ts
   - postcss.config.js

2. Dependencies:
   - next, react, react-dom
   - typescript, tailwindcss, postcss
   - @reduxjs/toolkit, react-redux
   - recharts (for charts)
   - axios or fetch for API
   - types for everything

3. Create folder structure:
   - src/pages/
   - src/components/
   - src/hooks/
   - src/lib/
   - src/styles/
   - src/types/
   - src/store/ (Redux)
   - __tests__/

4. Create src/pages/_app.tsx:
   - Redux provider setup
   - Global styles
   - Layout wrapper

5. Create src/pages/index.tsx:
   - Main dashboard layout
   - Import all components (will create next)

6. Test:
   - npm run dev
   - http://localhost:3000
   - Should show blank dashboard

Success criteria:
- npm install completes without errors
- Next.js dev server runs
- TypeScript compilation clean
- Tailwind CSS working
```

#### Task 3.2: Frontend Components
**Agent**: Frontend Engineer
**Time**: 2 hours

**Prerequisites**: Backend API running, API Specification complete

**Instructions**:
```
Build React components for trading dashboard.

Create components in src/components/:

1. Header.tsx
   - App title/logo
   - Connection status dot (green/yellow/red)
   - Current time
   - Current portfolio value
   - Cash balance display

2. PriceGrid.tsx
   - Grid of watched tickers
   - Ticker symbol, price, change $, change %
   - Small sparkline chart (from Recharts)
   - Green/red background flash on price movement
   - Click to view detailed chart

3. DetailChart.tsx
   - Large price chart (line chart from Recharts)
   - Time range selectors (1D, 5D, 1M, 3M, 1Y)
   - BUY/SELL buttons
   - Buy/Sell modal underneath

4. Heatmap.tsx
   - Treemap of positions (use Recharts Treemap)
   - Size = position value
   - Color = P&L color (green/red gradient)
   - Hover shows details

5. PositionsTable.tsx
   - Table of current holdings
   - Columns: Ticker, Quantity, Avg Cost, Price, Value, P&L($), P&L(%)
   - Sortable by any column
   - Sell buttons for each position

6. PnlChart.tsx
   - Line chart of total portfolio value over time
   - X-axis: time, Y-axis: portfolio value
   - Update in real-time as prices change

7. Chat.tsx
   - Chat message area (scrollable)
   - Input field with send button
   - Display user messages (blue, right)
   - Display assistant messages (gray, left)
   - Show loading spinner while AI responds
   - Display suggested trades with Execute buttons

8. TradeModal.tsx
   - Modal for buying/selling shares
   - Ticker display
   - Quantity input
   - Current price display
   - Total cost calculation
   - Confirmation button
   - Success/error messages

9. ConnectionStatus.tsx
   - Small indicator showing SSE connection state
   - Green = connected (prices updating)
   - Yellow = reconnecting
   - Red = disconnected
   - Last update timestamp

Connect to backend:
- Use axios/fetch to call /api/* endpoints
- Use Redux for global state (prices, portfolio, trades)
- Use hooks for data fetching (usePortfolio, useMarketData, etc.)
- Convert backend dates to local time
- Format numbers (currency, percentages)

Styling:
- Use Tailwind CSS
- Color scheme from planning/FRONTEND_REQUIREMENTS.md
- Dark backgrounds: #0d1117, #1a1a2e
- Primary blue: #209dd7
- Accent yellow: #ecad0a
- Text: #c9d1d9
- Responsive design

Testing:
- Create __tests__/components/ with Jest tests
- Test component rendering
- Test data fetching
- Test user interactions

Success criteria:
- All components render without errors
- Data flows from backend to components
- Responsive layout works
- Professional dark theme applied
- No TypeScript errors
```

#### Task 3.3: Real-time Data Integration
**Agent**: Frontend Engineer  
**Time**: 1 hour

**Prerequisites**: Backend SSE endpoint working

**Instructions**:
```
Implement SSE for real-time price updates.

Create hooks/useMarketData.ts:
```typescript
import { useEffect, useState } from 'react';

export function useMarketData() {
  const [prices, setPrices] = useState({});
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource('/api/stream/prices');
    
    eventSource.onopen = () => setConnected(true);
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPrices(prev => ({
        ...prev,
        [data.ticker]: data
      }));
    };
    eventSource.onerror = () => setConnected(false);
    
    return () => eventSource.close();
  }, []);

  return { prices, connected };
}
```

Connect in components:
- PriceGrid uses useMarketData for live prices
- Price flash animation on change (500ms fade)
- Portfolio components recalculate on price updates
- Connection status reflects EventSource state

Success criteria:
- SSE connection established automatically
- Prices update every ~500ms
- Flash animation visible
- Connection status indicator changes
- Reconnection works if connection drops
```

---

### PHASE 4: Integration & Final Setup (Hours 6-8)

#### Task 4.1: LLM Integration
**Agent**: LLM Engineer  
**Time**: 1 hour

**Prerequisites**: Backend API running

**Instructions**:
```
Integrate Cerebras LLM for chat functionality.

Create backend/src/llm/:
- cerebras_client.py - LiteLLM wrapper
- prompts.py - Prompt templates
- tools.py - Trading action tools

cerebras_client.py:
- Connect to OpenRouter API
- Use Cerebras model for speed
- Handle streaming responses
- Manage token usage

prompts.py:
```python
PORTFOLIO_ANALYSIS_PROMPT = """
You are a financial advisor. Analyze this portfolio:
{portfolio_json}

Provide:
1. Current holdings analysis
2. Risk assessment
3. Recommended trades (if any)
4. Reasoning for recommendations

Format response as JSON with: analysis, trades[], confidence
"""
```

tools.py:
- Execute buy/sell commands
- Format trading recommendations
- Parse LLM structured outputs

Create backend/src/api/chat.py:
- POST /api/chat - Send message, get response
  - Queries portfolio
  - Calls Cerebras with context
  - Returns analysis + suggested trades
- GET /api/chat/history - Chat message history

Requirements:
- OPENROUTER_API_KEY environment variable required
- Handle API errors gracefully
- Log all requests/responses
- Streaming optional (can return full response)

Success criteria:
- Chat endpoint responsive
- Responds to queries in <5 seconds
- Structured trading recommendations
- Error handling for API failures
```

#### Task 4.2: Frontend-Backend Integration
**Agent**: Frontend Engineer
**Time**: 1 hour

**Prerequisites**: All backend endpoints and LLM working

**Instructions**:
```
Connect frontend to ACTUAL backend.

Tasks:
1. Update API client (lib/api.ts):
   - Point all endpoints to localhost:8000/api/*
   - Handle authentication (will be none for demo)
   - Error handling
   - Retry logic

2. Update Redux store (store/):
   - Actions for API calls
   - State for portfolio, prices, trades
   - Async thunks for API requests
   - Loading states

3. Update all components:
   - Use Redux for global state
   - Call API on component mount
   - Update state on API responses
   - Show loading states

4. Test flows:
   - Load portfolio ✓
   - Update prices in real-time via SSE ✓
   - Buy/sell orders ✓
   - Chat interactions ✓
   - Watchlist updates ✓

5. Performance:
   - Browser DevTools Network tab
   - Monitor API response times
   - Optimize re-renders

Success criteria:
- All components fetch real data
- No "undefined" values in UI
- Portfolio calculations correct
- Trades execute properly
- Chat works end-to-end
```

#### Task 4.3: Docker Build & DevOps Completion
**Agent**: DevOps Engineer
**Time**: 1 hour

**Prerequisites**: Frontend ready to export, all APIs working

**Instructions**:
```
Complete Docker containerization.

Tasks:
1. Frontend build:
   - npm run build (Next.js static export)
   - Output in frontend/out/
   - Verify all files generated

2. Backend Dockerfile completion:
   - Copy frontend/out/* to backend/static/
   - FastAPI serves static files: app.mount("/", StaticFiles(...))
   - Or use nginx as reverse proxy (simpler for demo)

3. Build Docker image:
   docker build -t finally:latest .

4. Test Docker locally:
   docker run -p 8000:8000 -v $(pwd)/db:/app/db finally:latest
   - Open http://localhost:8000
   - Verify everything works
   - Check both frontend and backend

5. Environment setup:
   - Copy .env.example to .env
   - Set OPENROUTER_API_KEY
   - (Optional) Set MASSIVE_API_KEY for real market data

6. Startup scripts:
   - start_windows.ps1 - Docker run script for Windows
   - start_mac.sh - Docker run script for Mac/Linux
   - Include volume mounting for persistence

Success criteria:
- Docker builds without errors
- Single container runs on port 8000
- Frontend loads at root /
- Backend APIs at /api/*
- Database persists across restarts
- All features work identically to development
```

#### Task 4.4: End-to-End Testing
**Agent**: Integration Tester
**Time**: 1 hour

**Prerequisites**: All components complete

**Instructions**:
```
Validate entire system works end-to-end.

Test suite (test/e2e_tests.py using Playwright):

1. Application startup
   - Server runs on port 8000
   - Frontend loads without errors
   - Health check passes: GET /api/health → 200

2. Portfolio operations
   - Load portfolio: /api/portfolio → valid structure
   - Positions table shows correctly
   - Cash balance displays
   - P&L calculations accurate

3. Price streaming
   - SSE connection established
   - Prices update every ~500ms
   - Sparklines build progressively
   - Price flashes visible
   - Connection status accurate

4. Trading
   - Execute buy order → /api/trades/buy
   - Position added to portfolio
   - Cash balance updated
   - P&L recalculated
   - Trade appears in history

5. Watchlist
   - Add ticker to watchlist
   - Remove ticker from watchlist
   - Watchlist persists on refresh
   - New tickers appear in price grid

6. Chat interaction
   - Send message to /api/chat
   - Response returns in <5 sec
   - Suggested trades display
   - Can click Execute to trade
   - Chat history loads on refresh

7. Database
   - Data persists across container restart
   - No data loss on shutdown
   - Can reset database cleanly
   - Seed data loads

8. Performance
   - Page loads in <2 sec
   - API responses <500ms
   - No UI freezing
   - Smooth animations

9. Error handling
   - Network error (fake disconnect) → Shows status
   - Invalid trade (negative quantity) → Error message
   - API error → Shows user-friendly message
   - Recovers gracefully

Run tests:
cd test
pytest e2e_tests.py -v

Report:
- List all tests: PASS/FAIL
- If any fail, file GitHub issue with:
  - Steps to reproduce
  - Expected vs actual result
  - Suggest fix

Success criteria:
- All E2E tests passing
- No critical bugs found
- Application ready for deployment
- Performance acceptable
```

---

### PHASE 5: Final Validation & Documentation (Hour 8)

#### Task 5.1: Overall Status Check
**Agent**: All agents
**Time**: 30 minutes

**Instructions**:
```
Use /test-check and /agent-status commands to verify everything.

From team lead:
1. Run /test-check
   - Should show 121+ unit tests PASSING
   - No failures

2. Run /agent-status
   - All agents report COMPLETE
   - No outstanding blockers
   - All deliverables approved

3. Docker test:
   - Build container: docker build -t finally:latest .
   - Run: docker run -p 8000:8000 finally:latest
   - Access: http://localhost:8000
   - All features functional

4. Git status:
   - All changes committed
   - Main branch clean
   - No merge conflicts

Success = Green checkmarks everywhere!
```

#### Task 5.2: Documentation & Handoff
**Agent**: Team Lead
**Time**: 30 minutes

**Instructions**:
```
Create final documentation for deployment/hand-off.

Create planning/DAY4_COMPLETION.md:
1. What was built (summary)
2. Tests passing (121+)
3. Known limitations (if any)
4. Deployment instructions
5. Next steps for Day 5
6. Contact points for questions

Update README.md:
- Quick start instructions
- How to run locally
- How to run with Docker
- Features implemented
- Architecture overview

Success criteria:
- Someone unfamiliar with project can:
  - Clone repo
  - Follow README
  - Have working app in 5 minutes
```

---

## Approval & Communication Pattern

### How Agents Get Approval

For routine operations (file creation, tests, commits):
```
User approves once per type:
"Approved: File creation"
"Approved: Test execution"
"Approved: npm install"
```

Then agent proceeds without asking for each individual file/test.

For unusual operations:
- Ask before doing
- Explain why needed
- Suggest approach
- Wait for approval

### Status Check Cadence

- Every 1 hour: `/agent-status` to sync
- After each phase: Team Lead reviews deliverables
- If blocked: Immediately escalate
- Successful handoffs: Document clearly

### Git Workflow

Agents commit frequently:
```
git commit -m "Backend: Implement portfolio endpoints"
git commit -m "Frontend: Build PriceGrid component"
git commit -m "Tests: Add 121 unit tests - all passing"
```

Main branch must always be working.

---

## Success Criteria Summary

### After Day 4 Completes: DONE! 🎉

✅ **Backend**:
- FastAPI running on port 8000
- All endpoints implemented per spec
- 121+ unit tests passing
- Database working
- Market data streaming
- LLM chat functional

✅ **Frontend**:
- Next.js builds to static export
- 9 major components built
- Real-time SSE integration
- Professional dark theme
- Responsive design
- No TypeScript/console errors

✅ **Infrastructure**:
- Docker build succeeds
- Single container on port 8000
- Both frontend + backend served
- Environment variables configurable
- Database persistence working

✅ **Testing**:
- All unit tests passing
- E2E tests passing
- No critical bugs
- Performance acceptable

✅ **Documentation**:
- All planning files updated
- API Specification complete
- Team Guidelines documented
- README for new users

---

## Quick Reference: Key Commands

```bash
# Backend
cd backend && pytest tests/ -v          # Run all tests
python -m uvicorn src.main:app --reload  # Start dev server

# Frontend
cd frontend && npm run dev               # Dev server
npm run build                            # Static export
npm run test                             # Jest tests

# Docker
docker build -t finally:latest .         # Build image
docker run -p 8000:8000 finally:latest   # Run container

# Git
git status                    # Check changes
git add .                     # Stage all
git commit -m "message"       # Commit
git push origin main          # Push
```

---

## Estimated Timeline

- **Phase 1** (Hours 1-2): Foundation & DB
- **Phase 2** (Hours 2-4): APIs & Tests  
- **Phase 3** (Hours 4-6): Frontend
- **Phase 4** (Hours 6-8): Integration & DevOps
- **Phase 5** (Hour 8): Final validation & docs

**Total: ~8 hours for complete, production-quality app!**

---

## Day 5 Handoff

After Day 4 completion, the application is:
- ✅ Fully functional
- ✅ Locally deployable
- ✅ Tested and validated
- ✅ Ready for production deployment (optional)

Day 5 will focus on:
- Deploying to Fly.io (optional)
- Integrating real market data
- Performance optimization
- Advanced features

But the core app is 100% complete and working!

---

**You've got this! Go build something amazing! 🚀**
