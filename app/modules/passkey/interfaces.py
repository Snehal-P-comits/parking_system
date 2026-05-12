from collections.abc import Callable
from typing import Protocol


class PasskeyGenerator(Protocol):
    def generate(self, length: int) -> str: ...


class PasskeyValidator(Protocol):
    def validate_format(self, value: str, length: int) -> bool: ...


class PasskeyHashStrategy(Protocol):
    def transform(self, value: str) -> str: ...


PasskeyUniquenessChecker = Callable[[str], bool]
