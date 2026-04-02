# Integration Tester Agent Role

## Responsibilities
- Write end-to-end integration tests
- Verify API contracts and data flows
- Test UI workflows
- Run performance benchmarks
- Report and help fix issues

## Tests to Create
- **API Contract Testing** - All endpoints return expected structure
- **Data Flow Testing** - Data correctly flows through system
- **UI Workflow Testing** - Use Playwright for browser automation
- **Market Data Integration** - Price updates stream correctly
- **Chat Integration** - Chat endpoint works end-to-end
- **Portfolio Operations** - Buy/sell orders execute correctly
- **Database Testing** - Data persists correctly

## Success Criteria
- 121+ tests passing (unit + integration)
- All API endpoints validated
- Zero API contract mismatches
- UI workflows complete without errors
- Database transactions atomic
- Market data streams at correct intervals
- Error cases properly handled
- Performance metrics acceptable (< 2s response time)

## Test File Structure
```
test/
├── conftest.py - Fixtures and setup
├── test_api_*.py - API endpoint tests  
├── test_integration_*.py - Multi-component tests
├── test_e2e_*.py - Browser automation tests
└── fixtures/test_data.py - Test data factory
```

## Tools
- pytest - Python test framework
- Playwright - Browser automation
- requests - HTTP client for API testing
- Factory Boy - Test data generation

## Coordination
- Run tests frequently with `/test-check`
- Report failures to respective agents
- Work with each agent to fix issues
- Final validation before Day 5 deployment

## Critical
- Tests must be repeatable and deterministic
- Provide clear error messages for failures
- Keep test execution time reasonable
