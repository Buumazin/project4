interface MainChartProps {
  priceHistory: Record<string, number[]>;
  activeTicker: string;
  setActiveTicker: (ticker: string) => void;
}

const tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NFLX", "META", "NVDA", "JPM", "XOM"];

function formatLinePoints(values: number[], width: number, height: number): string {
  if (values.length === 0) return "";
  const max = Math.max(...values, 1);
  const min = Math.min(...values, 0);
  const span = max - min || 1;
  const step = width / (values.length - 1 || 1);

  return values
    .map((value, idx) => {
      const x = idx * step;
      const y = height - ((value - min) / span) * height;
      return `${x},${y}`;
    })
    .join(" ");
}

export default function MainChart({ priceHistory, activeTicker, setActiveTicker }: MainChartProps) {
  const values = priceHistory[activeTicker] || [];
  const points = formatLinePoints(values, 780, 220);
  const latest = values.length > 0 ? values[values.length - 1] : 0;

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-900 p-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl text-cyan-300 font-semibold">Main Chart - {activeTicker}</h2>
        <span className="text-sm text-gray-400">{latest.toFixed(2)}</span>
      </div>

      <div className="grid grid-cols-5 gap-2 mb-3">
        {tickers.map((ticker) => (
          <button
            key={ticker}
            onClick={() => setActiveTicker(ticker)}
            className={`rounded-md py-1 text-xs ${ticker === activeTicker ? 'bg-blue-500 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
          >
            {ticker}
          </button>
        ))}
      </div>

      <div className="w-full bg-gray-800 rounded-lg px-2 py-2">
        {values.length === 0 ? (
          <div className="text-gray-400 text-sm">Waiting for price updates...</div>
        ) : (
          <svg viewBox="0 0 780 220" className="w-full h-56">
            <polyline fill="none" stroke="#38bdf8" strokeWidth="2" points={points} />
          </svg>
        )}
      </div>
    </div>
  );
}
