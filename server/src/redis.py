from asyncio import sleep
from datetime import datetime, timezone
from json import loads
from typing import Any, Awaitable, Dict
from async_timeout import timeout
from pydantic import BaseModel
from redis.asyncio import Redis


class RedisMessage(BaseModel):
    timestamp: datetime
    channel: str
    data: dict

    class Config:
        orm_mode = True

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]):
        return cls(
            timestamp=datetime.now(timezone.utc),
            channel=raw.get("channel"),
            data=loads(raw.get("data")),
        )


async def create_subscription(redis: Redis, channel: str, canceller: Awaitable = None):
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    while True:
        try:
            if canceller and await canceller():
                break
            async with timeout(1):
                raw = await pubsub.get_message(ignore_subscribe_messages=True)
                if raw:
                    yield RedisMessage.from_raw(raw)
                    await sleep(0.01)
        except TimeoutError:
            pass
    await pubsub.close()
