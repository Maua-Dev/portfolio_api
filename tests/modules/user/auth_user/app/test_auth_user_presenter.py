import json
import os

import pytest

os.environ["STAGE"] = "TEST"

from src.modules.user.auth_user.app import auth_user_presenter as presenter
from src.modules.user.auth_user.app.auth_user_controller import AuthUserController
from src.modules.user.auth_user.app.auth_user_usecase import AuthUserUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

CLAIMS = {
    "sub": "00000000-0000-0000-0000-000000000099",
    "mail": "leo@maua.br",
    "name": "Leo",
}


@pytest.fixture(autouse=True)
def isolated_controller(monkeypatch):
    repo = UserRepositoryMock()
    monkeypatch.setattr(
        presenter, "controller", AuthUserController(AuthUserUsecase(repo))
    )


def build_event():
    return {
        "httpMethod": "POST",
        "path": "/portfolio/auth-user",
        "requestContext": {
            "authorizer": {"user": json.dumps(CLAIMS)},
        },
        "body": None,
    }


def test_first_and_second_login():
    first = presenter.lambda_handler(build_event(), None)
    second = presenter.lambda_handler(build_event(), None)
    assert first["statusCode"] == second["statusCode"] == 200
    assert json.loads(first["body"])["created"] is True
    assert json.loads(second["body"])["created"] is False


@pytest.mark.parametrize("location", ["body", "queryStringParameters", "headers"])
def test_claims_in_client_payload_do_not_authenticate(location):
    spoofed = {"user_from_authorizer": CLAIMS}
    event = {
        location: json.dumps(spoofed) if location == "body" else spoofed
    }
    assert presenter.lambda_handler(event, None)["statusCode"] == 401


def test_verified_context_overrides_client_payload():
    event = build_event()
    event["body"] = json.dumps({
        "user_from_authorizer": {**CLAIMS, "mail": "attacker@maua.br"},
        "role": "Admin",
    })
    response = presenter.lambda_handler(event, None)
    body = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert body["user_email"] == "leo@maua.br"
    assert body["user_role"] == "User"


@pytest.mark.parametrize("raw", ["invalid JSON", "[]", "{}"])
def test_invalid_authorizer_context_returns_401(raw):
    event = build_event()
    event["requestContext"]["authorizer"]["user"] = raw
    assert presenter.lambda_handler(event, None)["statusCode"] == 401