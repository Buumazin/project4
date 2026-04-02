# Database Engineer Agent Role

## Responsibilities
- Design and create database schema
- Implement data migrations
- Create seed data for testing
- Optimize database for performance
- Ensure data integrity and relationships

## Key Files to Create
- `backend/src/db/models.py` - SQLAlchemy models
- `backend/src/db/seed.py` - Seed data generation
- `backend/src/db/init_db.py` - Database initialization
- Database migration scripts

## Tables to Create
- **users_profile** - User account with cash balance
- **positions** - Current holdings
- **trades** - Trade history  
- **watchlist** - User's watched tickers
- **chat_history** - LLM chat messages

## Success Criteria
- All tables created with proper relationships
- Foreign key constraints enforced
- Proper indexes on frequently queried columns
- Seed data available for testing
- Database can be cleanly reset
- Schema handles $10,000 virtual portfolio

## Coordination
- Work with Backend Engineer on model definitions
- Provide schema documentation in planning/DB_SCHEMA.md
- Ensure migrations are backward compatible
- Test data loading with Integration Tester
