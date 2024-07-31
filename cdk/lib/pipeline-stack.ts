import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket to store pipeline artifacts
    const artifactBucket = new s3.Bucket(this, 'PipelineArtifactsBucket');
    const sourceOutput = new codepipeline.Artifact();
    const buildOutput = new codepipeline.Artifact();

    // IAM role for the pipeline with necessary permissions
    const pipelineRole = new iam.Role(this, 'PipelineRole', {
      assumedBy: new iam.ServicePrincipal('codepipeline.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodePipeline_FullAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodeBuildAdminAccess')
      ],
    });

    // Define the CodePipeline with Source and Build stages
    const pipeline = new codepipeline.Pipeline(this, 'Pipeline', {
      artifactBucket,
      role: pipelineRole,
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
                  environmentVariables: {
                    DATABASE_URL: { value: cdk.SecretValue.secretsManager('prod/DATABASE_URL').unsafeUnwrap() },
                  },
                },
                buildSpec: codebuild.BuildSpec.fromSourceFilename('buildspec.yml'),
              }),
              input: sourceOutput,
              outputs: [buildOutput],
            }),
          ],
        },
      ],
    });

    // Fetch database credentials from AWS Secrets Manager
    const dbCredentialsSecret = secretsmanager.Secret.fromSecretNameV2(this, 'DBCredentials', 'prod/DATABASE_URL');
    
    // Grant permissions for CodeBuild to read from Secrets Manager
    dbCredentialsSecret.grantRead(pipelineRole);
  }
}
