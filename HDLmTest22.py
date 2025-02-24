# This file was created to find EC2 VPCs in AWS regions

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time

# Get the list of EC2 VPCs in a region
def getListEc2Vpcs(client):
  vpcs = HDLmAwsUtility.getAwsEc2Vpcs(client) 
  return vpcs

# Process all of the AWS regions
def processAllRegions():
  # Get the list of regions
  regionList, regionNames = HDLmAwsUtility.getAwsRegions()
  # Process each region
  for region in regionList:
    print('Region:', region)
    # Build an EC2 client for the region
    client = HDLmAwsUtility.buildAwsEc2Client(region)
    # Get the list of AWS EC2 VPCs for the current region      
    try:
      vpcs =  getListEc2Vpcs(client)
      print('VPCs:', len(vpcs))
    except Exception as e:
      print('Error:', e)
      continue
    # Process each VPC
    for vpc in vpcs:
      print('IsDefault:', vpc['IsDefault']) 
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