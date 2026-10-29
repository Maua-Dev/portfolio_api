import json
import uuid

from src.modules.microsoft_authorizer.app import microsoft_authorizer_presenter as presenter_module
from src.modules.microsoft_authorizer.app.microsoft_authorizer_presenter import lambda_handler
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
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

    def test_presenter_allows_existing_user(self):
        user_id = uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e")
        presenter_module.user_repo.users[0] = User(
            id=user_id,
            email="21.00000-0@maua.br",
            role=RoleEnum.USER,
        )
        presenter_module.usecase.jwt_verifier = _FakeJwtVerifier(
            claims={
                "sub": str(user_id),
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

        assert response["principalId"] == str(user_id)
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

    def test_presenter_allows_onboarding_route(self):
        new_id = str(uuid.uuid4())
        presenter_module.usecase.jwt_verifier = _FakeJwtVerifier(
            claims={
                "sub": new_id,
                "mail": "21.99999-9@maua.br",
            }
        )

        response = lambda_handler(
            {
                "authorizationToken": "token-123",
                "methodArn": "arn:aws:execute-api:sa-east-1:123:api/POST/auth",
            },
            None,
        )

        assert response["principalId"] == new_id
        assert response["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        assert json.loads(response["context"]["user"]) == {
            "sub": new_id,
            "mail": "21.99999-9@maua.br",
        }
