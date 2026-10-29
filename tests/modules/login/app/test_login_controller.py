from unittest.mock import MagicMock
import uuid

from src.modules.login.app.login_controller import LoginController
from src.modules.login.app.login_usecase import LoginUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_LoginController:
    def test_login_controller_missing_id_token(self):
        repo = UserRepositoryMock()
        observability = MagicMock()
        usecase = LoginUsecase(repo=repo, observability=observability)
        controller = LoginController(usecase=usecase, observability=observability)

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert response.body == "Field id_token is missing"

    def test_login_controller_wrong_type_id_token(self):
        repo = UserRepositoryMock()
        observability = MagicMock()
        usecase = LoginUsecase(repo=repo, observability=observability)
        controller = LoginController(usecase=usecase, observability=observability)

        response = controller(HttpRequest(body={"id_token": 123}))

        assert response.status_code == 400
        assert "id_token" in response.body

    def test_login_controller_happy_path(self):
        user = User(
            id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
            email="23.00847-4@maua.br",
            role=RoleEnum.USER,
        )

        observability = MagicMock()
        usecase = MagicMock()
        usecase.return_value = ("signed.access.token", "a" * 64, user)
        controller = LoginController(usecase=usecase, observability=observability)

        response = controller(HttpRequest(body={"id_token": "aaa.bbb.ccc"}))

        assert response.status_code == 200
        assert response.body["access_token"] == "signed.access.token"
        assert response.body["user"]["role"] == user.role.value
        assert response.body["message"] == "Login successful"
        assert "Set-Cookie" in response.headers
        assert response.headers["Set-Cookie"].startswith("refresh_token=")
        assert "HttpOnly" in response.headers["Set-Cookie"]
        assert "Secure" in response.headers["Set-Cookie"]
        assert "SameSite=Strict" in response.headers["Set-Cookie"]
        usecase.assert_called_once_with(id_token="aaa.bbb.ccc")
