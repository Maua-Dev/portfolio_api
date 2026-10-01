from src.modules.delete_project.app.delete_project_viewmodel import DeleteProjectViewmodel
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

class TestDeleteProjectViewmodel:
    def test_delete_project_viewmodel(self):
        repo = ProjectRepositoryMock()
        project = repo.projects[0]
        
        viewmodel = DeleteProjectViewmodel(project)
        
        expected = {
            'id': str(project.id),
            'title': project.title,
            'description': project.description,
            'cell_image': project.cell_image,
            'tech_frontend': project.tech_frontend,
            'tech_backend': project.tech_backend,
            'color': project.color.as_hex().replace("#fff", "#FFFFFF"),
            'message': "the project was deleted successfully"
        }
        
        assert viewmodel.to_dict() == expected
