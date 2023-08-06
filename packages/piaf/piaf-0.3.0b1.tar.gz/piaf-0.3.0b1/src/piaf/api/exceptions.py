# coding: utf-8
"""All exceptions and errors that can occur in the WebAPI."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException


class BadRequestException(HTTPException):
    """Base exception for all client-related errors (4XX)."""

    def __init__(
        self, code: int = 400, detail: Any = None, headers: Dict[str, Any] | None = None
    ) -> None:
        """
        Create a new :class:`BadRequestException` instance.

        :param code: HTTP code, must be 4XX (default is 400)
        :param detail: optional detail about what happened
        :param headers: additional headers
        """
        super().__init__(code, detail, headers)


class InternalServerError(HTTPException):
    """Base exception for all server-related errors (5XX)."""

    def __init__(
        self, code: int = 500, detail: Any = None, headers: Dict[str, Any] | None = None
    ) -> None:
        """
        Create a new :class:`InternalServerError` instance.

        :param code: HTTP code, must be 5XX (default is 500)
        :param detail: optional detail about what happened
        :param headers: additional headers
        """
        super().__init__(500, detail, headers)
