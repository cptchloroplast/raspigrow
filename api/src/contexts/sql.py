from databases import Database
from fastapi import FastAPI, Request
from sqlalchemy import MetaData, create_engine

from ..settings import Settings

metadata = MetaData()


class SqlContext:
    settings: Settings
    database: Database

    def __init__(self, settings: Settings):
        self.settings = settings

    def _init_database(self):
        from ..models.sensor import readings

        engine = create_engine(self.settings.DATABASE_URL)
        metadata.create_all(engine)

    async def start(self):
        self.database = Database(url=self.settings.DATABASE_URL_ASYNC)
        await self.database.connect()
        if self.settings.DATABASE_INIT:
            self._init_database()

    async def stop(self):
        await self.database.disconnect()


async def start_sql_context(app: FastAPI, settings: Settings):
    sql = SqlContext(settings)
    await sql.start()
    app.state.sql = sql
    return sql


async def stop_sql_context(app: FastAPI):
    sql: SqlContext = app.state.sql
    await sql.stop()


async def get_sql_database(request: Request):
    sql: SqlContext = request.app.state.sql
    return sql.database
