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
        return value


class PasskeyService:
    def __init__(
        self,
        generator: PasskeyGenerator,
        validator: PasskeyValidator,
        hash_strategy: PasskeyHashStrategy | None = None,
        max_retries: int = 25,
    ) -> None:
        self.generator = generator
        self.validator = validator
        self.hash_strategy = hash_strategy or PlainTextPasskeyHashStrategy()
        self.max_retries = max_retries

    def generate_unique(
        self,
        length: int,
        uniqueness_checker: PasskeyUniquenessChecker,
    ) -> str:
        for _ in range(self.max_retries):
            value = self.generator.generate(length)
            if self.validator.validate_format(value, length) and uniqueness_checker(value):
                return value
        raise PasskeyGenerationFailedError("Unable to generate a unique passkey.")

    def validate_or_raise(self, raw_value: str, expected_length: int) -> None:
        if not self.validator.validate_format(raw_value, expected_length):
            raise InvalidPasskeyFormatError("Invalid passkey format.")

    def transform(self, raw_value: str) -> str:
        return self.hash_strategy.transform(raw_value)
