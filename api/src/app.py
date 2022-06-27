from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .contexts.redis import start_redis_context, stop_redis_context
from .contexts.sql import start_sql_context, stop_sql_context
from .settings import Settings
from .routers import stream
from .services import sensor

def create_app(settings: Settings):
  app = FastAPI(title=settings.TITLE)
  app.include_router(stream.router)
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  @app.on_event("startup")
  async def on_startup():
    sql = await start_sql_context(app, settings)
    redis = start_redis_context(app, settings)
    sensor.log_reading(sql, redis)

  @app.on_event("shutdown")
  async def on_shutdown():
    await stop_sql_context(app)
    await stop_redis_context(app)
  
  return app