interface PortfolioPnLProps {
  portfolio: {
    cash_balance: number;
    total_value: number;
    positions: Array<{ market_value: number; unrealized_pnl: number; }>;
  } | null;
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
}

export default function PortfolioPnL({ portfolio }: PortfolioPnLProps) {
  if (!portfolio) return null;

  const totalPnl = portfolio.positions.reduce((acc, pos) => acc + pos.unrealized_pnl, 0);
  const positionsValue = portfolio.positions.reduce((acc, pos) => acc + pos.market_value, 0);
  const pnlPct = positionsValue ? (totalPnl / positionsValue) * 100 : 0;

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
      <h2 className="text-lg font-bold text-white mb-3">Portfolio P&L</h2>
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-gray-900 p-3 rounded-lg">
          <div className="text-xs text-gray-400">Total P&L</div>
          <div className={`text-xl font-semibold ${totalPnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {formatCurrency(totalPnl)}
          </div>
        </div>
        <div className="bg-gray-900 p-3 rounded-lg">
          <div className="text-xs text-gray-400">P&L %</div>
          <div className={`text-xl font-semibold ${pnlPct >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {pnlPct.toFixed(2)}%
          </div>
        </div>
      </div>
    </div>
  );
}
