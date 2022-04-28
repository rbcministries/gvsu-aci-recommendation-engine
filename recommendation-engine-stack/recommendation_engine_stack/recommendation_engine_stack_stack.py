from aws_cdk import (
    Stack,
)
from constructs import Construct
<<<<<<< HEAD
# from datalake_stack.datalake_stack import DatalakeStack
from .api.api_stack import ApiStack
=======
from datalake_stack.datalake_stack import DatalakeStack
from api_stack.api_stack import ApiStack
from cloud_watch.cloud_watch import CloudWatchStack
>>>>>>> a4cad9f14c3ef740bf2556fe6f6964f43943cd8e

class RecommendationEngineStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

<<<<<<< HEAD
        # DatalakeStack(self, "DataLakeStack")
        ApiStack(self, "ApiStack")
=======
        DatalakeStack(self, "DataLakeStack")
        api_stack = ApiStack(self, "ApiStack")
        CloudWatchStack(self, "CloudWatch", api_stack.api_resource)
>>>>>>> a4cad9f14c3ef740bf2556fe6f6964f43943cd8e
