"""
FinAlly Trading Platform - FastAPI Backend
AI-powered trading workstation with real-time market data
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import asyncio
import json
from contextlib import asynccontextmanager

from db.init_db import initialize_database
from market_data.simulator import MarketDataSimulator, set_market_simulator, get_market_simulator
from api.portfolio import router as portfolio_router
from api.trades import router as trades_router
from api.watchlist import router as watchlist_router
from api.prices import router as prices_router
from api.chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    from globals import market_simulator

    # Startup
    print("🚀 Starting FinAlly Trading Platform...")

    # Initialize database
    initialize_database()

    # Start market data simulator
    simulator = MarketDataSimulator()
    set_market_simulator(simulator)
    await simulator.start()

    print("✅ FinAlly backend ready!")

    yield

    # Shutdown
    print("🛑 Shutting down FinAlly...")
    simulator = get_market_simulator()
    if simulator:
        await simulator.stop()

# Create FastAPI app
app = FastAPI(
    title="FinAlly Trading Platform",
    description="AI-powered trading workstation with real-time market data",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(portfolio_router, prefix="/api")
app.include_router(trades_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")
app.include_router(prices_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    from market_data.simulator import get_market_simulator
    simulator = get_market_simulator()
    return {
        "status": "healthy",
        "message": "FinAlly trading platform is running",
        "market_data": "active" if simulator and simulator.is_running() else "inactive"
    }

@app.get("/api/stream/prices")
async def stream_prices():
    """Server-Sent Events stream for real-time price updates"""
    from market_data.simulator import get_market_simulator
    simulator = get_market_simulator()
    if not simulator:
        raise HTTPException(status_code=503, detail="Market data simulator not available")

    async def generate():
        while True:
            try:
                # Get current prices
                prices = simulator.get_all_prices()
                if prices:
                    # Format as SSE with JSON payload
                    payload = {"prices": prices, "timestamp": simulator.get_timestamp()}
                    yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(0.5)  # Update every 500ms
            except Exception as e:
                print(f"Error in price stream: {e}")
                break

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )