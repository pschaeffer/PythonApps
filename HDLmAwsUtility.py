# Class for providing a set of AWS utility functions. This is considered to be 
# a low-level routine that can not import any higher-level routines. The ban on 
# imports is required to avoid Python circular import errors.  

from   HDLmAssert import *     
import boto3
import json

class HDLmAwsUtility(object):
  # Build a secret manager client for accessing secrets
  # stored by the AWS Secrets Manager
  @staticmethod
  def buildAwsSecretsManagerClient(regionName = 'us-east-2'):
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager',
                          region_name = regionName)
    return client
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