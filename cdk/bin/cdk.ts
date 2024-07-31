#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CdkStack } from '../lib/cdk-stack';
import { PipelineStack } from '../lib/pipeline-stack';

const app = new cdk.App();
new CdkStack(app, 'CdkStack');
new PipelineStack(app, 'PipelineStack');
