import logging
import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from shared.utils import PolygonWebSocketClient

logging.basicConfig(level=logging.INFO)

def main():
    # Now run the WebSocket client (which creates its own event loop)
    client = PolygonWebSocketClient()
    client.get_all_crypto_tickers()
    
if __name__ == "__main__":
    main()
