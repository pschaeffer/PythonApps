from   HDLmString  import *
from   HDLmUtility import *
import copy
import json
import os
import sys
import time

# This program appears to have been written to analyze the info log files.
# These files have (may have) records from several different domains. The 
# info log files combine everything into one file.  
# 
# Some of the lines have bad JSON. This problem is caught using Try/Catch.
# Some lines don't have a session ID. For example, lines created for bad browsers don't 
#   have a session ID. These lines are ignored.
# If the current line has a session ID, but the session ID is 'unknown' (without the 
#   quotes, then the current line is ignored
# If the exception count is greater than zero, the current session ID is bypassed
# If we only have one line for a given session ID, then the session ID is ignored

# The log input directory name is stored in the field below
glbInDirName = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\PHPApps\\PHPWebProject1\\PHPWebProject1'
# The log input file name is stored in the field below
glbInFileNamb = 'info 2020-10-09.log'
glbInFileNamc = 'info 2020-11-29.log'
glbInFileNamd = 'info 2021-01-08.log'
glbInFileName = 'info 2021-02-01.log'
# The output file name is stored in the field below
glbOutDirName = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\PHPApps\\PHPWebProject1\\PHPWebProject1'
glbOutFileName = 'info 2022-04-12.out'

# Each instance of this class has all of the information about
# how a parameter number was used for some period of time
class ParmUsage(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, parmNumber, parmModName, parmFirstTime, parmLastTime):
    self.number = parmNumber
    self.modName = parmModName
    self.firstTime = parmFirstTime
    self.lastTime = parmLastTime
    self.usageCount = 0 
  # Get a full copy of the current instance and return the
  # copy to the caller
  def getCopy(self):
    # Obtain copies of all of the values inside the current instance
    copyFirstTime = self.getFirstTime()
    copyLastTime = self.getLastTime()
    copyModName = self.getModName()
    copyParmNumber = self.getParmNumber()
    copyUsageCount = self.getUsageCount()   
    # Create a new instance with most of the saved (copied) values
    newInstance = ParmUsage(copyParmNumber, copyModName, copyFirstTime, copyLastTime)
    newInstance.setUsageCount(copyUsageCount)
    # Return the new instance to the caller
    return newInstance   
  # Get the first time this combination of values was used from an instance of
  # this class
  def getFirstTime(self):
    return self.firstTime
  # Get the last time this combination of values was used from an instance of
  # this class
  def getLastTime(self):
    return self.lastTime
  # Get the current modification name from an instance of
  # this class
  def getModName(self):
    return self.modName
  # Get the current parameter number from an instance of
  # this class
  def getParmNumber(self):
    return self.number
  # Get the current usage count from an instance of this class
  def getUsageCount(self):
    return self.usageCount
  # Increment the usage count for an instance of this class
  def incrementUsageCount(self):
    self.usageCount += 1
  # Set the last time this combination of values was used
  def setLastTime(self, newLastTime):
    self.lastTime = newLastTime
  # Set the current modification name for an instance of
  # this class
  def setModName(self, newModName):
    self.modName = newModName
  # Set the usage count using a value passed by the caller 
  def setUsageCount(self, newUsageCount):
    self.usageCount = newUsageCount

# This routine analyzes a dictionary and returns a boolean
# value showing if the current set of objects should be 
# processed or not.
def analyzeDict(curDict):
  execeptionCount = 0
  rv = True
  # Check the curent dictionary
  if 'exception' in curDict:
    exceptionCount = curDict['exception']
    if exceptionCount > 0:
      rv = False
  # Return the final boolean value to the caller
  return rv

# This routine analyzes a list of objects and returns a 
# dictionary of reason values. A count is associated with
# each return value. The count is the number of times that
# return value was actually used.
def analyzeList(curList):
  outDict = dict()
  # Check each entry in the list
  for curEntry in curList:
    curReason = curEntry['reason']
    # Check if the current reason is already in the dictionary
    if curReason in outDict:
      curCount = outDict[curReason]
      curCount += 1
      outDict[curReason] = curCount
    # The current reason is not in the dictionary
    else:
      outDict[curReason] = 1
  # Return the final dictionary to the caller
  return outDict

