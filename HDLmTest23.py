# This file was created to find and delete (if need be) ECS
# task definitions in AWS regions

from   HDLmAwsUtility import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
import boto3
import time

glbWordList = ['auth', 'extension', 'generic', 'project', 'remote', 'rule', 'web']

# Delete an ECS task definition
def deleteTaskDefintion(client, taskArn):
  response = HDLmAwsUtility.deregisterAwsEcsTaskDefinition(client, taskArn)
  response = HDLmAwsUtility.deleteAwsEcsTaskDefinition(client, taskArn) 
  return response

# Get the count of words in a string
def getWordCount(inStr, wordList):
  count = 0
  for word in wordList:
    count += inStr.count(word)
  return count

# Get the list of ECS task definitions in a region
def getListEcsTaskDefintions(client):
  tasks = HDLmAwsUtility.getAwsEcsTaskDefinitions(client) 
  return tasks

# Process all of the AWS regions
def processAllRegions():
  # Get the list of regions
  regionList, regionNames = HDLmAwsUtility.getAwsRegions()
  # Process each region
  for region in regionList:
    print('Region:', region)
    # Build an ECS client for the region
    client = HDLmAwsUtility.buildAwsEcsClient(region)
    # Get the list of AWS ECS task definitions for the 
    # current region      
    try:
      tasks =  getListEcsTaskDefintions(client)
      print('Tasks:', len(tasks))
    except Exception as e:
      print('Error:', e)
      continue
    # Process each task definition
    for task in tasks:
      count = getWordCount(task, glbWordList)
      # Delete one task definition
      if count == 0:
        deleteTaskDefintion(client, task)
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