from   HDLmBuildLines import *
from   mutableint     import MutableInt
import argparse
import json
import platform
import time

# This program appears to have been written to analyze several different
# types of log files. Some log files only have records from just one domain.
# Other log files have records from several different domains. The current 
# log file is specified later. In some important cases, several log files 
# are checked together. Note that this program is oriented towards info log
# files, not raw log files. 

# The log input directory name is stored in the field below
glbInDirName = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\PHPApps\\PHPWebProject1\\PHPWebProject1'
# The log input file name is stored in the field below
glbInFileNama = 'info 2019-05-29'
glbInFileNamb = 'info 2019-05-30'
glbInFileNamc = 'info 2019-07-27'
glbInFileNamd = 'info 2019-08-06'
glbInFileName = 'info 2019-08-23'
glbInFileNamf = 'info 2019-09-04'
glbInFileNamg = 'info 2019-09-10'
glbInFileNamh = 'info 2019-09-17'
glbInFileNami = 'info 2019-09-27'
glbInFileNamj = 'info 2019-10-04'
glbInFileNamk = 'info 2019-10-05'
glbInFileNaml = 'info 2019-10-09'
glbInFileNamm = 'info 2019-10-10'
glbInFileNamn = 'info 2019-10-16'
glbInFileNamo = 'info 2019-10-21'
glbInFileNamp = 'info 2020-10-09'
glbInFileNamq = 'info 2020-11-29'
glbInFileNamr = 'info 2021-01-08'
glbInFileNams = 'info 2021-02-01'
glbInFileNamt = 'info 2021-03-05'
glbInFileNamu = 'info 2021-07-12'
glbInFileNamv = 'info 2021-08-11'
glbInFileNamw = 'info 2022-11-02'
glbInFileNamx = 'info 2023-11-19'
glbInFileNamy = 'info 2023-12-13'
glbInFileNamz1 = 'info.www.yogadirect.com 2022-11-02'
glbInFileNamz2 = 'info.www.yogadirect.com 2023-11-19'
glbInFileNamz3 = 'info.www.yogadirect.com 2023-12-13'
glbInFileNamz4 = 'info.www.yogadirect.com 2023-12-15'
glbInFileNamz5 = 'info.www.yogadirect.com 2023-12-16 ccole'
  
# Create a class for keeping track of all of the session ID
# counts and the related counts
class HDLmCounts(object):
  # The __init__ method creates an instance of the class
  def __init__(self): 
    self.exceptions = 0
    self.jsonErrorCount = 0
    self.linkLines = 0
    self.linkSessionIdNotFound = 0
    self.sessionIdDuplicate = 0
    self.sessionIdNotSet = 0
    self.sessionIdNull = 0 
    self.sessionIdUnknown = 0 
    self.sessionIdUnique = 0
    self.updateLines = 0
    self.updateSessionIdNotFound = 0
  # Get each of the counters
  def getExceptions(self):
    return self.exceptions
  def getJsonErrorCount(self):
    return self.jsonErrorCount
  def getSessionIdNotSet(self):
    return self.sessionIdNotSet 
  def getSessionIdNull(self):
    return self.sessionIdNull 
  def getSessionIdUnknown(self):
    return self.sessionIdUnknown  
  def getSessionIdDuplicate(self):
    return self.sessionIdDuplicate
  def getSessionIdUnique(self):
    return self.sessionIdUnique
  def getLinkLines(self):
    return self.linkLines
  def getLinkSessionIdNotFound(self):   
    return self.linkSessionIdNotFound
  def getUpdateLines(self):
    return self.updateLines
  def getUpdateSessionIdNotFound(self):   
    return self.updateSessionIdNotFound
  # Increment each of the counters
  def incrExceptions(self):
    self.exceptions += 1
  def incrJsonErrorCount(self):
    self.jsonErrorCount += 1
  def incrSessionIdNotSet(self):
    self.sessionIdNotSet += 1 
  def incrSessionIdNull(self):
    self.sessionIdNull += 1   
  def incrSessionIdUnknown(self):
    self.sessionIdUnknown += 1  
  def incrSessionIdDuplicate(self):
    self.sessionIdDuplicate += 1
  def incrSessionIdUnique(self):
    self.sessionIdUnique += 1   
  def incrGetLinkLines(self):
    self.linkLines += 1 
  def incrLinkSessionIdNotFound(self):
    self.linkSessionIdNotFound += 1 
  def incrGetUpdateLines(self):
    self.updateLines += 1 
  def incrUpdateSessionIdNotFound(self):
    self.updateSessionIdNotFound += 1 

# Create a class for keeping track of all of the information
# associated with a session
class HDLmSession(object):
  # The __init__ method creates an instance of the class
  def __init__(self):
    self.count = None 
    self.updates = []
  # Add an update to the list of updates
  def addUpdate(self, update):
    self.updates.append(update)

