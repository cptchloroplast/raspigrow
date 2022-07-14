from os import environ
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from random import randint

from src.database import DatabaseFactory
from src.settings import Settings
from src.models.sensor import SensorReading
from src.redis import RedisFactory, RedisMessage


pytest.mark.usefixtures("anyio_backend")


integration = pytest.mark.skipif(
    "TEST_INTEGRATION" not in environ, reason="Skipping integration tests"
)


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
def mock_database(anyio_backend):
    with patch("src.database.DatabaseFactory") as mock_factory:
        mock_database = AsyncMock()
        mock_factory.create.return_value = mock_database
        yield mock_database
        mock_factory.create.assert_called_once()


@pytest.fixture
def redis(settings: Settings, anyio_backend):
    return RedisFactory.create(settings)


@pytest.fixture
def mock_redis(anyio_backend):
    with patch("src.redis.RedisFactory") as mock_factory:
        mock_redis = MagicMock()
        mock_factory.create.return_value = mock_redis
        mock_pubsub = AsyncMock()
        mock_redis.pubsub.return_value = mock_pubsub
        yield mock_redis
        mock_factory.create.assert_called_once()


@pytest.fixture
def mock_subscription():
    with patch("src.redis.create_subscription") as mock:
        yield mock


@pytest.fixture
def mock_sensor_data():
    with patch("src.data.sensor.SensorData", new=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_logger():
    with patch("logging.getLogger") as mock:
        yield mock


@pytest.fixture
def unknown_message():
    return create_message()


@pytest.fixture
def v1_sensor_message():
    return create_message(
        channel="grow:v1:sensor",
        data={"temperature": get_temperature(), "humidity": get_humidity()},
    )


@pytest.fixture
def reading():
    return create_reading()


@pytest.fixture
def readings():
    return [
        create_reading(timestamp=datetime.now(timezone.utc) + timedelta(minutes=i))
        for i in range(0, 60)
    ]


def get_temperature():
    return randint(-10, 30)


def get_humidity():
    return randint(0, 100)


def create_message(
    timestamp=datetime.now(timezone.utc), channel="grow:v1:test", data={"key": "value"}
):
    return RedisMessage(timestamp=timestamp, channel=channel, data=data)


def create_reading(
    timestamp=datetime.now(timezone.utc),
    channel="grow:test:v1",
    temperature=get_temperature(),
    humidity=get_humidity(),
):
    return SensorReading(
        timestamp=timestamp,
        channel=channel,
        temperature=temperature,
        humidity=humidity,
    )
