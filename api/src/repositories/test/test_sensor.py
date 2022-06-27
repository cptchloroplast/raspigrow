from datetime import datetime
import pytest
from unittest.mock import AsyncMock

from ...models.sensor import SensorReading
from .. import sensor

pytestmark = pytest.mark.anyio

async def test_create():
  reading = SensorReading(
    timestamp=datetime.utcnow(),
    temperature=10,
    humidity=19.1
  )
  db = AsyncMock()
  db.execute.return_value = 123
  result = await sensor.create(db, reading)
  db.execute.assert_called_once()
  assert result.id == 123