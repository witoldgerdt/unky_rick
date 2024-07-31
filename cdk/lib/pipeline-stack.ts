import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const artifactBucket = new s3.Bucket(this, 'PipelineArtifactsBucket');

    const sourceOutput = new codepipeline.Artifact();

    const role = new iam.Role(this, 'PipelineRole', {
      assumedBy: new iam.ServicePrincipal('codepipeline.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodePipeline_FullAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodeBuildAdminAccess')
      ],
    });

    new codepipeline.Pipeline(this, 'Pipeline', {
      artifactBucket,
      role: role,
      stages: [
        {
          stageName: 'Source',
          actions: [
            new codepipeline_actions.GitHubSourceAction({
              actionName: 'GitHub_Source',
              owner: 'witoldgerdt',  
              repo: 'unky_rick',       
              oauthToken: cdk.SecretValue.secretsManager('prod/GITHUB_TOKEN', { jsonField: 'github-token' }),
              output: sourceOutput,
              branch: 'main',
            }),
          ],
        },
        {
          stageName: 'Build',
          actions: [
            new codepipeline_actions.CodeBuildAction({
              actionName: 'Build',
              project: new codebuild.PipelineProject(this, 'BuildProject', {
                environment: {
                  buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
                },
              }),
              input: sourceOutput,
              outputs: [new codepipeline.Artifact()],
            }),
          ],
        },
      ],
    });
  }
}
