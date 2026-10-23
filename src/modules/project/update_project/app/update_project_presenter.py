import uuid

from src.modules.project.update_project.app.update_project_controller import UpdateProjectController
from src.modules.project.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler




repo = Environments.get_project_repo()()
usecase = UpdateProjectUsecase(repo)
controller = UpdateProjectController(usecase)


def update_project_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()


@observed_handler("update_project")
def lambda_handler(event, context):
    response = update_project_presenter(event)
    return response