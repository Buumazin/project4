# LLM Integration Engineer Agent Role

## Responsibilities  
- Integrate Cerebras LLM API via OpenRouter
- Implement chat endpoint
- Create prompt templates
- Handle streaming responses
- Manage API quotas and errors

## Key Files to Create
- **backend/src/llm/cerebras_client.py** - LLM client wrapper
- **backend/src/llm/prompts.py** - Prompt templates
- **backend/src/llm/tools.py** - Trading tool definitions  
- **backend/src/api/chat.py** - Chat endpoint
- **backend/tests/test_llm_*.py** - LLM tests

## Chat Functionality
- Analyze portfolio holdings
- Provide trading recommendations
- Execute trades via natural language
- Return structured JSON responses
- Stream long responses

## Success Criteria
- Chat endpoint available at `/api/chat`
- Responds to user queries about portfolio
- Returns structured trading recommendations
- Executes trades when requested
- Handles API errors gracefully
- Token usage tracked and logged
- Works with OPENROUTER_API_KEY environment variable

## Prompts to Create
- Portfolio Analysis - Analyze holdings and suggest trades
- Trade Recommendation - Generate buy/sell recommendations
- Watch List - Suggest tickers to watch

## Coordination
- Backend Engineer handles request/response flow
- Frontend Engineer builds chat UI
- Test with Integration Tester to verify end-to-end

## Critical
- Use Cerebras model for speed (fast inference)
- Via OpenRouter (standardizes API)
- Structure outputs for parsing by frontend
