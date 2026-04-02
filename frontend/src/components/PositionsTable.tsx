interface PositionsTableProps {
  positions: Array<{
    ticker: string;
    quantity: number;
    avg_cost: number;
    current_price: number;
    market_value: number;
    unrealized_pnl: number;
    unrealized_pnl_pct: number;
  }>;
  prices: Record<string, number>;
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
}

export default function PositionsTable({ positions, prices }: PositionsTableProps) {
  if (positions.length === 0) {
    return (
      <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
        <h2 className="text-lg font-bold text-white">Positions</h2>
        <p className="text-gray-400">No positions open.</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4 overflow-x-auto">
      <h2 className="text-lg font-bold text-white mb-4">Positions</h2>
      <table className="min-w-full divide-y divide-gray-700 text-sm">
        <thead>
          <tr className="text-left text-gray-300">
            <th className="px-3 py-2">Ticker</th>
            <th className="px-3 py-2">Qty</th>
            <th className="px-3 py-2">Avg Cost</th>
            <th className="px-3 py-2">Current Price</th>
            <th className="px-3 py-2">Value</th>
            <th className="px-3 py-2">P&L</th>
            <th className="px-3 py-2">P&L %</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {positions.map((pos) => {
            const changeClass = pos.unrealized_pnl >= 0 ? 'text-green-400' : 'text-red-400';
            const currentPrice = prices[pos.ticker] ?? pos.current_price;

            return (
              <tr key={pos.ticker} className="hover:bg-gray-700">
                <td className="px-3 py-2">{pos.ticker}</td>
                <td className="px-3 py-2">{pos.quantity}</td>
                <td className="px-3 py-2">{formatCurrency(pos.avg_cost)}</td>
                <td className="px-3 py-2">{formatCurrency(currentPrice)}</td>
                <td className="px-3 py-2">{formatCurrency(pos.market_value)}</td>
                <td className={`px-3 py-2 ${changeClass}`}>{formatCurrency(pos.unrealized_pnl)}</td>
                <td className={`px-3 py-2 ${changeClass}`}>{pos.unrealized_pnl_pct.toFixed(2)}%</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}