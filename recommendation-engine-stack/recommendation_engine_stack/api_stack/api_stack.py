from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    NestedStack
)

# https://github.com/aws-samples/aws-cdk-examples/blob/master/python/api-cors-lambda/app.py
class ApiStack(NestedStack):

    def __init__(self, scope: Construct, id: str, 
        content_type: str, endpoint: sagemaker.CfnEndpoint, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Sample code for initial setup of API - waiting for recommendation engine to be setup
        # to connect to that. Will probably be through a Lambda function would be my guess.
        recommendation_fn = _lambda.Function(self, "ApiSageMakerLambda",
                                         handler='lambda_handler.handler',
                                         code=_lambda.Code.from_asset('lambda'),
                                         environment={"endpoint_name": endpoint.endpoint_name, 
                                                    "content_type": content_type})

        recommendation_fn.add_to_role_policy(iam.PolicyStatement(actions=['sagemaker:InvokeEndpoint',],
            resources = [endpoint.get_att('Arn'),]))

        # Create an API GW Rest API
        # base_api = apigw.RestApi(self, 'ApiGW', rest_api_name='RecommendationAPI')
        self.recommendation_api = apigw.LambdaRestApi(self, "RecommendationApi", handler=recommendation_fn, proxy=True)

        # Not needed with proxy. This will probably need to be changed but needs specifications.
        # I think mostly for 
        # api_resource = lambda_api.root.add_resource('recommendation')

        # api_resource.add_method(
        #     'GET', example_entity_lambda_integration,
        #     method_responses=[{
        #         'statusCode': '200',
        #         'responseParameters': {
        #             'method.response.header.Access-Control-Allow-Origin': True,
        #         }
        #     }]
        # )