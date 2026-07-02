# -*- encoding: utf-8 -*-

"""
SQLAlchemy ORM Models Package for User's Project Data
-----------------------------------------------------

Aggregates SQLAlchemy ORM model so that importing :mod:`app.models` populates
the shared :class:`~app.models.base.ORMBase` metadata in full. Alembic's (migration)
``target_metadata`` and the test harness both rely on this single import to see
all tables across every schema in the PostgreSQL database.
"""

from app.models.base import ORMBase, TimestampMixin
from app.models.identity import ClerkUserProfile, WebhookEvent

__all__ = [
    "ORMBase", "TimestampMixin",
    "ClerkUserProfile", "WebhookEvent"
]
