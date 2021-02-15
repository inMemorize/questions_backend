from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_logs as logs,
)

class QuestionBackendStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # questions_backend_func = lambda_.Function(self, "HelloAppFunction",
        #                                       code=lambda_.Code.from_asset('functions/hello'),
        #                                       handler="index.lambda_handler",
        #                                       runtime=lambda_.Runtime.PYTHON_3_8,
        #                                       tracing=lambda_.Tracing.ACTIVE,
        #                                       timeout=core.Duration.seconds(29),
        #                                       memory_size=128,
        #                                       )

        # logs.LogGroup(self, 'HelloAppFunctionLogGroup',
        #               log_group_name='/aws/lambda/' + questions_backend.function_name,
        #               retention=logs.RetentionDays.TWO_WEEKS
        #               )