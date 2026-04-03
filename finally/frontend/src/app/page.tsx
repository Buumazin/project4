"use client";

import { useState, useEffect } from "react";
import Header from "@/components/Header";
import PriceGrid from "@/components/PriceGrid";
import PriceChart from "@/components/PriceChart";
import MainChart from "@/components/MainChart";
import PositionHeatmap from "@/components/PositionHeatmap";
import PortfolioPnL from "@/components/PortfolioPnL";
import PortfolioSummary from "@/components/PortfolioSummary";
import PositionsTable from "@/components/PositionsTable";
import ChatInterface from "@/components/ChatInterface";

interface PortfolioData {
  cash_balance: number;
  total_value: number;
  positions: Array<{
    ticker: string;
    quantity: number;
    avg_cost: number;
    current_price: number;
    market_value: number;
    unrealized_pnl: number;
    unrealized_pnl_pct: number;
  }>;
  total_positions_value: number;
}

interface PriceData {
  [ticker: string]: number;
}

export default function Dashboard() {
  const [portfolio, setPortfolio] = useState<PortfolioData | null>(null);
  const [prices, setPrices] = useState<PriceData>({});
  const [priceHistory, setPriceHistory] = useState<Record<string, number[]>>({});
  const [activeTicker, setActiveTicker] = useState("AAPL");
  const [isConnected, setIsConnected] = useState(false);

  const [tradeTicker, setTradeTicker] = useState("AAPL");
  const [tradeQuantity, setTradeQuantity] = useState(1);
  const [tradeMessage, setTradeMessage] = useState<string>("");
  const [isAutoTrading, setIsAutoTrading] = useState(false);
  const [agentStrategy, setAgentStrategy] = useState<'momentum' | 'meanReversion'>('momentum');
  const [tradeHistory, setTradeHistory] = useState<Array<any>>([]);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  const fetchPortfolio = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/portfolio/`);
      if (response.ok) {
        const data = await response.json();
        setPortfolio(data);
      } else {
        const errorText = await response.text();
        console.error("Portfolio fetch error", response.status, errorText);
        setTradeMessage(`Portfolio fetch failed: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to fetch portfolio:", error);
      setTradeMessage(`Failed to fetch portfolio: ${error}`);
    }
  };

  const fetchTradeHistory = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/trades/history?limit=20`);
      if (response.ok) {
        const data = await response.json();
        setTradeHistory(data.trades || []);
      } else {
        const errorText = await response.text();
        console.error("Trade history fetch error", response.status, errorText);
      }
    } catch (error) {
      console.error("Failed to fetch trade history:", error);
    }
  };

  useEffect(() => {
    fetchPortfolio();
    fetchTradeHistory();
    const interval = setInterval(() => {
      fetchPortfolio();
      fetchTradeHistory();
    }, 2000); // Update every 2 seconds
    return () => clearInterval(interval);
  }, [apiUrl]);

  const executeTrade = async (action: 'buy' | 'sell', ticker: string, quantity: number) => {
    try {
      const response = await fetch(`${apiUrl}/api/trades/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, quantity }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Trade failed');

      setTradeMessage(`${action.toUpperCase()} ${ticker} x${quantity} @ ${data.trade.price}`);
      setTradeHistory((prev) => [data.trade, ...prev].slice(0, 12));
      await fetchPortfolio();
      await fetchTradeHistory();
    } catch (error: any) {
      setTradeMessage(`Trade error: ${error.message}`);
    }
  };

  useEffect(() => {
    const streamUrl = `${apiUrl}/api/stream/prices`;
    const eventSource = new EventSource(streamUrl);

    eventSource.onopen = () => {
      console.log("SSE open", streamUrl);
      setIsConnected(true);
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setPrices(data.prices);
        setIsConnected(true);

        setPriceHistory((prev) => {
          const next: Record<string, number[]> = { ...prev };
          Object.entries(data.prices).forEach(([ticker, price]) => {
            const hist = next[ticker] ? [...next[ticker]] : [];
            hist.push(price as number);
            if (hist.length > 80) hist.shift();
            next[ticker] = hist;
          });
          return next;
        });
      } catch (error) {
        console.error("Failed to parse price data:", error, event.data);
      }
    };

    eventSource.onerror = (event) => {
      console.warn("SSE error", event, "readyState", eventSource.readyState);
      if (eventSource.readyState === EventSource.CLOSED) {
        setIsConnected(false);
      } else if (eventSource.readyState === EventSource.CONNECTING) {
        // Temporary reconnect state, keep as is
        return;
      }
    };

    return () => {
      eventSource.close();
    };
  }, [apiUrl]);

  useEffect(() => {
    if (!isAutoTrading) return;

    const runAgent = () => {
      const ticker = activeTicker;
      const current = prices[ticker] ?? 0;
      if (current <= 0) return;

      if (agentStrategy === 'momentum') {
        const hist = priceHistory[ticker] || [];
        if (hist.length < 5) return;
        const delta = hist[hist.length - 1] - hist[hist.length - 5];
        if (delta > 1) executeTrade('buy', ticker, 1);
        else if (delta < -1) executeTrade('sell', ticker, 1);
      } else {
        const hist = priceHistory[ticker] || [];
        if (hist.length < 10) return;
        const avg = hist.reduce((a, b) => a + b, 0) / hist.length;
        if (current < avg * 0.98) executeTrade('buy', ticker, 1);
        else if (current > avg * 1.02) executeTrade('sell', ticker, 1);
      }
    };

    const agentInterval = setInterval(runAgent, 2500);

    return () => clearInterval(agentInterval);
  }, [isAutoTrading, agentStrategy, activeTicker, priceHistory, prices]);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header
        portfolioValue={portfolio?.total_value || 0}
        cashBalance={portfolio?.cash_balance || 0}
        isConnected={isConnected}
      />

      <div className="container mx-auto px-4 py-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
            <h3 className="text-sm text-gray-300 mb-2">Trade Bar</h3>
            <div className="flex flex-wrap gap-2 items-end">
              <select
                className="bg-gray-900 border border-gray-600 px-2 py-1 rounded-md"
                value={tradeTicker}
                onChange={(e) => setTradeTicker(e.target.value)}
              >
                {['AAPL','GOOGL','MSFT','TSLA','AMZN','NFLX','META','NVDA','JPM','XOM'].map((symbol) => (
                  <option key={symbol} value={symbol}>{symbol}</option>
                ))}
              </select>
              <input
                type="number"
                min="1"
                value={tradeQuantity}
                onChange={(e) => setTradeQuantity(Number(e.target.value))}
                className="w-20 bg-gray-900 border border-gray-600 px-2 py-1 rounded-md"
              />
              <button
                className="rounded-md bg-green-500 px-3 py-1 text-sm font-semibold"
                onClick={() => executeTrade('buy', tradeTicker, tradeQuantity)}
              >
                Buy
              </button>
              <button
                className="rounded-md bg-red-500 px-3 py-1 text-sm font-semibold"
                onClick={() => executeTrade('sell', tradeTicker, tradeQuantity)}
              >
                Sell
              </button>
            </div>
            <div className="text-xs text-green-300 mt-2">{tradeMessage}</div>
          </div>

          <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
            <h3 className="text-sm text-gray-300 mb-2">Recent Trades</h3>
            {tradeHistory.length === 0 ? (
              <p className="text-gray-400 text-sm">No trades yet</p>
            ) : (
              <ul className="space-y-1 max-h-32 overflow-y-auto text-xs text-gray-200">
                {tradeHistory.map((t, idx) => (
                  <li key={`${t.ticker}-${idx}`} className="border-b border-gray-700 pb-1">
                    <span className="font-medium">{t.action.toUpperCase()}</span> {t.quantity} {t.ticker} @ {t.price}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>

      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <MainChart
              priceHistory={priceHistory}
              activeTicker={activeTicker}
              setActiveTicker={setActiveTicker}
            />
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <PriceGrid prices={prices} />
              <PortfolioPnL portfolio={portfolio} />
            </div>
          </div>

          <div className="space-y-6">
            <PositionHeatmap positions={portfolio?.positions || []} />
            <PortfolioSummary portfolio={portfolio} />
            <ChatInterface />
          </div>
        </div>

        <div className="mt-6">
          <PositionsTable positions={portfolio?.positions || []} prices={prices} />
        </div>
      </main>
    </div>
  );
}
