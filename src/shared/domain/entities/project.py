import uuid

from pydantic import BaseModel, Field, ConfigDict
from pydantic.color import Color

class Project(BaseModel):
    id:uuid.UUID = Field(default_factory=uuid.uuid4, 
    description="Identificador único do projeto")

    title:str = Field(..., 
    description="Titulo do projeto")

    description:str = Field(..., 
    description="Descrição do projeto")

    cell_image:str = Field(..., 
    description="Imagem de capa do projeto")

    tech_frontend:str = Field(..., 
    description="Tecnologias utilizadas no frontend do projeto")

    tech_backend:str = Field(..., 
    description="Tecnologias utilizadas no backend do projeto")

    color: Color= Field(...,
    description="Cor do projeto")

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )