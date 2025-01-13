# Class for providing a set of AWS utility functions. This is considered to be 
# a low-level routine that can not import any higher-level routines. The ban on 
# imports is required to avoid Python circular import errors.  

from   HDLmAssert import *     
import boto3
import json

class HDLmAwsUtility(object):
  # Build an EC2 AWS client 
  @staticmethod
  def buildAwsEc2Client(regionName = 'us-east-2'):
    # Create a EC2 client
    client = boto3.client('ec2',
                          region_name = regionName)
    return client
  # Build an ECR AWS client 
  @staticmethod
  def buildAwsEcrClient(regionName = 'us-east-2'):
    # Create a ECR client
    client = boto3.client('ecr',
                          region_name = regionName)
    return client
  # Build an ECS AWS client 
  @staticmethod
  def buildAwsEcsClient(regionName = 'us-east-2'):
    # Create a ECS client
    client = boto3.client('ecs',
                          region_name = regionName)
    return client
  # Build an EMR AWS client 
  @staticmethod
  def buildAwsEmrClient(regionName = 'us-east-2'):
    # Create an EMR client
    client = boto3.client('emr',
                          region_name = regionName)
    return client
  # Build an IAM AWS client 
  @staticmethod
  def buildAwsIamClient(regionName = 'us-east-2'):
    # Create an IAM client
    client = boto3.client('iam',
                          region_name = regionName)
    return client
  # Build a secret manager client for accessing secrets
  # stored by the AWS Secrets Manager
  @staticmethod
  def buildAwsSecretsManagerClient(regionName = 'us-east-2'):
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager',
                          region_name = regionName)
    return client
  # Build an AWS SSM client 
  @staticmethod
  def buildAwsSsmClient(regionName = 'us-east-2'):
    # Create an SSM client
    client = boto3.client('ssm', region_name = regionName)
    return client
  # Delete an AWS EC2 key pair 
  @staticmethod
  def deleteAwsEc2KeyPair(client, keyName, keyPairId):
    # Delete an AWS EC2 key pair
    response = client.delete_key_pair(KeyName=keyName, KeyPairId=keyPairId)
    return response
  # Delete an ECS AWS cluster 
  @staticmethod
  def deleteAwsEcsCluster(client, clusterArn):
    # Delete an ECS cluster
    response = client.delete_cluster(cluster=clusterArn)
    return response
  # Delete an ECS AWS service in one AWS cluster   
  @staticmethod
  def deleteAwsEcsService(client, clusterArn, serviceArn, forceValue = False):
    # Delete an ECS service in one AWS cluster
    response = client.delete_service(cluster=clusterArn, service=serviceArn, force=forceValue)
    return response
  # Delete an ECS AWS task definition
  @staticmethod
  def deleteAwsEcsTaskDefinition(client, taskDefinitionArn):
    # Delete an ECS AWS task definition
    taskDefinitionArnList = [taskDefinitionArn]
    response = client.delete_task_definitions(taskDefinitions=taskDefinitionArnList)
    return response
  # This method deregisters an ECS container instance from an ECS cluster.
  # The caller provides the client, the cluster ARN, and the container 
  # instance ARN. The method returns a response from AWS.
  @staticmethod
  def deregisterAwsEcsContainerInstance(client, clusterArn, containerInstanceArn):
    # Deregister an ECS container instance
    response = client.deregister_container_instance(cluster=clusterArn, containerInstance=containerInstanceArn)
    return response
  # This method deregisters an ECS task definition. The caller
  # provides the client and the task definition ARN. This method   
  # returns a response from AWS.
  @staticmethod
  def deregisterAwsEcsTaskDefinition(client, taskArn):
    # Deregister an ECS task definition
    response = client.deregister_task_definition(taskDefinition=taskArn)
    return response
  # Describe the set of AWS EC2 regions. The regions are 
  # returned to the caller as a Python list. Each element
  # in the list is a string that represents an AWS region. 
  @staticmethod
  def describeAwsEc2Regions(client, allRegionsValue = True):
    # Describe the set of EC2 regions
    response = client.describe_regions(AllRegions=allRegionsValue) 
    regions = response['Regions']
    regionList = []
    for region in regions:
      regionList.append(region['RegionName'])
    return regionList
  # Describe a set of AWS ECS clusters 
  @staticmethod
  def describeAwsEcsClusters(client, clusterListArn):
    # Describe an ECS cluster
    response = client.describe_clusters(clusters=clusterListArn) 
    return response
  # Get a bunch of AWS secret values. The secret values
  # are return to the caller in a Python map. The caller
  # provides the secret names of each secret value in a 
  # Python list. 
  @staticmethod
  def getAMapOfSecrets(secretsClient, secretsNames):
    # Check a few values passed by the caller
    if secretsClient == None:
      errorText = 'Secrets client reference passed to getASetOfSecrets is None'
      HDLmAssert(False, errorText)
    if str(type(secretsClient)) != "<class 'botocore.client.SecretsManager'>":
      errorText = 'Secrets names passed to getASetOfSecrets is not a boto3 client'
      HDLmAssert(False, errorText)
    # Make sure that the names of the secrets are in a list
    if secretsNames == None:
      errorText = 'Secrets names reference passed to getASetOfSecrets is None'
      HDLmAssert(False, errorText)
    if type(secretsNames) is not list:
      errorText = 'Secrets names passed to getASetOfSecrets is not a list'
      HDLmAssert(False, errorText)
    if len(secretsNames) <= 0:
      errorText = 'Length of secrets names passed to getASetOfSecrets is invalid'
      HDLmAssert(False, errorText)
    # The request we send to AWS gets a bunch of secrets, all at once
    batchGetSecretValueResponse = secretsClient.batch_get_secret_value(SecretIdList = secretsNames)
    secretValues = batchGetSecretValueResponse['SecretValues']
    # Create a map of secret names and values that is initially empty
    mapOfSecrets = {}
	  # Process each secret value
    for secretValue in secretValues:
      secretName = secretValue['Name']
      secretString = secretValue['SecretString'] 
      mapOfSecrets[secretName] = secretString
    # Return the map of secret names and values to the caller 
    return mapOfSecrets	 
  # Get a set of AWS access values. These values are used to access 
  # AWS. The AWS access values are stored in the AWS Secrets Manager.
  # This routine is no longer used. 
  @staticmethod
  def getAwsAccessValuesNotUsed():
    # Retrieve the AWS Access Key ID 
    secretName = 'AwsAccessKeyId'
    secretsClient, awsAccessStr = HDLmAwsUtility.getSecretFromAws(None, secretName)
    # Retrieve the AWS Secret Access Key
    secretName = 'AwsSecretAccessKey'
    secretsClient, awsSecretStr = HDLmAwsUtility.getSecretFromAws(secretsClient, secretName)
    # Return the values to the caller
    return awsAccessStr, awsSecretStr
  # This method returns the list of EC2 key pairs in an AWS region.
  # The list of key pairs is returned as a Python list. Each element
  # in the list is an object that represents one AWS key pair in one
  # AWS region. 
  @staticmethod
  def getAwsEc2KeyPairs(client):
    # Get the list of key pairs
    response = client.describe_key_pairs()
    keyPairs = response['KeyPairs']
    return keyPairs
  # This method returns the list of EC2 security groups in an AWS region.
  # The list of security groups is returned as a Python list. Each element
  # in the list is an object that represents one AWS security group in one
  # AWS region. 
  @staticmethod
  def getAwsEc2SecurityGroups(client):
    # Get the list of security groups
    response = client.describe_security_groups()
    securityGroups = response['SecurityGroups']
    return securityGroups
  # This method returns the list of EC2 VPCs in an AWS region.
  # The list of VPCs is returned as a Python list. Each element
  # in the list is a object that represents one AWS VPC in one
  # AWS region. 
  @staticmethod
  def getAwsEc2Vpcs(client):
    # Get the list of VPCs
    response = client.describe_vpcs()
    vpcs = response['Vpcs']
    return vpcs
  # This method returns the list of ECR repositories in an AWS region.
  # The list of repositories is returned as a Python list. Each element
  # in the list is an object that represents one AWS repository. 
  @staticmethod
  def getAwsEcrRepositories(client):
    # Get the list of repositories
    response = client.describe_repositories()
    repositoryObjs = response['repositories']
    return repositoryObjs
  # This method returns the list of ECS clusters in an AWS region. 
  # The list of clusters is returned as a Python list. Each element
  # in the list is a string that represents an AWS cluster. The list
  # of clusters is returned to the caller as ARNs.
  @staticmethod
  def getAwsEcsClusters(client):
    # Get the list of clusters
    response = client.list_clusters()
    # Get the list of cluster ARNs
    clusterArnList = response['clusterArns']
    # Extract the cluster ARNs from the list
    clusterArns = []
    for clusterArn in clusterArnList: 
      clusterArns.append(clusterArn)
    return clusterArns
  # This method returns the list of ECS containers for one ECS cluster
  # in one AWS region. The list of containers is returned as a Python list.
  # Each element in the list is a string that represents one AWS container. 
  @staticmethod
  def getAwsEcsContainers(client, clusterArn):
    # Get the list of containers
    response = client.list_container_instances(cluster=clusterArn)
    containerArns = response['containerInstanceArns']
    return containerArns
  # This method returns the list of ECS services for one ECS cluster
  # in one AWS region. The list of services is returned as a Python list.
  # Each element in the list is a string that represents one AWS service. 
  @staticmethod
  def getAwsEcsServices(client, clusterArn):
    # Get the list of services
    response = client.list_services(cluster=clusterArn)
    serviceArns = response['serviceArns']
    return serviceArns
  # This method returns the list of ECS task definitions for 
  # one AWS region. The list of task definitions is returned 
  # as a Python list. Each element in the list is a string 
  # that represents one AWS task definition. Note that ARNs
  # are used to represent task definitions.
  @staticmethod
  def getAwsEcsTaskDefinitions(client):
    # Get the list of task definitions
    response = client.list_task_definitions()
    taskArns = response['taskDefinitionArns']
    return taskArns
  # This method returns the list of IAM roles. The list 
  # of roles is returned as a Python list. Each element
  # in the list is an object that represents one AWS role.
  # In practice, IAM roles are global and not associated 
  # with one AWS region.
  @staticmethod
  def getAwsIamRoles(client):
    # Get the list of roles
    response = client.list_roles()
    roles = response['Roles']
    return roles
  # The next method returns the list of AWS regions. This list is 
  # returned as a Python list. Each element in the list is a string
  # that represents an AWS region.
  @staticmethod
  def getAwsRegions():
    # The list of AWS regions follows
    regionList = ['us-east-2',                                          \
                  'us-east-1',                                          \
                  'us-west-1',                                          \
                  'us-west-2',                                          \
                  'af-south-1',                                         \
                  'ap-east-1',                                          \
                  'ap-south-2',                                         \
                  'ap-southeast-3',                                     \
                  'ap-southeast-5',                                     \
                  'ap-southeast-4',                                     \
                  'ap-south-1',                                         \
                  'ap-northeast-3',                                     \
                  'ap-northeast-2',                                     \
                  'ap-southeast-1',                                     \
                  'ap-southeast-2',                                     \
                  'ap-northeast-1',                                     \
                  'ca-central-1',                                       \
                  'ca-west-1',                                          \
                  'eu-central-1',                                       \
                  'eu-west-1',                                          \
                  'eu-west-2',                                          \
                  'eu-south-1',                                         \
                  'eu-west-3',                                          \
                  'eu-south-2',                                         \
                  'eu-north-1',                                         \
                  'eu-central-2',                                       \
                  'il-central-1',                                       \
                  'me-south-1',                                         \
                  'me-central-1',                                       \
                  'sa-east-1',                                          \
                  'cn-north-1',                                         \
                  'cn-northwest-1',                                     \
                  'us-gov-east-1',                                      \
                  'us-gov-west-1']
    # The list of AWS region names follows
    regionNames = ['US East (Ohio)',                              \
                   'US East (N. Virginia)',                       \
                   'US West (N. California)',                     \
                   'US West (Oregon)',                            \
                   'Africa (Cape Town)',                          \
                   'Asia Pacific (Hong Kong)',                    \
                   'Asia Pacific (Hyderabad)',                    \
                   'Asia Pacific (Jakarta)',                      \
                   'Asia Pacific (Malaysia)',                     \
                   'Asia Pacific (Melbourne)',                    \
                   'Asia Pacific (Mumbai)',                       \
                   'Asia Pacific (Osaka)',                        \
                   'Asia Pacific (Seoul)',                        \
                   'Asia Pacific (Singapore)',                    \
                   'Asia Pacific (Sydney)',                       \
                   'Asia Pacific (Tokyo)',                        \
                   'Canada (Central)',                            \
                   'Canada West (Calgary)',                       \
                   'Europe (Frankfurt)',                          \
                   'Europe (Ireland)',                            \
                   'Europe (London)',                             \
                   'Europe (Milan)',                              \
                   'Europe (Paris)',                              \
                   'Europe (Spain)',                              \
                   'Europe (Stockholm)',                          \
                   'Europe (Zurich)',                             \
                   'Israel (Tel Aviv)',                           \
                   'Middle East (Bahrain)',                       \
                   'Middle East (UAE)',                           \
                   'South America (São Paulo)',                   \
                   'China (Beijing)',                             \
                   'China (Ningxia)',                             \
                   'AWS GovCloud (US-East)',                      \
                   'AWS GovCloud (US-West)']
                   
    return regionList, regionNames
  # This method returns an AWS parameter value. The caller
  # provides the client and the parameter name. This method
  # is used to get a parameter value from the AWS System. 
  # The client is used to access the AWS System. The parameter
  # name is used to identify the parameter value. The client  
  # must be a valid AWS SSM client.
  @staticmethod
  def getAwsSsmParameter(client, paramName):
    response = client.get_parameter(Name=paramName)
    parameter = response['Parameter'] 
    paramValue = parameter['Value']  
    return paramValue
  # Get a set of database secret values. The database secret values
  # are stored in the AWS Secrets Manager. The secret name is passed
  # by the caller. The secret values are returned to the caller in a
  # dictionary. This routine is no longer in use.
  @staticmethod
  def getDatabaseSecretsFromAwsNotUsed(secretName = 'Main9Auroa'):
    # Retrieve the secret value
    secretsClient, databaseJsonStr = HDLmAwsUtility.getSecretFromAws(None, secretName)
    # Convert the JSON string to a dictionary with the 
    # database secret values
    databaseJsonDict = json.loads(databaseJsonStr)
    # Return the dictionary to the caller
    return databaseJsonDict
  # Retrieve a secret from the AWS Secrets Manager. The client 
  # value passed by the caller is used to access the secret. The
  # secret name is also passed by the caller. The actual secret
  # value is returned to the caller. The client value can be 
  # None. If the client value is None, this routine will build
  # the client.
  @staticmethod
  def getJustSecretFromAws(client, secretName):
    if client == None:
      # Build a secret manager client
      client = HDLmAwsUtility.buildAwsSecretsManagerClient()
    # Retrieve the secret value
    response = client.get_secret_value(SecretId = secretName)
    actualSecret = response['SecretString']
    return actualSecret
  # Retrieve a secret from the AWS Secrets Manager. The client 
  # value passed by the caller is used to access the secret. The
  # secret name is also passed by the caller. The actual secret
  # value is returned to the caller. The client value can be 
  # None. If the client value is None, this routine will build
  # the client and return it to the caller.
  @staticmethod
  def getSecretFromAws(client, secretName):
    if client == None:
      # Build a secret manager client
      client = HDLmAwsUtility.buildAwsSecretsManagerClient()
    # Retrieve the secret value
    response = client.get_secret_value(SecretId = secretName)
    actualSecret = response['SecretString']
    return client, actualSecret
  # Get a set of Twilio access values. These values are used to access 
  # Twilio. The Twilio access values are stored in the AWS Secrets Manager.
  @staticmethod
  def getTwilioAccessValues():
    # Retrieve the Twilio Account SID
    secretName = 'TwilioSID'
    secretsClient, twilioSidStr = HDLmAwsUtility.getSecretFromAws(None, secretName)
    # Retrieve the Twilio Auth Token
    secretName = 'TwilioAuthToken'
    secretsClient, twilioAuthTokenStr = HDLmAwsUtility.getSecretFromAws(secretsClient, secretName)
    # Retrieve the Twilio phone number
    secretName = 'TwilioPhoneNumber'
    secretsClient, twilioPhoneNumberStr = HDLmAwsUtility.getSecretFromAws(secretsClient, secretName)
    # Return the values to the caller
    return twilioSidStr, twilioAuthTokenStr, twilioPhoneNumberStr