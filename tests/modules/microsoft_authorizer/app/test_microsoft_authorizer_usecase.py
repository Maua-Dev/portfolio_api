import json
import uuid

from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import (
    MicrosoftAuthorizerUsecase,
)
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


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

    def _usecase(self, claims: dict, repo: UserRepositoryMock | None = None):
        repo = repo or UserRepositoryMock()
        return MicrosoftAuthorizerUsecase(
            jwt_verifier=_FakeJwtVerifier(claims=claims),
            user_repo=repo,
        ), repo

    def test_allow_existing_user_on_protected_route(self):
        user_id = uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e")
        repo = UserRepositoryMock()
        repo.users[0] = User(
            id=user_id,
            email="21.00000-0@maua.br",
            role=RoleEnum.USER,
        )
        usecase, _ = self._usecase(
            {
                "sub": str(user_id),
                "mail": "21.00000-0@maua.br",
            },
            repo=repo,
        )

        policy = usecase(
            authorization_token="Bearer token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["principalId"] == str(user_id)
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        context_user = json.loads(policy["context"]["user"])
        assert context_user == {
            "sub": str(user_id),
            "mail": "21.00000-0@maua.br",
        }

    def test_deny_when_user_missing_on_protected_route(self):
        usecase, _ = self._usecase(
            {
                "sub": str(uuid.uuid4()),
                "mail": "21.00000-0@maua.br",
            }
        )

        policy = usecase(
            authorization_token="token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/GET/users",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"
        assert "context" not in policy

    def test_allow_onboarding_route_without_existing_user(self):
        user_id = str(uuid.uuid4())
        usecase, _ = self._usecase(
            {
                "sub": user_id,
                "mail": "21.00000-0@maua.br",
            }
        )

        policy = usecase(
            authorization_token="Bearer token-123",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["principalId"] == user_id
        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Allow"
        context_user = json.loads(policy["context"]["user"])
        assert context_user == {
            "sub": user_id,
            "mail": "21.00000-0@maua.br",
        }

    def test_deny_non_maua_email(self):
        usecase, _ = self._usecase(
            {
                "sub": str(uuid.uuid4()),
                "mail": "user@gmail.com",
            }
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_deny_invalid_uuid_sub(self):
        usecase, _ = self._usecase(
            {
                "sub": "not-a-uuid",
                "mail": "21.00000-0@maua.br",
            }
        )

        policy = usecase(
            authorization_token="token",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_deny_invalid_jwt_signature(self):
        repo = UserRepositoryMock()
        usecase = MicrosoftAuthorizerUsecase(
            jwt_verifier=_FakeJwtVerifier(
                error=JwtVerificationError("invalid signature")
            ),
            user_repo=repo,
        )

        policy = usecase(
            authorization_token="Bearer bad.token.here",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert policy["policyDocument"]["Statement"][0]["Effect"] == "Deny"

    def test_strips_bearer_prefix_before_verify(self):
        verifier = _FakeJwtVerifier(
            claims={
                "sub": str(uuid.uuid4()),
                "mail": "21.00000-0@maua.br",
            }
        )
        usecase = MicrosoftAuthorizerUsecase(
            jwt_verifier=verifier,
            user_repo=UserRepositoryMock(),
        )

        usecase(
            authorization_token="Bearer abc.def.ghi",
            method_arn="arn:aws:execute-api:sa-east-1:123:api/POST/auth",
        )

        assert verifier.last_token == "abc.def.ghi"
