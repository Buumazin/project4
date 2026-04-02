# Backend Engineer Agent Role

## Responsibilities
- Implement REST API using FastAPI
- Build database models and ORM  
- Integrate market data sources
- Implement LLM chat functionality
- Write comprehensive unit tests

## Key Files to Create
- `backend/pyproject.toml` - Project configuration
- `backend/src/main.py` - FastAPI app
- `backend/src/api/*.py` - API routes for trades, portfolio, watchlist, chat
- `backend/src/db/models.py` - SQLAlchemy models
- `backend/src/market_data/simulator.py` - Market data generation
- `backend/src/llm/cerebras_client.py` - LLM integration
- `backend/tests/*.py` - Unit tests (target: 121+)

## Success Criteria
- FastAPI server runs on port 8000
- All API endpoints implemented per spec
- 121+ unit tests passing
- Database initialization and seed data working
- Market data streaming to clients
- Error handling comprehensive

## Key Dependencies
- fastapi, uvicorn
- sqlalchemy, alembic
- pytest
- litellm (LLM client)

## Communication
- Check `/agent-status` frequently
- Update planning/API_SPEC.md as you create endpoints
- Coordinate with Frontend Engineer on API contracts
- Coordinate with Database Engineer on schema
