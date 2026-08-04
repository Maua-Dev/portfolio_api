import uuid

import pytest

from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetUserUsecase:

    def test_get_user_success(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        user = usecase(user_id=uuid.UUID("00000000-0000-0000-0000-000000000001"))

        assert isinstance(user, User)
        assert user.id == uuid.UUID("00000000-0000-0000-0000-000000000001")
        assert user.email == "soller@maua.br"
        assert user.role == RoleEnum.ADMIN

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id=uuid.uuid4())

    def test_get_user_wrong_type(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        with pytest.raises(EntityError):
            usecase(user_id="00000000-0000-0000-0000-000000000001")