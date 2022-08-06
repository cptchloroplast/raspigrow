from asyncio import sleep
from logging import getLogger
from databases import Database

from src.mqtt import ClientFactory, Message
from src.sql import DatabaseFactory
from src.settings import Settings
from src.data.sensor import SensorData
from src.models.sensor import SensorReading

logger = getLogger(__name__)


class Worker:
    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    async def start(self, topic: str):
        while True:
            try:
                await self.listen(topic)
            except Exception as ex:
                logger.error(ex)
            finally:
                await sleep(3)

    async def listen(self, topic: str):
        async with DatabaseFactory.create(self.settings) as database:
            async with ClientFactory.create(self.settings) as client:
                async with client.unfiltered_messages() as messages:
                    await client.subscribe(topic)
                    async for raw in messages:
                        message = Message.from_raw(raw)
                        logger.info(message.json())
                        await self.handle(database, message)

    async def handle(self, database: Database, message: Message):
        match message.topic:
            case "grow/v1/sensor":
                await SensorData(database).persist_reading(
                    SensorReading.from_message(message)
                )
            case _:
                logger.warning("Unknown topic %s", message.topic)
