import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class PipelineStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // Define the pipeline
        const pipeline = new codepipeline.Pipeline(this, 'Pipeline', {
            pipelineName: 'MyPipeline',
        });

        // Define the source stage
        const sourceOutput = new codepipeline.Artifact();
        pipeline.addStage({
            stageName: 'Source',
            actions: [
                new codepipeline_actions.GitHubSourceAction({
                    actionName: 'GitHub_Source',
                    owner: 'OWNER',
                    repo: 'REPO',
                    branch: 'main',
                    oauthToken: cdk.SecretValue.secretsManager('prod/GITHUB_TOKEN'),
                    output: sourceOutput,
                }),
            ],
        });

        // Define the build stage
        const buildOutput = new codepipeline.Artifact();
        pipeline.addStage({
            stageName: 'Build',
            actions: [
                new codepipeline_actions.CodeBuildAction({
                    actionName: 'CodeBuild',
                    project: new codebuild.PipelineProject(this, 'BuildProject'),
                    input: sourceOutput,
                    outputs: [buildOutput],
                }),
            ],
        });
    }
}
