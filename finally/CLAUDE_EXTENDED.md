# FinAlly - Complete AI Agent Implementation Guide

This document guides AI agents to build a complete AI-powered trading workstation through Days 1-5 of the project timeline.

## Core Project Requirements

See `planning/PLAN.md` for complete specification. Key summary:

- **Vision**: Bloomberg-style trading workstation with AI copilot
- **Market Data**: Live streaming via SSE (simulator default, Polygon.io optional)
- **Portfolio**: $10,000 virtual cash, market orders only, instant fills
- **AI Chat**: Cerebras LLM for portfolio analysis and trade execution
- **UI**: Dark professional theme with real-time updates and animations
- **Architecture**: Single Docker container on port 8000

## Day 1: Foundation & Infrastructure (Agent-Ready Prep)

### Tasks for Day 1
1. Review and enhance `planning/PLAN.md` with any gaps
2. Create `.claude/` structure (✓ done)
3. Set up custom slash commands (✓ done)
4. Create documentation for agent coordination
5. Verify project structure is agent-friendly

### Day 1 Deliverables
- Comprehensive project documentation
- Slash commands for status, testing, reviews
- Skills for project context
- Clear agent responsibilities defined
- Git repository ready for agent commits

---

## Day 2: Research & Discovery

### Research Tasks (Can be done via agents or manually)

#### Market Data Research
- Research current Polygon.io (Massive) pricing and tier structure
- Document API endpoints, rate limits, authentication
- Compare with alternatives (Alpha Vantage, IEX Cloud)
- Update `planning/MARKET_DATA_DISCOVERY.md`

#### Frontend Requirements Analysis  
- Document live data update patterns needed
- Analyze responsive design requirements
- Plan component hierarchy
- Create UI wireframes or sketches
- Update `planning/FRONTEND_REQUIREMENTS.md`

#### Backend Architecture
- Database schema finalization
- API endpoint specification
- Authentication strategy
- Error handling patterns
- Update `planning/BACKEND_ARCHITECTURE.md`

---

## Day 3: Team Setup & Large Codebase Prep

### Setup Tasks
1. Create team guidelines in `planning/TEAM_GUIDELINES.md`
2. Define API contracts between frontend/backend
3. Set up `.claude/agents/` templates
4. Create integration testing framework
5. Document context management strategies

### Agent Preparation
- Create specialist agent descriptions
- Define inter-agent communication patterns
- Set up knowledge base for team members
- Create issue/PR templates

---

## Day 4: MAIN BUILD PHASE - Agent Teams

### ⭐ CRITICAL: This is where the entire app is built ⭐

Use Claude Code Agent Teams feature to coordinate 6-7 specialist agents:

### Agent 1: Backend Engineer (FastAPI)
**Files to Create**:
- `backend/pyproject.toml` - uv project configuration
- `backend/src/main.py` - FastAPI application
- `backend/src/api/trades.py` - Trade execution API
- `backend/src/api/portfolio.py` - Portfolio management
- `backend/src/api/watchlist.py` - Watchlist API
- `backend/src/api/chat.py` - AI chat endpoint  
- `backend/src/db/models.py` - SQLAlchemy models
- `backend/src/db/schema.py` - Database schema  
- `backend/src/market_data/simulator.py` - Price simulator
- `backend/src/market_data/polygon.py` - Polygon.io integration
- `backend/src/llm/chat.py` - Cerebras LLM integration
- `backend/tests/test_*.py` - Unit tests (121+ tests target)

**Success Criteria**:
- FastAPI server runs on port 8000
- All endpoints implemented per spec
- 121+ unit tests passing
- Error handling complete
- Database migrations working

### Agent 2: Frontend Engineer (React/Next.js)
**Files to Create**:
- `frontend/package.json` - npm project config  
- `frontend/next.config.js` - Static export config
- `frontend/src/pages/index.tsx` - Main dashboard
- `frontend/src/pages/_app.tsx` - App layout
- `frontend/src/components/PriceGrid.tsx` - Watchlist display
- `frontend/src/components/Chart.tsx` - Price chart
- `frontend/src/components/Portfolio.tsx` - Portfolio view 
- `frontend/src/components/Heatmap.tsx` - Treemap heatmap
- `frontend/src/components/Chat.tsx` - AI chat interface
- `frontend/src/components/Positions.tsx` - Positions table
- `frontend/src/hooks/useMarketData.ts` - SSE market data hook
- `frontend/src/styles/globals.css` - Tailwind styles

