import asyncio
import time
import async_timeout
from redis.asyncio import Redis

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
