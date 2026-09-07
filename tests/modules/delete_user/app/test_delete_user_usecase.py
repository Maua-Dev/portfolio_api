import uuid

import pytest

from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestDeleteUserUsecase:

    def test_delete_user_success(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        rubio = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            email="rubio@maua.br",
            role=RoleEnum.USER,
        )
        repo.create_user(rubio)

        user = usecase(user_id=rubio.id)

        assert isinstance(user, User)
        assert user.id == uuid.UUID("00000000-0000-0000-0000-000000000004")
        assert user.email == "rubio@maua.br"
        assert user.role == RoleEnum.USER
        assert len(repo.users) == 3

    def test_delete_user_twice_raises_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        usecase(user_id=uuid.UUID("00000000-0000-0000-0000-000000000002"))

        with pytest.raises(NoItemsFound):
            usecase(user_id=uuid.UUID("00000000-0000-0000-0000-000000000002"))

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id=uuid.uuid4())

    def test_delete_user_wrong_type(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)

        with pytest.raises(EntityError):
            usecase(user_id="00000000-0000-0000-0000-000000000002")
