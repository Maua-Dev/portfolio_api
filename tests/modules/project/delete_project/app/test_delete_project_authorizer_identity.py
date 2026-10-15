import pytest

from src.modules.project.delete_project.app.delete_project_usecase import DeleteProjectUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def test_existing_admin_is_resolved_by_user_id():
    projects = ProjectRepositoryMock()
    users = UserRepositoryMock()
    project_id = projects.projects[0].id
    admin_id = str(users.users[0].id)

    result = DeleteProjectUsecase(projects, users)(
        str(project_id),
        {
            "sub": admin_id,
            "mail": "soller@maua.br",
            "name": "Admin",
        },
    )

    assert result.id == project_id


@pytest.mark.parametrize("email", ["brancas@maua.br", "unknown@maua.br"])
def test_claimed_admin_role_does_not_grant_permission(email):
    projects = ProjectRepositoryMock()
    users = UserRepositoryMock()
    regular_user_id = str(users.users[1].id)

    with pytest.raises(ForbiddenAction):
        DeleteProjectUsecase(projects, users)(
            str(projects.projects[0].id),
            {
                "sub": regular_user_id,
                "mail": email,
                "role": "Admin",
            },
        )

    assert len(projects.projects) == 3