from abc import ABC, abstractmethod
from uuid import UUID

from src.shared.domain.entities.session import Session


class ISessionRepository(ABC):

    @abstractmethod
    def create_session(self, session: Session) -> Session:
        """
        If session already exists raise DuplicatedItem.
        """
        pass

    @abstractmethod
    def update_session(self, session: Session) -> Session:
        """
        If session not found raise NoItemsFound.
        """
        pass

    @abstractmethod
    def delete_session(self, user_id: UUID) -> Session:
        """
        If session not found raise NoItemsFound.
        """
        pass

    @abstractmethod
    def get_session(self, user_id: UUID) -> Session:
        """
        If session not found raise NoItemsFound.
        """
        pass