import uuid
from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(
                id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                email="soller@maua.br",
                role=RoleEnum.ADMIN,
                senha_hash="hash_soller"
            ),
            User(
                id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
                email="brancas@maua.br",
                role=RoleEnum.USER,
                senha_hash="hash_brancas"
            ),
            User(
                id=uuid.UUID("00000000-0000-0000-0000-000000000003"),
                email="vilas@maua.br",
                role=RoleEnum.USER,
                senha_hash="hash_vilas"
            )
        ]

    def get_user(self, id: uuid.UUID) -> User:
        for user in self.users:
            if user.id == id:
                return user

        raise NoItemsFound("id")

    def get_all_user(self) -> List[User]:
        return self.users

    def create_user(self, new_user: User) -> User:
        for user in self.users:
            if user.id == new_user.id or user.email == new_user.email:
                raise DuplicatedItem("user")

        self.users.append(new_user)
        return new_user

    def delete_user(self, id: uuid.UUID) -> User:
        for idx, user in enumerate(self.users):
            if user.id == id:
                return self.users.pop(idx)

        raise NoItemsFound("id")

    def update_user(self, user: User) -> User:
        for idx, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[idx] = user
                return user

        raise NoItemsFound("id")
