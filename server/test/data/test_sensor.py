from src.data.sensor import SensorData


async def test_persist_reading(database, reading):
    sensor = SensorData(database)
    result = await sensor.persist_reading(reading)
    assert result is not None
    assert type(result) is int
