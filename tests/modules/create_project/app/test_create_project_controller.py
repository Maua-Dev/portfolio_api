from pydantic.color import Color
from src.modules.create_project.app.create_project_controller import CreateProjectController
from src.modules.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestCreateProjectController:
    def test_create_project_controller(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "title": "Projeto Teste 1",
            "description": "Descrição projeto teste 1",
            "cell_image": "imagem.jpeg",
            "tech_frontend": "React",
            "tech_backend": "Node.js",
            "color": "#FFFFFF"
                })

        response = controller(request)

        assert response.status_code == 201
        assert response.body["id"] == str(repo.projects[-1].id)
        assert response.body["title"] == repo.projects[-1].title
        assert response.body["description"] == repo.projects[-1].description
        assert response.body["cell_image"] == repo.projects[-1].cell_image
        assert response.body["tech_frontend"] == repo.projects[-1].tech_frontend
        assert response.body["tech_backend"] == repo.projects[-1].tech_backend
        assert response.body["color"] == str(repo.projects[-1].color)
        assert response.body["message"] == "the project was created successfully"
    

    def test_create_project_controller_missing_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "description": "Descrição projeto teste 1",
            "cell_image": "imagem.jpeg",
            "tech_frontend": "React",
            "tech_backend": "Node.js",
            "color": "#FFFFFF"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field title is missing"


    def test_create_project_controller_missing_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "title": "Projeto Teste 1",
            "cell_image": "imagem.jpeg",
            "tech_frontend": "React",
            "tech_backend": "Node.js",
            "color": "#FFFFFF"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field description is missing"


    def test_create_project_controller_missing_cell_image(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "title": "Projeto Teste 1",
            "description": "Descrição projeto teste 1",
            "tech_frontend": "React",
            "tech_backend": "Node.js",
            "color": "#FFFFFF"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field cell_image is missing"


    def test_create_project_controller_missing_tech_frontend(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "title": "Projeto Teste 1",
            "description": "Descrição projeto teste 1",
            "cell_image": "imagem.jpeg",
            "tech_backend": "Node.js",
            "color": "#FFFFFF"
        })

        response = controller(request=request)
        assert response.status_code == 400
        assert response.body == "Field tech_frontend is missing"


    def test_create_project_controller_missing_tech_backend(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "title": "Projeto Teste 1",
            "description": "Descrição projeto teste 1",
            "cell_image": "imagem.jpeg",
            "tech_frontend": "React",
            "color": "#FFFFFF"
        })

        response = controller(request=request)
        assert response.status_code == 400
        assert response.body == "Field tech_backend is missing"


    def test_create_project_controller_missing_color(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "title": "Projeto Teste 1",
            "description": "Descrição projeto teste 1",
            "cell_image": "imagem.jpeg",
            "tech_frontend": "React",
            "tech_backend": "Node.js"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field color is missing"