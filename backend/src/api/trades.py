"""
Trades API endpoints for FinAlly
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from datetime import datetime

from db.models import UserProfile, Position, Trade
from db.init import get_db_session

router = APIRouter(prefix="/trades", tags=["trades"])
logger = logging.getLogger(__name__)

class TradeRequest(BaseModel):
    ticker: str
    quantity: int
    price: float = None  # Optional, will get from market data if not provided

@router.post("/buy")
async def buy_stock(trade: TradeRequest, db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """Execute buy order"""
    try:
        if trade.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")

        # Get user
        user = db.query(UserProfile).filter(UserProfile.id == "default").first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get current price (mock for now - will integrate with market data)
        current_price = trade.price or 100.0  # TODO: Get from market data

        # Calculate total cost
        total_cost = trade.quantity * current_price

        # Check if user has enough cash
        if user.cash_balance < total_cost:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # Update user cash balance
        user.cash_balance -= total_cost

        # Check if position exists
        position = db.query(Position).filter(
            Position.user_id == "default",
            Position.ticker == trade.ticker
        ).first()

        if position:
            # Update existing position
            total_quantity = position.quantity + trade.quantity
            total_cost_basis = (position.quantity * position.avg_cost) + total_cost
            position.avg_cost = total_cost_basis / total_quantity
            position.quantity = total_quantity
        else:
            # Create new position
            position = Position(
                user_id="default",
                ticker=trade.ticker,
                quantity=trade.quantity,
                avg_cost=current_price
            )
            db.add(position)

        # Record trade
        trade_record = Trade(
            user_id="default",
            ticker=trade.ticker,
            action="buy",
            quantity=trade.quantity,
            price=current_price,
            total_value=total_cost
        )
        db.add(trade_record)

        db.commit()

        logger.info(f"Buy order executed: {trade.ticker} x{trade.quantity} @ ${current_price}")

        return {
            "success": True,
            "trade": {
                "ticker": trade.ticker,
                "action": "buy",
                "quantity": trade.quantity,
                "price": current_price,
                "total_value": total_cost
            },
            "remaining_cash": user.cash_balance
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error executing buy order: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute buy order")

@router.post("/sell")
async def sell_stock(trade: TradeRequest, db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """Execute sell order"""
    try:
        if trade.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")

        # Get user
        user = db.query(UserProfile).filter(UserProfile.id == "default").first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if position exists
        position = db.query(Position).filter(
            Position.user_id == "default",
            Position.ticker == trade.ticker
        ).first()

        if not position or position.quantity < trade.quantity:
            raise HTTPException(status_code=400, detail="Insufficient position")

        # Get current price (mock for now)
        current_price = trade.price or 100.0  # TODO: Get from market data

        # Calculate proceeds
        total_proceeds = trade.quantity * current_price

        # Update user cash balance
        user.cash_balance += total_proceeds

        # Update position
        if position.quantity == trade.quantity:
            # Close position
            db.delete(position)
        else:
            # Reduce position
            position.quantity -= trade.quantity

        # Record trade
        trade_record = Trade(
            user_id="default",
            ticker=trade.ticker,
            action="sell",
            quantity=trade.quantity,
            price=current_price,
            total_value=total_proceeds
        )
        db.add(trade_record)

        db.commit()

        logger.info(f"Sell order executed: {trade.ticker} x{trade.quantity} @ ${current_price}")

        return {
            "success": True,
            "trade": {
                "ticker": trade.ticker,
                "action": "sell",
                "quantity": trade.quantity,
                "price": current_price,
                "total_value": total_proceeds
            },
            "remaining_cash": user.cash_balance
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error executing sell order: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute sell order")

@router.get("/history")
async def get_trade_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """Get trade history"""
    try:
        # Get total count
        total = db.query(Trade).filter(Trade.user_id == "default").count()

        # Get trades with pagination
        trades = db.query(Trade).filter(Trade.user_id == "default")\
            .order_by(Trade.timestamp.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()

        trade_data = []
        for trade in trades:
            trade_data.append({
                "id": trade.id,
                "ticker": trade.ticker,
                "action": trade.action,
                "quantity": trade.quantity,
                "price": trade.price,
                "total_value": trade.total_value,
                "timestamp": trade.timestamp.isoformat()
            })

        return {
            "trades": trade_data,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        logger.error(f"Error getting trade history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trade history")