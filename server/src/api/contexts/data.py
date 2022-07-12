from databases import Database

from src.database import DatabaseFactory
from src.api.contexts.base import BaseContext
from src.data.sensor import SensorData
from src.settings import Settings


class DataContext(BaseContext):
    key = "data"
    database: Database

    # Data
    sensor: SensorData

    def __init__(self, settings: Settings):
        self.database = DatabaseFactory.create(settings)
        self.sensor = SensorData(self.database)

    async def start(self):
        await self.database.connect()

    async def stop(self):
        await self.database.disconnect()