**Success Criteria**:
- React app builds successfully
- Next.js static export completes
- All components render without errors
- Responsive design works (desktop + mobile)
- Professional dark theme applied
- Real-time data bindings functional

### Agent 3: Database Engineer  
**Files to Create**:
- `backend/src/db/seed.py` - Seed data script
- Database migrations for:
  - users_profile table
  - positions table
  - trades table
  - watchlist table
  - chat_history table
- `backend/src/db/init_db.py` - Database initialization

**Success Criteria**:
- All tables created with proper relationships
- Indexes on frequently queried columns
- Foreign key constraints enforced
- Seed data for testing available
- Database can be reset cleanly

### Agent 4: DevOps Engineer (Containerization)
**Files to Create**:
- `Dockerfile` - Multi-stage build (Node for frontend, Python for backend)
- `docker-compose.yml` - Local development setup
- `.dockerignore` - Exclude build artifacts
- `scripts/start_windows.ps1` - Windows startup script
- `scripts/start_mac.sh` - macOS/Linux startup script
- `.github/workflows/ci.yml` - GitHub Actions (optional)
- Environment variable documentation

**Success Criteria**:
- Docker builds successfully
- Single container runs on port 8000 ✓
- Docker volumes mount correctly
- Environment variables configurable
- Health checks working

### Agent 5: LLM Integration Engineer
**Files to Create**:
- `backend/src/llm/cerebras_client.py` - Cerebras API client
- `backend/src/llm/prompts.py` - Prompt templates
- `backend/src/llm/tools.py` - Trading action tools
- `backend/src/api/chat_routes.py` - Chat endpoints
- LLM response streaming

**Success Criteria**:
- Connects to Cerebras via OpenRouter
- Chat endpoint responds with analysis
- Trade recommendations generated
- Structured output parsing works
- Token usage tracked
- Error handling for API failures

### Agent 6: Integration Tester
**Files to Create**:
- `test/e2e_tests.py` - End-to-end tests using Playwright
- Integration test suites for:
  - API contract testing
  - Database operation validation
  - UI workflow verification
  - Market data integration
  - Chat functionality
- `test/fixtures/test_data.py` - Test data factory

**Success Criteria**:
- All integration tests passing
- No API contract mismatches
- UI workflows complete successfully
- Database transactions atomic
- Error cases handled
- Performance acceptable

### Coordination Rules for Agent Teams
1. **Start Sequence**:
   - Backend Engineer first (defines API contracts)
   - Database Engineer immediately after (schema needed)
   - DevOps parallel (prepares Docker)
   - Frontend after backend APIs exist
   - LLM Engineer can work in parallel
   - Tester validates after each module

2. **Communication**:
   - API contracts documented in `planning/API_SPEC.md`
   - Database schema in `planning/DB_SCHEMA.md`
   - Frontend component API in code comments
   - Daily status updates via `/agent-status` command

3. **Approval Strategy**:
   - Approve file creation once per agent
   - Watch for unexpected requests
   - Always approve test runs
   - Review before major refactors

4. **Success Metrics**:
   - ✅ 121+ unit tests passing
   - ✅ All API endpoints working
   - ✅ Frontend builds and loads
   - ✅ Database properly seeded
   - ✅ Docker container runs
   - ✅ Chat responds to queries
   - ✅ Live in browser at localhost:8000

---

## Day 5: Advanced Orchestration & Production Deployment

### Option A: Codex Build (Recommended for Production)
If using Codex orchestrator:
1. Prepare deployment specifications
2. Run Codex to generate optimized code
3. Build production Docker image
4. Deploy to Fly.io
5. Configure live market data API keys
6. Verify production instance

### Option B: Manual Production Steps
1. Optimize final code
2. Add performance monitoring
3. Configure auth/security
4. Deploy Docker to Fly.io
5. Set up CI/CD pipeline
6. Monitor production instance

### Production Deployment
```bash
# Build and push Docker image
docker build -t finally-app .
docker tag finally-app gcr.io/PROJECT/finally-app:latest

# Deploy to Fly.io (if chosen)
fly auth login  
fly deploy --build-arg ENV=production

# Expected result: Live trading app at https://finally-[name].fly.dev
```

---

## File Structure After Day 4 Completion

