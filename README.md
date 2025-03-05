# Tradetron

A Python package for algorithmic trading with robust data management and analysis capabilities.

## Features

- Data fetching from Polygon.io API
- Efficient data caching and storage
- OHLCV data processing
- Technical analysis indicators
- Market data validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tradetron.git
cd tradetron
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Project Structure

```
tradetron/
├── config/             # Configuration files
├── data/              # Data storage
│   ├── processed/     # Processed data files
│   └── raw/          # Raw data files
├── docs/              # Documentation
├── examples/          # Example scripts
├── src/               # Source code
│   └── tradetron/
│       └── data/     # Data management module
├── tests/             # Test files
└── notebooks/         # Jupyter notebooks
```

## Usage

```python
from tradetron.data.storage.data_manager import DataManager
from tradetron.data.config import DataConfig

# Initialize
config = DataConfig(POLYGON_API_KEY='your-api-key')
manager = DataManager(config)

# Fetch data
data = manager.get_daily_data('AAPL', start_date, end_date)
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Polygon.io](https://polygon.io/) for providing market data
- Contributors and maintainers
