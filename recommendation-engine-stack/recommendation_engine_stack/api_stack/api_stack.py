from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    NestedStack
)

# https://github.com/aws-samples/aws-cdk-examples/blob/master/python/api-cors-lambda/app.py
class ApiStack(NestedStack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #Create an API GW Rest API
        base_api = apigw.RestApi(self, 'ApiGW', rest_api_name='RecommendationAPI')

        #Create a resource named "example" on the base API
        api_resource = base_api.root.add_resource('example')

        # Sample code for initial setup of API - waiting for recommendation engine to be setup
        # to connect to that. Will probably be through a Lambda function would be my guess.
        example_lambda = _lambda.Function(self, "ApiSampleLambda",
                                         handler='lambda_handler.handler',
                                         code=_lambda.Code.from_asset('lambda'))

        example_entity_lambda_integration = apigw.LambdaIntegration(
            example_lambda,
            proxy=False,
            integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                }
            }]
        )

        api_resource.add_method(
            'GET', example_entity_lambda_integration,
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': True,
                }
            }]
        )