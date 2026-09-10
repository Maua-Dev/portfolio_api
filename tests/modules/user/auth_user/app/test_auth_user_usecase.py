import uuid

import pytest

from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_AuthUserUsecase:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = AuthUserUsecase(self.repo)

    def test_auth_user_retrieves_existing_user(self):
        user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")

        user, created = self.usecase(
            user_id=user_id,
            email="soller@maua.br"
        )

        assert created is False
        assert isinstance(user, User)
        assert user.id == user_id
        assert user.email == "soller@maua.br"
        assert user.role == RoleEnum.ADMIN
        assert len(self.repo.users) == 3

    def test_auth_user_does_not_reassign_existing_user(self):
        user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")

        user, created = self.usecase(
            user_id=user_id,
            email="outro@maua.br"
        )

        assert created is False
        assert user.email == "soller@maua.br"
        assert user.role == RoleEnum.ADMIN
        assert self.repo.get_user(user_id).email == "soller@maua.br"

    def test_auth_user_creates_when_not_found(self):
        user_id = uuid.UUID("00000000-0000-0000-0000-000000000099")

        user, created = self.usecase(
            user_id=user_id,
            email="giulia@maua.br"
        )

        assert created is True
        assert isinstance(user, User)
        assert user.id == user_id
        assert user.email == "giulia@maua.br"
        assert user.role == RoleEnum.USER
        assert len(self.repo.users) == 4
        assert self.repo.users[3] == user

    def test_auth_user_duplicated_email(self):
        with pytest.raises(DuplicatedItem):
            self.usecase(
                user_id=uuid.UUID("00000000-0000-0000-0000-000000000099"),
                email="soller@maua.br"
            )

    def test_auth_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            self.usecase(
                user_id=uuid.UUID("00000000-0000-0000-0000-000000000099"),
                email="isso_nao_e_email"
            )

    def test_auth_user_email_is_not_str(self):
        with pytest.raises(EntityError):
            self.usecase(
                user_id=uuid.UUID("00000000-0000-0000-0000-000000000099"),
                email=123
            )

    def test_auth_user_user_id_is_not_uuid(self):
        with pytest.raises(EntityError):
            self.usecase(
                user_id="00000000-0000-0000-0000-000000000099",
                email="giulia@maua.br"
            )
