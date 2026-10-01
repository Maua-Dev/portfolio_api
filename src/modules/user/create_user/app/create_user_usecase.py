from pydantic import ValidationError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class CreateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, role: str = RoleEnum.USER.value) -> User:
        if type(email) != str:
            raise EntityError("email")

        try:
            user = User(
                email=email,
                role=role
            )
        except ValidationError:
            raise EntityError("user")

        return self.repo.create_user(user)
