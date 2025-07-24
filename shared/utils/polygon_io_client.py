from polygon import RESTClient
from dotenv import load_dotenv
import os
import requests
# Load environment variables
load_dotenv()

# Map of interval to timespan
INTERVAL_MAP = {
    "1m": "minute",
    "5m": "minute",
    "15m": "minute",
    "1h": "hour",
    "1d": "day"
}

# Initialize Polygon.io client
class PolygonIOClient:
    def __init__(self):
        self.api_key = os.getenv("POLYGON_IO_API_KEY")

    # Get all crypto tickers
    def get_all_crypto_tickers(self, limit: int = 100, sort: str = "market", order: str = "desc"):
        
        url = f"https://api.polygon.io/v3/reference/tickers?market=crypto&active=true&order={order}&limit={limit}&sort={sort}&apiKey={self.api_key}"
        
        try:    
            response = requests.get(url)
            response.raise_for_status()
            return response.json()["results"]
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tickers: {e}")
            return None

    # Get ohlcv for a ticker
    def get_ohlcv(self, ticker: str, interval: str, from_date: str, to_date: str, limit: int = 100, sort: str = "desc"):
        timespan = INTERVAL_MAP[interval]
        interval_int = int(interval[:-1])
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/X:{ticker}USD/range/"
            f"{interval_int}/{timespan}/{from_date}/{to_date}"
            f"?adjusted=true&sort={sort}&limit={limit}&apiKey={self.api_key}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()["results"]
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ohlcv: {e}")
            return None
    # Get EMA Indicators
    def get_ema_indicators(self, ticker: str, interval: str, from_date: str, to_date: str, limit: int = 100, sort: str = "desc"):
        timespan = INTERVAL_MAP[interval]
        interval_int = int(interval[:-1])
        url = (
            f"https://api.polygon.io/v1/indicators/ema/X:{ticker}USD"
            f"?timespan={timespan}"
            f"&series_type=close"
            f"&order={sort}"
            f"&limit={limit}"
            f"&from={from_date}"
            f"&to={to_date}"
            f"&apiKey={self.api_key}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("results").get("values")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ema indicators: {e}")
            return None
    # Get RSI Indicators
    def get_rsi_indicators(self, ticker: str, interval: str, from_date: str, to_date: str, limit: int = 100, sort: str = "desc"):
        timespan = INTERVAL_MAP[interval]
        interval_int = int(interval[:-1])
        url = (
            f"https://api.polygon.io/v1/indicators/rsi/X:{ticker}USD"
            f"?timespan={timespan}"
            f"&timeframe=day"
            f"&series_type=close"
            f"&order={sort}"
            f"&limit={limit}"
            f"&from={from_date}"
            f"&to={to_date}"
            f"&apiKey={self.api_key}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("results").get("values")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching rsi indicators: {e}")
            return None
    # Get MACD Indicators
    def get_macd_indicators(self, ticker: str, interval: str, from_date: str, to_date: str, limit: int = 100, sort: str = "desc"):
        timespan = INTERVAL_MAP[interval]
        interval_int = int(interval[:-1])
        url = (
            f"https://api.polygon.io/v1/indicators/macd/X:{ticker}USD"
            f"?timespan={timespan}"
            f"&short_window=12"
            f"&long_window=26"
            f"&signal_window=9"
            f"&series_type=close"
            f"&order={sort}"
            f"&limit={limit}"
            f"&from={from_date}"
            f"&to={to_date}"
            f"&apiKey={self.api_key}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("results").get("values")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching macd indicators: {e}")
            return None
    # Get Stochastic Indicators
    def get_sma_indicators(self, ticker: str, interval: str, from_date: str, to_date: str, limit: int = 100, sort: str = "desc"):
        timespan = INTERVAL_MAP[interval]
        interval_int = int(interval[:-1])
        url = (
            f"https://api.polygon.io/v1/indicators/sma/X:{ticker}USD"
            f"?timespan={timespan}"
            f"&timeframe=day"
            f"&series_type=close"
            f"&order={sort}"
            f"&limit={limit}"
            f"&from={from_date}"
            f"&to={to_date}"
            f"&apiKey={self.api_key}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("results").get("values")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sma indicators: {e}")
            return None

if __name__ == "__main__":
    client = PolygonIOClient()
    tickers = client.get_all_crypto_tickers()
    for ticker in tickers:
        print(ticker["ticker"])
    
    ohlcv = client.get_ohlcv("SUI", "15m", "2025-07-21", "2025-07-22")
    for ohlcv in ohlcv:
        print(ohlcv)
    
    ema_indicators = client.get_ema_indicators("SUI", "15m", "2025-07-21", "2025-07-22")
    for ema_indicator in ema_indicators:
        print(ema_indicator)
    
    rsi_indicators = client.get_rsi_indicators("SUI", "15m", "2025-07-21", "2025-07-22")
    for rsi_indicator in rsi_indicators:
        print(rsi_indicator)
    
    macd_indicators = client.get_macd_indicators("SUI", "15m", "2025-07-21", "2025-07-22")  
    for macd_indicator in macd_indicators:
        print(macd_indicator)
    
    sma_indicators = client.get_sma_indicators("SUI", "15m", "2025-07-21", "2025-07-22")
    for sma_indicator in sma_indicators:
        print(sma_indicator)