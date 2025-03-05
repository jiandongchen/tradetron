import os
from datetime import datetime, timedelta
import json
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List
from ..models.stock_data import OHLCV, StockTicker, AggregateData
from ..providers.polygon.client import PolygonClient
from ..config import DataConfig

class DataManager:
    """Manages data storage, caching, and retrieval"""
    
    def __init__(self, config: DataConfig):
        self.config = config
        self.client = PolygonClient(api_key=config.POLYGON_API_KEY)
        self.cache_dir = Path(config.DATA_CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, symbol: str, start_date: datetime, end_date: datetime) -> Path:
        """Generate a cache file path for the given parameters"""
        cache_key = f"{symbol}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json"
        return self.cache_dir / cache_key
    
    def _save_to_cache(self, data: AggregateData, cache_path: Path) -> None:
        """Save data to cache"""
        cache_data = {
            "symbol": data.symbol,
            "data": [bar.dict() for bar in data.data],
            "cached_at": datetime.now().isoformat()
        }
        cache_path.write_text(json.dumps(cache_data, default=str))
    
    def _load_from_cache(self, cache_path: Path) -> Optional[AggregateData]:
        """Load data from cache if available and not expired"""
        if not cache_path.exists():
            return None
            
        # Check if cache is expired (1 day for daily data)
        if cache_path.stat().st_mtime < (datetime.now() - timedelta(days=1)).timestamp():
            return None
            
        try:
            cache_data = json.loads(cache_path.read_text())
            bars = []
            for bar_data in cache_data["data"]:
                bar_data["timestamp"] = datetime.fromisoformat(bar_data["timestamp"])
                bars.append(OHLCV(**bar_data))
            return AggregateData(symbol=cache_data["symbol"], data=bars)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def get_daily_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Get daily OHLCV data for a symbol with caching
        
        Args:
            symbol: The stock symbol
            start_date: Start date for data
            end_date: End date for data
            use_cache: Whether to use cached data if available
            
        Returns:
            DataFrame with OHLCV data
        """
        cache_path = self._get_cache_path(symbol, start_date, end_date)
        
        # Try to load from cache first
        if use_cache:
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None:
                return self._convert_to_dataframe(cached_data)
        
        # Fetch from API if not in cache or cache disabled
        try:
            data = self.client.get_daily_bars(symbol, start_date, end_date)
            if use_cache:
                self._save_to_cache(data, cache_path)
            return self._convert_to_dataframe(data)
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def _convert_to_dataframe(self, data: AggregateData) -> pd.DataFrame:
        """Convert AggregateData to pandas DataFrame"""
        df = pd.DataFrame([{
            'date': bar.timestamp,
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
            'vwap': bar.vwap if bar.vwap else None
        } for bar in data.data])
        
        if not df.empty:
            df.set_index('date', inplace=True)
            df.sort_index(inplace=True)
        
        return df
    
    def get_ticker_info(self, symbol: str) -> StockTicker:
        """Get ticker information"""
        return self.client.get_ticker_details(symbol)
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate data quality
        
        Checks:
        - No missing values in critical columns
        - Prices are positive
        - Volume is non-negative
        - No duplicate indices
        """
        if df.empty:
            return False
            
        # Check for missing values in critical columns
        critical_columns = ['open', 'high', 'low', 'close', 'volume']
        if df[critical_columns].isnull().any().any():
            return False
            
        # Check price validity
        price_columns = ['open', 'high', 'low', 'close']
        if (df[price_columns] <= 0).any().any():
            return False
            
        # Check volume validity
        if (df['volume'] < 0).any():
            return False
            
        # Check for duplicate indices
        if df.index.duplicated().any():
            return False
            
        return True 