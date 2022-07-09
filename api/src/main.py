import logging
from .app import create_app
from .settings import Settings


logging.basicConfig(level=logging.INFO)


settings = Settings()
app = create_app(settings)
