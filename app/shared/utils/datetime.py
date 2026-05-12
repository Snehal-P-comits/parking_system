"""Date-time helpers used across services and models."""

from datetime import UTC, datetime


def utc_now() -> datetime:
    # Always return timezone-aware UTC values for consistent persistence.
    return datetime.now(UTC)
