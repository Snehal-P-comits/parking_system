"""Passkey contracts to keep implementation framework-agnostic."""

from collections.abc import Callable
from typing import Protocol


class PasskeyGenerator(Protocol):
    # Generate a passkey string with requested length.
    def generate(self, length: int) -> str: ...


class PasskeyValidator(Protocol):
    # Validate generated/provided key shape.
    def validate_format(self, value: str, length: int) -> bool: ...


class PasskeyHashStrategy(Protocol):
    # Transform key before storage (plain, hash, encrypted, etc.).
    def transform(self, value: str) -> str: ...


PasskeyUniquenessChecker = Callable[[str], bool]
