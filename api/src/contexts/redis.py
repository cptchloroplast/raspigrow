from asyncio import CancelledError, Task, sleep, TimeoutError, create_task
from json import loads
from typing import Callable, Dict, List
from async_timeout import timeout
from redis.asyncio import Redis
from fastapi import FastAPI
from starlette.requests import Request

from ..settings import Settings

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
            self._process_message(message)
            yield message
            await sleep(0.01)
      except TimeoutError:
        pass
      except CancelledError:
        break

  def _process_message(self, message: Dict[str, any]):
    for key, value in message.items():
      if isinstance(value, bytes):
        decoded = value.decode("utf8")
        if key is "data":
          decoded = loads(decoded)
        message[key] =  decoded

  def subscribe(self, channel: str, handler: Callable[[dict], None] = None, cancelled: Callable = None):
    subscription = self._create_subscription(channel, cancelled)
    async def loop():
      async for message in subscription:
        if handler:
          handler(message)
        pass
    self.subscriptions.append(create_task(loop()))
    return subscription

def start_redis_context(app: FastAPI, settings: Settings):
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
