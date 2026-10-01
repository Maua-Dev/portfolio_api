from .delete_project_controller import DeleteProjectController
from .delete_project_usecase import DeleteProjectUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
import json

repo = Environments.get_project_repo()()
user_repo = Environments.get_user_repo()()
usecase = DeleteProjectUsecase(repo=repo, user_repo=user_repo)
controller = DeleteProjectController(usecase)

def lambda_handler(event, context):
    from pprint import pprint
    pprint(event)

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()
