import argparse
import os

import boto3
import dotenv

from src.shared.environments import Environments, STAGE
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def setup_dynamo_table():
    envs = Environments.get_envs()
    table_name = envs.dynamo_table_name
    endpoint_url = envs.dynamo_endpoint_url
    pk = envs.dynamo_partition_key
    sk = envs.dynamo_sort_key

    print("Setting up DynamoDB table...")
    dynamo_client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    tables = dynamo_client.list_tables()["TableNames"]

    if table_name in tables:
        print("Table already exists!")
        return

    print("Creating table...")
    dynamo_client.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": pk, "KeyType": "HASH"},
            {"AttributeName": sk, "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": pk, "AttributeType": "S"},
            {"AttributeName": sk, "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    print("Waiting for table to be created...")
    dynamo_client.get_waiter("table_exists").wait(TableName=table_name)
    print(f'Table "{table_name}" created!')


def _load_users(dynamo_repo: UserRepositoryDynamo) -> int:
    mock_repo = UserRepositoryMock()
    count = 0

    print("Loading mock data to dynamo...")
    for user in mock_repo.get_all_user():
        print(f"Loading user {user.id} | {user.email} to dynamo")
        try:
            dynamo_repo.create_user(user)
            count += 1
        except DuplicatedItem:
            print(f"  user {user.id} already exists, skipping")

    print(f"{count} users loaded to dynamo!")
    return count


def load_mock_to_local_dynamo():
    """Create local table (if needed) and seed DynamoDB Local."""
    setup_dynamo_table()
    _load_users(UserRepositoryDynamo())


def load_mock_to_real_dynamo():
    """
    Seed an already-deployed AWS table.

    Run manually after `cdk deploy` on DEV/HOMOLOG.
    Does not create the table — CDK owns that.
    Blocks PROD by default.
    """
    envs = Environments.get_envs()
    if envs.stage == STAGE.PROD:
        raise RuntimeError(
            "Refusing to seed PROD. Use DEV or HOMOLOG (or override intentionally)."
        )

    print(
        f"Seeding AWS DynamoDB "
        f"(stage={envs.stage.value}, table={envs.dynamo_table_name}, region={envs.region})"
    )
    _load_users(UserRepositoryDynamo())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed User mock data into DynamoDB (local or AWS)."
    )
    parser.add_argument(
        "--target",
        choices=("local", "aws"),
        default="local",
        help="local = DynamoDB Local (+ create table). aws = table already deployed by CDK.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    dotenv.load_dotenv()
    args = _parse_args()

    if args.target == "local":
        os.environ.setdefault("STAGE", STAGE.TEST.value)
        load_mock_to_local_dynamo()
    else:
        load_mock_to_real_dynamo()
