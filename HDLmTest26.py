# This file was created to find and delete EC2 key pairs in AWS regions

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time

# Get the value of a stored parameter. The caller provides 
# the parameter name. This routine does the rest. 
def getParameterValue(client, paramName):
  # Get the parameter value 
  paramValue = HDLmAwsUtility.getAwsSsmParameter(client, paramName)
  return paramValue

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Get the maximum number of clusters. This value is not
  # really used in this program. It is just here to show
  # how to get the value.
  maxClusterCount = HDLmConfigInfo.getClustersMaxCount()
  # Get the SSM client      
  client = HDLmAwsUtility.buildAwsSsmClient()
  # Get a few parameter values
  # Get the current server
  currentServer = getParameterValue(client, '/Test1/CurrentServer')
  # Get and fix the list of servers
  serverList = getParameterValue(client, '/Test1/ServerList')

  # Collect some ending time values   
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()