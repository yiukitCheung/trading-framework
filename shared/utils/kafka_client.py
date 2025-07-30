from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
import logging
import os

# Get logger for this module
logger = logging.getLogger(__name__)

# Configure logging to see the messages (fallback if not configured elsewhere)
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

class KafkaProducer:
    _producer = None

    @classmethod
    async def init(cls):
        if cls._producer is None:
            cls._producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8')
            )
            await cls._producer.start()
            logger.info("KafkaProducer: Kafka producer started.")

    @classmethod
    async def send(cls, topic: str, key: str, value: dict):
        if cls._producer is None:
            await cls.init()
        try:
            await cls._producer.send_and_wait(topic, key=key, value=value)
            logger.info(f"KafkaProducer: Message sent to topic '{topic}' with key '{key}'")
            logger.debug(f"KafkaProducer: Message content: {value}")
        except Exception as e:
            logger.error(f"KafkaProducer: Failed to send Kafka message: {e}")

    @classmethod
    async def close(cls):
        if cls._producer is not None:
            await cls._producer.stop()
            logger.info("KafkaProducer: Kafka producer closed.")

class KafkaConsumer:
    def __init__(self, topic: str, group_id: str, message_handler, loop=None):
        self.topic = topic
        self.group_id = group_id
        self.message_handler = message_handler
        self.loop = loop or asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            loop=self.loop,
            auto_offset_reset="latest"
        )

    async def start(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                await self.message_handler(msg.key, msg.value)
        finally:
            await self.consumer.stop()
            
if __name__ == "__main__":
    # Test KafkaProducer
    # async def test_producer():
    #     await KafkaProducer.init()
    #     await KafkaProducer.send("test-topic", "test-key", {"message": "Hello, Kafka!"})
    #     await KafkaProducer.close()

    # asyncio.run(test_producer())
    
    # Test KafkaConsumer
    async def test_consumer():
        async def message_handler(key, value):
            print(f"KafkaConsumer: Received message: {value}")
        consumer = KafkaConsumer("ohlcv.realtime", "OGN-USD", message_handler)
        await consumer.start()
    asyncio.run(test_consumer())
    
    