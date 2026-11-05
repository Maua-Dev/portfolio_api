from typing import List
from uuid import UUID

from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import (
    ISessionRepository,
)
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    NoItemsFound,
)


class SessionRepositoryMock(ISessionRepository):

    def __init__(self):
        self.sessions: List[Session] = []

    def get_session(self, user_id: UUID) -> Session:
        for session in self.sessions:
            if session.user_id == user_id:
                return session

        raise NoItemsFound("user_id")

    def create_session(self, session: Session) -> Session:
        for existing_session in self.sessions:
            if existing_session.user_id == session.user_id:
                raise DuplicatedItem("user_id")

        self.sessions.append(session)
        return session

    def update_session(self, session: Session) -> Session:
        for index, existing_session in enumerate(self.sessions):
            if existing_session.user_id == session.user_id:
                self.sessions[index] = session
                return session

        raise NoItemsFound("user_id")

    def delete_session(self, user_id: UUID) -> Session:
        for index, session in enumerate(self.sessions):
            if session.user_id == user_id:
                return self.sessions.pop(index)

        raise NoItemsFound("user_id")