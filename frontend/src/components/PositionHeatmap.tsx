interface PositionHeatmapProps {
  positions: Array<{ ticker: string; market_value: number; unrealized_pnl_pct: number; }>;
}

export default function PositionHeatmap({ positions }: PositionHeatmapProps) {
  const sorted = [...positions].sort((a, b) => Math.abs(b.unrealized_pnl_pct) - Math.abs(a.unrealized_pnl_pct));

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
      <h2 className="text-lg font-semibold text-white mb-3">Position Heatmap</h2>
      <div className="grid grid-cols-2 gap-2">
        {sorted.map((pos) => {
          const color = pos.unrealized_pnl_pct >= 0 ? 'bg-green-500/20 border-green-400/40' : 'bg-red-500/20 border-red-400/40';
          return (
            <div key={pos.ticker} className={`rounded-md border p-2 ${color}`}>
              <div className="text-sm text-gray-300">{pos.ticker}</div>
              <div className="text-lg font-bold text-white">{pos.market_value.toFixed(2)}</div>
              <div className="text-xs text-gray-200">{pos.unrealized_pnl_pct.toFixed(2)}%</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
