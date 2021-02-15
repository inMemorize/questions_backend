from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as actions,
    aws_codecommit as codecommit,
    aws_codebuild as codebuild,
    aws_ssm as ssm,
    pipelines,
    core
)
from pipeline_lib.pipeline_stage import PipelineStage
import os

STAGE = "dev"

class PipelineDevStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        sourceArtifact = codepipeline.Artifact()
        cloudAssemblyArtifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'Pipeline',
                                         pipeline_name=self.node.try_get_context(
                                             'repository_name') + "-{}-pipeline".format(STAGE),
                                         cloud_assembly_artifact=cloudAssemblyArtifact,
                                         source_action=actions.GitHubSourceAction(
                                            action_name='GitHub',
                                            output=sourceArtifact,
                                            oauth_token=core.SecretValue.secrets_manager('github-token'),
                                            owner=self.node.try_get_context(
                                             'owner'),
                                            repo=self.node.try_get_context(
                                             'repository_name'),
                                            branch=STAGE
                                        ),
                                         synth_action=pipelines.SimpleSynthAction(
                                             synth_command="cdk synth",
                                             install_commands=[
                                                 "pip install --upgrade pip",
                                                 "npm i -g aws-cdk",
                                                 "pip install -r requirements.txt"
                                             ],
                                             source_artifact=sourceArtifact,
                                             cloud_assembly_artifact=cloudAssemblyArtifact,
                                             environment={
                                                 'privileged': True
                                             },
                                             environment_variables={
                                                 'DEV_ACCOUNT_ID': codebuild.BuildEnvironmentVariable(value=os.environ['DEV_ACCOUNT_ID']),
                                                 'STG_ACCOUNT_ID': codebuild.BuildEnvironmentVariable(value=os.environ['STG_ACCOUNT_ID']),
                                                 'PROD_ACCOUNT_ID': codebuild.BuildEnvironmentVariable(value=os.environ['PROD_ACCOUNT_ID']),
                                                 'MANAGE_ACCOUNT_ID': codebuild.BuildEnvironmentVariable(value=os.environ['MANAGE_ACCOUNT_ID'])
                                             }
                                         )
                                         )

        dev = PipelineStage(
            self,
            self.node.try_get_context('repository_name') + "-{}".format(STAGE),
            env={
                'region': "ap-northeast-1",
                'account': os.environ['DEV_ACCOUNT_ID']
            }
        )

        dev_stage = pipeline.add_application_stage(dev)