# This routine finds all of the updates in all of lines
# and keeps track of how parameter numbers have been used
def buildParmUsage(linesJson, parmUsages):
  curParmUsage = dict()
  countJson = len(linesJson)
  for i in range(countJson):
    curJson = linesJson[i]
    # Check if the current JSON even has any updates
    if 'updates' not in curJson:
      continue
    # Get some information that applies to all updates
    curTimestamp = curJson['timestamp']
    # Get the list of updates and process each one
    curUpdates = curJson['updates']
    for curUpdate in curUpdates:
      # Get some information about the current updates
      curParmNumber = curUpdate['parmNumber']
      curModType = curUpdate['modType']
      # Check if the parameter number is not set. For example, the parameter number is
      # not set for 'notify' events
      if curParmNumber == None:
        continue
      curModName = curUpdate['modName']
      # We need to check if we have any information for this 
      # parameter number
      if curParmNumber not in curParmUsage:
        # Create a new parameter usage object
        curUsage = ParmUsage(curParmNumber, curModName, curTimestamp, curTimestamp)
        curUsage.setUsageCount(0)
        curParmUsage[curParmNumber] = curUsage
      # Check if the modification name has changed
      oldParmModName = curParmUsage[curParmNumber].getModName()
      # Make copies of the old modification name and the new modification name 
      curModNameTemp = curModName
      oldParmModNameTemp = oldParmModName
      # Make some changes to the old modification name and the new modification name 
      if 1 == 1:
        if curModNameTemp.startswith('OWO Buy Tickets Gradient'):
          curModNameTemp = 'OWO Buy Tickets Gradient'
        if oldParmModNameTemp.startswith('OWO Buy Tickets Gradient'):
          oldParmModNameTemp = 'OWO Buy Tickets Gradient'
        if curModNameTemp.startswith('OWO Buy Tickets Image'):
          curModNameTemp = 'OWO Buy Tickets Image'
        if oldParmModNameTemp.startswith('OWO Buy Tickets Image'):
          oldParmModNameTemp = 'OWO Buy Tickets Image'
      # Check if the old modification name and the new modification name 
      # are the same
      if curModNameTemp == oldParmModNameTemp:
        # The modification name for the current parameter number has
        # not changed. Just reset the last time this combination of a 
        # parameter number and a modification name was used and increment 
        # the usage count.
        curParmUsage[curParmNumber].setLastTime(curTimestamp)
        curParmUsage[curParmNumber].incrementUsageCount()
        continue
      # Check if this parameter number has already been used
      if curParmNumber not in parmUsages:
        parmUsages[curParmNumber] = []
      # Build a parameter usage instance using all of the old values
      copyParmUsage = curParmUsage[curParmNumber].getCopy()
      # Add the parameter usage instance to list of uses for the current
      # parameter number
      parmUsages[curParmNumber].append(copyParmUsage)
      # The modification name associated with the current parameter 
      # number has changed. We need to reset the information for the
      # current parameter number.
      curUsage = ParmUsage(curParmNumber, curModName, curTimestamp, curTimestamp)
      curUsage.setUsageCount(1)
      curParmUsage[curParmNumber] = curUsage
  # Add the final parameter usage to dictionary returned by 
  # this routine
  for curParmNumber, curUsage in curParmUsage.items():
    # Make a copy of the current parameter usage
    copyCurUsage = curUsage.getCopy()
    # Check if this parameter number has already been used
    if curParmNumber not in parmUsages:
      parmUsages[curParmNumber] = []
    parmUsages[curParmNumber].append(copyCurUsage)
  return
    
# Check each line passed to this routine
def checkLines(outJsonList, sessionIdDict): 
  unknownCount = 0
  # Set a few starting values
  jsonCount = len(outJsonList)
  for i in range(jsonCount):
    curJson = outJsonList[i]
    # Check if the current JSON even has a session ID
    if 'sessionid' not in curJson and 'sessionId' not in curJson:
      continue
    # Check if the current JSON has a reason
    if 'reason' not in curJson:
      continue
    # Get a few values from the current JSON
    if 'sessionid' in curJson:
      curSessionId = curJson['sessionid']
    else:
      curSessionId = curJson['sessionId']
    curReason = curJson['reason']
    # Check if the current session ID is unknown. We can't do much
    # if the session ID is not properly set.
    if curSessionId == 'unknown':
      unknownCount += 1
      continue
    # Check if the current session ID is already known or not
    if curSessionId in sessionIdDict:        
      curList = sessionIdDict[curSessionId]
      curList.append(copy.deepcopy(curJson))
      sessionIdDict[curSessionId] = curList
      continue
    # We have not seen this session ID before. Add it to the 
    # dictionary of session ID values.  
    curList = []
    curList.append(copy.deepcopy(curJson))
    sessionIdDict[curSessionId] = curList     
  return

