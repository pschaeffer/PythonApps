from   HDLmBuildLines import *
from   mutableint     import MutableInt
from   ReadLogs3      import * 
import argparse
import json
import platform
import time

# This program appears to have been written to analyze raw log files. All
# of the raw log files are found in one directory. Each of the raw log files
# is read and analyzed. 

# The log input directory name is stored in the field below
glbInDirName = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\PHPApps\\PHPWebProject1\\PHPWebProject1'
# The raw log files all start with the prefix specified below
glbRawPrefix = 'HDLmLog'

# Build a line describing the current count and add it to the lines object 
def addCountLine(outLines, countName, count):
  line = ''
  # Add the name/description of the count
  line += '"'
  line += countName
  line += '"'
  line += ','
  # Add an empty cell
  line += '"'
  line += '"'
  line += ','
  # Add the count value
  line += '"'
  line += str(count)
  line += '"'
  # Add the final output line
  outLines.addLine(line)

# Build a line describing the current event and add it to the lines object
def addEventLine(outLines, typeOfEvent, eventText, eventNumber, \
                 fileName, lineNumber, offset, \
                 timestampStr, sessionIdStr, curLineStr):
  # Start the output line
  line = ''
  # Add the type of event
  line += '"'
  line += typeOfEvent
  line += '"'
  line += ','
  # Add the event text
  line += '"'
  line += eventText
  line += '"'
  line += ','
  # Add the event number
  line += '"'
  line += str(eventNumber)
  line += '"'
  line += ','
  # Add the file name
  line += '"'
  line += fileName
  line += '"'
  line += ','
  # Add the line number
  line += '"'
  line += str(lineNumber)
  line += '"'
  line += ','
  # Add the line offset
  line += '"'
  if offset != None:
    line += hex(offset)
  else:
    line += 'Not Set'
  line += '"'
  line += ','
  # Add the timestamp
  line += '"'
  if timestampStr != None:
    line += timestampStr
  line += '"'
  line += ','
  # Add the session ID
  line += '"'
  if sessionIdStr != None:
    line += sessionIdStr
  else:
    line += 'Not Set'
  line += '"'
  line += ','
  # Add the current line
  line += '"'
  if curLineStr != None:
    line += curLineStr.replace('"', '""')
  line += '"'
  # Add the final output line
  outLines.addLine(line)    

# Build the standard heading line string and add it to the lines object
def addHeadingLine(outLines):
  heading = '"Type of event","Event Text","Event Number",'
  heading += '"Filename","Line Number","Offset",'
  heading += '"Timestamp","Session ID","Current Line"'
  outLines.addLine(heading)

# Extract some information from the update(s) and return the
# extracted information to the caller
def extractFromUpdates(updateList):
  # Set a default return value
  sessionIdValue = None
  # Process each update
  for curUpdate in updateList:
    # Check if the current update contains a session ID
    if 'sessionId' in curUpdate:
      sessionIdValue = curUpdate['sessionId']
      break
  # Return the extracted information to the caller
  return sessionIdValue

# Filter the file list using the prefix specified above
def filterFileList(fileList, prefixStr):
  outList = []
  for fileName in fileList:
    if fileName == 'HDLmLog.csv':
      continue
    if fileName.startswith(prefixStr):
      fileName = HDLmString.removeSuffix(fileName, '.log')
      outList.append(fileName)
  return outList

