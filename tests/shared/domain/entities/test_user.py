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
       )

       assert isinstance(user.id, uuid.UUID)
       assert user.email == "ana@maua.br"
       assert user.role == "Admin"  # use_enum_values=True guarda o valor do enum

   def test_user_id_is_generated_and_unique(self):
       user1 = User(email="a@maua.br")
       user2 = User(email="b@maua.br")

       assert isinstance(user1.id, uuid.UUID)
       assert user1.id != user2.id

   def test_user_id_can_be_passed(self):
       meu_id = uuid.uuid4()
       user = User(id=meu_id, email="a@maua.br")

       assert user.id == meu_id

   def test_user_role_default_is_user(self):
       user = User(email="a@maua.br")

       assert user.role == RoleEnum.USER
       assert user.role == "User"

   def test_user_role_accepts_valid_string(self):
       user = User(email="a@maua.br", role="Admin")

       assert user.role == RoleEnum.ADMIN

   def test_user_email_is_not_valid(self):
       with pytest.raises(ValidationError):
           User(email="isso_nao_e_email")

   def test_user_email_is_required(self):
       with pytest.raises(ValidationError):
           User()

   def test_user_role_is_not_valid(self):
       with pytest.raises(ValidationError):
           User(email="a@maua.br", role="Superuser")

   def test_user_extra_field_is_forbidden(self):
       with pytest.raises(ValidationError):
           User(email="a@maua.br", campo_inexistente="x")
