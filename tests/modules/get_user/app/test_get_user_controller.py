import uuid

from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class TestGetUserController:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = GetUserUsecase(self.repo)
        self.controller = GetUserController(self.usecase)

    def test_get_user_success(self):
        request = MockHttpRequest(data={'user_id': '00000000-0000-0000-0000-000000000001'})

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body['user_id'] == '00000000-0000-0000-0000-000000000001'
        assert response.body['user_email'] == 'soller@maua.br'
        assert response.body['user_role'] == 'Admin'

    def test_get_user_missing_user_id(self):
        request = MockHttpRequest(data={})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_get_user_wrong_type(self):
        request = MockHttpRequest(data={'user_id': 123})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_get_user_invalid_uuid(self):
        request = MockHttpRequest(data={'user_id': 'not-a-uuid'})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_get_user_not_found(self):
        request = MockHttpRequest(data={'user_id': str(uuid.uuid4())})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.NOT_FOUND.value