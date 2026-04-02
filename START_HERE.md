# FinAlly Trading Platform - Week 3 AI Coding Course

## 🚀 START HERE

This repository contains the complete scaffold and instructions for building FinAlly (Finance Ally) - an AI-powered trading workstation - using Claude Code agents across 5 days.

### What is FinAlly?

A visually stunning trading application with:
- 📊 Live market data streaming in real-time
- 🤖 AI chat assistant for portfolio analysis and trade execution
- 💰 Simulated portfolio with $10,000 virtual cash
- 📈 Professional Bloomberg-style dark UI
- 🎯 Built entirely by AI agents in <8 hours
- 🐳 Single Docker container deployment

---

## 📅 Week 3 Timeline (Days 1-5)

### ✅ Day 1: Foundation & Infrastructure (COMPLETE)
- [x] Claude Code project setup
- [x] Slash commands and skills created
- [x] Sub-agent architecture documented
- [x] Team role specifications written
- [x] Git repository prepared

**Files created**:
- `.claude/commands/` - Slash commands
- `.claude/skills/project-context.md` - Project context skill
- `.claude/agents/` - Agent role definitions
- `CLAUDE_EXTENDED.md` - Complete build guide
- Planning documents for Days 2-3

### ✅ Days 2-3: Research & Team Prep (COMPLETE)
- [x] Market data evaluation (`planning/MARKET_DATA_RESEARCH.md`)
- [x] Backend architecture spec (`planning/BACKEND_ARCHITECTURE.md`)
- [x] Frontend requirements (`planning/FRONTEND_REQUIREMENTS.md`)
- [x] Team guidelines (`planning/TEAM_GUIDELINES.md`)
- [x] Agent specialist role definitions

**Ready for**: Day 4 Agent Team build

### 🔄 Day 4: MAIN BUILD PHASE ← YOU ARE HERE
- Build entire application using Agent Teams
- 6 specialist agents working in coordinated sequence
- Target: 8 hours to complete, fully functional app
- Expected results: 121+ tests passing, Docker running

**Start**: Read `planning/DAY4_ORCHESTRATION.md`

### 🎯 Day 5: Production & Optimization (Next)
- Deploy to Fly.io (optional)
- Integrate live market data
- Performance optimization
- Final validation

---

## 📋 How to Execute Day 4 Build

### Step 1: Read This
Read the complete project spec:
```
→ planning/PLAN.md (full requirements)
→ CLAUDE_EXTENDED.md (build instructions)
```

### Step 2: Enable Agent Teams
In Claude Code, enable the experimental Agent Teams feature through settings.

### Step 3: Follow the Orchestration
Use `planning/DAY4_ORCHESTRATION.md` as your guide:
- It shows the 5 phases
- Each phase has specific agent tasks
- Clear success criteria for each
- Estimated timeline: 8 hours total

### Step 4: Coordinate Agents
Following the sequence in DAY4_ORCHESTRATION.md:

**Phase 1** (Hours 1-2):
1. Database Engineer → Create schema & models
2. Backend Engineer → Set up FastAPI + database integration
3. DevOps Engineer → Start Dockerfile

**Phase 2** (Hours 2-4):
1. Backend Engineer → Implement all API endpoints
2. Backend Engineer → Write 121+ unit tests
3. Backend Engineer → Document API specification

**Phase 3** (Hours 4-6):
1. Frontend Engineer → Set up Next.js project
2. Frontend Engineer → Build 9 React components
3. Frontend Engineer → Implement SSE for real-time data

**Phase 4** (Hours 6-8):
1. LLM Engineer → Integrate Cerebras chat
2. Frontend Engineer → Connect to backend APIs
3. DevOps Engineer → Complete Docker containerization
4. Integration Tester → Validate everything works

**Phase 5** (Hour 8):
1. All agents → Final testing and validation
2. Team Lead → Documentation and handoff

### Step 5: Use Slash Commands
Monitor progress with:
```
/agent-status    - See what all agents have done
/test-check      - Verify 121+ tests passing
/docreview       - Review planning documents
```

### Step 6: Deploy
Once Day 4 completes:
```bash
docker build -t finally:latest .
docker run -p 8000:8000 finally:latest
# Open http://localhost:8000 → Full trading app!
```

---

## 🎯 Success Criteria

### Day 4 Completion = "Done!"

