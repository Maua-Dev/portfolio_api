import uuid

from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class TestGetAllUsersController:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = GetAllUsersUsecase(self.repo)
        self.controller = GetAllUsersController(self.usecase)

    def test_get_all_users_success(self):
        request = MockHttpRequest(data={})

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert len(response.body['all_users']) == 3
        assert response.body['message'] == "all users were retrieved successfully"

    def test_get_all_users_body_fields(self):
        request = MockHttpRequest(data={})

        response = self.controller(request)
        first_user = response.body['all_users'][0]

        assert first_user['user_id'] == '00000000-0000-0000-0000-000000000001'
        assert first_user['user_email'] == 'soller@maua.br'
        assert first_user['user_role'] == 'Admin'

    def test_get_all_users_includes_created_user(self):
        rubio = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            email="rubio@maua.br",
            role=RoleEnum.USER,
        )
        self.repo.create_user(rubio)
        request = MockHttpRequest(data={})

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert len(response.body['all_users']) == 4
        assert response.body['all_users'][3]['user_email'] == 'rubio@maua.br'

    def test_get_all_users_empty_repository(self):
        self.repo.users = []
        request = MockHttpRequest(data={})

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body['all_users'] == []
