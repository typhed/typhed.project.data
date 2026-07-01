# -*- encoding: utf-8 -*-

"""
Asynchronous Database Engine & Session Lifecycle for the Project
----------------------------------------------------------------

Owns the single application-wide async SQLAlchemy engine and the session
factory built on top of it. The engine is created lazily and cached so that
importing this module has no side effects (modules that never touch the
database - for example the pure Pydantic validation schemas - can be imported
without a configured DSN).

The :func:`get_session` dependency yields one :class:`AsyncSession` per request
and guarantees it is closed afterwards. ``expire_on_commit`` is disabled so ORM
instances remain usable after ``commit`` without triggering an implicit
(awaitable) reload. Always dispose the engine on shutdown via
:func:`dispose_engine` so pooled connections are released cleanly.
"""

import functools
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

@functools.lru_cache
def get_engine() -> AsyncEngine:
    """
    Build (once) and return the application-wide async engine. Connection-pool
    parameters are taken from :class:`~app.core.config.Settings`.
    The ``pool_pre_ping`` is enabled so stale connections (for example after a
    database restart) are transparently recycled instead of surfacing as errors.

    :rtype:   sqlalchemy.ext.asyncio.AsyncEngine
    :returns: The cached async engine bound to the configured DSN. This is an
        application-wide session factory for all operations.
    """

    settings = get_settings()

    return create_async_engine(
        settings.database_url,
        pool_pre_ping = True, future = True,
        pool_size = settings.db_pool_size,
        max_overflow = settings.db_max_overflow,
        pool_recycle = settings.db_pool_recycle
    )


@functools.lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """
    Build (once) and return the async session factory. The function binds the
    application-wide session manager for an asynchronous operations.

    :rtype:   sqlalchemy.ext.asyncio.async_sessionmaker
    :returns: A session factory producing :class:`AsyncSession` instances with
        ``expire_on_commit`` disabled.
    """

    return async_sessionmaker(
        bind = get_engine(),
        class_ = AsyncSession,
        expire_on_commit = False,
        autoflush = False,
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    The session is opened on entry and closed on exit. Transaction control
    (``commit`` / ``rollback``) is left to the caller so a single request can
    span several repository operations atomically.

    :rtype:   typing.AsyncGenerator[AsyncSession, None]
    :returns: An async generator yielding exactly one session, this will handle
        all queries for the database across the running instance.
    """

    factory = get_sessionmaker()
    async with factory() as session:
        yield session


async def check_database_connection() -> bool:
    """
    Execute a trivial round-trip query to confirm database reachability. Used by
    the readiness probe to distinguish process/traffic status.

    :rtype:   bool
    :returns: ``True`` when a ``SELECT 1`` succeeds, else the module waits for
        the existing process to complete for another task load.

    :raises sqlalchemy.exc.SQLAlchemyError: Propagated when the database is
        unreachable so the caller can translate it into a 503 response.
    """

    factory = get_sessionmaker()

    async with factory() as session:
        await session.execute(text("SELECT 1"))

    return True


async def dispose_engine() -> None:
    """
    Dispose the cached engine and release every pooled connection. Invoked from
    the FastAPI lifespan shutdown hook.
    """

    if get_engine.cache_info().currsize:
        await get_engine().dispose()
