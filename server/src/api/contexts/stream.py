from typing import Awaitable
from redis.asyncio import Redis
from fastapi import FastAPI
from starlette.requests import Request
import logging

from src.redis import create_subscription
from src.settings import Settings

logger = logging.getLogger(__name__)


class StreamContext:
    channel = "grow:v1:sensor"
    redis: Redis

    def __init__(self, settings: Settings):
        self.redis = Redis(host=settings.REDIS_HOSTNAME, decode_responses=True)

    async def start(self):
        pass

    async def stop(self):
        pass

    @classmethod
    async def initialize(cls, app: FastAPI, settings: Settings):
        ctx = cls(settings)
        await ctx.start()
        app.state.stream = ctx
        return ctx

    @staticmethod
    async def dispose(app: FastAPI):
        ctx: StreamContext = app.state.stream
        await ctx.stop()

    @staticmethod
    def depends(request: Request):
        return request.app.state.stream

    async def subscribe(self, canceller: Awaitable = None):
        async for message in create_subscription(self.redis, self.channel, canceller):
            yield message.json()
