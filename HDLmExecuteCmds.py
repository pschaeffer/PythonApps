# Class for executing a set of commands. The commands are constructed 
# from some JSON that is coded into this routine. The commands are 
# exexuted in a fairly standard way. 

from   HDLmUtility import *
import json
import os
import subprocess   
import time

# The following JSON data structure is used to build each of the 
# commands that is executed later                      
HDLmExecuteCmdsData = \
  [
    {
      'description': 'Run docker to start the webpage-improver',
      'type': 'docker',
      'enabled': False,
      'command': 'docker run',
      'internalPort' : 80,
      'exposedPort'  : 5005,
      'options': 'itd', 
      'volumes': ['${HOME}/.aws:/root/.aws'],
      'envs': [
                {
                   'envName': 'OpenAI__ApiKey',
                   'secretName': 'abtesting-dev/openAiKey'
                }
              ], 
      'image': '546307548582.dkr.ecr.us-east-1.amazonaws.com/extension-webpage-improver:latest',
    },
    {
      'description': 'Run Dot Net to start the webpage-improver code',
      'type': 'dotnet',
      'enabled': True,
      'command': 'dotnet run',
      'programName': 'Program.cs',
      'directory': 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\abtesting\\extension-microservices\\webpage-improver',
      'envs': []
    },
    {
      'description': 'Run Dot Net to start the suggest-text code',
      'type': 'dotnet',
      'enabled': True,
      'command': 'dotnet run',
      'programName': 'Program.cs',
      'directory': 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\abtesting\\extension-microservices\\suggest-text',
      'envs': []
    },
    {
      'description': 'Run Dot Net to start the extension-ai code',
      'type': 'dotnet',
      'enabled': True,
      'command': 'dotnet run',
      'programName': 'Program.cs',
      'directory': 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\abtesting\\extension-microservices\\ai',
      'envs': []
    },
  ]

# Build a docker comamnd from the command data structure passed in
def buildDockerCommand(secretsClient, commandData):
  # Start the command string
  outStr = ''
  # Add the command  
  outStr += commandData['command'] 
  # Add the options
  if 'options' in commandData:
    outStr += ' -' + commandData['options']
  # Add the port mapping
  if 'internalPort' in commandData and 'exposedPort' in commandData:
    outStr += ' -p ' + str(commandData['exposedPort']) + ':' + str(commandData['internalPort'])
  # Add the environment variables (if any)
  envStr = getEnvsString(secretsClient, commandData['envs'])
  outStr += envStr
  # Add the volumes (if any)
  volsStr = getVolsString(commandData['volumes'])
  outStr += volsStr
   # Add the image name
  if 'image' in commandData:
    outStr += ' ' + commandData['image']
  return outStr

# Build a Dot Net comamnd for PowerShell from the command data structure passed in
def buildDotNetCommandPs(secretsClient, commandData):
  # Start the command string
  outStr = ''
  # Run the Dot Net command in the background
  outStr += 'Start-Job -ScriptBlock {'
  # Add the command  
  outStr += commandData['command'] 
  # Add the project name   
  outStr += ' --project ' 
  outStr += commandData['directory'] 
  # Terminate the script block
  outStr += '}' 
  # Add the environment variables (if any)
  envStr = getEnvsString(secretsClient, commandData['envs'])
  outStr += envStr
  return outStr

# Build a Dot Net comamnd for Popen from the command data structure passed in
def buildDotNetCommandPo(secretsClient, commandData):
  # Start the command string
  outStr = ''
  # Add the command  
  outStr += commandData['command'] 
  # Add the Dot Net program name
  if 'programName' in commandData:
    outStr += ' ' + commandData['programName']
  # Add the environment variables (if any)
  envStr = getEnvsString(secretsClient, commandData['envs'])
  outStr += envStr
  return outStr

# Build and execute a set of commands. The caller provide the list   
# of commands to be executed. The commands are built from the JSON 
# data structure passed to this routine. 
def executeCmds(secretsClient, cmdList):
  retCode = 0
  # Handle each command in the list
  for cmdData in cmdList: 
    # Get and check the enabled flag
    enabledValue = cmdData['enabled']    
    if enabledValue == False:
      print('Command not enabled:', cmdData['description'])
      continue
    # Get the command description 
    cmdDesc = cmdData['description']
    # Switch to the target directory (if any)
    if 'directory' in cmdData:
      HDLmUtility.changeDirectory(cmdData['directory'])
    # Get the command type
    cmdType = cmdData['type']
    # Check the command type
    match cmdType:
      # Handle the docker command type
      case 'docker':    
        # Build the command string
        commandStr = buildDockerCommand(secretsClient, cmdData)
        # Execute the command and get the return code
        retCode = HDLmUtility.executeCommandPsGetRetCode(commandStr)
      # Handle the Dot Net command type
      case 'dotnet':    
        # Build the command string
        commandStr = buildDotNetCommandPo(secretsClient, cmdData)
        # Execute the command and get a few values 
        retCode = HDLmUtility.executeCommandPoGetRetCode(commandStr)
      # Check if the command type did not match anything
      case _:
        print('Command type not recognized:', cmdType)
        continue
    if isinstance(retCode, int) and retCode != 0:
      print('Error executing command:', cmdData['description'])
  return 0
  
# Get a string that sets the environment variables for the command
def getEnvsString(secretsClient, envList):
  envStr = ''
  # Check if we have any environment variables to set
  if len(envList) > 0:
    # Loop through the list of environment variables
    for env in envList:
      # Check if we have a secret name
      if 'secretName' in env:
        # Get the secret value from AWS secrets manager
        secretValue = HDLmAwsUtility.getJustSecretFromAws(secretsClient, env['secretName'])
        # Add the environment variable to the command string
        envStr += ' -e ' + env['envName'] + '=' + "'" + secretValue + "'"
  return envStr

# Get a string that sets the volumes for the command
def getVolsString(volumeList):
  volumeStr = ''
  # Check if we have any volumes to set
  if len(volumeList) > 0:
    # Loop through the list of volumes
    for volume in volumeList:
      # Add the volume to the command string
      volumeStr += ' -v ' + volume
  return volumeStr

# Handle startup 
def startup():
  return
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Start executing commands
  startup() 
  # Start the AWS secrets manager code
  secretsClient = HDLmAwsUtility.buildAwsSecretsManagerClient()
  # Build and excute th3 list of commands
  retCode = executeCmds(secretsClient, HDLmExecuteCmdsData)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()