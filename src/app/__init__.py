# -*- encoding: utf-8 -*-

"""
Extension of Clerk's User ID to Capture Project Data
====================================================

A production-grade FastAPI service that receives `Clerk Authentication
<https://clerk.com>`_ webhooks (delivered and signed via ``Svix``) and normalizes
the user identity into a multi-schema PostgreSQL database.

The shared ``identity.users`` table - keyed on the immutable Clerk User ID - is
the anchor that every sub-project schema (``demography``, ``profile``, ...)
references through a cross-schema foreign key. The webhook owns the identity
row; the per-sub-project APIs own their own enrichment tables.
"""

__version__ = "v0.0.1.dev0"
