from asyncio import CancelledError, Task, sleep, TimeoutError, create_task
from typing import Callable, List
from async_timeout import timeout
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from fastapi import FastAPI
from starlette.requests import Request

from .settings import Settings

async def listener(pubsub: PubSub):
  while True:
    try:
      async with timeout(1):
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
          yield message
          await sleep(0.01)
    except TimeoutError:
      pass
    except CancelledError:
      break

async def loop(pubsub: PubSub):
  async for message in listener(pubsub):
    pass

class RedisContext:
  settings: Settings
  redis: Redis
  pubsub: PubSub
  __loop: List[Task] = []

  def __init__(self, settings: Settings):
    self.settings = settings

  def start(self):
    self.redis = Redis(host=self.settings.REDIS_HOST)
    self.pubsub = self.redis.pubsub()

  async def stop(self):
    for sub in self.__loop:
      sub.cancel()
    await self.redis.close()

  async def subscribe(self, channel: str, handler: Callable[[dict], None]):
    await self.pubsub.subscribe(**{channel: handler})
    self.__loop.append(create_task(loop(self.pubsub)))

def handler(message):
  print(message)

async def start_redis_context(app: FastAPI, settings: Settings):
  context = RedisContext(settings)
  context.start()
  await context.subscribe("default", handler)
  app.state.redis = context

async def stop_redis_context(app: FastAPI):
  redis: RedisContext = app.state.redis
  await redis.stop()

def get_redis_context(request: Request):
  redis: RedisContext = request.app.state.redis
  return redis
