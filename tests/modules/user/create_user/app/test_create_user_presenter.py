import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.user.create_user.app.create_user_presenter import create_user_presenter


def build_event(body: dict = None) -> dict:
    return {
        'body': json.dumps(body) if body is not None else None
    }


class Test_CreateUserPresenter:

    def test_create_user_presenter(self):
        event = build_event({
            'email': 'giulia@maua.br',
            'role': 'Admin'
        })

        response = create_user_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 201
        assert body['user_email'] == 'giulia@maua.br'
        assert body['user_role'] == 'Admin'
        assert body['message'] == 'the user was created successfully'

    def test_create_user_presenter_missing_email(self):
        event = build_event({})

        response = create_user_presenter(event)

        assert response['statusCode'] == 400

    def test_create_user_presenter_email_is_not_valid(self):
        event = build_event({
            'email': 'isso_nao_e_email',
        })

        response = create_user_presenter(event)

        assert response['statusCode'] == 400

    def test_create_user_presenter_already_exists(self):
        event = build_event({
            'email': 'soller@maua.br',
        })

        response = create_user_presenter(event)

        assert response['statusCode'] == 409
