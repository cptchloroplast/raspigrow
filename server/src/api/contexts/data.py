from databases import Database
from fastapi import FastAPI, Request

from src.api.contexts.base import BaseContext
from src.data.sensor import SensorData
from src.settings import Settings


class DataContext(BaseContext):
    key = "data"
    database: Database

    # Data
    sensor: SensorData

    def __init__(self, settings: Settings):
        self.database = Database(url=settings.DATABASE_URL_ASYNC)
        self.sensor = SensorData(self.database)

    async def start(self):
        await self.database.connect()

    async def stop(self):
        await self.database.disconnect()
