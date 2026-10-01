import uuid

from src.modules.user.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_CreateUserViewmodel:

    def test_create_user_viewmodel(self):
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            email="giulia@maua.br",
            role=RoleEnum.ADMIN,
        )

        viewmodel = CreateUserViewmodel(user)

        assert viewmodel.user_id == "00000000-0000-0000-0000-000000000001"
        assert viewmodel.user_email == "giulia@maua.br"
        assert viewmodel.user_role == RoleEnum.ADMIN

    def test_create_user_viewmodel_to_dict(self):
        user = User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            email="giulia@maua.br",
            role=RoleEnum.ADMIN,
        )

        viewmodel = CreateUserViewmodel(user)

        assert viewmodel.to_dict() == {
            'user_id': "00000000-0000-0000-0000-000000000001",
            'user_email': "giulia@maua.br",
            'user_role': "Admin",
            'message': "the user was created successfully"
        }
