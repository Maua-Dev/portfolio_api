import json
from typing import Any, Optional

import urllib3


class MicrosoftGraphClient:
    def __init__(
        self,
        graph_endpoint: str,
        http: Optional[urllib3.PoolManager] = None,
    ):
        self.graph_endpoint = graph_endpoint
        self.http = http if http is not None else urllib3.PoolManager()

    def get_user_profile(self, access_token: str) -> dict[str, Any]:
        response = self.http.request(
            "GET",
            self.graph_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=urllib3.Timeout(connect=3.0, read=5.0),
            retries=False,
            redirect=False,
        )

        if response.status != 200:
            raise ValueError(f"Microsoft Graph retornou status {response.status}")

        profile = json.loads(response.data.decode("utf-8"))
        if not isinstance(profile, dict):
            raise ValueError("Resposta inválida do Microsoft Graph")

        return profile