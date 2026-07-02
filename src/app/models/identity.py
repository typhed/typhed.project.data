# -*- encoding: utf-8 -*-

"""
Identity Schema Models holds Clerk's Exclusive User ID
------------------------------------------------------

The ``identity`` schema holds the records owned exclusively by the Clerk
webhook: the shared :class:`ClerkUserProfile` table (the cross-project identity
anchor, keyed on the immutable Clerk user id) and the :class:`WebhookEvent` ledger
used for at-least-once delivery de-duplication.
"""

import datetime as dt

from typing import Optional
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ORMBase, TimestampMixin

class ClerkUserProfile(ORMBase, TimestampMixin):
    """
    The shared identity row for a Clerk User ID. Every  sub-project schema
    references :attr:`clerk_id` through a cross-schema foreign key, so
    this table is the single source of truth for user existence.
    """

    __tablename__ = "clerk_users_mw"
    __table_args__ = {"schema": "identity"}

    clerk_id : Mapped[str] = mapped_column(
        String(255), primary_key = True
    )

    email_id : Mapped[str] = mapped_column(
        String(320), index = True, unique = True, nullable = False
    )

    username : Mapped[str] = mapped_column(
        String(255), index = True, unique = True, nullable = False
    )

    first_name : Mapped[str] = mapped_column(
        String(255), nullable = False
    )

    last_name : Mapped[str] = mapped_column(
        String(255), nullable = False
    )

    full_name : Mapped[str] = mapped_column(
        String(512), nullable = False
    )

    synced_at : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), server_default = func.now(),
        onupdate = func.now(), nullable = False
    )


class WebhookEvent(ORMBase):
    """
    Svix guarantees at-least-once delivery, so the same event may arrive more
    than once (notably on retries). The unique :attr:`svix_id` lets the receiver
    detect and short-circuit duplicates. Append-only ledger of processed Svix
    message ids for idempotency.
    """

    __tablename__ = "webhook_events_tx"
    __table_args__ = {"schema": "identity"}

    svix_id : Mapped[str] = mapped_column(
        String(255), primary_key = True
    )

    event_type : Mapped[str] = mapped_column(
        String(128), index = True, nullable = False
    )

    clerk_object_id : Mapped[Optional[str]] = mapped_column(
        String(255), nullable = True, unique = True
    )

    received_at : Mapped[dt.datetime] = mapped_column(
        DateTime(timezone = True), server_default = func.now(),
        nullable = False
    )
