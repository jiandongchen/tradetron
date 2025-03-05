import pandas as pd
import numpy as np
from typing import List, Optional, Dict
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice

class DataProcessor:
    """Handles data preprocessing and feature engineering"""
    
    def __init__(self):
        self.required_columns = ['open', 'high', 'low', 'close', 'volume']
    
    def validate_columns(self, df: pd.DataFrame) -> bool:
        """Validate that DataFrame has required columns"""
        return all(col in df.columns for col in self.required_columns)
    
    def add_technical_indicators(
        self,
        df: pd.DataFrame,
        indicators: Optional[Dict[str, Dict]] = None
    ) -> pd.DataFrame:
        """
        Add technical indicators to the DataFrame
        
        Args:
            df: DataFrame with OHLCV data
            indicators: Dictionary of indicators to add with their parameters
                Example: {
                    'sma': {'window': 20},
                    'rsi': {'window': 14},
                    'bbands': {'window': 20, 'window_dev': 2},
                    'macd': {'window_slow': 26, 'window_fast': 12, 'window_sign': 9}
                }
        
        Returns:
            DataFrame with added technical indicators
        """
        if not self.validate_columns(df):
            raise ValueError("DataFrame missing required columns")
            
        # Default indicators if none specified
        if indicators is None:
            indicators = {
                'sma': {'window': 20},
                'ema': {'window': 20},
                'rsi': {'window': 14},
                'bbands': {'window': 20, 'window_dev': 2},
                'macd': {'window_slow': 26, 'window_fast': 12, 'window_sign': 9},
                'stoch': {'window': 14, 'smooth_window': 3},
                'vwap': {}
            }
        
        df = df.copy()
        
        # Add each indicator
        for indicator, params in indicators.items():
            if indicator == 'sma':
                sma = SMAIndicator(close=df['close'], **params)
                df['sma'] = sma.sma_indicator()
                
            elif indicator == 'ema':
                ema = EMAIndicator(close=df['close'], **params)
                df['ema'] = ema.ema_indicator()
                
            elif indicator == 'rsi':
                rsi = RSIIndicator(close=df['close'], **params)
                df['rsi'] = rsi.rsi()
                
            elif indicator == 'bbands':
                bb = BollingerBands(close=df['close'], **params)
                df['bb_high'] = bb.bollinger_hband()
                df['bb_mid'] = bb.bollinger_mavg()
                df['bb_low'] = bb.bollinger_lband()
                
            elif indicator == 'macd':
                macd = MACD(close=df['close'], **params)
                df['macd'] = macd.macd()
                df['macd_signal'] = macd.macd_signal()
                df['macd_diff'] = macd.macd_diff()
                
            elif indicator == 'stoch':
                stoch = StochasticOscillator(
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    **params
                )
                df['stoch_k'] = stoch.stoch()
                df['stoch_d'] = stoch.stoch_signal()
                
            elif indicator == 'vwap':
                vwap = VolumeWeightedAveragePrice(
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    volume=df['volume']
                )
                df['vwap'] = vwap.volume_weighted_average_price()
        
        return df
    
    def add_price_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add price-derived features"""
        df = df.copy()
        
        # Returns
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close']).diff()
        
        # Price changes
        df['price_change'] = df['close'] - df['open']
        df['price_change_pct'] = (df['close'] - df['open']) / df['open']
        
        # Volatility
        df['true_range'] = pd.DataFrame({
            'hl': df['high'] - df['low'],
            'hc': abs(df['high'] - df['close'].shift(1)),
            'lc': abs(df['low'] - df['close'].shift(1))
        }).max(axis=1)
        
        df['atr'] = df['true_range'].rolling(window=14).mean()
        
        # Volume features
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        return df
    
    def process_data(
        self,
        df: pd.DataFrame,
        add_indicators: bool = True,
        add_features: bool = True,
        indicators: Optional[Dict[str, Dict]] = None
    ) -> pd.DataFrame:
        """
        Process data by adding technical indicators and derived features
        
        Args:
            df: DataFrame with OHLCV data
            add_indicators: Whether to add technical indicators
            add_features: Whether to add derived features
            indicators: Dictionary of indicators to add with their parameters
        
        Returns:
            Processed DataFrame
        """
        if not self.validate_columns(df):
            raise ValueError("DataFrame missing required columns")
            
        processed_df = df.copy()
        
        if add_indicators:
            processed_df = self.add_technical_indicators(processed_df, indicators)
            
        if add_features:
            processed_df = self.add_price_derived_features(processed_df)
            
        # Drop rows with NaN values that result from calculations
        processed_df.dropna(inplace=True)
        
        return processed_df 