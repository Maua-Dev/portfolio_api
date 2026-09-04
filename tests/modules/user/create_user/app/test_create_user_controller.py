from src.modules.user.create_user.app.create_user_controller import CreateUserController
from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class Test_CreateUserController:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = CreateUserUsecase(self.repo)
        self.controller = CreateUserController(self.usecase)

    def test_create_user(self):
        request = MockHttpRequest(data={
            'email': 'giulia@maua.br',
            'role': 'Admin'
        })

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.CREATED.value
        assert response.body['user_email'] == 'giulia@maua.br'
        assert response.body['user_role'] == 'Admin'
        assert response.body['message'] == 'the user was created successfully'
        assert len(self.repo.users) == 4

    def test_create_user_role_default_is_user(self):
        request = MockHttpRequest(data={
            'email': 'giulia@maua.br',
        })

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.CREATED.value
        assert response.body['user_role'] == 'User'

    def test_create_user_missing_email(self):
        request = MockHttpRequest(data={})
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_create_user_email_is_not_str(self):
        request = MockHttpRequest(data={'email': 123})
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_create_user_email_is_not_valid(self):
        request = MockHttpRequest(data={
            'email': 'isso_nao_e_email',
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_create_user_role_is_not_valid(self):
        request = MockHttpRequest(data={
            'email': 'giulia@maua.br',
            'role': 'Superuser'
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_create_user_role_is_not_str(self):
        request = MockHttpRequest(data={
            'email': 'giulia@maua.br',
            'role': 123
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_create_user_already_exists(self):
        request = MockHttpRequest(data={
            'email': 'soller@maua.br',
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.CONFLICT.value