# This routine tries to convert each line to a JSON object.
# In a few cases, this will fail. In all other cases, the
# JSON object is added to a list that is returned to the 
# caller.
def fixFile(sessionMap, fileName, lineList, outLines, countObject):
  # Set a few starting values
  offset = 0
  outListJson = []
  # Get the number of lines
  lineCount = len(lineList)
  # Process each line
  for i in range(lineCount):
    curLine = lineList[i]
    curLength = len(curLine)
    # Check if the current line can just be ignored. A lot of
    # lines are not actually POSTs of JSON objects.
    if curLine.find('using POST') < 0:
      continue
    # Check if the current line can just be ignored. A lot of 
    # checking is needed for lines that have 'Event' in them.
    if curLine.find('Event') >= 0:
      # Check for events that can be ignored
      if curLine.find('AnimationEvent') >= 0:
        continue
      if curLine.find('BeforeUnloadEvent') >= 0:
        continue
      if curLine.find('ClipboardEvent') >= 0:
        continue
      if curLine.find('CustomEvent') >= 0:
        continue
      if curLine.find('DeviceMotionEvent') >= 0:
        continue
      if curLine.find('DeviceOrientationEvent') >= 0:
        continue
      if curLine.find('ErrorEvent') >= 0:
        continue
      if curLine.find('"Event"') >= 0:
        continue
      if curLine.find('FormDataEvent') >= 0:
        continue
      if curLine.find('FocusEvent') >= 0:
        continue
      if curLine.find('HashChangeEvent') >= 0:
        continue
      if curLine.find('InputEvent') >= 0:
        continue
      if curLine.find('KeyboardEvent') >= 0:
        continue
      if curLine.find('MessageEvent') >= 0:
        continue
      if curLine.find('MouseEvent') >= 0:
        continue
      if curLine.find('PointerEvent') >= 0:
        continue
      if curLine.find('PopStateEvent') >= 0:
        continue
      if curLine.find('PromiseRejectionEvent') >= 0:
        continue
      if curLine.find('SecurityPolicyViolationEvent') >= 0:
        continue
      if curLine.find('StorageEvent') >= 0:
        continue
      if curLine.find('SubmitEvent') >= 0:
        continue
      if curLine.find('TransitionEvent') >= 0:
        continue
      if curLine.find('UIEvent') >= 0:
        continue
      if curLine.find('WheelEvent') >= 0:
        continue
    if curLine.find('[native code]') >= 0:
      continue
    if curLine.find('[object Event]') >= 0:
      continue
    if curLine.find('function ') >= 0:
      continue
    # Check for a few cases where the session ID will not be set. Note
    # that these are JavaScript errors that are reported by the browser.
    # if curLine.find('nodeElements[Symbol.iterator] is not') >= 0:
    #   continue
    # if curLine.find('currentElement of nodeElements is not a function') >= 0:
    #   continue
    # if curLine.find("Failed to execute 'appendChild' on 'Node'") >= 0:
    #   continue
    # if curLine.find("Object doesn't support property or method") >= 0:
    #   continue
    # Try to convert the current line to JSON. This will fail if the 
    # current line is invalid. 
    try:
      # The statement below will fail, if the current line contains bad
      # (or incomplete) JSON. The current input file has some number of
      # bad JSON lines in it.
      HDLmPostOffset = curLine.find('HDLmPostData=') 
      if HDLmPostOffset < 0:
        continue  
      HDLmPostStr = curLine[HDLmPostOffset+13:]
      curLineJson = json.loads(HDLmPostStr)
      outListJson.append(curLineJson)
      # Process the current JSON object. In some cases, this JSON object 
      # will have been created for a new session. In other cases, this
      # JSON object will have been created for a set of updates.
      processCurLine(sessionMap, fileName, i+1, curLine, curLineJson, countObject, outLines)
    except Exception as e:
      # Increment the JSON error counter
      countObject.incrJsonErrorCount()
      # Report the error
      typeOfError = 'JSON error'
      errorText = str(e)
      errorNumber = countObject.getJsonErrorCount()
      lineNumber = i+1
      timestampStr = 'Not Set'
      sessionIdStr = 'Not Set'
      curLineStr = curLine
      addEventLine(outLines, typeOfError, errorText, errorNumber, \
                   fileName, lineNumber, offset, \
                   timestampStr, sessionIdStr, curLineStr)
    offset += curLength + 1   
  # Return the list of JSON objects to the caller
  return outListJson

# Process the current line. The line is converted to JSON 
# and passed to this routine. This routine will check the
# current line. 
def processCurLine(sessionMap, fileName, lineNumber, curLineStr, curLineJson, countObject, outLines):
  # set a few starting values
  linkOrUpdates = False
  # Assume we don't have some keys
  hostNameKey = False
  linkKey = False
  reasonKey = False
  sessionIdKey = False
  updatesKey = False
  # Set a few starting values
  hostNameValue = None
  linkValue = None
  reasonValue = None
  sessionIdValue = None
  updatesValue = None
  # Check if the JSON has the keys
  if 'hostName' in curLineJson:
    hostNameKey = True
  if 'link' in curLineJson:
    linkKey = True
  if 'reason' in curLineJson:
    reasonKey = True
  if 'sessionid' in curLineJson or 'sessionId' in curLineJson:
    sessionIdKey = True
  if 'updates' in curLineJson:
    updatesKey = True
  # Check if we have updates or a link
  if linkKey or updatesKey:
    linkOrUpdates = True
  # Get the value of the host name, if any
  if hostNameKey:
    hostNameValue = curLineJson['hostName'] 
  # Get the value of the link, if any
  if linkKey:
    linkValue = curLineJson['link'] 
  # Get the value of the reason, if any
  if reasonKey:
    reasonValue = curLineJson['reason']
  # Get the value of the session ID, if any
  if sessionIdKey:
    if 'sessionid' in curLineJson:
      sessionIdValue = curLineJson['sessionid']
    else:
      sessionIdValue = curLineJson['sessionId']
  # We need to get the timestamp value from the current line
  timestampValue = curLineStr[0:19] + '.' + curLineStr[20:23]
  # Get the value of the update(s), if any
  if updatesKey:
    updatesValue = curLineJson['updates']
  # If the link key is set, we should have a session ID   
  if linkKey == True:
    # Check if we got a valid session ID from the link. We 
    # should always get a valid session ID from the link, but  
    # you never know. 
    if sessionIdValue != None:
      sessionIdKey = True
      if sessionIdValue not in sessionMap:
        # Create a new session for the current session ID
        curSession = HDLmSession()
        curSession.count = 1
        # Add the new session to the session map
        sessionMap[sessionIdValue] = curSession
        countObject.incrSessionIdUnique()
  # In some cases, we can get the session ID from the update(s).
  # If this is possible, we pretend to get the session ID from the 
  # normal location. Of course, the session ID is not really there.
  if updatesKey == True:
    sessionIdValue = extractFromUpdates(updatesValue)
    # Check if we got a valid session ID from the update(s). We 
    # should always get a valid session ID from the update(s), but  
    # you never know. 
    if sessionIdValue != None:
      sessionIdKey = True
      if sessionIdValue not in sessionMap:
        # Create a new session for the current session ID
        curSession = HDLmSession()
        curSession.count = 1
        # Add the new session to the session map
        sessionMap[sessionIdValue] = curSession
        countObject.incrSessionIdUnique()
  # Check if the 'reason' is 'Exception'. This is a very
  # special case. 
  if reasonValue == 'exception':
    countObject.incrExceptions()
    typeOfError = 'Exception'
    errorText = 'Exception'
    errorNumber = countObject.getExceptions()
    offset = None
    timestampStr = timestampValue
    sessionIdStr = sessionIdValue
    addEventLine(outLines, typeOfError, errorText, errorNumber, \
                 fileName, lineNumber, offset, \
                 timestampStr, sessionIdStr, curLineStr)
    return
  # Check if the session ID key is set
  if sessionIdKey:
    # Check if they session ID is null (a zero-length string)
    if sessionIdValue == '':
      countObject.incrSessionIdNull()    
      typeOfError = 'Session ID is null'
      errorText = 'Session ID is null'
      errorNumber = countObject.getSessionIdNull()
      offset = None
      timestampStr = timestampValue
      sessionIdStr = sessionIdValue
      addEventLine(outLines, typeOfError, errorText, errorNumber, \
                   fileName, lineNumber, offset, \
                   timestampStr, sessionIdStr, curLineStr)
      return
    # Check if the session ID is unknown
    if sessionIdValue == 'unknown':
      countObject.incrSessionIdUnknown() 
      typeOfError = "Session ID is 'unknown'"
      errorText = "Session ID is 'unknown'"
      errorNumber = countObject.getSessionIdUnknown()
      offset = None
      timestampStr = timestampValue
      sessionIdStr = sessionIdValue
      addEventLine(outLines, typeOfError, errorText, errorNumber, \
                   fileName, lineNumber, offset, \
                   timestampStr, sessionIdStr, curLineStr)
      return
  else:
    countObject.incrSessionIdNotSet()   
    typeOfError = "Session ID is not set"
    errorText = "Session ID is not set"
    errorNumber = countObject.getSessionIdNotSet()
    offset = None
    timestampStr = timestampValue
    sessionIdStr = sessionIdValue
    addEventLine(outLines, typeOfError, errorText, errorNumber, \
                 fileName, lineNumber, offset, \
                 timestampStr, sessionIdStr, curLineStr) 
  # Check if this is a link
  if sessionIdKey and linkKey:
    countObject.incrGetLinkLines()   
  # Check if this is one or more updates. Updates are
  # created when rules fire.
  if sessionIdKey and updatesKey:
    # Process all of the current update(s)
    processUpdates(sessionMap, sessionIdValue, timestampValue, curLineJson, countObject, outLines, lineNumber)
    # Increment the update counter
    countObject.incrGetUpdateLines() 
  return

# This routine processes one of more files. The caller
# provides a list of file names. This routine will process
# each file in the list.
def processFiles(fileList, sessionMap, outLines, countObject):
  # Process each file in the list
  for fileName in fileList:
    # Process the current file
    # Get the full input file name
    localName = fileName
    localNamePlusLog = localName + '.log'
    inputFileName = glbInDirName + '\\' + localNamePlusLog
    # Read the input log file
    listInFile = HDLmUtility.readInputFile(inputFileName)  
    # Fix and process the input log file
    outJsonList = fixFile(sessionMap, localNamePlusLog, listInFile, outLines, countObject)
  return

# Report the final count values
def reportFinalCounts(outLines, countObject):
  # Report the exception count
  addCountLine(outLines, 'Exceptions', countObject.getExceptions())
  # Report the JSON error count
  addCountLine(outLines, 'JSON error count', countObject.getJsonErrorCount())
  # Report the session ID error/non-error counts
  addCountLine(outLines, 'Session ID not set', countObject.getSessionIdNotSet())
  addCountLine(outLines, 'Session ID null', countObject.getSessionIdNull())
  addCountLine(outLines, 'Session ID unknown', countObject.getSessionIdUnknown())
  addCountLine(outLines, 'Session ID unique', countObject.getSessionIdUnique())
  # Report the link counts
  addCountLine(outLines, 'Link lines', countObject.getLinkLines())
  # Report the update counts
  addCountLine(outLines, 'Update lines', countObject.getUpdateLines())

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)  
  # Build the input file list
  outList = HDLmUtility.getFileList(glbInDirName)
  fileList = filterFileList(outList, glbRawPrefix)
  # Get the operating system name
  osName = getOperatingSystemName()
  # Create the error/non-errors counters data object
  countObject = HDLmCounts()
  # Get some values provided by the invoker or use default values
  result = getArgs()
  internalUseOnlyFlag = result.internal
  browserName = HDLmString.capitalize(result.Browser)
  urlStr = result.URL
  # Create the object used to accumulate output lines and add the
  # heading line
  outLines = HDLmBuildLines()
  localName = glbRawPrefix
  outputFileName = glbInDirName + '\\' + localName + '.csv'
  outLines.setFileName(outputFileName)
  # We only really need a heading line if we are not running
  # in internal use only mode
  if not internalUseOnlyFlag:  
    addHeadingLine(outLines) 
  # Create the session map for keeping track of all of the sessions
  sessionMap = {}
  # Process all of the input files
  processFiles(fileList, sessionMap, outLines, countObject)
  # Report the final counts
  reportFinalCounts(outLines, countObject)
  # Check if we are running in internal use only mode. If not,
  # write the collected output lines to a file. If we are running
  # in internal use only mode, the collect lines need to be writter
  # to standard output.
  if not internalUseOnlyFlag:
    outLines.writeOutputFile()
  else:
    for line in outLines.getLines():
      print(line)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__": 
  main()