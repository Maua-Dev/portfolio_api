from uuid import UUID

import pytest

from src.modules.user.auth_user.app.auth_user_viewmodel import AuthUserViewmodel
from src.shared.domain.entities.user import User


@pytest.mark.parametrize("created, message", [
    (True, "the user was created successfully"),
    (False, "the user was retrieved successfully"),
])
def test_serializes_user_and_login_result(created, message):
    user = User(
        id=UUID("00000000-0000-0000-0000-000000000099"),
        email="leo@maua.br",
    )
    assert AuthUserViewmodel(user, created).to_dict() == {
        "user_id": str(user.id),
        "user_email": "leo@maua.br",
        "user_role": "User",
        "created": created,
        "message": message,
    }