# Create a class for keeping track of just one update. Each 
# instance of this class will be added to a list of updates.
# Each instance of this class will have all of the information  
# about just one update.
class HDLmUpdate(object):
  # The __init__ method creates an instance of the class
  def __init__(self, ruleTypeEnum, \
               ruleName, hostName, divisionName, siteName, \
               parmNumber, parmValue, modPathValue, pathValue, \
               newValue, oldValue, timestamp): 
    self.hostName = hostName
    self.divisionName = divisionName
    self.siteName = siteName
    self.modName = ruleName
    self.modType = ruleTypeEnum
    self.parmNumber = parmNumber
    self.parmValue = parmValue
    self.modPathValue = modPathValue 
    self.pathValue = pathValue
    self.newValue = newValue
    self.oldValue = oldValue
    self.timestamp = timestamp

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
def addEventLine(outLines, typeOfEvent, eventText, eventNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr):
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
  heading = '"Type of event","Event Text","Event Number","Line Number","Offset","Timestamp","Session ID","Current Line"'
  outLines.addLine(heading)

# Report the current error
def displayError(curLineJson, localCount, lineNumber, errorStr):
  print(errorStr + ' - Error count ' + str(localCount))
  print(curLineJson)
  print('Line number ' + str(lineNumber))
  return

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
      curLineJson = json.loads(curLine)
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
      addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr)
    offset += curLength + 1   
  # Return the list of JSON objects to the caller
  return outListJson

# This function gets the arguments passed by the caller (if any). Default
# values are provided as need be. 
def getArgs():
  # Set a few default values
  fullBrowserName = 'Firefox'
  urlStr = 'www.yogadirect.com'
  # urlStr = 'themarvelouslandofoz.com'
  # Build the argument parser object
  parser = argparse.ArgumentParser()
  # Add a few arguements
  parser.add_argument('Browser', nargs='?', default=fullBrowserName, 
                       help='specify the web browser to be used')
  parser.add_argument('URL', nargs='?', default=urlStr,
                      help='specify the URL to be used')
  parser.add_argument('-e', '--errors', action="store_true", default=False,
                      help='only report errors')
  parser.add_argument('-i', '--internal', action="store_true", default=False,
                      help='internal use only')
  result = parser.parse_args()  
  # Build the browser dictionary
  browserDict = {'Brave': 'Brave Browser', 'Chrome': 'Chrome', 'Dolphin': 'Dolphin Browser', 
                 'Edge': 'Microsoft Edge', 'Firefox': 'Firefox', 'Ie': 'Internet Explorer',
                 'Opera': 'Opera', 'Safari': 'Safari', 'Uc': 'UC Browser',
                 'Yandex': 'Yandex'}
  # Check the browser name
  browserName = result.Browser
  browserName = HDLmString.capitalize(browserName)
  # Check if the browser name is known or not
  if browserName not in browserDict:
    raise ValueError('Invalid browser name - ' + browserName)
  # Get the full browser name 
  fullBrowserName = browserDict[browserName]
  if fullBrowserName == None:
    raise SystemError("No browser full name for - " + browserName)
  return result

