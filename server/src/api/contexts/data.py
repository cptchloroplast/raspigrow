from databases import Database
from fastapi import FastAPI, Request

from ...data.sensor import SensorData
from ...settings import Settings


class DataContext:
    settings: Settings
    database: Database

    # Data
    sensor: SensorData

    def __init__(self, settings: Settings):
        self.settings = settings
        self.database = Database(url=self.settings.DATABASE_URL_ASYNC)
        self.sensor = SensorData(self.database)

    async def start(self):
        await self.database.connect()

    async def stop(self):
        await self.database.disconnect()

    @classmethod
    async def initialize(cls, app: FastAPI, settings: Settings):
        ctx = cls(settings)
        await ctx.start()
        app.state.data = ctx
        return ctx

    @staticmethod
    async def dispose(app: FastAPI):
        ctx: DataContext = app.state.data
        await ctx.stop()

    @staticmethod
    def depends(request: Request):
        return request.app.state.data
