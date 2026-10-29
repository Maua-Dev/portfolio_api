from src.shared.helpers.errors.base_error import BaseError


class JwtVerificationError(BaseError):
    def __init__(self, message: str):
        super().__init__(message)
