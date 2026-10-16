from unittest.mock import Mock

from src.modules.user.auth_user.app.auth_user_controller import AuthUserController
from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

CLAIMS = {
    "sub": "00000000-0000-0000-0000-000000000099",
    "mail": "leo@maua.br",
    "name": "Leo",
}


def test_authenticated_user_returns_200():
    controller = AuthUserController(AuthUserUsecase(UserRepositoryMock()))
    response = controller(HttpRequest(body={"user_from_authorizer": CLAIMS}))
    assert response.status_code == 200
    assert response.body["user_email"] == "leo@maua.br"
    assert response.body["created"] is True


def test_missing_authentication_returns_401():
    response = AuthUserController(Mock())(HttpRequest())
    assert response.status_code == 401


def test_invalid_claims_return_400():
    controller = AuthUserController(AuthUserUsecase(UserRepositoryMock()))
    response = controller(HttpRequest(body={"user_from_authorizer": []}))
    assert response.status_code == 400


def test_internal_error_does_not_expose_exception():
    usecase = Mock(side_effect=RuntimeError("private database details"))
    response = AuthUserController(usecase)(
        HttpRequest(body={"user_from_authorizer": CLAIMS})
    )
    assert response.status_code == 500
    assert response.body == "Erro interno ao autenticar usuário"