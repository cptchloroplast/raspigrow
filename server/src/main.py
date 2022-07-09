import logging
from .api.factory import create_app
from .settings import Settings


logging.basicConfig(level=logging.INFO)


settings = Settings()
app = create_app(settings)
