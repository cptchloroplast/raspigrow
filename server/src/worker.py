import logging
from databases import Database
from redis.asyncio import Redis

from src.models.sensor import SensorReading
from src.redis import create_subscription, RedisFactory
from src.database import DatabaseFactory
from src.settings import Settings
from src.data.sensor import SensorData

logger = logging.getLogger(__name__)


class Worker:
    redis: Redis
    database: Database
    sensor: SensorData

    def __init__(self, settings: Settings):
        self.redis = RedisFactory.create(settings)
        self.database = DatabaseFactory.create(settings)
        self.sensor = SensorData(self.database)

    async def start(self, channel: str):
        await self.database.connect()
        async for message in create_subscription(self.redis, channel):
            logger.info(message.json())
            if message.channel == "grow:v1:sensor":
                await self.sensor.persist_reading(SensorReading.from_message(message))
        await self.database.disconnect()
