from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
)

class TopicAnalysisStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        build_model_lambda = lambda_.Function(
            self, 'BuildModelHandler',
            runtime=lambda_.Runtime.PYTHON_3_7,
            code=lambda_.Code.from_asset('./sagemaker/lambda'),
            handler='build_model.handler'
        )