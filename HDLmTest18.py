# This file was created to test storing secrets in AWS Secrets Manager

from   HDLmUtility import *
import boto3
import time

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Build a secret manager client
  client = HDLmUtility.buildAwsSecretsManagerClient();
  # Specify the secret name
  secretName = "TwilioSID"
  # secretName = "Main9Auroa"
  # Retrieve the secret value
  secretclient, secret = HDLmUtility.getSecretFromAws(None, secretName) 
  # Get some database secrets
  databaseSecrets = HDLmUtility.getDatabaseSecretsFromAws()
  # Collect some ending time values   
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()