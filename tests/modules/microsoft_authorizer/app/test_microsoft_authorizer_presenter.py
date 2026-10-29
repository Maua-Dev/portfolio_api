import json
import uuid

from src.modules.microsoft_authorizer.app import microsoft_authorizer_presenter as presenter_module
from src.modules.microsoft_authorizer.app.microsoft_authorizer_presenter import lambda_handler
from src.shared.helpers.errors.external_errors import JwtVerificationError


class _FakeJwtVerifier:
    def __init__(self, claims: dict | None = None, error: Exception | None = None):
        self.claims = claims or {}
        self.error = error

    def verify_and_decode(self, token: str) -> dict:
        if self.error is not None:
            raise self.error
        return self.claims


class Test_MicrosoftAuthorizerPresenter:

    def test_presenter_allows_valid_token(self):
        user_id = str(uuid.uuid4())
        presenter_module.usecase.jwt_verifier = _FakeJwtVerifier(
            claims={
                "sub": user_id,
                "mail": "21.00000-0@maua.br",
            }
        )

        response = lambda_handler(
            {
                "authorizationToken": "Bearer token-123",
                "methodArn": "arn:aws:execute-api:sa-east-1:123:api/GET/users",
            },
            None,
        )

        assert response["principalId"] == user_id
        assert response["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert json.loads(response["context"]["user"])["mail"] == "21.00000-0@maua.br"

    def test_presenter_denies_when_jwt_verify_fails(self):
        presenter_module.usecase.jwt_verifier = _FakeJwtVerifier(
            error=JwtVerificationError("invalid signature")
        )

        response = lambda_handler(
            {
                "authorizationToken": "Bearer token-123",
                "methodArn": "arn:aws:execute-api:sa-east-1:123:api/GET/users",
            },
            None,
        )

        assert response["policyDocument"]["Statement"][0]["Effect"] == "Deny"
        assert response["principalId"] == "user"
