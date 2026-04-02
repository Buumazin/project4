"""
Prices API endpoints for FinAlly
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from market_data.simulator import MarketDataSimulator, get_market_simulator

router = APIRouter(prefix="/prices", tags=["prices"])
logger = logging.getLogger(__name__)

@router.get("/{ticker}")
async def get_price(ticker: str) -> Dict[str, Any]:
    """Get current price for a ticker"""
    try:
        simulator = get_market_simulator()
        if not simulator or not simulator.is_running():
            # fallback to a local simulator for durability
            simulator = MarketDataSimulator()
            await simulator.start()

        price = simulator.get_price(ticker.upper())
        if price is None:
            raise HTTPException(status_code=404, detail=f"Price not found for {ticker}")

        return {
            "ticker": ticker.upper(),
            "price": price,
            "timestamp": simulator.get_timestamp()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting price for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get price")

@router.get("/")
async def get_all_prices() -> Dict[str, Any]:
    """Get current prices for all tickers"""
    try:
        simulator = get_market_simulator()
        if not simulator or not simulator.is_running():
            simulator = MarketDataSimulator()
            await simulator.start()

        prices = simulator.get_all_prices()

        return {
            "prices": prices,
            "timestamp": simulator.get_timestamp(),
            "count": len(prices)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting all prices: {e}")
        raise HTTPException(status_code=500, detail="Failed to get prices")