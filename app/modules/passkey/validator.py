"""Passkey format validators."""

from app.modules.passkey.interfaces import PasskeyValidator


class NumericPasskeyValidator(PasskeyValidator):
    def validate_format(self, value: str, length: int) -> bool:
        # Current policy: numeric-only and exact length.
        return value.isdigit() and len(value) == length
