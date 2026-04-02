"""
Watchlist API endpoints for FinAlly
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from db.models import WatchlistItem
from db.init import get_db_session

router = APIRouter(prefix="/watchlist", tags=["watchlist"])
logger = logging.getLogger(__name__)

class WatchlistRequest(BaseModel):
    ticker: str

@router.get("/")
async def get_watchlist(db: Session = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """Get user's watchlist"""
    try:
        watchlist_items = db.query(WatchlistItem).filter(
            WatchlistItem.user_id == "default"
        ).order_by(WatchlistItem.added_at.desc()).all()

        result = []
        for item in watchlist_items:
            # Get current price (mock for now)
            current_price = 100.0  # TODO: Get from market data

            result.append({
                "ticker": item.ticker,
                "added_at": item.added_at.isoformat(),
                "current_price": current_price
            })

        return result

    except Exception as e:
        logger.error(f"Error getting watchlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to get watchlist")

@router.post("/")
async def add_to_watchlist(request: WatchlistRequest, db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """Add ticker to watchlist"""
    try:
        ticker = request.ticker.upper()

        # Check if already exists
        existing = db.query(WatchlistItem).filter(
            WatchlistItem.user_id == "default",
            WatchlistItem.ticker == ticker
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Ticker already in watchlist")

        # Add to watchlist
        watchlist_item = WatchlistItem(
            user_id="default",
            ticker=ticker
        )
        db.add(watchlist_item)
        db.commit()

        logger.info(f"Added {ticker} to watchlist")

        return {
            "success": True,
            "ticker": ticker,
            "message": f"Added {ticker} to watchlist"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding to watchlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to add to watchlist")

@router.delete("/{ticker}")
async def remove_from_watchlist(ticker: str, db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """Remove ticker from watchlist"""
    try:
        ticker = ticker.upper()

        # Find and delete
        item = db.query(WatchlistItem).filter(
            WatchlistItem.user_id == "default",
            WatchlistItem.ticker == ticker
        ).first()

        if not item:
            raise HTTPException(status_code=404, detail="Ticker not in watchlist")

        db.delete(item)
        db.commit()

        logger.info(f"Removed {ticker} from watchlist")

        return {
            "success": True,
            "ticker": ticker,
            "message": f"Removed {ticker} from watchlist"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing from watchlist: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove from watchlist")