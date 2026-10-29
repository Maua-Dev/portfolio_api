import json
from typing import Any, Optional

import boto3

from src.shared.infra.external.jwt.jwt_utils import (
    DEFAULT_SIGNING_ALGORITHM,
    b64url_encode,
)


class JwtKmsSigner:
    """Assina JWT com KMS (mesmo algoritmo usado no JwtKmsVerifier)."""

    def __init__(
        self,
        key_arn: str,
        kms_client: Optional[Any] = None,
        signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM,
    ):
        self.key_arn = key_arn
        self.kms_client = kms_client or boto3.client("kms")
        self.signing_algorithm = signing_algorithm

    def sign(self, payload: dict) -> str:
        if not self.key_arn:
            raise ValueError("JWT sign key ARN is required")

        header = {"alg": "RS256", "typ": "JWT"}
        segments = (
            f"{b64url_encode(json.dumps(header, separators=(',', ':')).encode())}"
            f".{b64url_encode(json.dumps(payload, separators=(',', ':')).encode())}"
        )
        resp = self.kms_client.sign(
            KeyId=self.key_arn,
            Message=segments.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm=self.signing_algorithm,
        )
        return f"{segments}.{b64url_encode(resp['Signature'])}"
