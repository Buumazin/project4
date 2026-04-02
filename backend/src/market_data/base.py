"""
Abstract market data interface for FinAlly
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import time

class MarketDataProvider(ABC):
    """Abstract base class for market data providers"""

    @abstractmethod
    async def start(self) -> None:
        """Start the market data provider"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the market data provider"""
        pass

    @abstractmethod
    def get_price(self, ticker: str) -> Optional[float]:
        """Get current price for a ticker"""
        pass

    @abstractmethod
    def get_all_prices(self) -> Dict[str, float]:
        """Get current prices for all tickers"""
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """Check if provider is running"""
        pass

    @abstractmethod
    def get_timestamp(self) -> float:
        """Get current timestamp"""
        pass