from asyncio import run
import logging

from src.worker import Worker
from src.api.factory import create_app
from src.settings import Settings


logging.basicConfig(level=logging.INFO)

def create_api():
    settings = Settings()
    return create_app(settings)

if __name__ == "__main__":
    settings = Settings()
    worker = Worker(settings)
    run(worker.start())