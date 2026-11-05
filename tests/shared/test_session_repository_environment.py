from types import SimpleNamespace

import pytest

from src.shared.environments import Environments, STAGE
from src.shared.infra.repositories.session_repository_dynamo import SessionRepositoryDynamo
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


def test_get_session_repo_returns_mock_on_test_stage(monkeypatch):
    monkeypatch.setattr(
        Environments,
        "get_envs",
        staticmethod(lambda: SimpleNamespace(stage=STAGE.TEST)),
    )

    assert Environments.get_session_repo() is SessionRepositoryMock


def test_get_session_repo_returns_dynamo_on_deployment_stages(monkeypatch):
    for stage in (STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD):
        monkeypatch.setattr(
            Environments,
            "get_envs",
            staticmethod(lambda stage=stage: SimpleNamespace(stage=stage)),
        )
        assert Environments.get_session_repo() is SessionRepositoryDynamo


def test_get_session_repo_rejects_unsupported_stage(monkeypatch):
    monkeypatch.setattr(
        Environments,
        "get_envs",
        staticmethod(lambda: SimpleNamespace(stage=STAGE.DOTENV)),
    )

    with pytest.raises(Exception, match="No session repository found for this stage"):
        Environments.get_session_repo()
