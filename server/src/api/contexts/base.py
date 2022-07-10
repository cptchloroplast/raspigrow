from abc import ABC, abstractmethod
from fastapi import FastAPI, Request

from src.settings import Settings


class BaseContext(ABC):
    key: str

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @classmethod
    async def initialize(cls, app: FastAPI, settings: Settings):
        ctx = cls(settings)
        await ctx.start()
        setattr(app.state, cls.key, ctx)
        return ctx

    @classmethod
    async def dispose(cls, app: FastAPI):
        ctx: BaseContext = getattr(app.state, cls.key)
        await ctx.stop()

    @classmethod
    def depends(cls, request: Request):
        return getattr(request.app.state, cls.key)