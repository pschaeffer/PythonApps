# This file was created to test storing secrets in AWS Secrets Manager

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Get the maximum number of clusters. This value is not
  # really used in this program. It is just here to show
  # how to get the value.
  maxClusterCount = HDLmConfigInfo.getClustersMaxCount()
  # Build a secrets manager client
  client = HDLmAwsUtility.buildAwsSecretsManagerClient()
  # Get a map of secrets
  secretsMap = HDLmAwsUtility.getAMapOfSecrets(client, ['TwilioSID', 'Main9Auroa'])
  # Specify the secret name
  secretName = "TwilioSID"
  # secretName = "Main9Auroa"
  # Retrieve the secret value
  secretclient, secret = HDLmAwsUtility.getSecretFromAws(None, secretName) 
  # Get some database secrets
  HDLmConfig.setConfigValuesNotUsed()
  # databaseSecrets = HDLmAwsUtility.getDatabaseSecretsFromAwsNotUsed()
  # Collect some ending time values   
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()