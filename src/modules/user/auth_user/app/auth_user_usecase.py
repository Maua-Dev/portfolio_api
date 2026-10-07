import re
from uuid import UUID

from pydantic import ValidationError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound


class AuthUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_from_authorizer: dict) -> tuple[User, bool]:
        if not isinstance(user_from_authorizer, dict):
            raise EntityError("user_from_authorizer")

        sub = user_from_authorizer.get("sub")
        mail = user_from_authorizer.get("mail")
        name = user_from_authorizer.get("name")

        if (
            not isinstance(sub, str)
            or not isinstance(mail, str)
            or not isinstance(name, str)
        ):
            raise EntityError("user_from_authorizer")

        mail = mail.strip().lower()
        if re.fullmatch(r"[^@\s]+@maua\.br", mail) is None:
            raise EntityError("mail")

        try:
            new_user = User(
                id=UUID(sub.strip()),
                email=mail,
                role=RoleEnum.USER,
            )
        except (ValueError, ValidationError):
            raise EntityError("user_from_authorizer") from None

        try:
            # Preserva ID e role de usuários já cadastrados.
            return self.repo.get_user_by_email(new_user.email), False
        except NoItemsFound:
            pass

        try:
            return self.repo.create_user(new_user), True
        except DuplicatedItem:
            # Outra chamada pode ter cadastrado o mesmo usuário neste intervalo.
            return self.repo.get_user_by_email(new_user.email), False