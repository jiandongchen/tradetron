from datetime import datetime, timedelta
import pandas as pd
from tradetron.data.storage.data_manager import DataManager
from tradetron.data.processors.data_processor import DataProcessor
from tradetron.data.config import DataConfig
import numpy as np

def analyze_stock(symbol: str, lookback_days: int = 60):
    """Analyze a stock using our data management system"""
    
    # Initialize components
    config = DataConfig()
    data_manager = DataManager(config)
    data_processor = DataProcessor()
    
    # Set up date range
    end_date = datetime.now() - timedelta(days=1)  # Yesterday
    start_date = end_date - timedelta(days=lookback_days)
    
    print(f"\nAnalyzing {symbol} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Get ticker information
    ticker = data_manager.get_ticker_info(symbol)
    print(f"\nTicker Info:")
    print(f"Name: {ticker.name}")
    print(f"Market: {ticker.market}")
    print(f"Exchange: {ticker.primary_exchange}")
    
    # Fetch historical data
    print(f"\nFetching historical data...")
    df = data_manager.get_daily_data(symbol, start_date, end_date)
    
    # Validate data
    if not data_manager.validate_data(df):
        print("Error: Invalid or incomplete data")
        return
    
    print(f"\nData shape: {df.shape}")
    print("\nFirst few rows of raw data:")
    print(df.head().to_string())
    
    # Process data
    print("\nProcessing data with technical indicators and features...")
    processed_df = data_processor.process_data(df)
    
    # Display some key metrics
    print("\nKey Metrics (latest):")
    latest = processed_df.iloc[-1]
    print(f"Close: ${latest['close']:.2f}")
    print(f"RSI: {latest['rsi']:.2f}")
    print(f"MACD: {latest['macd']:.2f}")
    print(f"Volume Ratio: {latest['volume_ratio']:.2f}x average")
    
    # Technical Analysis Summary
    print("\nTechnical Analysis Summary:")
    
    # Trend Analysis
    trend = "Bullish" if latest['close'] > latest['sma'] else "Bearish"
    print(f"Trend (vs SMA): {trend}")
    
    # RSI Analysis
    rsi = latest['rsi']
    rsi_signal = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
    print(f"RSI Signal: {rsi_signal} ({rsi:.2f})")
    
    # MACD Analysis
    macd_signal = "Bullish" if latest['macd'] > latest['macd_signal'] else "Bearish"
    print(f"MACD Signal: {macd_signal}")
    
    # Bollinger Bands
    bb_position = (latest['close'] - latest['bb_low']) / (latest['bb_high'] - latest['bb_low'])
    bb_signal = "Oversold" if bb_position < 0.2 else "Overbought" if bb_position > 0.8 else "Neutral"
    print(f"Bollinger Band Position: {bb_signal} ({bb_position:.2%})")
    
    # Volume Analysis
    volume_signal = "High" if latest['volume_ratio'] > 1.5 else "Low" if latest['volume_ratio'] < 0.5 else "Normal"
    print(f"Volume: {volume_signal} ({latest['volume_ratio']:.2f}x average)")
    
    # Performance Metrics
    print("\nPerformance Metrics:")
    returns = processed_df['returns'].dropna()
    print(f"Average Daily Return: {returns.mean():.2%}")
    print(f"Daily Return Std Dev: {returns.std():.2%}")
    print(f"Sharpe Ratio (0% risk-free): {(returns.mean() / returns.std() * np.sqrt(252)):.2f}")
    
    return processed_df

def main():
    # Analyze some popular stocks
    symbols = ['AAPL', 'MSFT', 'TSLA']
    
    for symbol in symbols:
        try:
            analyze_stock(symbol)
        except Exception as e:
            print(f"\nError analyzing {symbol}: {str(e)}")

if __name__ == "__main__":
    main() 