```
finally/
├── backend/
│   ├── pyproject.toml
│   ├── src/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── trades.py
│   │   │   ├── portfolio.py
│   │   │   ├── watchlist.py
│   │   │   └── chat.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   ├── schema.py
│   │   │   └── init_db.py
│   │   ├── market_data/
│   │   │   ├── simulator.py
│   │   │   └── polygon.py
│   │   └── llm/
│   │       ├── cerebras_client.py
│   │       ├── prompts.py
│   │       └── tools.py
│   └── tests/ (121+ tests)
│
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   └── src/
│       ├── pages/
│       │   ├── index.tsx
│       │   └── _app.tsx
│       ├── components/
│       │   ├── PriceGrid.tsx
│       │   ├── Chart.tsx
│       │   ├── Heatmap.tsx
│       │   ├── Portfolio.tsx
│       │   ├── Chat.tsx
│       │   └── Positions.tsx
│       ├── hooks/
│       │   └── useMarketData.ts
│       └── styles/
│           └── globals.css
│
├── planning/
│   ├── PLAN.md
│   ├── MARKET_DATA_DISCOVERY.md
│   ├── FRONTEND_REQUIREMENTS.md
│   ├── BACKEND_ARCHITECTURE.md
│   ├── API_SPEC.md
│   ├── DB_SCHEMA.md
│   ├── TEAM_GUIDELINES.md
│   └── MARKET_DATA_SUMMARY.md
│
├── test/
│   ├── e2e_tests.py
│   └── fixtures/
│       └── test_data.py
│
├── .claude/
│   ├── commands/
│   │   ├── docreview.md
│   │   ├── agent-status.md
│   │   └── test-check.md
│   ├── skills/
│   │   └── project-context.md
│   └── agents/ (skill definitions)
│
├── scripts/
│   ├── start_windows.ps1
│   └── start_mac.sh
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Quick Start for Agents (Day 4)

### Step 1: Read Project Spec
```
Read: planning/PLAN.md (full requirements)
Reference: planning/MARKET_DATA_SUMMARY.md (context)
```

### Step 2: Run Tests
```
/test-check - Before starting to verify baseline
```

### Step 3: Create API Specification
```
Create: planning/API_SPEC.md with all endpoints
```

### Step 4: Execute Agency Build
```
Deploy 6 agents in the order:
1. Backend Engineer (fastapi implementation)
2. Database Engineer (schema + migrations)
3. Frontend Engineer (React component build)
4. DevOps Engineer (Dockerfile setup)
5. LLM Engineer (Cerebras integration)
6. Integration Tester (test everything)
```

### Step 5: Verify Success
```
/agent-status - Get comprehensive status
All 121+ tests passing
Frontend builds without errors
Docker container runs successfully
Live at http://localhost:8000
```

---

## Environment Variables (.env)

```bash
# Required
OPENROUTER_API_KEY=sk-... (for Cerebras inference)

# Optional  
MASSIVE_API_KEY=... (for live market data, leave empty for simulator)

# Optional
LLM_MOCK=true (for testing with deterministic responses)

# Database
DATABASE_URL=sqlite:///db/finally.db (development)

# Deployment
FLASK_ENV=production (when deploying)
```

---

## Success Criteria Summary

### After Day 1 (Today)
✅ Project structure prepared
✅ Documentation complete
✅ Agent infrastructure ready

### After Day 2
✅ Research documented
✅ API specifications drafted
✅ Database schema finalized

### After Day 3  
✅ Team guidelines written
✅ Integration testing framework ready
✅ Specialist agents trained/prepared

### After Day 4 ⭐
✅ Backend API (121+ tests passing) ✅
✅ React frontend (builds, responsive) ✅
✅ Database (seeded, optimized) ✅
✅ Docker (builds, single container) ✅
✅ LLM integration (chat working) ✅
✅ Full integration tests passing ✅
✅ Live in browser at localhost:8000 ✅

### After Day 5
✅ Production-ready build (Codex option)
✅ Deployed to Fly.io (optional)
✅ Live market data integrated
✅ Performance optimized
✅ Monitoring configured

---

## Notes for Agents

- **Context Sharing**: Use `/agent-status` command frequently to stay aware
- **Documentation**: Update planning files as tasks complete
- **Testing**: Run `/test-check` after each major change
- **Communication**: Be explicit about blockers or unexpected issues
- **Git**: Commit frequently with clear commit messages
- **Approvals**: Many routine operations can be approved by pattern (file creation, tests, etc.)

Good luck! You're building something amazing! 🚀
