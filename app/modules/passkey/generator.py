import secrets

from app.modules.passkey.interfaces import PasskeyGenerator


class NumericPasskeyGenerator(PasskeyGenerator):
    def generate(self, length: int) -> str:
        return "".join(str(secrets.randbelow(10)) for _ in range(length))
