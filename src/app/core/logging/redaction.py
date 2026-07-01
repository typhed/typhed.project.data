# -*- encoding: utf-8 -*-

"""
Logging Constants - Reserved & Sensitive Keyword Checks
-------------------------------------------------------

Logging does not automatically redacts sensitive information which is
a security concern. The logging parts are divided to seperate and
replace the sensitive parts with default asterix values.
"""

import logging

RESERVED_RECORD_KEYS = frozenset(vars(logging.makeLogRecord({})).keys())

# Any structured-context key whose name contains one of these substrings
# has its value redacted before it is serialized, so a secret accidentally
# passed via ``extra=`` never reaches the log stream.
SENSITIVE_KEY_PARTS = (
    "secret", "password", "passwd", "token", "authorization",
    "api_key", "apikey", "database_url", "dsn", "host", "hostname"
)


def is_sensitive(key : str) -> bool:
    """
    Reports whether the part of the logging content is sensitive, i.e.,
    the part is within ``SENSITIVE_KEY_PARTS`` with secret-bearing.
    """

    return any(part in key.lower() for part in SENSITIVE_KEY_PARTS)


def redacted_logstring(record : dict) -> dict:
    """
    Gracefully redacts the sensitive information from the logging
    message and returns a clean message with "***" inplace of secrets.
    """

    return {
        key : {"***" if is_sensitive(key) else value}
        for key, value in record.__dict__.items() if (
            key not in RESERVED_RECORD_KEYS and not key.startswith("_")
        )
    }
