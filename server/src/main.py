import logging

from src.api.factory import create_app
from src.settings import Settings


logging.basicConfig(level=logging.INFO)


settings = Settings()
app = create_app(settings)
