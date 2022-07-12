from typing import Awaitable
from redis.asyncio import Redis
import logging

from src.redis import create_subscription, RedisFactory
from src.settings import Settings
from src.api.contexts.base import BaseContext

logger = logging.getLogger(__name__)


class StreamContext(BaseContext):
    key = "stream"
    channel = "grow:v1:sensor"
    redis: Redis

    def __init__(self, settings: Settings):
        self.redis = RedisFactory.create(settings)

    async def start(self):
        pass

    async def stop(self):
        pass

    async def subscribe(self, canceller: Awaitable = None):
        async for message in create_subscription(self.redis, self.channel, canceller):
            yield message.json()
