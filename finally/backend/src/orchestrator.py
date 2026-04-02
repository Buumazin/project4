"""Simple orchestrator for the Day1-4 AI agent pipeline"""
import asyncio
import json
from market_data.simulator import MarketDataSimulator
from api.trades import TradeRequest, buy_stock, sell_stock
from db.init_db import initialize_database
from db.init import get_db_session

async def run_strategy(simulator, db):
    # Start simulator and run quick strategy loop
    await simulator.start()
    try:
        for step in range(3):  # run 3 steps for demo
            await asyncio.sleep(1)
            prices = simulator.get_all_prices()
            # very small strategy: buy lowest price 1 share if cash available
            ticker, price = min(prices.items(), key=lambda x: x[1])

            # execute a buy on the cheapest stock and a sell on the most expensive
            buy_req = TradeRequest(ticker=ticker, quantity=1, price=price)
            sell_ticker, sell_price = max(prices.items(), key=lambda x: x[1])
            if sell_ticker != ticker:
                sell_req = TradeRequest(ticker=sell_ticker, quantity=1, price=sell_price)
            else:
                sell_req = None

            # Execute in sequence
            try:
                buy_result = await buy_stock(buy_req, db)
            except Exception as e:
                buy_result = {"error": str(e)}

            sell_result = None
            if sell_req:
                try:
                    sell_result = await sell_stock(sell_req, db)
                except Exception as e:
                    sell_result = {"error": str(e)}

            state = {
                "step": step + 1,
                "buy": {"ticker": ticker, "price": price, "result": buy_result},
                "sell": {"ticker": sell_ticker, "price": sell_price, "result": sell_result},
            }

            with open("../orchestrator_plan.json", "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)

            with open("../swarm_state.json", "w", encoding="utf-8") as f:
                json.dump({"step": step + 1, "price_snapshot": prices}, f, indent=2)

            await asyncio.sleep(0.5)

    finally:
        await simulator.stop()


if __name__ == "__main__":
    initialize_database()
    simulator = MarketDataSimulator(update_interval=0.1)
    db = get_db_session()
    print("🧠 Orchestrator started: Market -> Strategy -> Order")
    asyncio.run(run_strategy(simulator, db))
    print("✅ Orchestrator finished")
