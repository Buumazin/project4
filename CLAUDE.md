# FinAlly Project - the Finance Ally

## Quick Navigation
- **Complete Build Instructions**: See `CLAUDE_EXTENDED.md` ← START HERE FOR AGENTS
- **Project Specification**: See `planning/PLAN.md`
- **Market Data**: See `planning/MARKET_DATA_SUMMARY.md`

## For AI Agents (Days 1-5)
1. **Day 1 (Complete)**: Infrastructure setup - see `.claude/` folder and commands
2. **Day 2**: Research and discovery phase
3. **Day 3**: Team setup and preparation
4. **Day 4 ⭐ MAIN BUILD**: Use Agent Teams to build entire application
5. **Day 5**: Production deployment

### Quick Start for Agent Teams (Day 4)
```
Start with: CLAUDE_EXTENDED.md (all instructions)
Then read: planning/PLAN.md (full requirements)
```

## For Humans (Project Overview)

All project documentation is in the `planning` directory.

The key document is PLAN.md; the market data component has been completed and is summarized in the file `planning/MARKET_DATA_SUMMARY.md` with more details in the `planning/archive` folder.

### Technologies
- **Backend**: FastAPI (Python/uv)
- **Frontend**: Next.js (TypeScript/React) 
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **LLM**: Cerebras via OpenRouter
- **Market Data**: Simulator (default) or Polygon.io API
- **Deployment**: Docker + Fly.io

### Features
- Live market data streaming via SSE
- Simulated portfolio with AI trading assistant
- Professional Bloomberg-style dark UI
- Real-time P&L tracking and visualizations
- Natural language trade execution via AI chat

@planning/PLAN.md