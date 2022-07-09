from asyncio import run
from redis.asyncio import Redis

from src.redis import create_subscription
from src.settings import Settings


class Worker:
    channel = "grow:v1:sensor"
    settings: Settings
    redis: Redis

    def __init__(self, settings: Settings):
        self.settings = settings
        print(self.settings.REDIS_HOSTNAME)
        self.redis = Redis(host=self.settings.REDIS_HOSTNAME)


    async def start(self):
        async for message in create_subscription(self.redis, self.channel):
            print(message.json())
