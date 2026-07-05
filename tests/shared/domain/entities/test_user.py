import uuid

import pytest
from pydantic import ValidationError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_User:
    def test_user(self):
        user = User(
            email="ana@maua.br",
            role=RoleEnum.ADMIN,
            senha_hash="hash_secreto_123",
        )

        assert isinstance(user.id, uuid.UUID)
        assert user.email == "ana@maua.br"
        assert user.role == "Admin"  # use_enum_values=True guarda o valor do enum
        assert user.senha_hash == "hash_secreto_123"

    def test_user_id_is_generated_and_unique(self):
        user1 = User(email="a@maua.br", senha_hash="h1")
        user2 = User(email="b@maua.br", senha_hash="h2")

        assert isinstance(user1.id, uuid.UUID)
        assert user1.id != user2.id

    def test_user_id_can_be_passed(self):
        meu_id = uuid.uuid4()
        user = User(id=meu_id, email="a@maua.br", senha_hash="h1")

        assert user.id == meu_id

    def test_user_role_default_is_user(self):
        user = User(email="a@maua.br", senha_hash="h1")

        assert user.role == RoleEnum.USER
        assert user.role == "User"

    def test_user_role_accepts_valid_string(self):
        user = User(email="a@maua.br", role="Admin", senha_hash="h1")

        assert user.role == RoleEnum.ADMIN

    def test_user_email_is_not_valid(self):
        with pytest.raises(ValidationError):
            User(email="isso_nao_e_email", senha_hash="h1")

    def test_user_email_is_required(self):
        with pytest.raises(ValidationError):
            User(senha_hash="h1")

    def test_user_senha_hash_is_required(self):
        with pytest.raises(ValidationError):
            User(email="a@maua.br")

    def test_user_role_is_not_valid(self):
        with pytest.raises(ValidationError):
            User(email="a@maua.br", role="Superuser", senha_hash="h1")

    def test_user_extra_field_is_forbidden(self):
        with pytest.raises(ValidationError):
            User(email="a@maua.br", senha_hash="h1", campo_inexistente="x")
