# FinAlly — AI Trading Workstation

A visually stunning AI-powered trading workstation that streams live market data, simulates portfolio trading, and integrates an LLM chat assistant that can analyze positions and execute trades via natural language.

Built entirely by coding agents as a capstone project for an agentic AI coding course.

## Features

- **Live price streaming** via SSE with green/red flash animations
- **Simulated portfolio** — $10k virtual cash, market orders, instant fills
- **Portfolio visualizations** — heatmap (treemap), P&L chart, positions table
- **AI chat assistant** — analyzes holdings, suggests and auto-executes trades
- **Watchlist management** — track tickers manually or via AI
- **Dark terminal aesthetic** — Bloomberg-inspired, data-dense layout

## Architecture

Single Docker container serving everything on port 8000:

- **Frontend**: Next.js (static export) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python/uv) with SSE streaming
- **Database**: SQLite with lazy initialization
- **AI**: LiteLLM → OpenRouter (Cerebras inference) with structured outputs
- **Market data**: Built-in GBM simulator (default) or Massive API (optional)

## Quick Start

```bash
# Clone and configure
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env if using OpenRouter / cloud LLM
# Optionally set localhost llama endpoint:
# LLAMA_API_URL=http://127.0.0.1:8080/v1/completions
# LLAMA_MODEL=llama-7b

# Run with Docker
docker build -t finally .
docker run -v finally-data:/app/db -p 8000:8000 --env-file .env finally

# Open http://localhost:8000
```

### Local llama.cpp (no external API key)

1. Install and build llama.cpp:

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
mkdir build && cd build
cmake .. && cmake --build .
```

2. Download / convert a model (7B recommended for 16GB RAM + 8GB GPU):

```bash
# If source in GGUF/ggml format, skip conversion. Otherwise:
python3 ../scripts/convert-llama.py /path/to/original/7b-model.bin /path/to/models/llama-7b-q4_0.bin
```

3. Launch API server (if supported by your build):

```bash
./main -m /path/to/models/llama-7b-q4_0.bin --api --host 0.0.0.0 --port 8080
```

4. Start FinAlly, và đặt trong .env:

```
LLAMA_API_URL=http://127.0.0.1:8080/v1/completions
LLAMA_MODEL=llama-7b
```

5. Dùng chat UI gửi lệnh như `mua AAPL 10` hoặc `bán MSFT 5`.

API sẽ cố gắng parse câu lệnh và thực thi buy/sell qua endpoint `/api/trades`.


## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | No | OpenRouter API key for AI chat (optional when using local llama.cpp)
| `LLAMA_API_URL` | No | Default `http://127.0.0.1:8080/v1/completions` for llama.cpp local endpoint
| `LLAMA_MODEL` | No | Default `llama-7b` (or your local model identifier) |
| `MASSIVE_API_KEY` | No | Massive (Polygon.io) key for real market data; omit to use simulator |
| `LLM_MOCK` | No | Set `true` for deterministic mock LLM responses (testing) |

## Day1-5 Validation

- Day1: Agent pipeline (`market -> strategy -> order`) ✅
- Day2: Local AI/LLM support (`llama.cpp` + rule-based fallbacks) ✅
- Day3: Agent team integration (`market-agent`, `strategy-agent`, `execution-agent`) ✅
- Day4: Orchestration artifacts (`orchestrator_plan.json`, `swarm_state.json`) ✅
- Day5: End-to-end deploy and tests (`ci.yml`, `day5_final_report.md`) ✅

## Project Structure

```
finally/
├── frontend/    # Next.js static export
├── backend/     # FastAPI uv project
├── planning/    # Project documentation and agent contracts
├── test/        # Playwright E2E tests
├── db/          # SQLite volume mount (runtime)
├── .github/workflows/ # CI + code review
├── day5_final_report.md
├── market_data_research.md
├── github_pr_simulation.md
├── agent_team_report.json
├── orchestrator_plan.json
├── swarm_state.json
└── scripts/     # Start/stop helpers
```

## License

See [LICENSE](LICENSE).
