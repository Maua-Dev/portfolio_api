import uuid

from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class DeleteProjectUsecase:
    def __init__(self, repo: IProjectRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self, project_id: str, user_from_authorizer: dict) -> Project:
        mail = user_from_authorizer.get("mail")
        try:
            if isinstance(mail, str) and mail.strip():
                # O sub Microsoft pode diferir do ID de um cadastro antigo.
                requester = self.user_repo.get_user_by_email(mail)
            else:
                # Compatibilidade com os testes e chamadas internas existentes.
                user_id = user_from_authorizer.get("user_id")
                if not user_id:
                    raise ForbiddenAction("user")
                requester = self.user_repo.get_user(id=uuid.UUID(user_id))
        except (NoItemsFound, ValueError, TypeError):
            raise ForbiddenAction("user") from None

        if requester.role != RoleEnum.ADMIN:
            raise ForbiddenAction("user")

        try:
            parsed_project_id = uuid.UUID(project_id)
        except (ValueError, TypeError):
            raise EntityError("project_id") from None

        return self.repo.delete_project(project_id=parsed_project_id)