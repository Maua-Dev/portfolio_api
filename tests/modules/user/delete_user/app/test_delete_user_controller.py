import uuid

from src.modules.user.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.user.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class MockHttpRequest:
    def __init__(self, data: dict):
        self.data = data


class TestDeleteUserController:

    def setup_method(self):
        self.repo = UserRepositoryMock()
        self.usecase = DeleteUserUsecase(self.repo)
        self.controller = DeleteUserController(self.usecase)

    def test_delete_user_success(self):
        rubio = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            email="rubio@maua.br",
            role=RoleEnum.ADMIN,
        )
        self.repo.create_user(rubio)
        request = MockHttpRequest(data={'user_id': '00000000-0000-0000-0000-000000000004'})

        response = self.controller(request)

        assert response.status_code == HttpStatusCodeEnum.OK.value
        assert response.body['user_id'] == '00000000-0000-0000-0000-000000000004'
        assert response.body['user_email'] == 'rubio@maua.br'
        assert response.body['user_role'] == 'Admin'
        assert response.body['message'] == "the user was deleted successfully"
        assert len(self.repo.users) == 3

    def test_delete_user_missing_user_id(self):
        request = MockHttpRequest(data={})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_delete_user_wrong_type(self):
        request = MockHttpRequest(data={'user_id': 123})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_delete_user_invalid_uuid(self):
        request = MockHttpRequest(data={'user_id': 'not-a-uuid'})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.BAD_REQUEST.value

    def test_delete_user_not_found(self):
        request = MockHttpRequest(data={'user_id': str(uuid.uuid4())})
        response = self.controller(request)
        assert response.status_code == HttpStatusCodeEnum.NOT_FOUND.value
