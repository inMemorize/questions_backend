from aws_cdk import (
    core
)
from questions_backend.questions_backend_stack import QuestionBackendStack


class PipelineStage(core.Stage):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        QuestionBackendStack(self, self.node.try_get_context('service_name') + '-stack')