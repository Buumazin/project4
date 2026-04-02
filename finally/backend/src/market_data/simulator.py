"""
Market data simulator using Geometric Brownian Motion (GBM)
Generates realistic price movements for trading simulation
"""

import asyncio
import math
import random
import time
from typing import Dict, List, Optional
from .base import MarketDataProvider

class MarketDataSimulator(MarketDataProvider):
    """GBM-based market data simulator"""

    def __init__(self, update_interval: float = 0.5):
        self.update_interval = update_interval
        self.is_active = False
        self.task: Optional[asyncio.Task] = None
        self.start_time = time.time()

        # Default tickers with realistic seed prices
        self.default_tickers = {
            "AAPL": 180.0,
            "GOOGL": 140.0,
            "MSFT": 380.0,
            "TSLA": 220.0,
            "AMZN": 155.0,
            "NFLX": 480.0,
            "META": 330.0,
            "NVDA": 450.0,
            "JPM": 165.0,
            "XOM": 110.0
        }

        # Current prices
        self.prices: Dict[str, float] = {}
        self.volatilities: Dict[str, float] = {}
        self.drifts: Dict[str, float] = {}

        # Initialize with seed prices
        self._initialize_prices()

    def _initialize_prices(self):
        """Initialize prices and parameters for GBM simulation"""
        for ticker, seed_price in self.default_tickers.items():
            self.prices[ticker] = seed_price
            # Realistic volatilities (annualized, daily adjusted)
            self.volatilities[ticker] = random.uniform(0.15, 0.35) / math.sqrt(252)  # Daily vol
            # Small positive drift (annualized, daily adjusted)
            self.drifts[ticker] = random.uniform(0.02, 0.08) / 252  # Daily drift

    async def start(self) -> None:
        """Start the price simulation"""
        if self.is_active:
            return

        self.is_active = True
        self.task = asyncio.create_task(self._simulation_loop())
        print("📈 Market data simulator started")

    async def stop(self) -> None:
        """Stop the price simulation"""
        self.is_active = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        print("🛑 Market data simulator stopped")

    async def _simulation_loop(self):
        """Main simulation loop using GBM"""
        while self.is_active:
            try:
                # Update all prices using GBM
                dt = self.update_interval
                current_time = time.time()

                for ticker in list(self.prices.keys()):
                    if ticker not in self.volatilities:
                        continue

                    # GBM formula: dS = μS dt + σS dW
                    # Discrete approximation: S(t+dt) = S(t) * exp((μ - σ²/2)dt + σ√dt * Z)
                    # where Z ~ N(0,1)

                    S = self.prices[ticker]
                    mu = self.drifts[ticker]
                    sigma = self.volatilities[ticker]
                    Z = random.gauss(0, 1)  # Standard normal

                    # GBM step
                    drift_term = (mu - 0.5 * sigma**2) * dt
                    diffusion_term = sigma * math.sqrt(dt) * Z
                    growth_factor = math.exp(drift_term + diffusion_term)

                    # Update price
                    new_price = S * growth_factor

                    # Add some realistic bounds and mean reversion
                    # Prevent extreme movements
                    max_change_pct = 0.05  # Max 5% change per step
                    min_price = self.default_tickers.get(ticker, S) * 0.5   # Min 50% of seed
                    max_price = self.default_tickers.get(ticker, S) * 2.0   # Max 200% of seed

                    change_pct = (new_price - S) / S
                    if abs(change_pct) > max_change_pct:
                        new_price = S * (1 + max_change_pct * (1 if change_pct > 0 else -1))

                    new_price = max(min_price, min(max_price, new_price))

                    self.prices[ticker] = round(new_price, 2)

                await asyncio.sleep(dt)

            except Exception as e:
                print(f"Error in simulation loop: {e}")
                await asyncio.sleep(1.0)

    def get_price(self, ticker: str) -> Optional[float]:
        """Get current price for a ticker"""
        return self.prices.get(ticker.upper())

    def get_all_prices(self) -> Dict[str, float]:
        """Get current prices for all tickers"""
        return self.prices.copy()

    def is_running(self) -> bool:
        """Check if simulator is running"""
        return self.is_active

    def get_timestamp(self) -> float:
        """Get current timestamp"""
        return time.time()

    def add_ticker(self, ticker: str, seed_price: float):
        """Add a new ticker to simulation"""
        if ticker not in self.prices:
            self.prices[ticker] = seed_price
            self.volatilities[ticker] = random.uniform(0.15, 0.35) / math.sqrt(252)
            self.drifts[ticker] = random.uniform(0.02, 0.08) / 252
            print(f"📈 Added {ticker} to market simulation at ${seed_price}")

    def remove_ticker(self, ticker: str):
        """Remove a ticker from simulation"""
        ticker = ticker.upper()
        if ticker in self.prices:
            del self.prices[ticker]
            del self.volatilities[ticker]
            del self.drifts[ticker]
            print(f"📉 Removed {ticker} from market simulation")

# Global instance management
_simulator_instance = None

def get_market_simulator():
    """Get the global market simulator instance"""
    return _simulator_instance

def set_market_simulator(simulator):
    """Set the global market simulator instance"""
    global _simulator_instance
    _simulator_instance = simulator