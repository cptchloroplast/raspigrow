from redis.asyncio import Redis

from src.settings import Settings


class RedisFactory:
    @staticmethod
    def create(settings: Settings):
        return Redis(host=settings.REDIS_HOSTNAME, decode_responses=True)
