import asyncio
from redis.asyncio import Redis
from fastapi import FastAPI
from starlette.requests import Request

from .settings import Settings

def start(app: FastAPI, settings: Settings):
  redis = Redis(host=settings.REDIS_HOST)
  app.state.redis = redis

async def stop(app: FastAPI):
  redis: Redis = app.state.redis
  await redis.close()

def get(request: Request):
  redis: Redis = request.app.state.redis
  return redis