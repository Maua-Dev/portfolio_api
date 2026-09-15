import uuid

from src.modules.user.auth_user.app.auth_user_controller import AuthUserController
from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class Test_AuthUserController:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = AuthUserUsecase(self.repo)
        self.controller = AuthUserController(self.usecase)

    def test_auth_user_retrieves_existing_user(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': '00000000-0000-0000-0000-000000000001',
                'mail': 'soller@maua.br',
                'name': 'Soller'
            }
        })

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body['user_id'] == '00000000-0000-0000-0000-000000000001'
        assert response.body['user_email'] == 'soller@maua.br'
        assert response.body['user_role'] == 'Admin'
        assert response.body['message'] == 'the user was retrieved successfully'
        assert len(self.repo.users) == 3

    def test_auth_user_does_not_reassign_existing_user(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': '00000000-0000-0000-0000-000000000001',
                'mail': 'outro@maua.br',
                'name': 'Soller'
            }
        })

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body['user_email'] == 'soller@maua.br'
        assert response.body['user_role'] == 'Admin'
        assert response.body['message'] == 'the user was retrieved successfully'

    def test_auth_user_creates_when_not_found(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': '00000000-0000-0000-0000-000000000099',
                'mail': 'giulia@maua.br',
                'name': 'Giulia'
            }
        })

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.CREATED.value
        assert response.body['user_id'] == '00000000-0000-0000-0000-000000000099'
        assert response.body['user_email'] == 'giulia@maua.br'
        assert response.body['user_role'] == 'User'
        assert response.body['message'] == 'the user was created successfully'
        assert len(self.repo.users) == 4

    def test_auth_user_missing_authorizer_user(self):
        request = MockHttpRequest(data={})
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.UNAUTHORIZED.value

    def test_auth_user_missing_sub(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'mail': 'giulia@maua.br',
                'name': 'Giulia'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.UNAUTHORIZED.value

    def test_auth_user_missing_mail(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': '00000000-0000-0000-0000-000000000099',
                'name': 'Giulia'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.UNAUTHORIZED.value

    def test_auth_user_sub_is_not_str(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': 123,
                'mail': 'giulia@maua.br',
                'name': 'Giulia'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_auth_user_mail_is_not_str(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': '00000000-0000-0000-0000-000000000099',
                'mail': 123,
                'name': 'Giulia'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_auth_user_invalid_uuid(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': 'not-a-uuid',
                'mail': 'giulia@maua.br',
                'name': 'Giulia'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_auth_user_email_is_not_valid(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': '00000000-0000-0000-0000-000000000099',
                'mail': 'isso_nao_e_email',
                'name': 'Giulia'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_auth_user_duplicated_email(self):
        request = MockHttpRequest(data={
            USER_FROM_AUTHORIZER_KEY: {
                'sub': str(uuid.uuid4()),
                'mail': 'soller@maua.br',
                'name': 'Soller'
            }
        })
        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.CONFLICT.value
