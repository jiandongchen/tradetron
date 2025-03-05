import os
import time
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import requests
from ratelimit import limits, sleep_and_retry

from ...config import DataConfig
from tradetron.data.models.stock_data import OHLCV, StockTicker, AggregateData

class PolygonClient:
    """Polygon.io API client with rate limiting for free tier"""
    
    BASE_URL = "https://api.polygon.io"
    CALLS_PER_MINUTE = 5
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })
    
    @sleep_and_retry
    @limits(calls=CALLS_PER_MINUTE, period=60)
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a rate-limited request to the Polygon API"""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_ticker_details(self, symbol: str) -> StockTicker:
        """Get details for a specific ticker"""
        endpoint = f"/v3/reference/tickers/{symbol}"
        response = self._make_request(endpoint)
        if response.get('status') != 'OK':
            raise Exception(f"Error fetching ticker details: {response.get('error')}")
        return StockTicker(**response['results'])
    
    def get_aggregates(
        self,
        symbol: str,
        from_date: datetime,
        to_date: datetime,
        multiplier: int = 1,
        timespan: str = "day",
        adjusted: bool = True,
    ) -> AggregateData:
        """Get aggregate bars for a ticker"""
        endpoint = f"/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date.strftime('%Y-%m-%d')}/{to_date.strftime('%Y-%m-%d')}"
        params = {"adjusted": str(adjusted).lower()}
        
        response = self._make_request(endpoint, params)
        if response.get('status') != 'OK' or 'results' not in response:
            raise Exception(f"Error fetching aggregates: {response.get('error', 'No results found')}")
        
        bars = []
        for bar in response['results']:
            bars.append(
                OHLCV(
                    open=bar['o'],
                    high=bar['h'],
                    low=bar['l'],
                    close=bar['c'],
                    volume=bar['v'],
                    vwap=bar.get('vw'),
                    timestamp=datetime.fromtimestamp(bar['t'] / 1000)
                )
            )
        
        return AggregateData(symbol=symbol, data=bars)
    
    def get_daily_bars(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        adjusted: bool = True
    ) -> AggregateData:
        """Get daily bars for a ticker"""
        return self.get_aggregates(
            symbol=symbol,
            from_date=start_date,
            to_date=end_date,
            multiplier=1,
            timespan="day",
            adjusted=adjusted
        ) 