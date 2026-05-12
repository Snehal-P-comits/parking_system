"""Passkey orchestration service.

Coordinates generation, validation, uniqueness checks, and storage transforms.
"""

from app.modules.passkey.exceptions import (
    InvalidPasskeyFormatError,
    PasskeyGenerationFailedError,
)
from app.modules.passkey.interfaces import (
    PasskeyGenerator,
    PasskeyHashStrategy,
    PasskeyUniquenessChecker,
    PasskeyValidator,
)


class PlainTextPasskeyHashStrategy(PasskeyHashStrategy):
    def transform(self, value: str) -> str:
        # Default no-op strategy; can be swapped with hash/encryption later.
        return value


class PasskeyService:
    def __init__(
        self,
        generator: PasskeyGenerator,
        validator: PasskeyValidator,
        hash_strategy: PasskeyHashStrategy | None = None,
        max_retries: int = 25,
    ) -> None:
        # Dependencies are injected to keep service reusable and testable.
        self.generator = generator
        self.validator = validator
        self.hash_strategy = hash_strategy or PlainTextPasskeyHashStrategy()
        self.max_retries = max_retries

    def generate_unique(
        self,
        length: int,
        uniqueness_checker: PasskeyUniquenessChecker,
    ) -> str:
        # Retry generation until both format and uniqueness constraints pass.
        for _ in range(self.max_retries):
            value = self.generator.generate(length)
            if self.validator.validate_format(value, length) and uniqueness_checker(value):
                return value
        raise PasskeyGenerationFailedError("Unable to generate a unique passkey.")

    def validate_or_raise(self, raw_value: str, expected_length: int) -> None:
        # Raise domain-specific error so services can map to API ValidationError.
        if not self.validator.validate_format(raw_value, expected_length):
            raise InvalidPasskeyFormatError("Invalid passkey format.")

    def transform(self, raw_value: str) -> str:
        return self.hash_strategy.transform(raw_value)
