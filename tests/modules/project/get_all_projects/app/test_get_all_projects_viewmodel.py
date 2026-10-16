from src.modules.project.get_all_projects.app.get_all_projects_viewmodel import GetAllProjectsViewmodel
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock

class Test_GetAllProjectsViewmodel:
    def test_get_all_projects_viewmodel(self):
        repo = ProjectRepositoryMock()
        projects = repo.get_all_project()
        viewmodel = GetAllProjectsViewmodel(projects=projects)
        
        expected = {
            'projects': [
                {
                    'project_id': str(projects[0].id),
                    'project_title': 'Projeto Teste 1',
                    'project_description': 'Descrição projeto teste 1',
                    'project_cell_image': 'imagem_teste1.jpeg',
                    'project_tech_frontend': 'React',
                    'project_tech_backend': 'Python',
                    'project_color': str(projects[0].color)
                },
                {
                    'project_id': str(projects[1].id),
                    'project_title': 'Projeto Teste 2',
                    'project_description': 'Descrição projeto teste 2',
                    'project_cell_image': 'imagem_teste2.jpeg',
                    'project_tech_frontend': 'HTML',
                    'project_tech_backend': 'Java',
                    'project_color': str(projects[1].color)
                },
                {
                    'project_id': str(projects[2].id),
                    'project_title': 'Projeto Teste 3',
                    'project_description': 'Descrição projeto teste 3',
                    'project_cell_image': 'imagem_teste3.jpeg',
                    'project_tech_frontend': 'React',
                    'project_tech_backend': 'C++',
                    'project_color': str(projects[2].color)
                }
            ],
            'message': "projects were retreived successfully"
        }
        
        assert viewmodel.to_dict() == expected
