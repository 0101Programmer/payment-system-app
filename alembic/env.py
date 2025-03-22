from logging.config import fileConfig
import asyncio
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

from app.database.connection import Base
from app.config import Config
from app.models.db_models import User, Account, Payment, Admin

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Настройка логирования
fileConfig(config.config_file_name)

# Определение URL базы данных
DATABASE_URL = Config.NO_DOCKER_DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Метаданные для миграций
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Run migrations in 'online' mode."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode asynchronously."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
