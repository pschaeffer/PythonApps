# This file was created to find and delete EC2 key pairs in AWS regions

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time


# Delete an EC2 key pair
def deleteKeyPair(client, pairObj):
  return
  keyName = pairObj['KeyName']
  keyPairId = pairObj['KeyPairId']
  response = HDLmAwsUtility.deleteAwsEc2KeyPair(client,  \
                                                keyName, \
                                                keyPairId)        
  return response

# Get the list of EC2 key pairs in a region
def getListEc2KeyPairs(client):
  resources = HDLmAwsUtility.getAwsEc2KeyPairs(client) 
  return resources

# Process all of the AWS regions
def processAllRegions():
  # Get the list of regions
  regionList, regionNames = HDLmAwsUtility.getAwsRegions()
  # Process each region
  for region in regionList:
    print('Region:', region)
    # Build an EC2 client for the region
    client = HDLmAwsUtility.buildAwsEc2Client(region)
    # Get the list of AWS EC2 key pairs for the current region      
    try:
      pairs =  getListEc2KeyPairs(client)
      print('Pairs:', len(pairs))
    except Exception as e:
      print('Error:', e)
      continue
    # Process each EC2 key pair  
    for pain in pairs:
      print('Pair name:', pain['KeyName'])
    # Skip a couple of regions in the US 
    if region == 'us-east-1':
      continue
    if region == 'us-east-2':
      continue
    if region == 'us-west-1':
      continue
    if region == 'us-west-2':
      continue
    # Delete a few EC2 key pairs  
    for pair in pairs:
      response = deleteKeyPair(client, pair)
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