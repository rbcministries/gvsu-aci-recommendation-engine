from aws_cdk import (
    Stack,
)
from constructs import Construct
from datalake_stack.datalake_stack import DatalakeStack

class RecommendationEngineStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        DatalakeStack(self, "DataLakeStack")