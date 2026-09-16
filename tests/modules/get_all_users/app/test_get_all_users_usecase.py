import uuid

from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetAllUsersUsecase:

    def test_get_all_users_success(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)

        all_users = usecase()

        assert isinstance(all_users, list)
        assert len(all_users) == len(repo.users)
        assert all(isinstance(user, User) for user in all_users)

    def test_get_all_users_returns_created_user(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)

        rubio = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            email="rubio@maua.br",
            role=RoleEnum.USER,
        )
        repo.create_user(rubio)

        all_users = usecase()

        assert len(all_users) == 4
        assert rubio in all_users

    def test_get_all_users_empty_repository(self):
        repo = UserRepositoryMock()
        repo.users = []
        usecase = GetAllUsersUsecase(repo)

        all_users = usecase()

        assert all_users == []
