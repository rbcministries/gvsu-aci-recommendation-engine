import aws_cdk as core
import aws_cdk.assertions as assertions

from recommendation_engine_stack.recommendation_engine_stack_stack import RecommendationEngineStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in recommendation_engine_stack/recommendation_engine_stack_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RecommendationEngineStackStack(app, "recommendation-engine-stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
