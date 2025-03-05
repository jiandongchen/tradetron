from datetime import datetime, timedelta
import pandas as pd
from src.data.providers.polygon.client import PolygonClient
from src.data.config import DataConfig

def main():
    # Validate configuration
    DataConfig.validate()
    
    # Create client
    client = PolygonClient()
    
    # Test ticker details
    symbol = "AAPL"
    print(f"\nGetting ticker details for {symbol}...")
    ticker = client.get_ticker_details(symbol)
    print(f"Ticker info: {ticker.dict()}")
    
    # Test daily bars
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)  # Get last 5 days of data
    
    print(f"\nGetting daily bars for {symbol}...")
    agg_data = client.get_daily_bars(symbol, start_date, end_date)
    
    # Convert to pandas DataFrame for better visualization
    df = pd.DataFrame([bar.dict() for bar in agg_data.data])
    df.set_index('timestamp', inplace=True)
    print("\nDaily bars:")
    print(df)

if __name__ == "__main__":
    main() 