import pytest
from datetime import datetime, timedelta
from tradetron.data.storage.data_manager import DataManager
from tradetron.data.config import DataConfig

def test_data_manager_initialization(sample_api_key):
    """Test DataManager initialization"""
    config = DataConfig(POLYGON_API_KEY=sample_api_key)
    manager = DataManager(config)
    assert manager.client is not None
    assert manager.cache_dir.exists()

def test_cache_path_generation(sample_api_key, sample_dates):
    """Test cache path generation"""
    config = DataConfig(POLYGON_API_KEY=sample_api_key)
    manager = DataManager(config)
    start_date, end_date = sample_dates
    
    cache_path = manager._get_cache_path("AAPL", start_date, end_date)
    assert cache_path.suffix == ".json"
    assert "AAPL" in cache_path.name
    assert start_date.strftime("%Y%m%d") in cache_path.name
    assert end_date.strftime("%Y%m%d") in cache_path.name 