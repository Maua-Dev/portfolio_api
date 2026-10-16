import logging
import os

from .microsoft_authorizer_usecase import MicrosoftAuthorizerUsecase
from src.shared.helpers.auth.iam_policy import generate_policy
from src.shared.infra.external.microsoft.graph_client import MicrosoftGraphClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

graph_endpoint = (
    os.environ.get("GRAPH_MICROSOFT_ENDPOINT")
    or os.environ.get("MS_GRAPH_ENDPOINT")
    or "https://graph.microsoft.com/v1.0/me"
)
graph_client = MicrosoftGraphClient(graph_endpoint=graph_endpoint)
usecase = MicrosoftAuthorizerUsecase(graph_client=graph_client)


def lambda_handler(event, context):
    method_arn = event.get("methodArn")
    if not isinstance(method_arn, str) or not method_arn:
        raise ValueError("methodArn ausente no evento do authorizer")

    try:
        return usecase(
            authorization_token=event.get("authorizationToken"),
            method_arn=method_arn,
        )
    except Exception as err:
        # Não registra o evento, o token nem o corpo da resposta do Graph.
        logger.warning("Autorização negada (%s)", type(err).__name__)
        return generate_policy("user", "Deny", method_arn)