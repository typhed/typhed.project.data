# -*- encoding: utf-8 -*-

"""
Default JSON Formatter for Logging Configuration
------------------------------------------------

Formats all incoming message and redacts sensitive information from
the message string to be logged into file - project specific or to
throw data into terminal based on environment and terminal configuration.
"""

import json
import logging
import datetime as dt

from typing import Any, Dict

from app.logging.redaction import redacted_logstring

class JSONFormatter(logging.Formatter):
    """
    Render a :class:`logging.LogRecord` as a compact single-line JSON
    document. Standard fields (timestamp, level, logger, message) are
    always present; any structured context passed through ``extra=``
    is merged into the same object.
    """

    def format(self, record : logging.LogRecord) -> str:
        """
        Serialize and redacts sensitive information from ``record``
        object to a JSON string.

        :type  record: logging.LogRecord
        :param record: The record emitted by the logging framework, the
            value is normalized to ``str`` format.
        """

        payload : Dict[str, Any] = {
            "timestamp" : dt.datetime.fromtimestamp(
                record.created, tz = dt.timezone.utc
            ).isoformat(),

            "level" : record.levelname, "logger" : record.name,
            "message" : record.getMessage()
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        extras = redacted_logstring(record)
        payload.update(extras)

        return json.dumps(payload, default = str)
