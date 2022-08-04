from typing import Awaitable
import logging

from src.mqtt import ClientFactory, Message
from src.settings import Settings
from src.api.contexts.base import BaseContext

logger = logging.getLogger(__name__)


class StreamContext(BaseContext):
    key = "stream"
    topic = "grow/v1/sensor"
    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    async def start(self):
        pass

    async def stop(self):
        pass

    async def subscribe(self):
        async with ClientFactory.create(self.settings) as client:
            async with client.unfiltered_messages() as messages:
                await client.subscribe(self.topic)
                async for raw in messages:
                    message = Message.from_raw(raw)
                    yield message.json()
