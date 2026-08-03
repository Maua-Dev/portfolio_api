from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class IProjectRepository(ABC):

    @abstractmethod
    def get_project(self, project_id: UUID) -> Project:
        """
        If project not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_all_project(self) -> List[Project]:
        pass

    @abstractmethod
    def create_project(self, new_project: Project) -> Project:
        """
        If project already exists raise DuplicatedItem
        """
        pass

    @abstractmethod
    def delete_project(self, project_id: UUID) -> Project:
        """
        If project not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def update_project(self, project: Project) -> Project:
        """
        If project not found raise NoItemsFound
        """
        pass