from polygon import RESTClient
from dotenv import load_dotenv
import os

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
        self.client = RESTClient(api_key=os.getenv("POLYGON_IO_API_KEY"))

    # Get all crypto tickers
    def get_all_crypto_tickers(self):
        return self.client.list_tickers(market="crypto", active="true", order="desc", limit=100, sort="market")
    # Get ohlcv for a ticker
    def get_ohlcv(self, ticker: str, interval: str, from_date: str, to_date: str, limit: int = 100):
        timespan = INTERVAL_MAP[interval]
        interval_int = int(interval[:-1])
        return self.client.list_aggs(ticker, interval_int, timespan, from_date, to_date, limit=limit)

if __name__ == "__main__":
    client = PolygonIOClient()
    tickers = client.get_all_crypto_tickers()
    for agg in client.get_ohlcv('SUI', "15m", "2025-07-21", "2025-07-22"):
        print(agg)