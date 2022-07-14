from importlib import reload
from test.conftest import integration
from unittest.mock import AsyncMock, MagicMock
from src.settings import Settings


def create_worker(settings: Settings):
    from src import worker

    reload(worker)

    return worker.Worker(settings)


async def test_mocked_worker_v1_sensor_message(
    settings,
    mock_database,
    mock_redis,
    mock_sensor_data,
    mock_subscription,
    v1_sensor_message,
):
    # arrage
    worker = create_worker(settings)
    channel = "*"
    mock_generator = MagicMock()
    mock_generator.__aiter__.return_value = [v1_sensor_message]
    mock_subscription.return_value = mock_generator
    mock_sensor_data.persist_reading = AsyncMock()
    # act
    await worker.start(channel)
    # assert
    mock_database.connect.assert_called_once()
    mock_subscription.assert_called_once_with(mock_redis, channel)
    mock_sensor_data.persist_reading.assert_called_once()
    mock_database.disconnect.assert_called_once()


async def test_mocked_worker_unknown_message(
    settings,
    mock_database,
    mock_redis,
    mock_sensor_data,
    mock_subscription,
    unknown_message,
    mock_logger,
):
    # arrage
    worker = create_worker(settings)
    channel = "*"
    mock_generator = MagicMock()
    mock_generator.__aiter__.return_value = [unknown_message]
    mock_subscription.return_value = mock_generator
    mock_sensor_data.persist_reading = AsyncMock()
    mock_logger.warning = MagicMock()
    # act
    await worker.start(channel)
    # assert
    mock_database.connect.assert_called_once()
    mock_subscription.assert_called_once_with(mock_redis, channel)
    mock_sensor_data.persist_reading.assert_not_called()
    # mock_logger.warning.assert_called_once()
    mock_database.disconnect.assert_called_once()


@integration
def test_real_worker(settings):
    pass
