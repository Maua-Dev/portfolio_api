from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Session(BaseModel):

    refresh_token: str = Field(
        ...,
        description="Refresh token da sessão"
    )

    user_id: UUID = Field(
        ...,
        description="Identificador do usuário associado à sessão"
    )

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )