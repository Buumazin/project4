import { Wifi, WifiOff } from "lucide-react";
import { useState, useEffect } from "react";

interface HeaderProps {
  portfolioValue: number;
  cashBalance: number;
  isConnected: boolean;
}

export default function Header({ portfolioValue, cashBalance, isConnected }: HeaderProps) {
  const [currentTime, setCurrentTime] = useState<string>('');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const updateTime = () => {
      setCurrentTime(new Date().toLocaleTimeString('en-US', { hour12: false }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  return (
    <header className="bg-gray-800 border-b border-gray-700 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-blue-400">FinAlly</h1>
          <div className="flex items-center space-x-2">
            {isConnected ? (
              <Wifi className="w-4 h-4 text-green-400" />
            ) : (
              <WifiOff className="w-4 h-4 text-red-400" />
            )}
            <span className={`text-sm ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-6">
          <div className="text-right">
            <div className="text-sm text-gray-400">Portfolio Value</div>
            <div className="text-lg font-semibold text-white">
              {formatCurrency(portfolioValue)}
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Cash Balance</div>
            <div className="text-lg font-semibold text-green-400">
              {formatCurrency(cashBalance)}
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Time</div>
            <div className="text-lg font-semibold text-white">
              {mounted ? currentTime : '--:--:--'}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}