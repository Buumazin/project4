# FinAlly Project Context Skill

This skill provides essential context about the FinAlly (Finance Ally) trading workstation project.

## Project Overview
FinAlly is an AI-powered trading workstation with:
- Live market data streaming via SSE
- Simulated portfolio with $10,000 virtual cash
- AI chat assistant for trading advice and execution
- Professional Bloomberg-style UI with dark theme
- Real-time P&L tracking and portfolio visualization

## Technology Stack
- **Frontend**: Next.js (static export) + TypeScript + Tailwind CSS + Redis/Redux
- **Backend**: FastAPI (Python/uv) with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production)
- **Real-time Data**: Server-Sent Events (SSE), market simulator, or Polygon.io API
- **LLM Integration**: Cerebras via OpenRouter with structured outputs
- **Deployment**: Docker + Docker Compose, deployable to Fly.io
- **Testing**: Pytest (backend) + Jest (frontend) + Playwright (E2E)

## Key Features to Implement
1. **Price Streaming**: Live market data updates via SSE at ~500ms intervals
2. **Portfolio Management**: Buy/sell market orders, view positions, track P&L
3. **Visualizations**: Heatmap treemap, P&L chart, positions table, sparkline charts
4. **AI Chat**: Natural language trading advice and trade execution
5. **Watchlist**: Manual ticker management + AI suggestions
6. **Connection Status**: Indicator showing SSE connection health

## Architecture Boundaries
- Frontend: Static export from Next.js, served by FastAPI as static files
- Backend: All API logic, database operations, market data, LLM integration
- Database: User profile (cash balance), positions, trades, watchlist, chat history
- Market Data: Abstracted interface (simulator by default, Polygon.io optional)

## Success Criteria
- All 121+ API tests passing
- Frontend loads without errors and is responsive
- Real-time market data streaming at 500ms intervals
- AI chat functional with trade execution
- Docker build and run successful
- Zero-shot implementation possible with agent teams

## Color Scheme
- Accent Yellow: #ecad0a
- Blue Primary: #209dd7
- Purple Submit: #753991
- Dark Backgrounds: #0d1117, #1a1a2e
