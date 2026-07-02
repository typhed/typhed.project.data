# -*- encoding: utf-8 -*-

"""
Alembic Migration Environment (Asynchronous, Multi-Schema, SQLAlchemy)
----------------------------------------------------------------------

Runs migrations against the async engine using ``connection.run_sync``
so the synchronous Alembic machinery operates over an asyncpg connection.
The database URL is injected from application settings rather than
``alembic.ini`` to avoid duplicating the secret-bearing DSN, and
``include_schemas`` is enabled so the ``identity`` / ``demography`` /
``profile`` schemas participate in autogenerate.
"""

import asyncio

from typing import Sequence, Union
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, MetaData
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.models import ORMBase
from app.core.config import get_settings

metadata : Union[MetaData, Sequence[MetaData], None] = ORMBase.metadata

def run_migrations(connection : Connection) -> None:
    """
    Configure the migration context and run migration on a synchronized
    connection. Finally, return function based on the environment.

    :type  connection: sqlalchemy.engine.Connection
    :param connection: The synchronous connection provided by
        ``run_sync``. The operation can be invoked either by sync/async
        based on the environment details.
    """
    context.configure(
        connection = connection, target_metadata = metadata,
        include_schemas = True, compare_type = True
    )

    with context.begin_transaction():
        context.run_migrations()
    
    return


async def run_migrations_online() -> None:
    """
    Create the asynchronous engine and drive the migration run while
    the system is running - allowed only when there is not table lock
    in progress else may result in data loss.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix = "sqlalchemy.", poolclass = pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations)
    await connectable.dispose()

    return


def run_migrations_offline() -> None:
    """
    Emit the migration SQL scripts with a live database connection,
    best for database initialization and handles data safely.
    """

    context.configure(
        url = config.get_main_option("sqlalchemy.url"),
        literal_binds = True, dialect_opts = {"paramstyle" : "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

    return


if __name__ == "__main__":
    config = context.config

    # configure file name, get details, to patch url
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    config.set_main_option(
        "sqlalchemy.url", get_settings().database_url
    )

    # get the environment context, and run migrations in mode::
    run_migrations_offline() if context.is_offline_mode() \
        else asyncio.run(run_migrations_online())
