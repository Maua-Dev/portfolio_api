import pytest
from unittest.mock import Mock
from uuid import UUID

from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

CLAIMS = {
    "sub": "00000000-0000-0000-0000-000000000099",
    "mail": "leo@maua.br",
    "name": "Leo",
}


def test_first_login_creates_regular_user():
    repo = UserRepositoryMock()
    user, created = AuthUserUsecase(repo)(CLAIMS)
    assert created is True
    assert user.id == UUID(CLAIMS["sub"])
    assert user.email == "leo@maua.br"
    assert user.role == "User"
    assert len(repo.users) == 4


def test_repeated_login_does_not_duplicate():
    repo = UserRepositoryMock()
    usecase = AuthUserUsecase(repo)
    first, _ = usecase(CLAIMS)
    second, created = usecase(CLAIMS)
    assert second == first
    assert created is False
    assert len(repo.users) == 4


def test_existing_admin_keeps_id_and_role():
    repo = UserRepositoryMock()
    user, created = AuthUserUsecase(repo)({
        **CLAIMS,
        "mail": " SOLLER@MAUA.BR ",
        "role": "User",
    })
    assert user == repo.users[0]
    assert str(user.id) != CLAIMS["sub"]
    assert user.role == "Admin"
    assert created is False


def test_client_cannot_choose_admin_role():
    user, _ = AuthUserUsecase(UserRepositoryMock())({
        **CLAIMS, "role": "Admin"
    })
    assert user.role == "User"


@pytest.mark.parametrize("changes", [
    {"sub": "invalid"},
    {"sub": None},
    {"mail": "leo@gmail.com"},
    {"mail": "leo@maua.br.evil.com"},
    {"mail": None},
    {"name": None},
])
def test_invalid_claims_are_rejected(changes):
    repo = UserRepositoryMock()
    with pytest.raises(EntityError):
        AuthUserUsecase(repo)({**CLAIMS, **changes})
    assert len(repo.users) == 3


def test_concurrent_registration_returns_existing_user():
    repo = UserRepositoryMock()
    original_create = repo.create_user

    def concurrent_create(user):
        original_create(user)
        raise DuplicatedItem("user")

    repo.create_user = Mock(side_effect=concurrent_create)
    user, created = AuthUserUsecase(repo)(CLAIMS)
    assert user.email == CLAIMS["mail"]
    assert created is False
    assert len(repo.users) == 4