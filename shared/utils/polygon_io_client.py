import asyncio
from .kafka_client import KafkaProducer
from polygon import RESTClient
from dotenv import load_dotenv
import os
import requests
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Market
from typing import List

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

class PolygonWebSocketClient:
    def __init__(self):
        self.api_key = os.getenv("POLYGON_WS_API_KEY")
        self.ws_client = WebSocketClient(market=Market.Crypto, api_key=self.api_key)

    def handle_msg(self, msgs: List[WebSocketMessage]):
        """Synchronous message handler for Polygon WebSocket"""
        for m in msgs:
            attrs = vars(m)
            keys_to_keep = ["pair", "open", "high", "low", "close", "volume", "vwap", "avg_trade_size"]
            filtered_msg = {k: attrs.get(k) for k in keys_to_keep if k in attrs and attrs.get(k) is not None}
            symbol = filtered_msg.get("pair")
            if symbol:
                # Schedule the async Kafka send in the event loop
                try:
                    loop = asyncio.get_running_loop()
                    task = loop.create_task(KafkaProducer.send("ohlcv.realtime", key=symbol, value=filtered_msg))
                    # Add error handling for the background task
                    task.add_done_callback(self._handle_kafka_task_result)
                except RuntimeError:
                    # If no event loop is running, print a warning
                    print(f"Warning: No event loop running, cannot send message for {symbol}")
    
    def _handle_kafka_task_result(self, task):
        """Handle the result of async Kafka send tasks"""
        try:
            task.result()  # This will raise an exception if the task failed
        except Exception as e:
            print(f"Error sending Kafka message: {e}")

    def get_all_crypto_tickers(self):
        self.ws_client.subscribe("XA.*")
        self.ws_client.run(self.handle_msg)
    
    def get_crypto_ticker_data(self, ticker: list[str]):
        for t in ticker:
            self.ws_client.subscribe(f"XA.{t}")
        self.ws_client.run(self.handle_msg)
    
    def get_all_level_2_data(self):
        self.ws_client.subscribe("XL2.*")
        self.ws_client.run(self.handle_msg)

if __name__ == "__main__":
    # client = PolygonIOClient()
    # tickers = client.get_all_crypto_tickers()
    # for ticker in tickers:
    #     print(ticker["ticker"])
    
    # ohlcv = client.get_ohlcv("SUI", "15m", "2025-07-21", "2025-07-22")
    # for ohlcv in ohlcv:
    #     print(ohlcv)
    
    # ema_indicators = client.get_ema_indicators("SUI", "15m", "2025-07-21", "2025-07-22")
    # for ema_indicator in ema_indicators:
    #     print(ema_indicator)
    
    # rsi_indicators = client.get_rsi_indicators("SUI", "15m", "2025-07-21", "2025-07-22")
    # for rsi_indicator in rsi_indicators:
    #     print(rsi_indicator)
    
    # macd_indicators = client.get_macd_indicators("SUI", "15m", "2025-07-21", "2025-07-22")  
    # for macd_indicator in macd_indicators:
    #     print(macd_indicator)
    
    # sma_indicators = client.get_sma_indicators("SUI", "15m", "2025-07-21", "2025-07-22")
    # for sma_indicator in sma_indicators:
    #     print(sma_indicator)
    
    ws_client = PolygonWebSocketClient()
    ws_client.get_all_crypto_tickers()