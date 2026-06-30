# -*- encoding: utf-8 -*-

"""
Application Settings for TyPhed Project Data - Environment Driven
-----------------------------------------------------------------

Strongly-typed, environment-driven configuration built on ``pydantic-settings``.
Values are read from process environment variables first and fall back to a
local ``.env`` file. Required secrets (the database DSN and the Clerk signing
secret) have no defaults, so the process fails fast at startup when they are
missing rather than at first request.
"""

import functools

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ProjectSettings(BaseSettings):
    """
    Validate runtime confiuration for the webhook service, and get each attribute
    from the environment variable of the same name (caseinsensitive). Unknown
    variables are silently ignored so the service can coexists with an unrelated
    environment configuration in the host machine.

    :type  database_url: str
    :param database_url: Async PostgreSQL DSN. Must use the ``postgresql+asyncpg``
        driver; a synchronous driver would block the event loop.

    :type  clerk_webhook_signing_secret: str
    :param clerk_webhook_signing_secret: Svix signing secret from the Clerk
        Dashboard, used to verify inbound webhook signatures. Prefixed ``whsec_``.
    """

    model_config = SettingsConfigDict(
        env_file = ".env", case_sensitive = False, extra = "ignore"
    )

    database_url : str = Field(
        ..., description = "Asynchronous PostgreSQL DSN Driver"
    )

    clerk_webhook_signing_secret : str = Field(
        ..., description = "Clerk/Svix Webhook Signing Secret"
    )

    # SQLAlchemy Connection Pool Tunneling
    db_pool_size : int = Field(
        10, ge = 1, description = "DB Pool Size"
    )

    db_max_overflow : int = Field(
        20, ge = 20, description = "DB Maximum Overflow Limit"
    )

    db_pool_recyle : int = Field(
        1_800, ge = -1, description = "DB Pool Recycle Size"
    )

    # Runtime Environment Metadata
    log_level : str = Field("INFO", description = "Min. Log Level")
    environment : str = Field("development", description = "Env. Name")


    @property
    def is_production(self) -> bool:
        """
        Report whether the service is running in a production environment
        (True) else returns False.

        :rtype:   bool
        :returns: Returns ``True`` when the ``environment`` is the literal
            ``production`` else ``False``. Note: shorthand values like ``prod``
            is not supported and will always return ``False`` otherwise.
        """

        return self.environment.strip().lower() == "production"


@functools.lru_cache
def get_settings() -> "ProjectSettings":
    """
    Returns the process-wide :class:`ProjectSettings` singleton, which is
    cached so the ``.env`` file and environment are parsed exactly once. Tests that
    need to override configuration can call ``get_settings.cache_clear()`` after
    mutating the environment.
    """

    return ProjectSettings()