# Get the name of current operating system
def getOperatingSystemName():
  osName = platform.system() 
  if osName == 'Darwin':
    osName = 'Macintosh'
  return osName

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
  timestampKey = False
  updatesKey = False
  # Set a few starting values
  hostNameValue = None
  linkValue = None
  reasonValue = None
  sessionIdValue = None
  timestampValue = None
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
  if 'timestamp' in curLineJson:
    timestampKey = True
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
  # Get the value of the timestamp, if any
  if timestampKey:
    timestampValue = curLineJson['timestamp']
  # Get the value of the update(s), if any
  if updatesKey:
    updatesValue = curLineJson['updates']
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
    addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr)
    return
  # Check if the session ID key is set
  if sessionIdKey:
    # Check if they session ID is null
    if sessionIdValue == '':
      countObject.incrSessionIdNull()    
      typeOfError = 'Session ID is null'
      errorText = 'Session ID is null'
      errorNumber = countObject.getSessionIdNull()
      offset = None
      timestampStr = timestampValue
      sessionIdStr = sessionIdValue
      addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr)
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
      addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr)
      return
  else:
    countObject.incrSessionIdNotSet()   
    typeOfError = "Session ID is not set"
    errorText = "Session ID is not set"
    errorNumber = countObject.getSessionIdNotSet()
    offset = None
    timestampStr = timestampValue
    sessionIdStr = sessionIdValue
    addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr) 
  # Check if the host name is present and if the 
  # session ID is present and if this is not a 
  # line for updates
  if hostNameKey and sessionIdKey and not linkOrUpdates:
    # Check if we have a session for the current
    # session ID
    if sessionIdValue in sessionMap:
      # Get the session for the current session ID
      curSession = sessionMap[sessionIdValue]
      # Increment the count for the current session
      curSession.count += 1
      countObject.incrSessionIdDuplicate() 
      typeOfError = "Session ID is duplicate"
      errorText = "Session ID is duplicate"
      errorNumber = countObject.getSessionIdDuplicate()
      offset = None
      timestampStr = timestampValue
      sessionIdStr = sessionIdValue
      addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr) 
    else:
      # Create a new session for the current session ID
      curSession = HDLmSession()
      curSession.count = 1
      # Add the new session to the session map
      sessionMap[sessionIdValue] = curSession
      countObject.incrSessionIdUnique()
  # Check if this is one or more updates. Updates are
  # created when rules fire.
  if sessionIdKey and updatesKey:
    # Check if we don't have a session for the current update
    if sessionIdValue not in sessionMap:
      # Increment the error counter
      countObject.incrUpdateSessionIdNotFound()
      typeOfError = "Session ID for an update not found"
      errorText = "Session ID for an update not found"
      errorNumber = countObject.getUpdateSessionIdNotFound()
      offset = None
      timestampStr = timestampValue
      sessionIdStr = sessionIdValue
      addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr) 
    # The session ID for the current update is in the session map
    else:
      # Process all of the current update(s)
      processUpdates(sessionMap, sessionIdValue, timestampValue, curLineJson, countObject, outLines, lineNumber)
      # Increment the update counter
      countObject.incrGetUpdateLines()
  # Check if this is a link
  if sessionIdKey and linkKey:
    # Check if we don't have a session for the current link
    if sessionIdValue not in sessionMap:
      # Increment the error counter
      countObject.incrLinkSessionIdNotFound()
      typeOfError = "Session ID for a link not found"
      errorText = "Session ID for a link not found"
      errorNumber = countObject.getLinkSessionIdNotFound()
      offset = None
      timestampStr = timestampValue
      sessionIdStr = sessionIdValue
      addEventLine(outLines, typeOfError, errorText, errorNumber, lineNumber, offset, timestampStr, sessionIdStr, curLineStr) 
    # The session ID for the current update is in the session map
    else:
      countObject.incrGetLinkLines()    
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

# This routine handles a set of updates. The caller provides
# the session map, the session ID, and the current line in 
# JSON format. This routine will process the updates and add
# them to the session object.
def processUpdates(sessionMap, sessionId, timestamp, curLineJson, countObject, outLines, lineNumber):
  # Get the session for the current session ID
  curSession = sessionMap[sessionId]
  # Get the updates for the current session
  updates = curLineJson['updates']
  # Process each update
  for update in updates:
    # Get the rule name
    ruleName = update['modName']
    # Get the rule type
    ruleTypeStr = update['modType']
    ruleTypeEnum = HDLmModTypes[ruleTypeStr]
    # Get some more values from the update
    hostName = update['hostName']
    divisionName = update['divisionName']
    siteName = update['siteName']
    # Get the update parameters
    parmNumber = update['parmNumber']
    parmValue = update['parmValue']
    # Get the update path values
    modPathValue = update['modPathValue']
    pathValue = update['pathValue']
    # Get the update new and old values. The old value
    # will have the dollar amount in some cases. This 
    # really only applies to notify rules.
    newValue = update['newValue']
    oldValue = update['oldValue']
    # Create the update object  
    curUpdate = HDLmUpdate(ruleTypeEnum, \
                           ruleName, hostName, divisionName, siteName, \
                           parmNumber, parmValue, modPathValue, pathValue, \
                           newValue, oldValue, timestamp)  
    # Check if the notify checkout rule fired. Print some information 
    # from the current update.
    if (ruleName.find('Notify Check Out') >= 0):
      print(timestamp, oldValue)
    # Add the update to the list of updates
    curSession.addUpdate(curUpdate)

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
  addCountLine(outLines, 'Session ID duplicate', countObject.getSessionIdDuplicate())
  addCountLine(outLines, 'Session ID unique', countObject.getSessionIdUnique())
  # Report the link counts
  addCountLine(outLines, 'Link lines', countObject.getLinkLines())
  addCountLine(outLines, 'Link session ID not found', countObject.getLinkSessionIdNotFound())
  # Report the update counts
  addCountLine(outLines, 'Update lines', countObject.getUpdateLines())
  addCountLine(outLines, 'Update session ID not found', countObject.getUpdateSessionIdNotFound())

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)  
  # Build the input file list
  fileList = []
  # fileList.append(glbInFileNamz1)
  # fileList.append(glbInFileNamz2)
  fileList.append(glbInFileNamz3)
  fileList.append(glbInFileNamz4)
  fileList.append(glbInFileNamz5)
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
  localName = fileList[-1]
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