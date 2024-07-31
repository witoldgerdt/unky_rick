import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const artifactBucket = new s3.Bucket(this, 'PipelineArtifactsBucket');
    const sourceOutput = new codepipeline.Artifact();
    const buildOutput = new codepipeline.Artifact();

    const pipelineRole = new iam.Role(this, 'PipelineRole', {
      assumedBy: new iam.ServicePrincipal('codepipeline.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodePipeline_FullAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodeBuildAdminAccess')
      ],
    });

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
                },
              }),
              input: sourceOutput,
              outputs: [buildOutput],
            }),
          ],
        },
      ],
    });

    const dbCredentialsSecret = secretsmanager.Secret.fromSecretNameV2(this, 'DBCredentials', 'prod/DATABASE_URL');

    const initDbFunction = new lambda.Function(this, 'InitDbFunction', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        const { Client } = require('pg');
        exports.handler = async function(event) {
          const client = new Client({
            connectionString: process.env.DATABASE_URL,
          });
          await client.connect();
          await client.query(\`
            CREATE TABLE IF NOT EXISTS data_status (
              id SERIAL PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              status BOOLEAN NOT NULL DEFAULT TRUE
            );
          \`);
          await client.end();
        };
      `),
      environment: {
        DATABASE_URL: dbCredentialsSecret.secretValue.toString(),
      },
    });

    dbCredentialsSecret.grantRead(initDbFunction);

    new events.Rule(this, 'PipelineSucceededRule', {
      eventPattern: {
        source: ['aws.codepipeline'],
        detailType: ['CodePipeline Pipeline Execution State Change'],
        detail: {
          state: ['SUCCEEDED'],
          pipeline: [pipeline.pipelineName],
        },
      },
      targets: [new targets.LambdaFunction(initDbFunction)],
    });
  }
}
