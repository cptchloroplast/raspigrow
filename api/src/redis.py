from asyncio import CancelledError, Task, sleep, TimeoutError, create_task
from typing import Callable, List
from async_timeout import timeout
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from fastapi import FastAPI
from starlette.requests import Request

from .settings import Settings

class RedisContext:
  settings: Settings
  redis: Redis
  subscriptions: List[Task] = []

  def __init__(self, settings: Settings):
    self.settings = settings

  def start(self):
    self.redis = Redis(host=self.settings.REDIS_HOST)

  async def stop(self):
    for task in self.subscriptions:
      task.cancel()
    await self.redis.close()

  async def subscribe(self, channel: str, pubsub: PubSub = None, cancelled: Callable = None):
    if not pubsub:
      pubsub = self.redis.pubsub()
      await pubsub.subscribe(channel)
    while True:
      try:
        if cancelled and await cancelled():
          break
        async with timeout(1):
          message = await pubsub.get_message(ignore_subscribe_messages=True)
          if message:
            yield message
            await sleep(0.01)
      except TimeoutError:
        pass
      except CancelledError:
        break

  def add_subscription(self, channel: str, handler: Callable[[dict], None]):
    async def loop():
      pubsub = self.redis.pubsub()
      await pubsub.subscribe(**{channel: handler})
      async for message in self.subscribe(channel, pubsub):
        pass
    self.subscriptions.append(create_task(loop()))

async def start_redis_context(app: FastAPI, settings: Settings):
  context = RedisContext(settings)
  context.start()
  app.state.redis = context
  return context

async def stop_redis_context(app: FastAPI):
  redis: RedisContext = app.state.redis
  await redis.stop()

def get_redis_context(request: Request):
  redis: RedisContext = request.app.state.redis
  return redis
