# Team Development Guidelines

## Team Structure (Day 4)

### Agent Team Lead
- Orchestrates all agents
- Makes high-level decisions
- Resolves blockers
- Validates deliverables

### Specialist Agents (6)
1. **Backend Engineer** - FastAPI implementation
2. **Frontend Engineer** - React/Next.js UI
3. **Database Engineer** - Schema and migrations
4. **DevOps Engineer** - Docker containerization
5. **LLM Engineer** - Cerebras integration
6. **Integration Tester** - Testing and validation

## Work Sequencing

### Phase 1: Foundation (Hours 1-2)
1. Database Engineer: Create database schema and migrations
2. Backend Engineer: Set up FastAPI project and database models
3. DevOps Engineer: Prepare Dockerfile (start, will complete later)

### Phase 2: API Development (Hours 2-4)
1. Backend Engineer: Implement all API endpoints
2. Backend Engineer: Write unit tests (target 121+ tests)
3. Create planning/API_SPEC.md with all endpoints
4. **Approve each API endpoint before frontend uses**

### Phase 3: Frontend Development (Hours 4-6)
1. Frontend Engineer: Once API endpoints exist, build React components
2. Build components in parallel:
   - Price Grid
   - Chart component
   - Portfolio visualizations
   - Chat interface
   - Positions table

### Phase 4: Integration (Hours 6-7)
1. DevOps Engineer: Complete Docker setup
2. LLM Engineer: Connect Cerebras integration
3. Frontend Engineer: Connect to ACTUAL backend APIs
4. Integration Tester: Run end-to-end tests

### Phase 5: Testing & Polish (Hours 7-8)
1. Integration Tester: Run full test suite
2. Fix any bugs found
3. Verify Docker deployment
4. Final validation

## Approval Strategy

**What to auto-approve** (human says OK once):
- File creation for new features
- Test execution and rerun
- npm/pip package installations
- Docker builds
- Routine git commits

**What to ask approval for**:
- Major refactoring
- Deleting code
- Changing API contracts
- Modifying database schema (after initial)
- Major dependency updates

**Golden Rule**: If in doubt, ask. Better safe than broken.

## Communication Protocol

### Status Updates
Use `/agent-status` command frequently to:
- See what other agents have done
- Understand blockers
- Coordinate dependencies

### Blockers
If blocked by another agent:
1. Document the blocker clearly
2. Use `/agent-status` to report it
3. Suggest solution if possible
4. Don't wait longer than 15 minutes - escalate to Team Lead

### Code Handoffs
When one agent blocks another:
1. Push working code to Git
2. Write clear README in that module
3. Create GitHub issue describing what's next
4. Example: "Backend API ready - Frontend can now build components"

## Module Responsibilities (Clear Boundaries)

### Backend
- All `/api/*` endpoints
- Database operations
- Market data generation/streaming
- LLM integration logic
- Authentication (if added)
- Error handling
- Logging

**Must NOT do**: UI, styling, frontend logic

### Frontend
- React components
- State management (Redux/Zustand)
- Tailwind CSS styling
- SSE connection to backend
- Local form validation
- Client-side animations

**Must NOT do**: API calls to non-/api/* endpoints, database access

### Database
- Schema definition
- Migrations
- Seed data
- Indexes
- Relationships

**Must NOT do**: Business logic, API implementation

### DevOps
- Docker image build
- Environment configuration
- Container orchestration
- Startup/shutdown scripts

**Must NOT do**: Application logic, styling

### LLM
- Cerebras/OpenRouter integration
- Prompt engineering
- Token management
- Streaming responses
- Chat history storage

**Must NOT do**: UI for chat (Frontend does that)

### Testing
- Test strategy and framework
- Unit test execution
- Integration tests
- E2E tests
- Bug reporting with clear steps to reproduce

**Must NOT do**: Implementing features (only testing them)

## Code Review Expectations

All code should:
- Follow language conventions (Python black, JavaScript prettier)
- Have docstrings/comments on complex logic
- Include tests for new functionality
- Pass linting checks
- Have clear variable names

## Success Metrics

### Backend
- FastAPI server runs on port 8000
- All specified endpoints implemented
- 121+ unit tests passing
- No unhandled exceptions
- Database operations atomicWhen complete: `/test-check` shows all backend tests green

### Frontend
- No build errors
- Next.js static export completes
- All components render
- Responsive design verified
- Professional styling applied

### Database
- Tables created with correct schema
- Migrations reversible
- Seed data loads
- Relationships enforced
- Performance acceptable

### DevOps
- Docker builds successfully
- Single container on port 8000
- Both frontend + backend accessible
- Volume mounts work
- Environment variables configurable

### LLM
- Chat endpoint responds
- Cerebras integration works
- Structured outputs parsed correctly
- Error handling covers API failures

### Testing
- All modules tested
- 80%+ code coverage
- Integration tests pass
- E2E tests verify workflows
- Performance benchmarks acceptable

## Daily Sync Points

At key milestones, use `/agent-status` to:
- Acknowledge completed work
- Identify next blockers
- Plan next phase

Example workflow:
```
Hour 1: Database schema ready
Hour 2: Backend models implemented
Hour 3: API endpoints mostly coded
Hour 4: **API test approval** - Frontend can now proceed
Hour 5: Frontend components building
Hour 6: Docker setup ready
Hour 7: Integration testing
Hour 8: All tests green - DONE!
```

## Escalation Path

If something is stuck:
1. Try to resolve within team (agents communicate)
2. Ask Team Lead to make decision
3. Team Lead can:
   - Override a decision
   - Reassign work
   - Extend timeline
   - Split a complex task

## Git Workflow

- Main branch: `main` (stable, always working)
- Development: each agent works on feature branch
- Commit frequency: every completed task
- Pull requests: optional (time crunch), but merge to main when ready

## Security Considerations

- API keys in environment variables (not in code)
- OPENROUTER_API_KEY required for LLM
- MASSIVE_API_KEY optional for market data
- Database queries use parameterized queries (SQLAlchemy ORM)
- No hardcoded credentials

## Document Updates

As work progresses, keep planning docs updated:
- `planning/PLAN.md` - Main spec (read-only after day 1)
- `planning/API_SPEC.md` - Updated as endpoints built
- `planning/DB_SCHEMA.md` - Updated as schema created
- `planning/FRONTEND_REQUIREMENTS.md` - Reference guide (read-only)
- `planning/BACKEND_ARCHITECTURE.md` - Reference guide (read-only)

## Celebration Moment

When complete:
- All tests passing ✅
- Docker running ✅
- Frontend live in browser ✅
- Chat working ✅
- Real-time data streaming ✅

🎉 You've built a production-quality trading platform with AI in less than 8 hours!
