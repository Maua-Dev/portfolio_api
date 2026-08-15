import json
import os
import uuid

os.environ["STAGE"] = "TEST"

from src.modules.delete_user.app.delete_user_presenter import delete_user_presenter, repo
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


def build_event(user_id: str = None) -> dict:
    return {
        'queryStringParameters': {'user_id': user_id} if user_id else None
    }


class TestDeleteUserPresenter:

    def test_delete_user_presenter_success(self):
        rubio = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            email="rubio@maua.br",
            role=RoleEnum.ADMIN,
            senha_hash="hash_rubio"
        )
        repo.create_user(rubio)
        event = build_event(user_id='00000000-0000-0000-0000-000000000004')

        response = delete_user_presenter(event)
        body = json.loads(response['body'])

        assert response['statusCode'] == 200
        assert body['user_id'] == '00000000-0000-0000-0000-000000000004'
        assert body['user_email'] == 'rubio@maua.br'
        assert body['user_role'] == 'Admin'
        assert body['message'] == "the user was deleted successfully"

    def test_delete_user_presenter_delete_twice_returns_not_found(self):
        event = build_event(user_id='00000000-0000-0000-0000-000000000004')

        response = delete_user_presenter(event)

        assert response['statusCode'] == 404

    def test_delete_user_presenter_missing_id(self):
        event = build_event()

        response = delete_user_presenter(event)

        assert response['statusCode'] == 400
