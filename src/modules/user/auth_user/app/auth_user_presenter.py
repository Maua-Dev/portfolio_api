from .auth_user_controller import AuthUserController
from .auth_user_usecase import AuthUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

repo = Environments.get_user_repo()()
usecase = AuthUserUsecase(repo)
controller = AuthUserController(usecase)


def auth_user_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()


@observed_handler("auth_user")
def lambda_handler(event, context):
    response = auth_user_presenter(event)
    return response
