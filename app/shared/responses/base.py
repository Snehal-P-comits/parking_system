"""Reusable API response builders."""

from typing import Any


def success_response(data: Any, message: str = "Success") -> dict[str, Any]:
    # Standard success envelope used by all routes.
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str, code: str) -> dict[str, Any]:
    # Standard error envelope used by global exception handlers.
    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
        },
    }
