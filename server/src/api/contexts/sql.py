from databases import Database
from fastapi import FastAPI, Request

from ...settings import Settings


class SqlContext:
    settings: Settings
    database: Database

    def __init__(self, settings: Settings):
        self.settings = settings

    async def start(self):
        self.database = Database(url=self.settings.DATABASE_URL_ASYNC)
        await self.database.connect()

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
