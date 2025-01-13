# This file was created to find ECR repositories in AWS regions

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time

# Get the list of ECR repositories in a region
def getListEcrRepositories(client):
  repositories = HDLmAwsUtility.getAwsEcrRepositories(client) 
  return repositories

# Process all of the AWS regions
def processAllRegions():
  # Get the list of regions
  regionList, regionNames = HDLmAwsUtility.getAwsRegions()
  # Process each region
  for region in regionList:
    print('Region:', region)
    # Build an ECR client for the region
    client = HDLmAwsUtility.buildAwsEcrClient(region)
    # Get the list of AWS ECR repositories for the current region      
    try:
      repositories = getListEcrRepositories(client)
      print('Repositories:', len(repositories))
    except Exception as e:
      print('Error:', e)
      continue
  return      

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Get the maximum number of clusters. This value is not
  # really used in this program. It is just here to show
  # how to get the value.
  maxClusterCount = HDLmConfigInfo.getClustersMaxCount()
  # Process all of the AWS regions
  processAllRegions()
  # Collect some ending time values   
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()