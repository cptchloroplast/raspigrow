from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .contexts.sensor import start_sensor_context
from .contexts.redis import start_redis_context, stop_redis_context
from .contexts.sql import start_sql_context, stop_sql_context
from .settings import Settings
from .routers.v1 import root as v1


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
    app.include_router(v1.router)
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
        start_sensor_context(app, sql, redis)

    @app.on_event("shutdown")
    async def on_shutdown():
        await stop_sql_context(app)
        await stop_redis_context(app)

    return app
