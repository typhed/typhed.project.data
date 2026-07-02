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
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models import ORMBase

metadata : Union[MetaData, Sequence[MetaData], None] = ORMBase.metadata


class MigrationSettings(BaseSettings):
    """
    Minimal, migration-scoped settings that read only the database DSN.

    The Alembic environment must run in database-only contexts (for
    example continuous integration) where unrelated application secrets
    such as the Clerk signing secret are legitimately absent, so it
    deliberately avoids the full :class:`~app.core.config.ProjectSettings`
    model to stay decoupled from the request-time configuration.
    """

    model_config = SettingsConfigDict(
        env_file = ".env", case_sensitive = False, extra = "ignore"
    )

    database_url : str

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
        include_schemas = True, compare_type = True,
        compare_server_default = True
    )

    with context.begin_transaction():
        context.run_migrations()
    
    return


async def run_migrations_online() -> None:
    """
    Create the asynchronous engine, open a connection, and drive the
    migration run through ``connection.run_sync``.
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
    Emit the migration SQL without opening a live database connection,
    e.g. for generating a SQL script (``--sql``) instead of applying it.
    """

    context.configure(
        url = config.get_main_option("sqlalchemy.url"),
        target_metadata = metadata, include_schemas = True,
        compare_type = True, compare_server_default = True,
        literal_binds = True, dialect_opts = {"paramstyle" : "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

    return


config = context.config

# configure file name, get details, to patch url
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = MigrationSettings().database_url # type: ignore

# ! escape "%" so ConfigParser interpolation does not choke on the DSN
config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

# get the environment context, and run migrations in mode::
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
