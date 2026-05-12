"""Numeric passkey generation strategies."""

import secrets

from app.modules.passkey.interfaces import PasskeyGenerator


class NumericPasskeyGenerator(PasskeyGenerator):
    def generate(self, length: int) -> str:
        # Use `secrets` for cryptographically stronger randomness.
        return "".join(str(secrets.randbelow(10)) for _ in range(length))
