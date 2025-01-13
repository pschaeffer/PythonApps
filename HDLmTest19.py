# This file was created to delete ECS clusters in AWS regions

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time

# Delete a cluster
def deleteCluster(client, cluster):
  # Get the services for the cluster
  services = HDLmAwsUtility.getAwsEcsServices(client, cluster)
  # Delete each service
  for service in services:
    HDLmAwsUtility.deleteAwsEcsService(client, cluster, service, True)
  # Get the container instances for the cluster
  instances = HDLmAwsUtility.getAwsEcsContainers(client, cluster)
  # Deregister each container instance
  for instance in instances:
    HDLmAwsUtility.deregisterAwsEcsContainerInstance(client, cluster, instance)
  # Delete the cluster
  HDLmAwsUtility.deleteAwsEcsCluster(client, cluster)
  return

# Get the list of ECS clusters in a region
def getListEcsClusters(client):
  clusters = HDLmAwsUtility.getAwsEcsClusters(client) 
  return clusters

# Process all of the AWS regions
def processAllRegions():
  # Get the list of regions
  regionList, regionNames = HDLmAwsUtility.getAwsRegions()
  # Process each region
  for region in regionList:
    print('Region:', region)
    # Build an ECS client for the region
    client = HDLmAwsUtility.buildAwsEcsClient(region)
    # Get the list of AWS ECS clusters for the current region      
    try:
      clusters = getListEcsClusters(client)
    except Exception as e:
      print('Error:', e)
      continue
    # Skip a couple of regions that we have 
    # already handled by hand
    if region == 'us-east-1':
      continue
    if region == 'us-east-2':
      continue
    # Try to delete each cluster
    for cluster in clusters:
      # Use the delete cluster routine
      print('Deleting a cluster in Region:', region)
      deleteCluster(client, cluster)
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