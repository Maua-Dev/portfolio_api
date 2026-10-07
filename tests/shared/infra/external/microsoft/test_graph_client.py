import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import urllib3

from src.shared.infra.external.microsoft.graph_client import MicrosoftGraphClient


def test_graph_request_has_bounded_timeout_and_no_redirects():
    http = Mock()
    http.request.return_value = SimpleNamespace(
        status=200, data=json.dumps({"id": "test-id"}).encode()
    )
    client = MicrosoftGraphClient("https://graph.microsoft.com/v1.0/me", http)
    assert client.get_user_profile("test-token") == {"id": "test-id"}
    args, kwargs = http.request.call_args
    assert args == ("GET", "https://graph.microsoft.com/v1.0/me")
    assert kwargs["headers"] == {"Authorization": "Bearer test-token"}
    assert kwargs["retries"] is False
    assert kwargs["redirect"] is False
    assert isinstance(kwargs["timeout"], urllib3.Timeout)


@pytest.mark.parametrize("status, data", [
    (401, b"Unauthorized"),
    (403, b"Forbidden"),
    (200, b"not-json"),
    (200, b"[]"),
])
def test_graph_failure_or_invalid_response_is_rejected(status, data):
    http = Mock()
    http.request.return_value = SimpleNamespace(status=status, data=data)
    client = MicrosoftGraphClient("https://graph.microsoft.com/v1.0/me", http)
    with pytest.raises(ValueError):
        client.get_user_profile("test-token")