import pytest

from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import EnvVarNotFound
from src.shared.infra.external.microsoft.id_token_verifier import MicrosoftIdTokenVerifier


class _FakeJwksClient:
    def __init__(self, key="fake-key", error: Exception | None = None):
        self.key = key
        self.error = error

    def get_signing_key_from_jwt(self, token: str):
        if self.error is not None:
            raise self.error

        class _Key:
            def __init__(self, key):
                self.key = key

        return _Key(self.key)


class Test_MicrosoftIdTokenVerifier:
    def test_missing_client_id_raises(self):
        with pytest.raises(EnvVarNotFound):
            MicrosoftIdTokenVerifier(client_id="", tenant_id="tenant")

    def test_missing_tenant_id_raises(self):
        with pytest.raises(EnvVarNotFound):
            MicrosoftIdTokenVerifier(client_id="client", tenant_id="")

    def test_verify_raises_jwt_verification_error_on_invalid_token(self, monkeypatch):
        import jwt as pyjwt

        verifier = MicrosoftIdTokenVerifier(
            client_id="client-id",
            tenant_id="tenant-id",
            jwks_client=_FakeJwksClient(),
        )

        def _boom(*args, **kwargs):
            raise pyjwt.InvalidTokenError("bad token")

        monkeypatch.setattr(pyjwt, "decode", _boom)

        with pytest.raises(JwtVerificationError, match="Invalid Microsoft id_token"):
            verifier.verify("header.payload.sig")
