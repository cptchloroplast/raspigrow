import asyncio
import async_timeout
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from fastapi import FastAPI
from starlette.requests import Request

from .settings import Settings

subscriptions = []

def start_redis(app: FastAPI, settings: Settings):
  redis = Redis(host=settings.REDIS_HOST)
  app.state.redis = redis

async def stop_redis(app: FastAPI):
  redis: Redis = app.state.redis
  await redis.close()

def get_redis(request: Request):
  redis: Redis = request.app.state.redis
  return redis

async def subscribe(channel: str, redis: Redis):
  pubsub = redis.pubsub()
  await pubsub.subscribe(channel)
  while True:
    try:
      async with async_timeout.timeout(1):
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
          print(message)
          yield {"event": "message", "data": message}
          await asyncio.sleep(0.01)
    except asyncio.TimeoutError:
      pass
