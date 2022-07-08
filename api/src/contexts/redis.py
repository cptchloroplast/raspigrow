from asyncio import Task, sleep, TimeoutError, create_task
from datetime import datetime, timezone
from json import loads
from typing import Callable, Dict, List
from async_timeout import timeout
from pydantic import BaseModel
from redis.asyncio import Redis
from fastapi import FastAPI
from starlette.requests import Request
import logging


from ..settings import Settings

logger = logging.getLogger(__name__)


class RedisMessage(BaseModel):
    timestamp: datetime
    channel: str
    data: dict

    class Config:
        orm_mode = True


class RedisContext:
    settings: Settings
    redis: Redis
    subscriptions: List[Task] = []

    def __init__(self, settings: Settings):
        self.settings = settings

    def start(self):
        self.redis = Redis(host=self.settings.REDIS_HOSTNAME, decode_responses=True)

    async def stop(self):
        for task in self.subscriptions:
            task.cancel()
            try:
                await task
            except Exception as ex:
                logger.error(ex)  # TODO: handle these better...
        await self.redis.close()

    async def _create_subscription(self, channel: str, cancelled: Callable = None):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        while True:
            try:
                if cancelled and await cancelled():
                    break
                async with timeout(1):
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message:
                        yield self._process_message(message)
                        await sleep(0.01)
            except TimeoutError:
                pass

    def _process_message(self, message: Dict[str, any]):
        try:
            return RedisMessage(
                timestamp=datetime.now(timezone.utc),
                channel=message.get("channel"),
                data=loads(message.get("data")),
            )
        except Exception as ex:
            logger.error(ex)

    def subscribe(
        self,
        channel: str,
        handler: Callable[[dict], None] = None,
        cancelled: Callable = None,
    ):
        subscription = self._create_subscription(channel, cancelled)

        async def loop():
            async for message in subscription:
                if handler:
                    await handler(message)
                pass

        self.subscriptions.append(create_task(loop()))
        return subscription


def start_redis_context(app: FastAPI, settings: Settings):
    redis = RedisContext(settings)
    redis.start()
    app.state.redis = redis
    return redis


async def stop_redis_context(app: FastAPI):
    redis: RedisContext = app.state.redis
    await redis.stop()


def get_redis_context(request: Request):
    redis: RedisContext = request.app.state.redis
    return redis
