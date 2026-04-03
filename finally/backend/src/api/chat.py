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

LLAMA_API_URL = os.getenv("LLAMA_API_URL", "http://127.0.0.1:8080/v1/chat/completions")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama-7b")


def parse_trade_command(text: str) -> Optional[Dict[str, Any]]:
    normalized = text.lower().strip()

    # Vietnamese / English simplified command patterns
    # 1) mua AAPL 10, buy MSFT 5
    buy_match = re.search(r"\b(?:mua|buy)\b\s+([a-z0-9]+)\s+(\d+)", normalized)
    sell_match = re.search(r"\b(?:ban|bán|sell)\b\s+([a-z0-9]+)\s+(\d+)", normalized)

    # 2) mua cho tôi 10 META, bán 5 TSLA
    buy_match_qty_first = re.search(r"\b(?:mua|buy)\b.*?(\d+)\s+([a-z0-9]+)", normalized)
    sell_match_qty_first = re.search(r"\b(?:ban|bán|sell)\b.*?(\d+)\s+([a-z0-9]+)", normalized)

    if buy_match:
        symbol, qty = buy_match.group(1), buy_match.group(2)
        return {"action": "buy", "ticker": symbol.upper(), "quantity": int(qty)}
    if sell_match:
        symbol, qty = sell_match.group(1), sell_match.group(2)
        return {"action": "sell", "ticker": symbol.upper(), "quantity": int(qty)}

    if buy_match_qty_first:
        qty, symbol = buy_match_qty_first.group(1), buy_match_qty_first.group(2)
        return {"action": "buy", "ticker": symbol.upper(), "quantity": int(qty)}
    if sell_match_qty_first:
        qty, symbol = sell_match_qty_first.group(1), sell_match_qty_first.group(2)
        return {"action": "sell", "ticker": symbol.upper(), "quantity": int(qty)}

    return None


async def query_llama(text: str) -> str:
    prompt = (
        "You are a trading assistant. "
        "Identify if the user asks to buy or sell stock. "
        "Return a concise natural language answer. "
        "If the user asks to trade, include the intent and symbol/qty exactly. "
        f"User: {text}\nAssistant:"
    )

    precise_prompt = (
        "Bạn là trợ lý giao dịch chứng khoán. \n"
        "Người dùng có thể hỏi bằng tiếng Việt hoặc tiếng Anh. \n"
        "Nếu người dùng yêu cầu giao dịch, trả lời CHÍNH XÁC với định dạng: 'mua SYMBOL QTY' hoặc 'bán SYMBOL QTY'. \n"
        "Trả lời ngắn gọn, không thêm văn bản thừa. Nếu không có ý định giao dịch, trả lời 'không giao dịch'.\n"
        f"Người dùng: {text}\nTrợ lý:"
    )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": LLAMA_MODEL,
                "messages": [{"role": "user", "content": precise_prompt}],
                "max_tokens": 64,
                "temperature": 0.1,
                "top_p": 0.95,
                "stop": ["\n"]
            }
            print(f"🔗 [DEBUG] Calling Llama API: {LLAMA_API_URL}")
            print(f"📝 [DEBUG] Prompt: {precise_prompt}")
            
            resp = await client.post(LLAMA_API_URL, json=payload)
            resp.raise_for_status()
            result = resp.json()
            
            print(f"📥 [DEBUG] Raw response from Llama: {result}")

            # Should support API returns with text in result.choices[0].message.content
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    text_output = choice["message"]["content"].strip()
                    print(f"✅ [DEBUG] Extracted from 'choices[0].message.content': '{text_output}'")
                    return text_output

            print(f"⚠️ [DEBUG] API response doesn't have 'choices', 'choice', or 'content' field")

    except Exception as e:
        # Fallback to local rule-based parsing if llama API unavailable
        print(f"❌ [ERROR] LLAMA API query failed: {type(e).__name__}: {e}")

    return ""


@router.post("/")
async def chat(message_req: ChatRequest, db=Depends(get_db_session)) -> Dict[str, Any]:
    user_msg = ChatMessage(user_id="default", role="user", content=message_req.message)
    db.add(user_msg)
    db.commit()

    # Try to call llama.cpp local API for better parsing and response
    print(f"🤖 [DEBUG] User message: {message_req.message}")
    llm_response_text = await query_llama(message_req.message)
    print(f"🤖 [DEBUG] Llama response: {llm_response_text}")

    # Use fallback response when llama did not produce text
    if not llm_response_text:
        llm_response_text = f"Agent nhận được: {message_req.message}. Hãy nhập lệnh như 'mua AAPL 10' hoặc 'bán MSFT 5'."

    # Parse trade command from direct user text first, then from llama response
    trade_cmd = parse_trade_command(message_req.message)
    if not trade_cmd:
        trade_cmd = parse_trade_command(llm_response_text)

    print(f"📊 [DEBUG] Parse result: {trade_cmd}")

    trade_result = None
    if trade_cmd:
        from api.trades import TradeRequest, buy_stock, sell_stock

        trade_req = TradeRequest(
            ticker=trade_cmd["ticker"],
            quantity=trade_cmd["quantity"]
        )

        try:
            if trade_cmd["action"] == "buy":
                print(f"✅ [DEBUG] Executing BUY: {trade_cmd['ticker']} x {trade_cmd['quantity']}")
                trade_result = await buy_stock(trade_req, db)
            else:
                print(f"✅ [DEBUG] Executing SELL: {trade_cmd['ticker']} x {trade_cmd['quantity']}")
                trade_result = await sell_stock(trade_req, db)

            # Use clean response for trades
            llm_response_text = f"✅ Đã thực hiện lệnh {trade_cmd['action']} {trade_cmd['ticker']} {trade_cmd['quantity']}"

        except Exception as e:
            llm_response_text = f"⚠️ Lỗi khi thực hiện lệnh: {str(e)}"

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
