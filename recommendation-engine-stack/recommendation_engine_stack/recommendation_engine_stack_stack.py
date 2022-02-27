from aws_cdk import (
    Stack,
)
from constructs import Construct
from api_stack.api_stack import ApiStack

class RecommendationEngineStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApiStack(self, "ApiStack")
