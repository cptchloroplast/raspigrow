from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from fastapi import FastAPI
from starlette.requests import Request
import logging

from ...settings import Settings

logger = logging.getLogger(__name__)


class StreamContext:
    settings: Settings
    pubsub: PubSub

    def __init__(self, settings: Settings):
        self.settings = settings
        redis = Redis(host=self.settings.REDIS_HOSTNAME, decode_responses=True)
        self.pubsub = redis.pubsub()

    async def start(self):
        pass

    async def stop(self):
        await self.pubsub.close()

    @classmethod
    async def initialize(cls, app: FastAPI, settings: Settings):
        ctx = cls(settings)
        app.state.stream = ctx
        return ctx

    @staticmethod
    async def dispose(app: FastAPI):
        ctx: StreamContext = app.state.stream
        await ctx.stop()

    @staticmethod
    def depends(request: Request):
        return request.app.state.stream