# Check each session ID in the dictionary. Note that if None
# is passed as the output list object, then no actual output 
# will be generated. 
def checkSessionIdValues(sessionIdDict, outList, \
                         firstTimestamp = None, \
                         lastTimestamp = None):
  # Check if the caller passed None for the output list object
  if outList == None:
    return
  lineCount = 0
  sessionIdCount = 0
  skipCount = 0
  # Check each session ID
  for sessionId in sorted(sessionIdDict.keys()):
    curList = sessionIdDict[sessionId]
    if len(curList) <= 1:
      continue
    # We can do some more checking on the current session ID value
    sessionIdCount += 1
    curDict = analyzeList(curList)
    rv = analyzeDict(curDict)
    # Check if the current session ID should be skipped
    if rv == False:
      skipCount += 1
      continue
    # It looks like the current session ID is OK. Add it to the 
    # output list of lines. Each unique session will yield one   
    # line. 
    outDict = dict()
    outDict['sessionId'] = sessionId
    # Create an empty list of reasons
    outReasons = []
    entryCount = 0
    outAmount = 0.0
    outTimestamp = None
    # Process all of the entries for the current session ID
    for curEntry in curList:
      entryCount += 1
      # If we are processing the first entry then we can try to capture
      # the timestamp and the parameters 
      if entryCount == 1:
        outParameters = curEntry['parameters']
        outTimestamp = curEntry['timestamp']
      # Add the current reason to the list of reasons
      curReason = curEntry['reason']
      # Look for the word 'Buy' (without the quotes) in current reason
      if curReason.find('Buy') >= 0:
        outAmount = 1.0
      # Look for the word 'Purchase' (without the quotes) in current reason
      if curReason.find('Purchase') >= 0:
        outAmount = 1.0
      outReasons.append(curReason)
    # Skip the current session ID if it is out of timestamp range
    print(outTimestamp)
    if outTimestamp != None:
      # Check if the current sesion is before the starting time (if 
      # the starting time was set)
      if firstTimestamp != None and \
        outTimestamp < firstTimestamp:
        continue
      # Check if the current sesion is after the ending time (if 
      # the ending time was set)
      if lastTimestamp != None and \
        outTimestamp > lastTimestamp:
        continue
    # Add the list of reasons to the output object
    outDict['amount'] = outAmount
    outDict['parameters'] = outParameters
    outDict['reasons'] = outReasons
    outDict['timestamp'] = outTimestamp
    curLine = json.dumps(outDict)
    outList.append(curLine)
  return lineCount

# This routine displays how parameter numbers have been 
# used over time. Note that if None is passed as the 
# output list object, then no actual output will be 
# generated. 
def displayParmUsage(parmUsages, outList):
  # Check if the caller passed None for the output list object
  if outList == None:
    return
  # Display the parameter usage information
  for curParmNumber in sorted(parmUsages.keys()):
    outLine = 'Current parameter number is ' + str(curParmNumber)
    outList.append(outLine)
    usageList = parmUsages[curParmNumber]
    usageListLength = len(usageList)
    outLine = '  List length is ' + str(usageListLength)
    outList.append(outLine)
    # Process each entry in the usage list
    for curUsage in usageList:
      curFirstTime = curUsage.getFirstTime()
      curLastTime = curUsage.getLastTime()
      curUsageCount = curUsage.getUsageCount()
      curModName = curUsage.getModName()
      curCountStr = 'Usage count(' + str(curUsageCount) + ')' 
      curCountStr = HDLmString.padRight(curCountStr, 20)
      outFormat = '    {0} {1} {2} {3}'
      outLine = outFormat.format(HDLmString.padRight(str(curModName), 40), curCountStr, str(curFirstTime), str(curLastTime))
      outList.append(outLine)
  return

# This routine tries to convert each line to a JSON object.
# In a few cases, this will fail. In all other cases, the
# JSON object is added to a list that is returned to the 
# caller.
def fixFile(lineList):
  # Set a few starting values
  offset = 0
  outListJson = []
  # Get the number of lines
  lineCount = len(lineList)
  # Process each line
  for i in range(lineCount):
    curLine = lineList[i]
    curLength = len(curLine)
    # Try to convert the current line to JSON. This will fail if the 
    # current line is invalid. 
    try:
      # The statement below will fail, if the current line contains bad
      # (or incomplete) JSON. The current input file has some number of
      # bad JSON lines in it.
      outListJson.append(json.loads(curLine))
    except Exception as e:
      print(str(e))
      print(i+1, hex(offset))
    offset += curLength + 1   
  # Return the list of JSON objects to the caller
  return outListJson

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)  
  # Get the full input file name
  inputFileName = glbInDirName + '\\' + glbInFileName
  # Read the input log file
  listInFile = HDLmUtility.readInputFile(inputFileName, 'iso-8859-1')
  # Fix the input log file
  outJsonList = fixFile(listInFile)
  # Figure out how each parameter number is used
  outLines = []
  parmUsage = dict()
  buildParmUsage(outJsonList, parmUsage)
  displayParmUsage(parmUsage, None)
  # Check each line  
  sessionIdDict = dict()
  checkLines(outJsonList, sessionIdDict)
  # checkSessionIdValues(sessionIdDict, None)
  # checkSessionIdValues(sessionIdDict, outLines, \
  #                      "2020-10-24T00:00:00.000000", \
  #                      "2020-10-29T23:59:59.999999")
  # checkSessionIdValues(sessionIdDict, outLines, \
  #                      "2015-10-25T14:15:30.332773", \
  #                      "2022-10-25T14:15:30.332773")
  checkSessionIdValues(sessionIdDict, outLines, \
                       "2021-01-23T08:01:54.573079", \
                       "2021-01-23T08:01:54.675520")
  # Get the full output file name
  outputFileName = glbOutDirName + '\\' + glbOutFileName
  HDLmUtility.writeOutputFile(outLines, outputFileName)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__": 
  main()