from importlib import reload
from test.conftest import integration
from unittest.mock import AsyncMock, MagicMock
from src.settings import Settings


def create_worker(settings: Settings):
    from src import worker

    reload(worker)

    return worker.Worker(settings)


async def test_mocked_worker_v1_sensor_message():
    # TODO: implement this
    pass


async def test_mocked_worker_unknown_message():
    # TODO: implement this
    pass


@integration
def test_real_worker():
    # TODO: implement this
    pass
