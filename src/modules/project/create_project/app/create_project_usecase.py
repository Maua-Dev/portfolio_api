from pydantic.color import Color
from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository

class CreateProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self,title: str,description: str,cell_image: str,tech_frontend: str,tech_backend: str,color: Color) -> Project:

        new_project = Project(
            title=title,
            description=description,
            cell_image=cell_image,
            tech_frontend=tech_frontend,
            tech_backend=tech_backend,
            color=color,
        )
        return self.repo.create_project(new_project=new_project)