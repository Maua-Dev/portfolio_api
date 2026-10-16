import json
import os

os.environ["STAGE"] = "TEST"

from src.modules.project.delete_project.app.delete_project_presenter import (
    lambda_handler,
    repo,
    user_repo,
)


def test_delete_project_with_verified_admin():
    project_id = str(repo.projects[0].id)
    admin = user_repo.users[0]
    event = {
        "httpMethod": "DELETE",
        "path": "/portfolio/delete-project",
        "requestContext": {
            "authorizer": {
                "user": json.dumps({
                    "sub": str(admin.id),
                    "mail": admin.email,
                    "name": "Admin",
                }),
            },
        },
        "body": json.dumps({"project_id": project_id}),
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"])["message"] == (
        "the project was deleted successfully"
    )