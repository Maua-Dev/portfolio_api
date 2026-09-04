from src.shared.domain.entities.project import Project

class CreateProjectViewmodel:
    id: str
    title: str
    description: str
    cell_image: str
    tech_frontend: str
    tech_backend: str
    color: str

    def __init__(self, project: Project):
        self.id = str(project.id)
        self.title = project.title
        self.description = project.description
        self.cell_image = project.cell_image
        self.tech_frontend = project.tech_frontend
        self.tech_backend = project.tech_backend
        self.color = self.color = project.color.as_hex().replace("#fff", "#FFFFFF")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cell_image': self.cell_image,
            'tech_frontend': self.tech_frontend,
            'tech_backend': self.tech_backend,
            'color': self.color,
            'message': "the project was created successfully"
        }