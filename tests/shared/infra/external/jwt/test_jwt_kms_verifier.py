import base64
import json
import time

import pytest
from botocore.exceptions import ClientError

from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.infra.external.jwt.jwt_kms_verifier import JwtKmsVerifier


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _make_token(payload: dict, signature: bytes = b"sig") -> str:
    header = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    body = _b64url(json.dumps(payload).encode())
    sig = _b64url(signature)
    return f"{header}.{body}.{sig}"


class _FakeKmsClient:
    def __init__(self, valid: bool = True, error: Exception | None = None):
        self.valid = valid
        self.error = error
        self.last_call = None

    def verify(self, **kwargs):
        self.last_call = kwargs
        if self.error is not None:
            raise self.error
        return {"SignatureValid": self.valid}


class Test_JwtKmsVerifier:
    def test_verify_and_decode_success(self):
        payload = {
            "sub": "af852f40-0135-406d-b5d7-7ed5dce9bc8e",
            "mail": "21.00000-0@maua.br",
            "name": "Soller",
            "exp": int(time.time()) + 3600,
        }
        token = _make_token(payload)
        kms = _FakeKmsClient(valid=True)
        verifier = JwtKmsVerifier(
            key_arn="arn:aws:kms:sa-east-1:123:key/abc",
            kms_client=kms,
        )

        claims = verifier.verify_and_decode(token)

        assert claims["sub"] == payload["sub"]
        assert claims["mail"] == payload["mail"]
        assert claims["name"] == payload["name"]
        assert kms.last_call["KeyId"] == "arn:aws:kms:sa-east-1:123:key/abc"
        assert kms.last_call["SigningAlgorithm"] == "RSASSA_PKCS1_V1_5_SHA_256"
        assert kms.last_call["MessageType"] == "RAW"

    def test_invalid_signature_raises(self):
        verifier = JwtKmsVerifier(
            key_arn="arn:aws:kms:sa-east-1:123:key/abc",
            kms_client=_FakeKmsClient(valid=False),
        )

        with pytest.raises(JwtVerificationError, match="not valid"):
            verifier.verify_and_decode(_make_token({"sub": "x"}))

    def test_kms_client_error_raises(self):
        error = ClientError(
            {"Error": {"Code": "SignatureDoesNotMatchException", "Message": "bad"}},
            "Verify",
        )
        verifier = JwtKmsVerifier(
            key_arn="arn:aws:kms:sa-east-1:123:key/abc",
            kms_client=_FakeKmsClient(error=error),
        )

        with pytest.raises(JwtVerificationError, match="verification failed"):
            verifier.verify_and_decode(_make_token({"sub": "x"}))

    def test_expired_token_raises(self):
        payload = {"sub": "x", "exp": int(time.time()) - 10}
        verifier = JwtKmsVerifier(
            key_arn="arn:aws:kms:sa-east-1:123:key/abc",
            kms_client=_FakeKmsClient(valid=True),
        )

        with pytest.raises(JwtVerificationError, match="expired"):
            verifier.verify_and_decode(_make_token(payload))

    def test_invalid_format_raises(self):
        verifier = JwtKmsVerifier(
            key_arn="arn:aws:kms:sa-east-1:123:key/abc",
            kms_client=_FakeKmsClient(valid=True),
        )

        with pytest.raises(JwtVerificationError, match="Invalid JWT format"):
            verifier.verify_and_decode("not-a-jwt")

    def test_missing_key_arn_raises(self):
        verifier = JwtKmsVerifier(
            key_arn="",
            kms_client=_FakeKmsClient(valid=True),
        )

        with pytest.raises(JwtVerificationError, match="JWT_SIGN_KEY_ARN"):
            verifier.verify_and_decode(_make_token({"sub": "x"}))
