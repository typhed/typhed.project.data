# -*- encoding: utf-8 -*-

"""
Exceptions & Warning Handlers - Dispatch Asynchronous Calls
-----------------------------------------------------------

Dispatch asynchronous calling to warnings and exception handlers for
the module which can register logging efficienctly without locking.
"""

import logging

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status

from app.errors.exceptions import ApplicationError

logger = logging.getLogger(__name__)

def register_exception(app : FastAPI) -> None:
    """
    Attach JSON exception handlers for the application error hierarchy,
    and asynchronously log information.
    """

    @app.exception_handler(ApplicationError)
    async def handle_app_error(_ : Request, exc : ApplicationError) -> JSONResponse:
        if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.error(
                "application error", extra = {"detail" : exc.message}
            )
        return JSONResponse(
            status_code = exc.status_code,
            content = {"detail" : exc.message}
        )
