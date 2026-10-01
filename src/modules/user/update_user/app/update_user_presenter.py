from .update_user_controller import UpdateUserController
from .update_user_usecase import UpdateUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.observability.wrap_handler import observed_handler

repo = Environments.get_user_repo()()
usecase = UpdateUserUsecase(repo)
controller = UpdateUserController(usecase)


@observed_handler("update_user")
def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
