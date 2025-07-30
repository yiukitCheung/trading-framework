

import asyncio
import logging
from shared.utils.kafka_client import KafkaProducer
from shared.utils.polygon_io_client import PolygonWebSocketClient

logging.basicConfig(level=logging.INFO)

def main():
    # Initialize Kafka producer in a separate event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(KafkaProducer.init())

    # Now run the WebSocket client (which creates its own event loop)
    client = PolygonWebSocketClient()
    client.get_all_crypto_tickers()

if __name__ == "__main__":
    main()