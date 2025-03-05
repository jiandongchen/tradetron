from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class OHLCV(BaseModel):
    """Open, High, Low, Close, Volume data"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    vwap: Optional[float] = None  # Volume Weighted Average Price
    transactions: Optional[int] = None

class StockTicker(BaseModel):
    """Stock ticker information"""
    ticker: str
    name: str
    market: str
    locale: str
    primary_exchange: str
    type: str
    active: bool
    currency_name: str
    cik: Optional[str] = None
    composite_figi: Optional[str] = None
    share_class_figi: Optional[str] = None
    last_updated_utc: Optional[str] = None

    @property
    def symbol(self) -> str:
        return self.ticker

    @property
    def currency(self) -> str:
        return self.currency_name

class AggregateData(BaseModel):
    """Aggregated stock data"""
    symbol: str
    data: List[OHLCV]
    adjusted: bool = False  # Whether the prices are adjusted for splits
    
    class Config:
        arbitrary_types_allowed = True 