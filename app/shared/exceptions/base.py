class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str, code: str = "NOT_FOUND") -> None:
        super().__init__(message=message, code=code, status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str, code: str = "CONFLICT") -> None:
        super().__init__(message=message, code=code, status_code=409)


class ValidationError(AppError):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR") -> None:
        super().__init__(message=message, code=code, status_code=422)


class AuthenticationError(AppError):
    def __init__(self, message: str, code: str = "AUTHENTICATION_FAILED") -> None:
        super().__init__(message=message, code=code, status_code=401)
