from datetime import datetime, timedelta
import pandas as pd
from tradetron.data.providers.polygon.client import PolygonClient
from tradetron.data.config import DataConfig

def main():
    # Initialize the client with API key from config
    config = DataConfig()
    client = PolygonClient(api_key=config.POLYGON_API_KEY)
    
    # Set up the symbol and date range
    symbol = "TSLA"
    end_date = datetime.now() - timedelta(days=1)  # Yesterday
    # Look back 10 days to ensure we get at least 5 trading days
    start_date = end_date - timedelta(days=10)
    
    print(f"\nGetting ticker details for {symbol}...")
    ticker = client.get_ticker_details(symbol)
    
    print(f"\nTicker info:")
    print(f"Name: {ticker.name}")
    print(f"Symbol: {ticker.symbol}")
    print(f"Market: {ticker.market}")
    print(f"Primary Exchange: {ticker.primary_exchange}")
    
    print(f"\nGetting trading data for {symbol} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    try:
        agg_data = client.get_daily_bars(symbol, start_date, end_date)
        
        # Convert to DataFrame for better display
        df = pd.DataFrame([{
            'date': bar.timestamp.strftime('%Y-%m-%d'),
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
            'vwap': bar.vwap if bar.vwap else 0
        } for bar in agg_data.data])
        
        if df.empty:
            print("\nNo trading data available for the specified date range.")
            return
        
        # Sort by date and get the last 5 trading days
        df = df.sort_values('date').tail(5)
        
        print("\nDaily trading data (last 5 trading days):")
        print(df.to_string(index=False))
        
        print("\nSummary statistics:")
        print(f"Latest close: ${df['close'].iloc[-1]:.2f}")
        print(f"5-day high: ${df['high'].max():.2f}")
        print(f"5-day low: ${df['low'].min():.2f}")
        print(f"Average volume: {df['volume'].mean():,.0f}")
        
    except Exception as e:
        print(f"\nError fetching trading data: {str(e)}")

if __name__ == "__main__":
    main() 