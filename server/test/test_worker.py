from src.settings import Settings


def create_worker(settings: Settings):
    from src.worker import Worker

    return Worker(settings)


def test_mocked_worker(settings, mock_database, mock_redis):
    worker = create_worker(settings)


def test_real_worker(settings):
    worker = create_worker(settings)
