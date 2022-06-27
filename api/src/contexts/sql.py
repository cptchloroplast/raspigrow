from databases import Database
from fastapi import FastAPI, Request
from sqlalchemy import MetaData, create_engine

from ..settings import Settings

metadata = MetaData()

from ..models.sensor import readings

class SqlContext:
  settings: Settings
  database: Database

  def __init__(self, settings: Settings):
    self.settings = settings

  def _init_database(self):
    engine = create_engine(self.settings.DATABASE_URL)
    metadata.create_all(engine) 

  def start(self):
    self.database = Database(url=self.settings.DATABASE_URL_ASYNC)
    if self.settings.DATABASE_INIT:
      self._init_database()

def start_sql_context(app: FastAPI, settings: Settings):
  context = SqlContext(settings)
  context.start()
  app.state.sql = context
  return context

async def get_sql_database(request: Request):
  sql: SqlContext = request.app.state.sql
  await sql.database.connect()
  try:
    yield sql.database
  finally:
    await sql.database.disconnect()