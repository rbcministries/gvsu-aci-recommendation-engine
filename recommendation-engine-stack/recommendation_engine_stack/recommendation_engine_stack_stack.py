from aws_cdk import (
    Stack
)
from constructs import Construct
from cloud_watch.cloud_watch import CloudWatchStack

class RecommendationEngineStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CloudWatchStack(self, "CloudWatch")