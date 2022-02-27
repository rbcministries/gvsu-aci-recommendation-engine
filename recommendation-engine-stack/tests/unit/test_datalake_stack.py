import aws_cdk as core
import aws_cdk.assertions as assertions

from datalake.datalake_stack import DatalakeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in datalake/datalake_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DatalakeStack(app, "datalake")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
