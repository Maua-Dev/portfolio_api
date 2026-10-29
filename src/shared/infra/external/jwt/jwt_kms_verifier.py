import json
import time
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.infra.external.jwt.jwt_utils import (
    DEFAULT_SIGNING_ALGORITHM,
    b64url_decode,
)


class JwtKmsVerifier:
    """Verifica JWT assinado com KMS e devolve o payload decodificado."""

    def __init__(
        self,
        key_arn: str,
        kms_client: Optional[Any] = None,
        signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM,
    ):
        self.key_arn = key_arn
        self.kms_client = kms_client or boto3.client("kms")
        self.signing_algorithm = signing_algorithm

    def verify_and_decode(self, token: str) -> dict[str, Any]:
        if not self.key_arn:
            raise JwtVerificationError("JWT_SIGN_KEY_ARN is required")

        header_b64, payload_b64, signature_b64 = self._split_token(token)
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")

        try:
            signature = b64url_decode(signature_b64)
        except Exception as err:
            raise JwtVerificationError("Invalid JWT encoding") from err

        try:
            response = self.kms_client.verify(
                KeyId=self.key_arn,
                Message=signing_input,
                MessageType="RAW",
                Signature=signature,
                SigningAlgorithm=self.signing_algorithm,
            )
        except ClientError as err:
            raise JwtVerificationError(
                f"JWT signature verification failed: {err}"
            ) from err

        if not response.get("SignatureValid"):
            raise JwtVerificationError("JWT signature is not valid")

        try:
            payload = json.loads(b64url_decode(payload_b64))
        except (ValueError, json.JSONDecodeError) as err:
            raise JwtVerificationError("JWT payload is not valid JSON") from err

        if not isinstance(payload, dict):
            raise JwtVerificationError("JWT payload must be a JSON object")

        self._validate_exp(payload)
        return payload

    @staticmethod
    def _split_token(token: str) -> tuple[str, str, str]:
        parts = token.split(".")
        if len(parts) != 3 or not all(parts):
            raise JwtVerificationError("Invalid JWT format")
        return parts[0], parts[1], parts[2]

    @staticmethod
    def _validate_exp(payload: dict[str, Any]) -> None:
        exp = payload.get("exp")
        if exp is None:
            return
        try:
            exp_ts = int(exp)
        except (TypeError, ValueError) as err:
            raise JwtVerificationError("Invalid JWT exp claim") from err
        if exp_ts < int(time.time()):
            raise JwtVerificationError("JWT has expired")
