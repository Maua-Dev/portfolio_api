import uuid
from typing import Tuple

from pydantic import ValidationError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class AuthUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: uuid.UUID, email: str) -> Tuple[User, bool]:
        if type(user_id) != uuid.UUID:
            raise EntityError("user_id")

        if type(email) != str:
            raise EntityError("email")

        try:
            return self.repo.get_user(user_id), False
        except NoItemsFound:
            try:
                user = User(
                    id=user_id,
                    email=email,
                    role=RoleEnum.USER.value
                )
            except ValidationError:
                raise EntityError("user")

            return self.repo.create_user(user), True
