"""
Chat API endpoints for FinAlly.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import logging

from db.init import get_db_session
from db.models import ChatMessage

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

import os
import re
from typing import Optional
import httpx

LLAMA_API_URL = os.getenv("LLAMA_API_URL", "http://127.0.0.1:8080/v1/completions")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama-7b")


def parse_trade_command(text: str) -> Optional[Dict[str, Any]]:
    normalized = text.lower().strip()

    # Vietnamese / English simplified command patterns
    buy_match = re.search(r"\b(?:mua|buy)\b\s+([A-Za-z0-9]+)\s+(\d+)", normalized)
    sell_match = re.search(r"\b(?:ban|bán|sell)\b\s+([A-Za-z0-9]+)\s+(\d+)", normalized)

    if buy_match:
        return {
            "action": "buy",
            "ticker": buy_match.group(1).upper(),
            "quantity": int(buy_match.group(2))
        }
    if sell_match:
        return {
            "action": "sell",
            "ticker": sell_match.group(1).upper(),
            "quantity": int(sell_match.group(2))
        }

    return None


async def query_llama(text: str) -> str:
    prompt = (
        "You are a trading assistant. "
        "Identify if the user asks to buy or sell stock. "
        "Return a concise natural language answer. "
        "If the user asks to trade, include the intent and symbol/qty exactly. "
        f"User: {text}\nAssistant:"
    )

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            payload = {
                "model": LLAMA_MODEL,
                "prompt": prompt,
                "max_tokens": 128,
                "temperature": 0.2,
                "top_p": 0.95,
                "stop": ["\n"]
            }
            resp = await client.post(LLAMA_API_URL, json=payload)
            resp.raise_for_status()
            result = resp.json()

            # Should support API returns with text in result.choice / result.choices
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("text", "").strip()
            if "choice" in result and isinstance(result["choice"], dict):
                return result["choice"].get("text", "").strip()

    except Exception as e:
        # Fallback to local rule-based parsing if llama API unavailable
        print(f"LLAMA API query failed: {e}")

    return ""


@router.post("/")
async def chat(message_req: ChatRequest, db=Depends(get_db_session)) -> Dict[str, Any]:
    user_msg = ChatMessage(user_id="default", role="user", content=message_req.message)
    db.add(user_msg)
    db.commit()

    # Try to call llama.cpp local API for better parsing and response
    llm_response_text = await query_llama(message_req.message)

    # Use fallback response when llama did not produce text
    if not llm_response_text:
        llm_response_text = f"Agent nhận được: {message_req.message}. Hãy nhập lệnh như 'mua AAPL 10' hoặc 'bán MSFT 5'."

    # Parse trade command from direct user text first, then from llama response
    trade_cmd = parse_trade_command(message_req.message)
    if not trade_cmd:
        trade_cmd = parse_trade_command(llm_response_text)

    trade_result = None
    if trade_cmd:
        from api.trades import TradeRequest, buy_stock, sell_stock

        trade_req = TradeRequest(
            ticker=trade_cmd["ticker"],
            quantity=trade_cmd["quantity"]
        )

        try:
            if trade_cmd["action"] == "buy":
                trade_result = await buy_stock(trade_req, db)
            else:
                trade_result = await sell_stock(trade_req, db)

            llm_response_text += f"\n✅ Đã thực hiện lệnh {trade_cmd['action']} {trade_cmd['ticker']} {trade_cmd['quantity']}"  # noqa: E501

        except Exception as e:
            llm_response_text += f"\n⚠️ Lỗi khi thực hiện lệnh: {str(e)}"

    assistant_msg = ChatMessage(user_id="default", role="assistant", content=llm_response_text)
    db.add(assistant_msg)
    db.commit()

    response_data = {
        "response": llm_response_text,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "ok",
    }

    if trade_result:
        response_data["trade_executed"] = trade_result

    return response_data

@router.get("/history")
async def chat_history(db=Depends(get_db_session)) -> Dict[str, Any]:
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == "default").order_by(ChatMessage.timestamp).all()
    return {
        "history": [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp.isoformat() if m.timestamp else None
            }
            for m in messages
        ]
    }
