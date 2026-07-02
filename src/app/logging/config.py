# -*- encoding: utf-8 -*-

"""
Base Config to Handle Stream of Logging Data
--------------------------------------------

Handle logging stream data and redirect to the correct file/terminal
based on the incoming project name.
"""

import sys
import logging

from app.logging.formatter import JsonFormatter

def configure_logging(level : str = "INFO") -> None:
    """
    Install the JSON formatter on the root logger. Existing handlers
    are removed first so repeated calls (for example under an
    auto-reloading dev server) do not stack duplicate handlers.

    :type  level: str
    :param level: Minimum level name to emit, for example ``INFO``
        or ``DEBUG`` (check :mod:`logging` for more information).
    """

    handler = logging.StreamHandler(stream = sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())
