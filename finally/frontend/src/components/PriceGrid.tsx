interface PriceGridProps {
  prices: Record<string, number>;
}

const tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NFLX", "META", "NVDA", "JPM", "XOM"];

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
}

export default function PriceGrid({ prices }: PriceGridProps) {
  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
      <h2 className="text-lg font-bold text-white mb-4">Watchlist</h2>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {tickers.map((ticker) => {
          const price = prices[ticker] ?? 0;
          return (
            <div key={ticker} className="rounded-lg border border-gray-700 p-3 hover:border-blue-400">
              <div className="text-sm text-gray-300">{ticker}</div>
              <div className="text-xl font-bold">{formatCurrency(price)}</div>
              <div className="text-xs text-gray-400">+0.28% / +2.30</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}