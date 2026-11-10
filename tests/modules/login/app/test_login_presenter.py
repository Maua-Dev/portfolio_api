import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.login.app import login_presenter as presenter_module
from src.modules.login.app.login_presenter import lambda_handler


class _FakeMsIdTokenVerifier:
    def __init__(self, claims: dict | None = None, error: Exception | None = None):
        self.claims = claims or {}
        self.error = error

    def verify(self, id_token: str) -> dict:
        if self.error is not None:
            raise self.error
        return self.claims


class _FakeJwtSigner:
    def sign(self, payload: dict) -> str:
        return "signed.access.token"


class Test_LoginPresenter:
    def test_login_presenter_success(self):
        user = presenter_module.user_repo.users[0]
        presenter_module.usecase.ms_id_token_verifier = _FakeMsIdTokenVerifier(
            claims={
                "oid": str(user.id),
                "preferred_username": user.email,
                "name": user.email,
            }
        )
        presenter_module.usecase.jwt_signer = _FakeJwtSigner()

        event = {
            "body": json.dumps({"id_token": "aaa.bbb.ccc"})
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["access_token"] == "signed.access.token"
        assert body["user"]["email"] == user.email
        assert body["user"]["role"] == (user.role.value if hasattr(user.role, "value") else user.role)
        assert "Set-Cookie" in response["headers"]

    def test_login_presenter_missing_id_token(self):
        event = {
            "body": json.dumps({})
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
