from databases import Database
from redis.asyncio import Redis

from src.models.sensor import SensorReading
from src.redis import create_subscription
from src.settings import Settings
from src.data.sensor import SensorData


class Worker:
    redis: Redis
    database: Database
    sensor: SensorData

    def __init__(self, settings: Settings):
        self.redis = Redis(host=settings.REDIS_HOSTNAME)
        self.database = Database(settings.DATABASE_URL_ASYNC)
        self.sensor = SensorData(self.database)

    async def start(self, channel: str):
        await self.database.connect()
        async for message in create_subscription(self.redis, channel):
            await self.sensor.persist_reading(SensorReading.from_message(message))
        await self.database.disconnect()
