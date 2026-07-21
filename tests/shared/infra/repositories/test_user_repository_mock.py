import uuid

import pytest

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(uuid.UUID("00000000-0000-0000-0000-000000000001"))

        assert user.id == uuid.UUID("00000000-0000-0000-0000-000000000001")
        assert user.email == "soller@maua.br"
        assert user.role == RoleEnum.ADMIN
        assert user.senha_hash == "hash_soller"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.get_user(uuid.UUID("00000000-0000-0000-0000-000000000069"))

    def test_get_all_user(self):
        repo = UserRepositoryMock()
        users = repo.get_all_user()

        assert len(users) == 3
        assert all(isinstance(user, User) for user in users)

    def test_create_user(self):
        repo = UserRepositoryMock()
        new_user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            email="ana@maua.br",
            role=RoleEnum.ADMIN,
            senha_hash="hash_ana"
        )

        user = repo.create_user(new_user)

        assert len(repo.users) == 4
        assert user == new_user
        assert repo.users[3].email == "ana@maua.br"
        assert repo.users[3].role == RoleEnum.ADMIN

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user(uuid.UUID("00000000-0000-0000-0000-000000000001"))

        assert user.email == "soller@maua.br"
        assert len(repo.users) == 2

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.delete_user(uuid.UUID("00000000-0000-0000-0000-000000000069"))

    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user(
            uuid.UUID("00000000-0000-0000-0000-000000000002"),
            new_role=RoleEnum.ADMIN
        )

        assert user.role == RoleEnum.ADMIN
        assert repo.users[1].role == RoleEnum.ADMIN
        # os outros campos permanecem intactos
        assert user.email == "brancas@maua.br"
        assert user.senha_hash == "hash_brancas"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()

        with pytest.raises(NoItemsFound):
            repo.update_user(
                uuid.UUID("00000000-0000-0000-0000-000000000069"),
                new_role=RoleEnum.ADMIN
            )
