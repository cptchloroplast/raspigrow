from typing import List
from aioredis import Channel, Redis


async def subscribe(channel: str, redis: Redis):
    (channel_subscription,) = await redis.subscribe(channel=Channel(channel, False))
    while await channel_subscription.wait_message():
        yield {"event": "message", "data": await channel_subscription.get()}
