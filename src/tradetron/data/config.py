from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class DataConfig:
    """Configuration for data providers"""
    
    def __init__(self):
        load_dotenv()
        self.POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
        if not self.POLYGON_API_KEY:
            raise ValueError("POLYGON_API_KEY environment variable is not set")
    
    # Polygon.io settings
    POLYGON_BASE_URL: str = "https://api.polygon.io"
    
    # Rate limiting settings (for free tier)
    POLYGON_RATE_LIMIT_PER_MINUTE: int = 5
    
    # Data storage settings
    DATA_CACHE_DIR: Path = Path(__file__).parent / 'storage' / 'cache'
    
    @classmethod
    def validate(cls) -> bool:
        """Validate the configuration"""
        if not cls.POLYGON_API_KEY:
            raise ValueError("POLYGON_API_KEY environment variable is not set")
        
        # Create cache directory if it doesn't exist
        cls.DATA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        return True 