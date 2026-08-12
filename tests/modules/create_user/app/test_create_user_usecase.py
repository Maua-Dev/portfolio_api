import pytest

from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = CreateUserUsecase(self.repo)

    def test_create_user(self):
        user = self.usecase(
            email="giulia@maua.br",
            senha_hash="hash_giulia",
            role=RoleEnum.ADMIN.value
        )

        assert isinstance(user, User)
        assert user.email == "giulia@maua.br"
        assert user.role == RoleEnum.ADMIN
        assert user.senha_hash == "hash_giulia"
        assert len(self.repo.users) == 4
        assert self.repo.users[3] == user

    def test_create_user_role_default_is_user(self):
        user = self.usecase(email="giulia@maua.br", senha_hash="hash_giulia")

        assert user.role == RoleEnum.USER

    def test_create_user_duplicated_email(self):
        with pytest.raises(DuplicatedItem):
            self.usecase(email="soller@maua.br", senha_hash="hash_qualquer")

    def test_create_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            self.usecase(email="isso_nao_e_email", senha_hash="hash_giulia")

    def test_create_user_email_is_not_str(self):
        with pytest.raises(EntityError):
            self.usecase(email=123, senha_hash="hash_giulia")

    def test_create_user_senha_hash_is_not_str(self):
        with pytest.raises(EntityError):
            self.usecase(email="giulia@maua.br", senha_hash=123)

    def test_create_user_senha_hash_is_empty(self):
        with pytest.raises(EntityError):
            self.usecase(email="giulia@maua.br", senha_hash="")

    def test_create_user_role_is_not_valid(self):
        with pytest.raises(EntityError):
            self.usecase(
                email="giulia@maua.br",
                senha_hash="hash_giulia",
                role="Superuser"
            )
