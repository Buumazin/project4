interface PriceChartProps {
  prices: Record<string, number>;
}

const tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NFLX", "META", "NVDA", "JPM", "XOM"];

function getPathPoints(prices: Record<string, number>) {
  const values = tickers.map((ticker) => prices[ticker] ?? 0);
  const max = Math.max(1, ...values);
  const min = Math.min(...values);
  const range = max - min || 1;

  const width = 300;
  const height = 120;
  const step = width / (values.length - 1 || 1);

  return values
    .map((value, i) => {
      const x = step * i;
      // flip y because SVG origin is top-left
      const y = height - ((value - min) / range) * height;
      return `${x},${y}`;
    })
    .join(" ");
}

export default function PriceChart({ prices }: PriceChartProps) {
  const points = getPathPoints(prices);
  const values = tickers.map((ticker) => prices[ticker] ?? 0);

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-lg font-bold text-white">Price Trend</h2>
        <span className="text-xs text-gray-400">Updated live</span>
      </div>
      <svg viewBox="0 0 300 120" className="w-full h-32">
        <polyline
          fill="none"
          stroke="#60a5fa"
          strokeWidth="2"
          points={points}
        />
        <polyline
          fill="rgba(96, 165, 250, 0.2)"
          stroke="none"
          points={`${points} 300,120 0,120`}
        />
      </svg>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs text-gray-300 mt-2">
        {tickers.map((ticker, i) => (
          <div key={ticker} className="text-left">
            <div className="font-semibold text-white">{ticker}</div>
            <div>{values[i].toFixed(2)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
