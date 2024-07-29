import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPC
    const vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2,
    });

    // Security Group for EC2
    const ec2SecurityGroup = new ec2.SecurityGroup(this, 'Ec2SecurityGroup', {
      vpc,
      allowAllOutbound: true,
    });

    ec2SecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP');
    ec2SecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'Allow HTTPS');
    ec2SecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'Allow SSH');

    // Security Group for RDS
    const rdsSecurityGroup = new ec2.SecurityGroup(this, 'RdsSecurityGroup', {
      vpc,
      allowAllOutbound: true,
    });

    rdsSecurityGroup.addIngressRule(ec2.Peer.securityGroupId(ec2SecurityGroup.securityGroupId), ec2.Port.tcp(5432), 'Allow PostgreSQL from EC2');

    // RDS Instance
    const dbInstance = new rds.DatabaseInstance(this, 'RDSInstance', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_16_3 // Updated to PostgreSQL 15
      }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO), // Using T3 instance class
      vpc,
      securityGroups: [rdsSecurityGroup],
      multiAz: false,
      allocatedStorage: 100, // Updated storage size to a valid value
      storageType: rds.StorageType.GP2,
      cloudwatchLogsExports: ['postgresql'],
      deletionProtection: false,
      publiclyAccessible: false,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      credentials: rds.Credentials.fromGeneratedSecret('postgres'), // Generated credentials
    });

    // Create a secret to store the database credentials
    const databaseSecret = new secretsmanager.Secret(this, 'DatabaseSecret', {
      secretName: 'DatabaseCredentials',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          username: dbInstance.secret?.secretValueFromJson('username')?.unsafeUnwrap() || 'postgres'
        }),
        generateStringKey: 'password',
      }
    });

    // IAM Role for EC2
    const role = new iam.Role(this, 'InstanceSSMRole', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('SecretsManagerReadWrite')
      ],
    });

    // EC2 Instance with User Data
    const instance = new ec2.Instance(this, 'EC2Instance', {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      machineImage: ec2.MachineImage.latestAmazonLinux2(),
      securityGroup: ec2SecurityGroup,
      role,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC,
      },
    });

    instance.userData.addCommands(
      'yum update -y',
      'yum install -y python3 python3-pip',
      'pip3 install virtualenv',
      'mkdir -p /var/www/unky_rick',
      'chown -R ec2-user:ec2-user /var/www/unky_rick'
    );

    // Output the database endpoint and secret ARN
    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: dbInstance.dbInstanceEndpointAddress,
    });

    new cdk.CfnOutput(this, 'DatabaseSecretARN', {
      value: databaseSecret.secretArn,
    });

    new cdk.CfnOutput(this, 'DatabaseName', {
      value: dbInstance.instanceIdentifier,
    });
  }
}

