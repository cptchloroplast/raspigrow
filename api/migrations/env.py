from logging.config import fileConfig
from sqlalchemy import create_engine, engine_from_config
from sqlalchemy import pool
from alembic import context

from src.settings import Settings
from src.contexts.sql import metadata
from src.models.sensor import sensor_readings

config = context.config
settings = Settings()
url = settings.DATABASE_URL

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    context.configure(
        url=url,
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
