import json
import uuid

from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import (
    MicrosoftAuthorizerUsecase,
)
from src.shared.helpers.errors.external_errors import JwtVerificationError


class _FakeJwtVerifier:
    def __init__(self, claims: dict | None = None, error: Exception | None = None):
        self.claims = claims or {}
        self.error = error
        self.last_token = None

    def verify_and_decode(self, token: str) -> dict:
        self.last_token = token
        if self.error is not None:
            raise self.error
        return self.claims


class Test_MicrosoftAuthorizerUsecase:

    def _usecase(self, claims: dict | None = None, error: Exception | None = None):
        return MicrosoftAuthorizerUsecase(
            jwt_verifier=_FakeJwtVerifier(claims=claims, error=error),
        )

    def test_allow_valid_signed_token(self):
        user_id = str(uuid.uuid4())
        usecase = self._usecase(
            claims={
                "sub": user_id,
                "mail": "21.00000-0@maua.br",
            }
        )

        policy = usecase(
            authorization_token="Bearer token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["principalId"] == user_id
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert json.loads(policy["context"]["user"]) == {
            "sub": user_id,
            "mail": "21.00000-0@maua.br",
        }

    def test_deny_non_maua_email(self):
        usecase = self._usecase(
            claims={
                "sub": str(uuid.uuid4()),
                "mail": "user@gmail.com",
            }
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_deny_invalid_uuid_sub(self):
        usecase = self._usecase(
            claims={
                "sub": "not-a-uuid",
                "mail": "21.00000-0@maua.br",
            }
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_deny_invalid_jwt_signature(self):
        usecase = self._usecase(error=JwtVerificationError("invalid signature"))

        policy = usecase(
            authorization_token="Bearer bad.token.here",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_strips_bearer_prefix_before_verify(self):
        verifier = _FakeJwtVerifier(
            claims={
                "sub": str(uuid.uuid4()),
                "mail": "21.00000-0@maua.br",
            }
        )
        usecase = MicrosoftAuthorizerUsecase(jwt_verifier=verifier)

        usecase(
            authorization_token="Bearer abc.def.ghi",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert verifier.last_token == "abc.def.ghi"
