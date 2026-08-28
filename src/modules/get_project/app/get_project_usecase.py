import uuid


from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.domain_errors import EntityError



class GetProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self, project_id: uuid.UUID) -> Project:
        if type(project_id) != uuid.UUID:
            raise EntityError("project_id")
        return self.repo.get_project(project_id)