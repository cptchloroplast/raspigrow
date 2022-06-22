from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .redis import start_redis_context, stop_redis_context
from .settings import Settings
from .routers import stream

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
    context = await start_redis_context(app, settings)
    context.subscribe("default", lambda x: print(x))

  @app.on_event("shutdown")
  async def on_shutdown():
    await stop_redis_context(app)
  
  return app