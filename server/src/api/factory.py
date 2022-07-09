from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .contexts.sensor import start_sensor_context
from .contexts.redis import start_redis_context, stop_redis_context
from .contexts.data import DataContext
from ..settings import Settings
from .routes.v1 import sensor


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.OPENAPI_TITLE,
        description=settings.OPENAPI_DESCRIPTION,
        version=settings.OPENAPI_VERSION,
        contact={
            "name": settings.OPENAPI_CONTACT_NAME,
            "url": settings.OPENAPI_CONTACT_URL,
            "email": settings.OPENAPI_CONTACT_EMAIL,
        },
        license_info={
            "name": settings.OPENAPI_LICENSE_NAME,
            "url": settings.OPENAPI_LICENSE_URL,
        },
        docs_url=None,
        redoc_url="/docs",
    )
    app.include_router(sensor.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup():
        data = await DataContext.initialize(app, settings)
        redis = start_redis_context(app, settings)
        start_sensor_context(app, data, redis)

    @app.on_event("shutdown")
    async def on_shutdown():
        await DataContext.dispose(app)
        await stop_redis_context(app)

    return app
