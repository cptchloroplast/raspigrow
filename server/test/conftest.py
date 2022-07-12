from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
import pytest
from random import randint

from src.database import DatabaseFactory
from src.settings import Settings
from src.models.sensor import SensorReading
from src.redis import RedisFactory


pytest.mark.usefixtures("anyio_backend")


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
async def database(settings: Settings, anyio_backend):
    db = DatabaseFactory.create(settings)
    await db.connect()
    yield db
    await db.disconnect()


@pytest.fixture
def mock_database():
    with patch("src.database.DatabaseFactory") as mock_factory:
        mock_database = MagicMock()
        mock_factory.create.return_value = mock_database
        yield mock_database
        mock_factory.create.assert_called_once()


@pytest.fixture
def redis(settings: Settings):
    return RedisFactory.create(settings)


@pytest.fixture
def mock_redis():
    with patch("src.redis.RedisFactory") as mock_factory:
        mock_redis = MagicMock()
        mock_factory.create.return_value = mock_redis
        yield mock_redis
        mock_factory.create.assert_called_once()


@pytest.fixture
def reading():
    return create_reading()


@pytest.fixture
def readings():
    return [
        create_reading(timestamp=datetime.now(timezone.utc) + timedelta(minutes=i))
        for i in range(0, 60)
    ]


def create_reading(
    timestamp=datetime.now(timezone.utc),
    temperature=randint(-10, 30),
    humidity=randint(0, 100),
):
    return SensorReading(
        timestamp=timestamp,
        channel="grow:test:v1",
        temperature=temperature,
        humidity=humidity,
    )
