from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context
from src.kernel.database.config import settings   
from src.kernel.models.baseModel import Base 

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = settings.DATABASE_URL_asyncpg
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(settings.DATABASE_URL_asyncpg, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(lambda conn: context.configure(connection=conn, target_metadata=target_metadata))

        async with connection.begin() as transaction:
            await connection.run_sync(context.run_migrations)

import asyncio
def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())

run_migrations()
