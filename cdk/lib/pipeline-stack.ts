import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codedeploy from 'aws-cdk-lib/aws-codedeploy';

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Source stage
    const sourceOutput = new codepipeline.Artifact();
    const sourceAction = new codepipeline_actions.GitHubSourceAction({
      actionName: 'GitHub_Source',
      owner: 'your-github-username',
      repo: 'your-repo-name',
      oauthToken: cdk.SecretValue.secretsManager('github-token'),
      output: sourceOutput,
      branch: 'main'
    });

    // Build stage
    const buildProject = new codebuild.PipelineProject(this, 'BuildProject', {
      buildSpec: codebuild.BuildSpec.fromSourceFilename('buildspec.yml')
    });
    const buildOutput = new codepipeline.Artifact();
    const buildAction = new codepipeline_actions.CodeBuildAction({
      actionName: 'CodeBuild',
      project: buildProject,
      input: sourceOutput,
      outputs: [buildOutput]
    });

    // Deploy stage (to prepare DB)
    const dbDeployAction = new codepipeline_actions.CodeBuildAction({
      actionName: 'DBDeploy',
      project: buildProject,
      input: sourceOutput,
      outputs: [buildOutput],
      environmentVariables: {
        'STAGE': {
          value: 'prepare_db'
        }
      }
    });

    // Deploy stage (to deploy the app)
    const deployAction = new codepipeline_actions.CodeDeployServerDeployAction({
      actionName: 'CodeDeploy',
      input: buildOutput,
      deploymentGroup: codedeploy.ServerDeploymentGroup.fromServerDeploymentGroupAttributes(this, 'CodeDeployGroup', {
        application: codedeploy.ServerApplication.fromServerApplicationName(this, 'unky_rick_app', 'unky_rick_app'),
        deploymentGroupName: 'unky_rick_deployment_group',
      }),
    });

    // Define the pipeline
    new codepipeline.Pipeline(this, 'Pipeline', {
      stages: [
        {
          stageName: 'Source',
          actions: [sourceAction]
        },
        {
          stageName: 'Build',
          actions: [buildAction]
        },
        {
          stageName: 'DBDeploy',
          actions: [dbDeployAction]
        },
        {
          stageName: 'Deploy',
          actions: [deployAction]
        }
      ]
    });
  }
}

const app = new cdk.App();
new PipelineStack(app, 'PipelineStack');
app.synth();
