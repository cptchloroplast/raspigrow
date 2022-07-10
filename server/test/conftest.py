from datetime import datetime, timedelta, timezone
from databases import Database
import pytest
from random import randint

from src.settings import Settings
from src.models.sensor import SensorReading


pytest.mark.usefixtures("anyio_backend")


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
async def database(settings: Settings, anyio_backend):
    db = Database(settings.DATABASE_URL_ASYNC)
    await db.connect()
    yield db
    await db.disconnect()


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
