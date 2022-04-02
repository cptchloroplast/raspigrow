from fastapi import FastAPI
from fastapi_plugins import redis_plugin

from .settings import Settings
from .routers.stream import router

app = FastAPI()
app.include_router(router)

settings = Settings()

@app.on_event("startup")
async def on_startup() -> None:
    await redis_plugin.init_app(app, config=settings)
    await redis_plugin.init()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await redis_plugin.terminate()
