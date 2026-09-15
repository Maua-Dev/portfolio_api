import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.user.auth_user.app.auth_user_presenter import auth_user_presenter


def build_event(sub: str = None, mail: str = None, name: str = "Test User") -> dict:
    event = {
        'body': None,
        'headers': {},
        'queryStringParameters': None,
        'requestContext': {
            'authorizer': {}
        }
    }

    if sub is not None and mail is not None:
        event['requestContext']['authorizer']['user'] = json.dumps({
            'sub': sub,
            'mail': mail,
            'name': name,
        })

    return event


class Test_AuthUserPresenter:

    def test_auth_user_presenter_retrieves_existing_user(self):
        event = build_event(
            sub='00000000-0000-0000-0000-000000000001',
            mail='soller@maua.br',
            name='Soller'
        )

        response = auth_user_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['user_id'] == '00000000-0000-0000-0000-000000000001'
        assert body['user_email'] == 'soller@maua.br'
        assert body['user_role'] == 'Admin'
        assert body['message'] == 'the user was retrieved successfully'

    def test_auth_user_presenter_creates_when_not_found(self):
        event = build_event(
            sub='00000000-0000-0000-0000-000000000088',
            mail='auth.created@maua.br',
            name='Auth Created'
        )

        response = auth_user_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 201
        assert body['user_id'] == '00000000-0000-0000-0000-000000000088'
        assert body['user_email'] == 'auth.created@maua.br'
        assert body['user_role'] == 'User'
        assert body['message'] == 'the user was created successfully'

    def test_auth_user_presenter_missing_authorizer_user(self):
        event = build_event()

        response = auth_user_presenter(event)

        assert response['statusCode'] == 401

    def test_auth_user_presenter_invalid_uuid(self):
        event = build_event(
            sub='not-a-uuid',
            mail='giulia@maua.br'
        )

        response = auth_user_presenter(event)

        assert response['statusCode'] == 400
