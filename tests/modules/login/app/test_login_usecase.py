from unittest.mock import MagicMock
import uuid

import pytest

from src.modules.login.app.login_usecase import LoginUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.entities.session import Session
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import InvalidJwtFormat
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class _FakeMsIdTokenVerifier:
    def __init__(self, claims: dict | None = None, error: Exception | None = None):
        self.claims = claims or {}
        self.error = error
        self.last_token = None

    def verify(self, id_token: str) -> dict:
        self.last_token = id_token
        if self.error is not None:
            raise self.error
        return self.claims


class _FakeJwtSigner:
    def __init__(self):
        self.last_payload = None

    def sign(self, payload: dict) -> str:
        self.last_payload = payload
        return "signed.access.token"


class Test_LoginUsecase:
    def test_login_usecase_invalid_jwt_shape(self):
        repo = UserRepositoryMock()
        session_repo = SessionRepositoryMock()
        usecase = LoginUsecase(
            repo=repo,
            session_repo=session_repo,
            observability=MagicMock(),
            ms_id_token_verifier=_FakeMsIdTokenVerifier(),
            jwt_signer=_FakeJwtSigner(),
        )

        with pytest.raises(InvalidJwtFormat):
            usecase(id_token="not-a-jwt")

    def test_login_usecase_invalid_microsoft_token(self):
        repo = UserRepositoryMock()
        session_repo = SessionRepositoryMock()
        usecase = LoginUsecase(
            repo=repo,
            session_repo=session_repo,
            observability=MagicMock(),
            ms_id_token_verifier=_FakeMsIdTokenVerifier(
                error=JwtVerificationError("bad signature")
            ),
            jwt_signer=_FakeJwtSigner(),
        )

        with pytest.raises(JwtVerificationError):
            usecase(id_token="aaa.bbb.ccc")

    def test_login_usecase_happy_path_existing_user_by_oid(self):
        repo = UserRepositoryMock()
        session_repo = SessionRepositoryMock()
        user = repo.users[0]
        signer = _FakeJwtSigner()
        usecase = LoginUsecase(
            repo=repo,
            session_repo=session_repo,
            observability=MagicMock(),
            ms_id_token_verifier=_FakeMsIdTokenVerifier(
                claims={
                    "oid": str(user.id),
                    "preferred_username": user.email,
                    "name": user.email,
                }
            ),
            jwt_signer=signer,
        )

        access_token, refresh_token, returned_user = usecase(id_token="aaa.bbb.ccc")

        assert access_token == "signed.access.token"
        assert len(refresh_token) == 64
        assert returned_user.id == user.id
        assert signer.last_payload["user_id"] == str(user.id)
        assert signer.last_payload["role"] == user.role
        assert signer.last_payload["sub"] == str(user.id)
        assert signer.last_payload["mail"] == str(user.email)
        assert "exp" in signer.last_payload
        assert session_repo.get_session(user.id).refresh_token == refresh_token

    def test_login_usecase_creates_user_when_not_found(self):
        repo = UserRepositoryMock()
        session_repo = SessionRepositoryMock()
        original_count = len(repo.users)
        new_oid = "d351a9b1-937f-423c-a9d1-9929b5795be1"
        signer = _FakeJwtSigner()
        usecase = LoginUsecase(
            repo=repo,
            session_repo=session_repo,
            observability=MagicMock(),
            ms_id_token_verifier=_FakeMsIdTokenVerifier(
                claims={
                    "oid": new_oid,
                    "preferred_username": "23.00847-4@maua.br",
                    "name": "LEONARDO LUIZ SEIXAS IORIO",
                }
            ),
            jwt_signer=signer,
        )

        access_token, refresh_token, returned_user = usecase(id_token="aaa.bbb.ccc")

        assert access_token == "signed.access.token"
        assert len(refresh_token) == 64
        assert len(repo.users) == original_count + 1
        assert returned_user.id == uuid.UUID(new_oid)
        assert returned_user.email == "23.00847-4@maua.br"
        assert returned_user.role == RoleEnum.USER
        assert signer.last_payload["user_id"] == new_oid
        assert session_repo.get_session(returned_user.id).refresh_token == refresh_token

    def test_login_usecase_replaces_refresh_token_for_existing_session(self):
        repo = UserRepositoryMock()
        session_repo = SessionRepositoryMock()
        user = repo.users[0]
        session_repo.create_session(
            Session(refresh_token="previous-refresh-token", user_id=user.id)
        )
        usecase = LoginUsecase(
            repo=repo,
            session_repo=session_repo,
            observability=MagicMock(),
            ms_id_token_verifier=_FakeMsIdTokenVerifier(
                claims={
                    "oid": str(user.id),
                    "preferred_username": user.email,
                }
            ),
            jwt_signer=_FakeJwtSigner(),
        )

        _, refresh_token, returned_user = usecase(id_token="aaa.bbb.ccc")

        stored_session = session_repo.get_session(returned_user.id)
        assert stored_session.refresh_token == refresh_token
        assert stored_session.refresh_token != "previous-refresh-token"
