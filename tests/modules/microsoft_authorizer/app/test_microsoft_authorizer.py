import json
from unittest.mock import Mock

import pytest

from src.modules.microsoft_authorizer.app import microsoft_authorizer_presenter as presenter
from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import MicrosoftAuthorizerUsecase

ARN = "arn:aws:execute-api:sa-east-1:123456789012:api/dev/POST/portfolio/auth-user"
PROFILE = {
    "id": "00000000-0000-0000-0000-000000000099",
    "mail": "Leo@Maua.br",
    "displayName": "Leo",
}


def make_usecase(profile=None):
    client = Mock()
    client.get_user_profile.return_value = PROFILE if profile is None else profile
    return MicrosoftAuthorizerUsecase(client), client


def test_valid_graph_profile_builds_expected_context():
    usecase, client = make_usecase()
    result = usecase("Bearer test-token", ARN)
    client.get_user_profile.assert_called_once_with("test-token")
    statement = result["policyDocument"]["Statement"][0]
    assert statement["Effect"] == "Allow"
    assert statement["Resource"] == ARN
    assert json.loads(result["context"]["user"]) == {
        "sub": PROFILE["id"], "mail": "leo@maua.br", "name": "Leo"
    }


def test_upn_fallback_and_missing_name():
    usecase, _ = make_usecase({
        "id": PROFILE["id"],
        "mail": None,
        "userPrincipalName": "leo@maua.br",
    })
    result = usecase("bearer test-token", ARN)
    assert json.loads(result["context"]["user"])["name"] == ""


@pytest.mark.parametrize("changes", [
    {"mail": "leo@gmail.com"},
    {"mail": "leo@maua.br.evil.com"},
    {"id": "not-a-uuid"},
    {"id": None},
    {"mail": 123},
])
def test_unaccepted_profile_is_denied(changes):
    usecase, _ = make_usecase({**PROFILE, **changes})
    result = usecase("Bearer test-token", ARN)
    assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"
    assert "context" not in result


@pytest.mark.parametrize("token", [None, "", "token", "Bearer ", "Bearer one two"])
def test_invalid_bearer_does_not_call_graph(token):
    usecase, client = make_usecase()
    with pytest.raises(ValueError):
        usecase(token, ARN)
    client.get_user_profile.assert_not_called()


def test_presenter_denies_graph_failure_without_logging_token(monkeypatch, caplog):
    usecase = Mock(side_effect=ValueError("secret-token"))
    monkeypatch.setattr(presenter, "usecase", usecase)
    result = presenter.lambda_handler({
        "methodArn": ARN, "authorizationToken": "Bearer secret-token"
    }, None)
    assert result["policyDocument"]["Statement"][0]["Effect"] == "Deny"
    assert "secret-token" not in caplog.text


def test_presenter_missing_arn_is_configuration_error():
    with pytest.raises(ValueError):
        presenter.lambda_handler({}, None)