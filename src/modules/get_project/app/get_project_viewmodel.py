from src.shared.domain.entities.project import Project
from pydantic.color import Color


class GetProjectViewmodel:
    project_id: str
    project_title: str 
    project_description: str
    project_cell_image: str
    project_tech_frontend: str
    project_tech_backend: str
    project_color: Color

    def __init__(self, project: Project):
        self.project_id = str(project.id)
        self.project_title = project.title
        self.project_description = project.description
        self.project_cell_image = project.cell_image
        self.project_tech_frontend = project.tech_frontend
        self.project_tech_backend = project.tech_backend 
        self.project_color = project.color

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'project_title': self.project_title,
            'project_description': self.project_description,
            'project_cell_image': self.project_cell_image,
            'project_tech_frontend': self.project_tech_frontend,
            'project_tech_backend': self.project_tech_backend,
            'project_color': str(self.project_color),
            'message': "the project was retrieved successfully"
        }