import base64
import re

_JWT_B64 = re.compile(r"^[A-Za-z0-9_-]+$")

# Algoritmo KMS alinhado com header JWT alg=RS256 (login + authorizer).
DEFAULT_SIGNING_ALGORITHM = "RSASSA_PKCS1_V1_5_SHA_256"


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def is_jwt_shape(token: str) -> bool:
    parts = token.split(".")
    if len(parts) != 3 or not all(parts):
        return False
    for part in parts:
        if not _JWT_B64.fullmatch(part):
            return False
        try:
            b64url_decode(part)
        except Exception:
            return False
    return True
