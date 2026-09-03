import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.get_all_users.app.get_all_users_presenter import get_all_users_presenter, lambda_handler


def build_event() -> dict:
    return {
        'version': '2.0',
        'rawPath': '/get_all_users',
        'requestContext': {
            'http': {
                'method': 'GET',
                'path': '/get_all_users'
            }
        }
    }


class TestGetAllUsersPresenter:

    def test_get_all_users_presenter_success(self):
        event = build_event()

        response = get_all_users_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert len(body['all_users']) == 3
        assert body['message'] == "all users were retrieved successfully"

    def test_get_all_users_presenter_body_fields(self):
        event = build_event()

        response = get_all_users_presenter(event)
        body = json.loads(response['body'])
        first_user = body['all_users'][0]

        assert first_user['user_id'] == '00000000-0000-0000-0000-000000000001'
        assert first_user['user_email'] == 'soller@maua.br'
        assert first_user['user_role'] == 'Admin'
        assert 'senha_hash' not in first_user

    def test_get_all_users_lambda_handler_success(self):
        event = build_event()

        response = lambda_handler(event, None)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert len(body['all_users']) == 3
