"""
Portfolio API endpoints for FinAlly
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from db.models import UserProfile, Position
from db.init import get_db_session
from market_data.simulator import get_market_simulator

router = APIRouter(prefix="/portfolio", tags=["portfolio"])
logger = logging.getLogger(__name__)

@router.get("/")
async def get_portfolio(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """Get complete portfolio overview"""
    try:
        # Get user profile
        user = db.query(UserProfile).filter(UserProfile.id == "default").first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get positions
        positions = db.query(Position).filter(Position.user_id == "default").all()

        # Calculate portfolio value
        total_value = user.cash_balance
        positions_data = []

        for pos in positions:
            # Get current price from market data simulator
            simulator = get_market_simulator()
            current_price = simulator.get_price(pos.ticker) if simulator else 100.0
            if current_price is None:
                current_price = 100.0  # Fallback

            position_value = pos.quantity * current_price
            total_value += position_value

            positions_data.append({
                "ticker": pos.ticker,
                "quantity": pos.quantity,
                "avg_cost": pos.avg_cost,
                "current_price": current_price,
                "market_value": position_value,
                "unrealized_pnl": (current_price - pos.avg_cost) * pos.quantity,
                "unrealized_pnl_pct": ((current_price - pos.avg_cost) / pos.avg_cost) * 100 if pos.avg_cost > 0 else 0
            })

        return {
            "cash_balance": user.cash_balance,
            "total_value": total_value,
            "positions": positions_data,
            "total_positions_value": total_value - user.cash_balance
        }

    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        raise HTTPException(status_code=500, detail="Failed to get portfolio")

@router.get("/positions")
async def get_positions(db: Session = Depends(get_db_session)) -> List[Dict[str, Any]]:
    """Get all positions"""
    try:
        positions = db.query(Position).filter(Position.user_id == "default").all()

        result = []
        for pos in positions:
            # Get current price from market data simulator
            simulator = get_market_simulator()
            current_price = simulator.get_price(pos.ticker) if simulator else 100.0
            if current_price is None:
                current_price = 100.0  # Fallback

            result.append({
                "ticker": pos.ticker,
                "quantity": pos.quantity,
                "avg_cost": pos.avg_cost,
                "current_price": current_price,
                "market_value": pos.quantity * current_price,
                "unrealized_pnl": (current_price - pos.avg_cost) * pos.quantity,
                "unrealized_pnl_pct": ((current_price - pos.avg_cost) / pos.avg_cost) * 100 if pos.avg_cost > 0 else 0
            })

        return result

    except Exception as e:
        logger.error(f"Error getting positions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get positions")

@router.get("/pnl")
async def get_pnl_history(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """Get P&L history for charting"""
    try:
        # For now, return mock data - in real implementation would calculate from trades
        # This would typically aggregate trade data to show daily/weekly P&L

        return {
            "daily_pnl": [
                {"date": "2024-01-01", "pnl": 1250.50},
                {"date": "2024-01-02", "pnl": -320.75},
                {"date": "2024-01-03", "pnl": 890.25},
                {"date": "2024-01-04", "pnl": -150.00},
                {"date": "2024-01-05", "pnl": 2100.80}
            ],
            "total_pnl": 2770.80,
            "total_pnl_pct": 27.71
        }

    except Exception as e:
        logger.error(f"Error getting P&L history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get P&L history")