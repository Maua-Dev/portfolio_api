from typing import List
from uuid import UUID
from pydantic.color import Color
from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.usecase_errors import (NoItemsFound, DuplicatedItem)

class ProjectRepositoryMock(IProjectRepository):
    projects: List[Project]

    def __init__(self):
        self.projects = [
            Project(
                title="Projeto Teste 1",
                description="Descrição projeto teste 1",
                cell_image="imagem_teste1.jpeg",  
                tech_frontend="React",
                tech_backend="Python",
                color=Color("#FFFFFF")
            ),
            Project(
                title="Projeto Teste 2",
                description="Descrição projeto teste 2",
                cell_image="imagem_teste2.jpeg",
                tech_frontend="HTML",
                tech_backend="Java",
                color=Color("#000000")
            ),
            Project(
                title="Projeto Teste 3",
                description="Descrição projeto teste 3",
                cell_image="imagem_teste3.jpeg",
                tech_frontend="React",
                tech_backend="C++",
                color=Color("#FF0000")
            )
        ]

    def get_project(self, project_id: UUID) -> Project:
        for project in self.projects:
            if project.id == project_id:
                return project
        raise NoItemsFound("project_id")

    def get_all_project(self) -> List[Project]:
        return self.projects

    def create_project(self, new_project: Project) -> Project:
        for project in self.projects:
            if project.id == new_project.id:
                raise DuplicatedItem("project_id")

        self.projects.append(new_project)
        return new_project

    def delete_project(self, project_id: UUID) -> Project:
        for index, project in enumerate(self.projects):
            if project.id == project_id:
                return self.projects.pop(index)

        raise NoItemsFound("project_id")

    def update_project(self, project: Project) -> Project:
        for index, current_project in enumerate(self.projects):
            if current_project.id == project.id:
                self.projects[index] = project
                return project

        raise NoItemsFound("project_id")