# -*- encoding: utf-8 -*-

"""
Application Exception Hierarchy and Handlers
--------------------------------------------

Defines the domain exceptions raised by the service layer together with
the FastAPI handlers that translate them into clean JSON responses.
Keeping the mapping in one place ensures error payloads stay consistent
and never leak internal details (stack traces, SQL, signature internals)
to clients. The module will always raise derived exception from below.
"""

from fastapi import status

class ApplicationError(Exception):
    """
    Base class for every expected, client-facing application errors. A
    custom error handler that throws HTTP error codes for easier
    debugging and data parsing in forward code integrations.
    """

    status_code : int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message : str) -> None:
        self.message = message
        super().__init__(message)


class UserNotFoundError(ApplicationError):
    """
    Raised when an operation targets a Clerk User ID that does not
    exists in the system. This raises a ``404`` not found error.
    """

    status_code : int = status.HTTP_404_NOT_FOUND


class WebhookSignatureError(ApplicationError):
    """
    Raised when an inbound webhook fails a ``Svix`` signature
    verification, and raises a ``401`` unauthorized error.
    """

    status_code : int = status.HTTP_401_UNAUTHORIZED
