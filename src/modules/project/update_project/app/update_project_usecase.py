from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from pydantic.color import Color

import uuid



class UpdateProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self, project_id: uuid.UUID, title: str = None, description: str = None,
    cell_image: str = None, tech_frontend: str = None, tech_backend: str = None, color: Color = None) -> Project:

        if type(project_id) != uuid.UUID:
            raise EntityError("project_id")
        
        project = self.repo.get_project(project_id=project_id)

        updated_project = Project(
            id = project.id,
            title = title if title is not None else project.title,
            description = description if description is not None else project.description,
            cell_image = cell_image if cell_image is not None else project.cell_image,
            tech_frontend = tech_frontend if tech_frontend is not None else project.tech_frontend,
            tech_backend = tech_backend if tech_backend is not None else project.tech_backend,
            color = color if color is not None else project.color

        )

        return self.repo.update_project(project=updated_project)