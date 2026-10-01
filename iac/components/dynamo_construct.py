from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

# Manter alinhado com src.shared.infra.external.dynamo/..._naming/..._TABLE_PREFIX
_PORTFOLIO_TABLE_PREFIX = "PortfolioTable"

RETAINED_STAGES = {"prod", "homolog"}


class DynamoConstruct(Construct):

    portfolio_table: dynamodb.Table

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage_lower = stage.lower()

        removal_policy = (
            RemovalPolicy.RETAIN if stage_lower in RETAINED_STAGES else RemovalPolicy.DESTROY
        )

        self.portfolio_table = dynamodb.Table(
            self,
            id="PortfolioTable",
            partition_key=dynamodb.Attribute(
                name="pk",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="sk",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            table_name=f"{_PORTFOLIO_TABLE_PREFIX}-{stage_lower}",
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=(stage_lower == "prod")
            ),
        )