import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.get_user.app.get_user_presenter import get_user_presenter


def build_event(user_id: str = None) -> dict:
    return {
        'queryStringParameters': {'user_id': user_id} if user_id else None
    }


class TestGetUserPresenter:

    def test_get_user_presenter_success(self):
        event = build_event(user_id='00000000-0000-0000-0000-000000000001')

        response = get_user_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['user_id'] == '00000000-0000-0000-0000-000000000001'
        assert body['user_email'] == 'soller@maua.br'
        assert body['user_role'] == 'Admin'

    def test_get_user_presenter_not_found(self):
        event = build_event(user_id='11111111-1111-1111-1111-111111111111')

        response = get_user_presenter(event)

        assert response['statusCode'] == 404

    def test_get_user_presenter_missing_id(self):
        event = build_event()

        response = get_user_presenter(event)

        assert response['statusCode'] == 400