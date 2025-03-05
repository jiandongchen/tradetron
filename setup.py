from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tradetron",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional Python-based trading system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tradetron",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "python-dateutil>=2.8.2",
        "pytz>=2021.1",
        "requests>=2.26.0",
        "websockets>=10.0",
        "ccxt>=2.0.0",
        "yfinance>=0.1.63",
        "scipy>=1.7.0",
        "scikit-learn>=0.24.2",
        "ta>=0.7.0",
        "pyyaml>=5.4.1",
        "python-dotenv>=0.19.0",
        "loguru>=0.5.3",
        "pytest>=6.2.5",
        "pytest-cov>=2.12.0",
        "black>=21.6b0",
        "flake8>=3.9.0",
        "isort>=5.9.0",
        "jupyter>=1.0.0",
        "notebook>=6.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.0",
            "black>=21.6b0",
            "flake8>=3.9.0",
            "isort>=5.9.0",
        ],
    },
)
