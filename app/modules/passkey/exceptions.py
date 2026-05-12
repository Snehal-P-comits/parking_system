class PasskeyError(Exception):
    pass


class InvalidPasskeyFormatError(PasskeyError):
    pass


class PasskeyGenerationFailedError(PasskeyError):
    pass