✅ Backend API fully implemented (121+ tests passing)
✅ Frontend React app built and styled  
✅ Database schema and operations working
✅ Docker container builds and runs
✅ LLM chat integration complete
✅ Real-time market data streaming
✅ Application live at http://localhost:8000
✅ All features working end-to-end

---

## 📚 Key Documents

For agents and developers:

| Document | Purpose | For Whom |
|----------|---------|----------|
| `planning/PLAN.md` | Full requirements spec | Everyone |
| `CLAUDE_EXTENDED.md` | Build instructions | Agents |
| `planning/DAY4_ORCHESTRATION.md` | Day 4 execution guide | Team Lead + Agents |
| `planning/BACKEND_ARCHITECTURE.md` | Backend spec | Backend Engineer |
| `planning/FRONTEND_REQUIREMENTS.md` | Frontend spec | Frontend Engineer |
| `planning/TEAM_GUIDELINES.md` | Team coordination | All Agents |
| `.claude/agents/*.md` | Role specifications | Individual agents |

---

## 🛠️ Technology Stack

**Backend**: FastAPI (Python/uv), SQLAlchemy, SQLite/PostgreSQL
**Frontend**: Next.js 14+, TypeScript, React, Tailwind CSS, Redux
**LLM**: Cerebras (via OpenRouter)
**Real-time**: Server-Sent Events (SSE), market simulator
**DevOps**: Docker, docker-compose
**Testing**: Pytest (121+), Jest, Playwright

---

## 🚀 What Happens Next (Days 4-5)

### If Using Agent Teams (Day 4)
- ~30 minutes per agent task
- Agents work in coordinated sequence
- Human approves routine operations
- Result: Fully functional app ~8 hours faster than manual

### If Using Codex 5.3 (Day 5)
- 15 minutes total for spec-driven build
- Even faster than Agent Teams
- Production-quality output
- Full deployment to Fly.io

---

## 💡 Quick Start for Manual Development

If you prefer to build manually instead of using Agent Teams:

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m uvicorn src.main:app --reload

# Frontend setup (separate terminal)
cd frontend
npm install
npm run dev
# Visit http://localhost:3000 for React dev server
# API calls go to http://localhost:8000/api/*

# Docker (after both are working)
docker build -t finally:latest .
docker run -p 8000:8000 finally:latest
# Visit http://localhost:8000 for full app
```

---

## ❓ Common Questions

**Q: How long does Day 4 take?**
A: With Agent Teams, ~8 hours. With Codex, ~15 minutes.

**Q: Can I start before reading the docs?**
A: No! The docs are essential context. Read them first.

**Q: What if an agent gets stuck?**
A: Check DAY4_ORCHESTRATION.md for that phase's success criteria. File a blocker.

**Q: Can I start from a different day?**
A: Days 1-3 infrastructure must be complete first. They're critical for Day 4.

**Q: What's the time limit?**
A: No hard limit, but the course is designed for 8 hours/day. Day 4 should complete in one sitting.

**Q: Why so many agents?**
A: Parallel work. Each agent specializes (backend/frontend/db/devops/llm/testing) for faster throughput.

---

## 📞 Need Help?

- **Architecture questions**: See `planning/PLAN.md`
- **Backend implementation**: See `planning/BACKEND_ARCHITECTURE.md`
- **Frontend implementation**: See `planning/FRONTEND_REQUIREMENTS.md`
- **Team coordination**: See `planning/TEAM_GUIDELINES.md`
- **Day 4 execution**: See `planning/DAY4_ORCHESTRATION.md`
- **Specific role**: See `.claude/agents/{role}.md`

---

## 🎉 Final Notes

- This project demonstrates the power of agent coordination
- Build a production-quality app faster than manual coding
- Everything is containerized and deployable
- Complete specification provided upfront
- Clear success metrics at each phase
- Git history shows incremental progress

**Total effort: < 8 hours of human oversight**
**Code generated: ~10,000 lines**
**Tests written: 121+**
**Features delivered: Complete trading platform with AI**

---

## 🚀 Ready?

1. Start by reading `planning/DAY4_ORCHESTRATION.md`
2. Enable Agent Teams in Claude Code
3. Follow the 5-phase build sequence
4. Watch the app come together in real-time
5. Celebrate when it all works! 🎉

**Let's build FinAlly! →** `planning/DAY4_ORCHESTRATION.md`
