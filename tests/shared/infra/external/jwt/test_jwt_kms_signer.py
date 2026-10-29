import base64
import json

from src.shared.infra.external.jwt.jwt_kms_signer import JwtKmsSigner


class _FakeKmsClient:
    def __init__(self):
        self.last_call = None

    def sign(self, **kwargs):
        self.last_call = kwargs
        return {"Signature": b"signed-bytes"}


class Test_JwtKmsSigner:
    def test_sign_builds_three_part_jwt(self):
        kms = _FakeKmsClient()
        signer = JwtKmsSigner(
            key_arn="arn:aws:kms:sa-east-1:123:key/abc",
            kms_client=kms,
        )

        token = signer.sign({"sub": "user-1", "mail": "a@maua.br"})
        parts = token.split(".")

        assert len(parts) == 3
        header = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
        assert header == {"alg": "RS256", "typ": "JWT"}
        assert payload["sub"] == "user-1"
        assert kms.last_call["KeyId"] == "arn:aws:kms:sa-east-1:123:key/abc"
        assert kms.last_call["SigningAlgorithm"] == "RSASSA_PKCS1_V1_5_SHA_256"
        assert kms.last_call["MessageType"] == "RAW"
