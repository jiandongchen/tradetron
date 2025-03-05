import os
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def sample_api_key():
    return "test_api_key"

@pytest.fixture
def sample_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    return start_date, end_date

@pytest.fixture
def sample_symbols():
    return ["AAPL", "MSFT", "TSLA"] 