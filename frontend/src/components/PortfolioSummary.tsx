import { useMemo } from "react";

interface PortfolioSummaryProps {
  portfolio: {
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
  } | null;
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
}

export default function PortfolioSummary({ portfolio }: PortfolioSummaryProps) {
  const positionsCount = portfolio?.positions.length ?? 0;

  const totalPnl = useMemo(() => {
    if (!portfolio) return 0;
    return portfolio.positions.reduce((acc, pos) => acc + pos.unrealized_pnl, 0);
  }, [portfolio]);

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
      <h2 className="text-lg font-bold text-white mb-4">Portfolio Summary</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-900 p-3 rounded-lg">
          <div className="text-xs text-gray-400">Total Value</div>
          <div className="text-xl font-semibold">{formatCurrency(portfolio?.total_value || 0)}</div>
        </div>
        <div className="bg-gray-900 p-3 rounded-lg">
          <div className="text-xs text-gray-400">Cash</div>
          <div className="text-xl font-semibold text-green-400">{formatCurrency(portfolio?.cash_balance || 0)}</div>
        </div>
        <div className="bg-gray-900 p-3 rounded-lg">
          <div className="text-xs text-gray-400">Positions</div>
          <div className="text-xl font-semibold">{positionsCount}</div>
        </div>
        <div className="bg-gray-900 p-3 rounded-lg">
          <div className="text-xs text-gray-400">Unrealized P&L</div>
          <div className="text-xl font-semibold text-cyan-300">{formatCurrency(totalPnl)}</div>
        </div>
      </div>
    </div>
  );
}