import uuid

# src/shared/domain/entities/project.py

import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Project(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Id único do projeto"
    )

    title: str = Field(
        ...,
        description="Título do projeto"
    )

    description: str = Field(
        ...,
        description="Descrição do projeto"
    )

    associates: Optional[list[uuid.UUID]] = Field(
        default=None,
        description="Lista de ID's dos usuários associados ao projeto"
    )

    display_image: Optional[str] = Field(
        default=None,
        description="URL ou path da imagem de exibição do projeto"
    )

    @field_validator("title")
    @classmethod
    def capitalize_title(cls, value: str) -> str:
        return value.capitalize()

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True,
    )