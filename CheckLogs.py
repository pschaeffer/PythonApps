from   HDLmConfig     import *
from   HDLmConfigInfo import *
from   io             import BytesIO
import base64
import datetime
import json
import os
import pycurl
import re
import stat
import subprocess
import sys
import tempfile
import time

# This very weird approach is needed because boto3 (the AWS Python SDK)
# is not available under Windows Visual Studio. Of course, we can't use
# any boto3 features in the Windows Visual Studio environment either.
try:
  import boto3
except Exception as e:
  pass

glbAwsAccessKeyId = '' 
glbAwsSecretAccessKey = '' 
glbCertifi = 'C:\\Users\\pscha\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\certifi\\cacert.pem'
glbDebug = True
glbFirefoxPath = '../../../../../HeadlampJetty/FirefoxCerts'
glbLambdaHandler = False
glbWindowsPassword = ''
glbWindowsUserid = ''
glbWorkPath = glbFirefoxPath
glbLogLevels = {'debug':0, 'all':1, 'info':1, 'none':1, 'notice':1, 'warn':2, 'error':3, 'exception':3, 'emerg':4}

# Each instance of this class has all of the information about
# one file system directory
class Directory(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, dirName, dirEntries):
    self.dirMap = dict()
    self.dirName = dirName
    self.dirEntries = dirEntries
    for entry in dirEntries:
      self.dirMap[entry.getFileName()] = entry
  # Get a directory entry using a file name. If the directory
  # entry does not exist, this routine will return None. 
  def getDirEntry(self, fileName):
    if fileName in self.dirMap:
      return self.dirMap[fileName]
    else:
      return None

# Each instance of this class has all of the information about
# one directory entry
class DirEntry(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, fileName, fileSize, fileLastMod, fileOwner, fileGroup, filePermissions, fileLinkCount):
    self.fileName = fileName
    self.fileSize = fileSize
    self.fileLastMod = fileLastMod
    self.fileOwner = fileOwner
    self.fileGroup = fileGroup
    self.filePermissions = filePermissions
    self.fileLinkCount = fileLinkCount
    # Get the file type from the first chraracter of the file permissions
    if len(filePermissions) > 0:
      firstChar = filePermissions[0]
      if firstChar == '-':
        self.fileType = 'file'
      elif firstChar == 'd':
        self.fileType = 'directory'
      elif firstChar == 'c':
        self.fileType = 'character device'
      elif firstChar == 'l':
        self.fileType = 'symlink'
      elif firstChar == 'p':
        self.fileType = 'named pipe'
      elif firstChar == 's':
        self.fileType = 'socket'
      elif firstChar == 'b':
        self.fileType = 'block device'
      elif firstChar == 'D':
        self.fileType = 'door'
      else:
        self.fileType = None
  # Get the file name from the current directory entry
  def getFileName(self):
    return self.fileName
  # Get the file size from the current directory entry
  def getFileSize(self):
    return self.fileSize

# Each instance of this class is an (will start out as) 
# an empty object
class EmptyObject(object):
  pass

# Each instance of this class is used to store a file range 
# and some additional information. A class must be used so 
# that the values in each instance can be changed. The file
# range value will be negative, if a negative offset from the
# end of the file should be used. The file range will be 
# positive, if the last set of bytes should be returned.
#
# Remove first is a flag used to show if the first line should
# be removed or not. This flag can be changed if the need to 
# remove the first line is detected. 
class FileRange(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, fileRange, removeFirst):
    self.fileRange = fileRange
    self.removeFirst = removeFirst
  # Get the current file range value
  def getFileRange(self):
    return self.fileRange
  # Get the current remove first value
  def getRemoveFirst(self):
    return self.removeFirst
  # Set (or reset) the current remove first value
  def setRemoveFirst(self, newRemoveFirst):
    self.removeFirst = newRemoveFirst

# Each instance of this class has all of the information about
# one HTML (really HTTP) response.
class HtmlResponse(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, httpCode, statusLine, httpHeaders, bodyLines):
    self.httpCode = httpCode
    self.statusLine = statusLine
    self.httpHeaders = httpHeaders
    self.bodyLines = bodyLines
  # Get the HTTP response code
  def getHttpCode(self):
    return self.httpCode
  # Get the HTTP headers
  def getHttpHeaders(self):
    return self.httpHeaders
  # Get the HTTP status line 
  def getStatusLine(self):
    return self.statusLine
  # Get the HTML body lines
  def getBodyLines(self):
    return self.bodyLines
  # Get the number of HTML body lines
  def getBodyLinesLen(self):
    return len(self.bodyLines)

# Each instance of this class has all of the information about
# one HTTP header
class HttpHeader(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, name, value):
    self.name = name
    self.value = value
  # Get the header name
  def getName(self):
    return self.name
    # Get the header value
  def getValue(self):
    return self.Value

# Each instance of this class has all of the information about
# one log entry
class LogEntry(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, timeStamp, type, pid, client, port, text, original):
    self.timeStamp = timeStamp
    self.type = type
    self.pid = pid
    self.client = client
    self.port = port
    self.text = text    
    self.original = original
  # Get the original log entry line and return it to the caller
  def getOriginal(self):
    return self.original
  # Get the text of the log entry and return it to the caller
  def getText(self):
    return self.text
  # Get the type of the log entry. This will be a string of 
  # some kind. 
  def getType(self):
    return self.type
  # Get the timestamp (datetime) value from a log entry
  def getTimeStamp(self):
    return self.timeStamp
  # Get the type value from a log entry
  def getType(self):
    return self.type

# Each instance of this class has all of the information about
# the entries (probably a subset) obtained from a log file
class LogFile(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, logFileName, logEntries):
    self.logFileName = logFileName
    self.logEntries = logEntries
    # Get the datetime values of the first and last log entries
    lenLogEntries = len(logEntries)
    if lenLogEntries > 0:
      firstTimeStamp = logEntries[0].getTimeStamp()
      lastTimeStamp = logEntries[lenLogEntries-1].getTimeStamp()
    else:
      firstTimeStamp = None
      lastTimeStamp = None
    # Store the first and last timestamp values
    self.firstTimeStamp = firstTimeStamp
    self.lastTimeStamp = lastTimeStamp
  # Get the first timestamp (datetime) value from a log instance
  def getFirstTimeStamp(self):
    return self.firstTimeStamp
  # Get the last timestamp (datetime) value from a log instance
  def getLastTimeStamp(self):
    return self.lastTimeStamp
  # Get the log entry objects (as a list) from the current log file
  def getLogEntries(self):
    return self.logEntries
  # Get the number of log entry objects and return the value to the
  # caller
  def getLogEntryCount(self):
    return len(self.logEntries)
  # Get the log file name and return it to the caller
  def getLogFileName(self):
    return self.logFileName

# Analyze a log file. This routine returns a list of messages.
# The number of messages in the list may be zero, one, or more
# than one. Note that the log file may actually be just an HTML
# response, rather than a complete log file. The log type is an
# actual log type. The log may have come from any one of several
# machines. For example, an error log may have come from any one 
# of several different machines.
def analyzeLog(checkName, logFile, logType, logLevel):
  outMsgs = []
  # Invoke the correct log analysis routine 
  if logType == 'ApacheAccess':
    outMsgs = analyzeLogApacheAccess(logFile, logLevel)
  elif logType == 'ApacheError':
    outMsgs = analyzeLogApacheError(logFile, logLevel)
  elif logType == 'ApacheHigh':
    outMsgs = analyzeLogApacheHigh(checkName, logType, logFile, logLevel)
  elif logType == 'ApacheStatus':
    outMsgs = analyzeLogApacheStatus(checkName, logType, logFile, logLevel)
  elif logType == 'html':
    outMsgs = analyzeLogHtml(checkName, logType, logFile, logLevel)
  elif logType == 'htmlCheckStatus':
    outMsgs = analyzeLogHtmlCheckStatus(checkName, logType, logFile, logLevel)
  elif logType == 'info':
    outMsgs = analyzeLogInfo(logFile, logLevel)
  elif logType == 'JavaLog4jAccess':
    outMsgs = analyzeLogJavaLog4j(logFile, logLevel, checkName, logType)
  elif logType == 'JavaLog4jError':
    outMsgs = analyzeLogJavaLog4j(logFile, logLevel, checkName, logType)
  elif logType == 'JavaLog4jLog':
    outMsgs = analyzeLogJavaLog4j(logFile, logLevel, checkName, logType)
  elif logType == 'JettyHigh':
    outMsgs = analyzeLogJettyHigh(checkName, logType, logFile, logLevel)
  elif logType == 'JettyStatus':
    outMsgs = analyzeLogJettyStatus(checkName, logType, logFile, logLevel)
  else:
    raise ValueError('Invalid log type specified')
  return outMsgs

# Analyze an Apache access log file. There isn't much to do here.
# Just count the number of log entries.
def analyzeLogApacheAccess(logFile, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  logFileLen = logFile.getLogEntryCount()
  outMsg = 'Access log - Total entries {}'.format(logFileLen)
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg) 
  return outMsgs

# Analyze an ApacheError log file. There isn't much to do
# here. Just count the number of log entries and the number
# of each type of entry.
def analyzeLogApacheError(logFile, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelValue, reqListValue] = checkLogLevelValues(requestedLogLevel)
  outMsgs = []
  logFileLen = logFile.getLogEntryCount()
  # Get a Python dictionary with each of the entry types
  outCounts = getTypeCount(logFile)
  # Get the number of messages that must be reported
  reportCount = 0
  for key, value in outCounts.items():
    keyValue = glbLogLevels.get(key, None)
    if keyValue == None:
      reportCount += 1
    elif keyValue >= reqLevelValue:
      reportCount += value
  # Build a standard message using the count values
  if reportCount > 0:
    typeCountsStr = getTypeString(outCounts)
    outMsgFormat = 'Error log - Total entries {} {}'
    outMsg = outMsgFormat.format(logFileLen, typeCountsStr)
    # If the number of remaining log file entries is greater than zero,
    # add the message to the output message list 
    outMsgs.append(outMsg)
  # Add output messages for every qualifying message if the caller
  # asked for them
  if reportCount > 0 and reqListValue == True:
    logFileEntries = logFile.getLogEntries()
    for logEntry in logFileEntries:
      logEntryType = logEntry.getType().lower()
      logEntryLevel = glbLogLevels.get(logEntryType, None)
      if logEntryLevel == None or logEntryLevel >= reqLevelValue:
        originalLine = logEntry.getOriginal()
        outMsgs.append(originalLine)
  return outMsgs

# Analyze an Apache (2) status HTML response. The log file is actually
# just an HTML response, rather than a complete log file in this case.
# The log type has no real meaning in this case. The log type should 
# always be 'ApacheHigh'. However, the check name is quite important 
# and shows what type of check (resource) we are running.
def analyzeLogApacheHigh(checkName, logType, highResponse, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  httpCode = highResponse.getHttpCode()
  checkNameCapitalized = checkName.capitalize()
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the HTTP code isn't some type of integer. That means that
    # a serious error was detected. 
    if isinstance(httpCode, int) == False:
      errorDetected = True
      outMsg = '{} - HTTP error ({})'.format(checkNameCapitalized, httpCode)
      break
    # Apparently, the HTTP code is really an integer. This allows for 
    # additional checks. 
    bodyLinesLen = highResponse.getBodyLinesLen()
    # Check if an error occurred. Any HTTP code other than 200 is 
    # considered to be an error. If we don't get more than 10 lines
    # of HTML output, that is considered to be an error. 
    if httpCode != 200 or bodyLinesLen <= 10:
      errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # At this point we need to scan the output HTML lines looking for the lines that give 
    # the status of each server process or potential server process 
    beforeRequests = True
    bodyLines = highResponse.getBodyLines()
    finalLine = ''
    lineExtend = ['', '', '', '', '', '']
    for line in bodyLines:
      # Remove any HTML tags from the current line
      line = removeHtmlTags(line)
      # We really want to skip all lines until we find a specific line
      # that is just before the server process status lines
      if beforeRequests:
        line = line.replace(',', ' ')
        # Split the current HTML line into a set of words
        lineSplit = line.split()        
        lineSplit.extend(lineExtend)
        # Skip the current line if it is not the line we are looking for
        if lineSplit[1] != 'requests' or \
           lineSplit[2] != 'currently' or \
           lineSplit[3] != 'being' or \
           lineSplit[4] != 'processed':
          continue
        # At this point we have found the line we are looking for
        beforeRequests = False
        continue 
      # Change a bunch of possible status value to a period
      lineCopy = line.replace('_', '.').replace('S', '.').replace('R', '.').\
                      replace('W', '.').replace('K', '.').replace('D', '.').\
                      replace('C', '.').replace('L', '.').replace('G', '.').\
                      replace('I', '.')
      # Check if we have a process status line
      if lineCopy.startswith('....'):
        finalLine += line.strip()
      # If the current line is not a process status line and if we have
      # already processed one or more status lines, we are done
      else:
        if len(finalLine) > 0:
          break 
    # We definitely have an error if we did not find the lines we 
    # looking for
    if len(finalLine) == 0:
      errorDetected = True
      outTxt = '{} - HTTP code {} HTML lines {} Target lines not found'
      outMsg = outTxt.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # The target lines were found. We can now calculate the current 
    # high-water mark.
    totalSlots = len(finalLine)
    unUsedSlots = finalLine.count('.')
    currentHighWater = totalSlots - unUsedSlots
    if currentHighWater > 50:
      errorDetected = True
    outTxt = '{} - Current high-water count {}'
    outMsg = outTxt.format(checkNameCapitalized, currentHighWater)
    break
  # Add the output message if need be
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  return outMsgs

# Analyze an Apache (2) status HTML response. The log file is actually
# just an HTML response, rather than a complete log file in this case.
# The log type has no real meaning in this case. The log type should 
# always be 'ApacheStatus'. However, the check name is quite important
# and shows what type of check (resource) we are running.
def analyzeLogApacheStatus(checkName, logType, statusResponse, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  httpCode = statusResponse.getHttpCode()
  checkNameCapitalized = checkName.capitalize()
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the HTTP code isn't some type of integer. That means that
    # a serious error was detected. 
    if isinstance(httpCode, int) == False:
      errorDetected = True
      outMsg = '{} - HTTP error ({})'.format(checkNameCapitalized, httpCode)
      break
    # Apparently, the HTTP code is really an integer. This allows for 
    # additional checks. 
    bodyLinesLen = statusResponse.getBodyLinesLen()
    # Check if an error occurred. Any HTTP code other than 200 is 
    # considered to be an error. If we don't get more than 10 lines
    # of HTML output, that is considered to be an error. 
    if httpCode != 200 or bodyLinesLen <= 10:
      errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # At this point we need to scan the output HTML lines looking for the number of requests
    # currently being processed
    bodyLines = statusResponse.getBodyLines()
    lineExtend = ['', '', '', '', '', '']
    lineFound = False
    for line in bodyLines:
      line = removeHtmlTags(line)
      line = line.replace(',', ' ')
      # Split the current HTML line into a set of words
      lineSplit = line.split()        
      lineSplit.extend(lineExtend)
      # Skip the current line if it is not the line we are looking for
      if lineSplit[1] != 'requests' or \
         lineSplit[2] != 'currently' or \
         lineSplit[3] != 'being' or \
         lineSplit[4] != 'processed':
        continue
      # At this point we have found the line we are looking for
      lineFound = True
      break
    # We definitely have an error if we did not find the line we 
    # looking for
    if lineFound == False:
      errorDetected = True
      outTxt = '{} - HTTP code {} HTML lines {} Target line not found'
      outMsg = outTxt.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # The target line was found. We can now check the number of current 
    # requests.
    requestCount = lineSplit[0]
    requestCount = int(requestCount)
    if requestCount > 35:
      errorDetected = True
    outTxt = '{} - Current requests {}'
    outMsg = outTxt.format(checkNameCapitalized, requestCount)
    break
  # Add the output message if need be
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  return outMsgs

# Analyze an HTML response. The log file is actually just
# an HTML response, rather than a complete log file in 
# this case. The log type has no real meaning in this case.
# The log type should always be 'html'. However, the check
# name is quite important and shows what type of check (resource)
# we are running.
def analyzeLogHtml(checkName, logType, htmlResponse, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  httpCode = htmlResponse.getHttpCode()
  checkNameCapitalized = checkName.capitalize()
  # The HTTP code may show that the request failed completely.
  # In that case, we can not try get the number of body lines.
  if isinstance(httpCode, int):
    # Check if we are looking for anomalies or not. If we are
    # looking for anomalies, then some very special code is 
    # needed here.
    if checkName == 'checkanomalies':
      bodyLinesLen = htmlResponse.getBodyLinesLen()
      # Check if an error occurred
      if httpCode != 200 or bodyLinesLen > 0:
        errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
    elif checkName == 'checkexceptcmd':
      bodyLinesLen = htmlResponse.getBodyLinesLen()
      # Check if an error occurred
      if httpCode != 200 or bodyLinesLen > 1:
        errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
    else:
      bodyLinesLen = htmlResponse.getBodyLinesLen()
      # Check if an error occurred
      if httpCode != 200 or bodyLinesLen < 100:
        errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
  # The HTTP code isn't some type of integer. That means that a serious error
  # was detected. 
  else:
    errorDetected = True
    outMsg = '{} - HTTP error ({})'.format(checkNameCapitalized, httpCode)
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  # Check if we need to generate output messages for each
  # anomaly that was found. This may well be the case.
  if checkName == 'checkanomalies' and \
     reqListValue == True and \
     bodyLinesLen >= 1: 
    # Try to get the HTML lines from HTML response
    bodyLines = htmlResponse.getBodyLines()
    bodyLinesLen = len(bodyLines)
    # Make sure we only got one HTML body line
    if bodyLinesLen != 1:
      raise ValueError('Body lines length ({}) is invalid'.format(bodyLinesLen))
    # Split the one body line into separate lines for each event type
    lines = bodyLines[0].split('</p>')
    linesLen = len(lines)
    lines = lines[0:linesLen-1]
    for line in lines:
      outMsg = line[3:]
      outMsgs.append(outMsg)
  # Check if we need to generate output messages for the current 
  # event
  if checkName == 'checkexceptcmd' and \
     reqListValue == True and \
     bodyLinesLen >= 0: 
    # Try to get the HTML lines from HTML response
    bodyLines = htmlResponse.getBodyLines()
    bodyLinesLen = len(bodyLines)
    # Make sure we only got one HTML body line
    if bodyLinesLen != 0 and bodyLinesLen != 1:
      raise ValueError('Body lines length ({}) is invalid'.format(bodyLinesLen))
    # Get the exception line and make some changes to it
    if bodyLinesLen > 0:
      line = bodyLines[0]
      line = line.replace('<p>', '')
      line = line.replace('</p>', '/')   
      outMsg = line[:-1]
      outMsgs.append(outMsg)
  return outMsgs

# Analyze an OWO Test HTML response for check status processing. 
# The log file is actually just an HTML response, rather than a 
# complete log file in this case. The log type has no real meaning 
# in this case. The log type should always be 'htmlCheckStatus'.
# However, the check name is quite important and shows what type
# of check (resource) we are running.
def analyzeLogHtmlCheckStatus(checkName, logType, htmlResponse, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  httpCode = htmlResponse.getHttpCode()
  checkNameCapitalized = checkName.capitalize()
  # The HTTP code may show that the request failed completely.
  # In that case, we can not try get the number of body lines.
  if isinstance(httpCode, int):
    # Check if we are check the status of the server. If the 
    # server is down, some very special code is needed. 
    bodyLinesLen = htmlResponse.getBodyLinesLen()
    # Check if an error occurred
    if httpCode != 200 or bodyLinesLen < 100:
      errorDetected = True
    outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
  # The HTTP code isn't some type of integer. That means that a serious error
  # was detected. 
  else:
    errorDetected = True
    outMsg = '{} - HTTP error ({})'.format(checkNameCapitalized, httpCode)  
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  # We need to switch servers if an error has been detected
  if errorDetected and (glbLambdaHandler == True):
    moveToNextServer('Java Proxy A')
  return outMsgs

# Analyze an info log file. There isn't much to do here.
# Just count the number of log entries.
def analyzeLogInfo(logFile, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  logFileLen = logFile.getLogEntryCount()
  outMsg = 'Info log - Total entries {}'.format(logFileLen)
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  return outMsgs

# Analyze a Java logging file. There isn't much to do here.
# Just count the number of log entries and the number of
# each type of entry. The log could have come from any 
# one of several machines that use Java logging.
def analyzeLogJavaLog4j(logFile, requestedLogLevel, checkName, logType):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelValue, reqListValue] = checkLogLevelValues(requestedLogLevel)
  outMsgs = []
  logFileLen = logFile.getLogEntryCount()
  # Get a Python dictionary with each of the entry types
  outCounts = getTypeCount(logFile)
  # Get the number of messages that must be reported
  reportCount = 0
  for key, value in outCounts.items():
    key = key.lower()
    keyValue = glbLogLevels.get(key, None)
    if keyValue == None:
      reportCount += 1
    elif keyValue >= reqLevelValue:
      reportCount += value
  # Build a standard message using the count values
  if reportCount > 0:
    typeCountsStr = getTypeString(outCounts)
    outMsgFormat = 'Java log - Total entries {} {}'
    outMsg = outMsgFormat.format(logFileLen, typeCountsStr)
    # If the number of remaining log file entries is greater than zero,
    # add the message to the output message list 
    outMsgs.append(outMsg)
  # Check if this was a request for exceptions from the Java log file.
  # If this is true, then we must check each log entry for an exception.
  # If an exception is found, we must add the exception to the output
  # message list.
  if checkName == 'checkexceptlog':
     logFileEntries = logFile.getLogEntries()
     for logEntry in logFileEntries: 
       text = logEntry.getText()
       # The statement below will fail, if the current line contains bad
       # (or incomplete) JSON. The current input file may have some number
       # of bad JSON lines in it.
       HDLmPostOffset = text.find('HDLmPostData=') 
       if HDLmPostOffset < 0:
         continue  
       HDLmPostStr = text[HDLmPostOffset+13:]
       textJson = json.loads(HDLmPostStr)
       # Check if the current line contains an exception
       if 'reason' not in textJson:
         continue
       if textJson['reason'] != 'exception':
         continue
       # Get some information about the exception
       hostName = textJson['hostName']
       divisionName = textJson['divisionName']
       siteName = textJson['siteName']
       ruleName = textJson['modification']
       fullRuleName = '{}/{}/{}/{}'.format(hostName, divisionName, siteName, ruleName)
       # Build the final exception message
       outMsg = 'Exception' + ' - ' + fullRuleName
       outMsgs.append(outMsg)
  # This is not a check for exceptions in the log file
  else:
    # Add output messages for every qualifying message if the caller
    # asked for them
    if reportCount > 0 and reqListValue == True:
      logFileEntries = logFile.getLogEntries()
      for logEntry in logFileEntries:
        logEntryType = logEntry.getType().lower()
        logEntryLevel = glbLogLevels.get(logEntryType, None)
        if logEntryLevel == None or logEntryLevel >= reqLevelValue:
          originalLine = logEntry.getOriginal()
          outMsgs.append(originalLine)
  return outMsgs

# Analyze a Jetty (Java) status HTML response. The log file is actually
# just an HTML response, rather than a complete log file in this case.
# The log type has no real meaning in this case. The log type should 
# always be 'JettyHigh'. However, the check name is quite important and 
# shows what type of check (resource) we are running.
def analyzeLogJettyHigh(checkName, logType, highResponse, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  httpCode = highResponse.getHttpCode()
  checkNameCapitalized = checkName.capitalize()
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the HTTP code isn't some type of integer. That means that
    # a serious error was detected. 
    if isinstance(httpCode, int) == False:
      errorDetected = True
      outMsg = '{} - HTTP error ({})'.format(checkNameCapitalized, httpCode)
      break
    # Apparently, the HTTP code is really an integer. This allows for 
    # additional checks. 
    bodyLinesLen = highResponse.getBodyLinesLen()
    # Check if an error occurred. Any HTTP code other than 200 is 
    # considered to be an error. If we don't get more than 10 lines
    # of HTML output, that is considered to be an error. 
    if httpCode != 200 or bodyLinesLen <= 10:
      errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # At this point we need to scan the output HTML lines looking for the maximum 
    # number of requests that have been processed
    bodyLines = highResponse.getBodyLines()
    lineExtend = ['', '', '', '', '', '']
    lineFound = False
    lineIndex = -1
    for line in bodyLines:
      lineIndex += 1
      line = removeHtmlTags(line)
      # Split the current HTML line into a set of words
      lineSplit = line.split()        
      lineSplit.extend(lineExtend)
      # Skip the current line if it is not the line we are looking for
      if lineSplit[0] != 'Requests' or \
         lineSplit[1] != 'active' or \
         lineSplit[2] != 'max' :
        continue
      break
    # We need to get the next line at this point. The next line will
    # actually have the number of active requests.
    if (lineIndex+1) < bodyLinesLen:
      line = bodyLines[lineIndex+1]
      line = removeHtmlTags(line)
      lineSplit = line.split() 
      # At this point we have found the line we are looking for
      lineFound = True    
    # We definitely have an error if we did not find the line we 
    # are looking for
    if lineFound == False:
      errorDetected = True
      outTxt = '{} - HTTP code {} HTML lines {} Target line not found'
      outMsg = outTxt.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # The target line was found. We can now check the number of current 
    # requests.
    maxRequestCount = lineSplit[0]
    maxRequestCount = int(maxRequestCount)
    if maxRequestCount > 150:
      errorDetected = True
    outTxt = '{} - Current high-water count {}'
    outMsg = outTxt.format(checkNameCapitalized, maxRequestCount)
    break
  # Add the output message if need be
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  return outMsgs

# Analyze an Jetty (Java) status HTML response. The log file is actually
# just an HTML response, rather than a complete log file in this case.
# The log type has no real meaning in this case. The log type should 
# always be 'JettyStatus'. However, the check name is quite important and 
# shows what type of check (resource) we are running.
def analyzeLogJettyStatus(checkName, logType, statusResponse, requestedLogLevel):
  # Check the log level string passed by the caller. The log 
  # level string may actually be quite complex. We need to 
  # check the log level string and break it down into each 
  # part.
  [reqLevelKey, reqListValue] = checkLogLevelKeys(requestedLogLevel)
  errorDetected = False
  outMsgs = []
  httpCode = statusResponse.getHttpCode()
  checkNameCapitalized = checkName.capitalize()
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the HTTP code isn't some type of integer. That means that
    # a serious error was detected. 
    if isinstance(httpCode, int) == False:
      errorDetected = True
      outMsg = '{} - HTTP error ({})'.format(checkNameCapitalized, httpCode)
      break
    # Apparently, the HTTP code is really an integer. This allows for 
    # additional checks. 
    bodyLinesLen = statusResponse.getBodyLinesLen()
    # Check if an error occurred. Any HTTP code other than 200 is 
    # considered to be an error. If we don't get more than 10 lines
    # of HTML output, that is considered to be an error. 
    if httpCode != 200 or bodyLinesLen <= 10:
      errorDetected = True
      outMsg = '{} - HTTP code {} HTML lines {}'.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # At this point we need to scan the output HTML lines looking for the number of requests
    # currently being processed
    bodyLines = statusResponse.getBodyLines()
    lineExtend = ['', '', '', '', '', '']
    lineFound = False
    lineIndex = -1
    for line in bodyLines:
      lineIndex += 1
      line = removeHtmlTags(line)
      # Split the current HTML line into a set of words
      lineSplit = line.split()        
      lineSplit.extend(lineExtend)
      # Skip the current line if it is not the line we are looking for
      if lineSplit[0] != 'Requests' or \
         lineSplit[1] != 'active' or \
         lineSplit[2] != '' :
        continue
      break
    # We need to get the next line at this point. The next line will
    # actually have the number of active requests.
    if (lineIndex+1) < bodyLinesLen:
      line = bodyLines[lineIndex+1]
      line = removeHtmlTags(line)
      lineSplit = line.split() 
      # At this point we have found the line we are looking for
      lineFound = True      
    # We definitely have an error if we did not find the line we 
    # are looking for
    if lineFound == False:
      errorDetected = True
      outTxt = '{} - HTTP code {} HTML lines {} Target line not found'
      outMsg = outTxt.format(checkNameCapitalized, httpCode, bodyLinesLen)
      break
    # The target line was found. We can now check the number of current 
    # requests.
    requestCount = lineSplit[0]
    requestCount = int(requestCount)
    if requestCount > 35:
      errorDetected = True
    outTxt = '{} - Current requests {}'
    outMsg = outTxt.format(checkNameCapitalized, requestCount)
    break
  # Add the output message if need be
  if reqLevelKey == 'all' or \
     (reqLevelKey == 'error' and errorDetected == True):
    outMsgs.append(outMsg)
  return outMsgs

# This routine assigns an elastic ip address to an instance.
# This step is needed for many reasons, including automater
# failover
def assignEipToInstance(eipId, instanceId):
  ec2 = boto3.client('ec2')
  response = ec2.associate_address(
    AllocationId=eipId,
    InstanceId=instanceId)
  return

# This code sends zero or more messages to the correct target
# which may be a phone number or may be an Email address
def awsSendTarget(outMsgs, target, sesClient, snsClient):
  # Send SMS message(s) to the specified phone number
  if target.find('@') < 0:
    for outMsg in outMsgs:
      response = snsClient.publish(PhoneNumber=target, Message=outMsg)
  # Send Email message(s) to the specified Email address
  if target.find('@') > 0 and len(outMsgs) > 0:
    # Build the Email message body by combining all of the lines
    bodyText = ''
    for outMsg in outMsgs:
      if bodyText != '':
        bodyText += '<br>'
      bodyText += outMsg
    # Actually, build and send the Email
    response = sesClient.send_email( \
      Source          = 'peter.schaeffer@headlamp-software.com', \
      Destination     = { \
        'CcAddresses' : [ ],  \
        'ToAddresses' : [ target ],  \
        'BccAddresses': [ ] }, \
      Message = { \
        'Subject' : {
          'Data'     : outMsgs[0],
          'Charset'  : 'UTF-8' },     
        'Body'       : {
          'Text'     : {
            'Data'   : 'TEXT_FORMAT_BODY',
            'Charset': 'UTF-8' },       
          'Html'     : {
            'Data'   : bodyText,
            'Charset': 'UTF-8' } } },
      ReplyToAddresses = [ 'peter.schaeffer@headlamp-software.com' ] )

# This code sends zero or more messages to zero or more phone
# numbers or Email addresses
def awsSendTargets(outMsgs, targets):
  # Count the SMS and Email targets
  countSes = 0
  countSns = 0
  for target in targets:
    if target.find('@') > 0:
      countSes += 1
    else:
      countSns += 1
  # Create a boto3/SES client, if need be
  if countSes > 0:
    sesClient = boto3.client('ses', \
                             aws_access_key_id=glbAwsAccessKeyId, \
                             aws_secret_access_key=glbAwsSecretAccessKey, \
                             region_name='us-east-1')
  else:
    sesClient = None
  # Create a boto3/SNS client, if need be
  if countSns > 0:
    snsClient = boto3.client('sns', \
                             aws_access_key_id=glbAwsAccessKeyId, \
                             aws_secret_access_key=glbAwsSecretAccessKey, \
                             region_name='us-east-1')
    snsClient.set_sms_attributes(attributes = {"DefaultSMSType": "Transactional"})
  else:
    snsClient = None
  # Handle each target (each target is a separate phone number)
  for target in targets:
    awsSendTarget(outMsgs, target, sesClient, snsClient)

# Build a directory class object for the directory passed by
# the caller. The log type is an actual log type. The log may 
# be coming from any one of several machines. For example, an
# error log may be coming from any one of several different 
# machines.
def buildDirectory(dirName, checkName, logType):
  dirList = []
  fileName = dirName
  hostName = getLogHostName(checkName)
  # Check is we are running under Windows or not. A completely
  # different set of code is needed for Windows. The Windows 
  # code does not use SFTP to get directory information.
  if isWindows():
    # The list returned below includes folders as well as files.
    # We really don't want to process folders. We only want to
    # process files.
    fileList = os.listdir(dirName)
    for fileName in fileList:
      fileData = os.stat(dirName + fileName)
      isBlk = stat.S_ISBLK(fileData.st_mode)
      isChr = stat.S_ISCHR(fileData.st_mode)
      isdir = stat.S_ISDIR(fileData.st_mode)
      isDoor = stat.S_ISDOOR(fileData.st_mode)
      isFile = stat.S_ISREG(fileData.st_mode)
      isFifo = stat.S_ISFIFO(fileData.st_mode)
      islink = stat.S_ISLNK(fileData.st_mode)
      isPort = stat.S_ISPORT(fileData.st_mode)
      isSock = stat.S_ISSOCK(fileData.st_mode)
      isWht = stat.S_ISWHT(fileData.st_mode)
      fileModificationDate = os.path.getmtime(dirName + fileName)
      filePermissions = None
      if isBlk:
        filePermissions = 'b'
      elif isChr:
        filePermissions = 'c'
      elif isdir:
        filePermissions = 'd'
      elif isDoor:
        filePermissions = 'D'
      elif isFile:
        filePermissions = '-'
      elif isFifo:
        filePermissions = 'p'
      elif islink:
        filePermissions = 'l'
      elif isPort:
        filePermissions = 'P'
      elif isSock:
        filePermissions = 's'
      elif isWht:
        filePermissions = 'w'
      fileSize = os.path.getsize(dirName + fileName)
      # The last modified date/time is not actually correct. The
      # Convert the epoch time (in floating-point seconds) to a
      # local time. The local time is wrong. The conversion appears
      # to not take into account daylight savings time.
      lastModDateTime = time.ctime(fileModificationDate)
      # Create the new directory entry object
      dirEntry = DirEntry(fileName, fileSize, lastModDateTime, None, None, filePermissions, None)
      dirList.append(dirEntry)
  # We are not running under Windows. We can use SFTP to get the
  # directory information.
  else:
    keyFileNames = buildKeyFiles()
    ftpBytes = getFtpBytes(hostName, fileName, keyFileNames, 'ubuntu')
    ftpString = ftpBytes.decode('iso-8859-1')
    # Split the headers into separate lines 
    ftpLines = ftpString.splitlines()
    # Process each line of data. Each line is a directory entry.
    for line in ftpLines:
      # Get a few values from the current line
      lineSplit = line.split()
      permissions = lineSplit[0]
      linkCount = int(lineSplit[1])
      ownerName = lineSplit[2]
      ownerGroup = lineSplit[3]
      fileSize = int(lineSplit[4])
      # Convert the month string to a month number
      lastModMonth = lineSplit[5]
      lastModMonth = lastModMonth.lower()
      lastModMonth = ('jan feb mar apr may jun jul aug sep oct nov dec'.index(lastModMonth))//4+1
      lastModDay = int(lineSplit[6])
      # Get the last modification time. This value may actually be a year 
      # value. 
      lastModTime = lineSplit[7]
      fileName = lineSplit[8]
      # The last modified date/time may be in several formats
      if lastModTime.find(':') < 0:
        # Get the year value as an integer
        lastModYear = int(lastModTime)
        lastModDateTime = datetime.datetime(lastModYear, lastModMonth, lastModDay)
      else:
        # Get the current year as an integer value for use below
        now = datetime.datetime.utcnow()
        lastModYear = int(now.year)
        # Get the hour and minute value
        lastModHour = int(lastModTime[0:2])
        lastModMinute = int(lastModTime[3:])
        lastModDateTime = datetime.datetime(lastModYear, lastModMonth, lastModDay, \
                                            lastModHour, lastModMinute)
      # Create the new directory entry object
      dirEntry = DirEntry(fileName, fileSize, lastModDateTime, ownerName, ownerGroup, permissions, linkCount)
      dirList.append(dirEntry)
  # Build the directory object
  dirObject = Directory(dirName, dirList)
  return dirObject

# Build the temporary key files. The file names are returned to 
# the caller using a list.
def buildKeyFiles():
  privateKeyData = \
    '-----BEGIN RSA PRIVATE KEY-----' + '    \n' + \
    'MIIEowIBAAKCAQEAua6ymEKZda3X4mDypMeHqnRZp26VC35WYB3Q+nP12p5cNcYp' + '    \n' + \
    'GTr5nxI2SCmWp+94xZoURvR/cfDo9SF0TynfqKyvJEPMpBOPg4FkHHWOA5AJCrKP' + '    \n' + \
    'pWhUuiuMG2CVP/7wQYHPmjj0Wc38uItFHPyvpI9XKMDSy809rsbWf9m2sIyw3dlc' + '    \n' + \
    'buyf7KIvBh23H0uPodVlai9YEhsQsiqrWngvbc0v4Za7yB2iqUeMS+xTfigoD/kc' + '    \n' + \
    'JAE5NlHLXML9U0qTcg1I5ib/vqToxM6F40S4nqTNTBKDkQNjvlMGPzJUK7u0ohJt' + '    \n' + \
    'sLZT0uD+NhtloOgH1JvffJ+a3gNZnkksH33eTQIDAQABAoIBAFfo8f1MasNgTvmK' + '    \n' + \
    '1NZW8VAuTdQLct1CLzrKYwpwpFGg8B81dnfPiCdbw/9eUUmpAxDq5fbCAyS63lBQ' + '    \n' + \
    'SnTAane9ah5NSzHTYPrt46vlrBrbsqwx5fh18MdDns3HaGIoHS+medeWZ3mtIJ1u' + '    \n' + \
    'soYKzE2o36cXw7VhsnZxBVT6ipgC9UVo5EjVay0uz4S4k/YLKfZDtVcNBYfMaefe' + '    \n' + \
    '9B7PaaD5MUCsUIxhQOviAstaB538euFgjjiMdu5Qhpq6X8ZyPRXoGZ9NH5ejzZD3' + '    \n' + \
    'yuNzGv4B8qSblNbQxBxciUPSZToQ9GQZ+5RZP4MfR+6Kx74pE6h8UtczT72yTyG5' + '    \n' + \
    '18EksIECgYEA6NEDXe32u8Iqa6zxVBVb8mmtw2nLnSTgSLCwRM1zFfzh4zh0NKch' + '    \n' + \
    '+1N+vkVbZVb/eR/FatnhtZqAc1bNp6j2qpwgkgb3RUB+6cOAPe9/yhMXSEzGNj7D' + '    \n' + \
    'o26U5XP5twmCI8lGMFWluZletfN5YVF3PQHijRQERDnYN+pQB/FEvYUCgYEAzCwj' + '    \n' + \
    'LEOP2P1WSvWSOg+nEyAVDkKBymXnTdQPRlNvO0xlKL0WowsN9ZMUKQkAY1gzI1KW' + '    \n' + \
    'Pb0lwX+Sd3KgmMCnYGb+X+Het3NDOfDs5Ftp26Ajei8zAp3xguJ3W4CSiW1rYRVn' + '    \n' + \
    'WpOfzRyCfPM9Vyv0yX16josCtfofeZaXzg1ytCkCgYBzbQzqSMyHEiDN+ZQ8R8qq' + '    \n' + \
    'SNKpi44zftDjuRXrRqDESfgEGz0hzar/W8n+s4w4lgVbG/FYpGVPECaXCHY1pYOF' + '    \n' + \
    '2pobS/DUGMHTS+YMzuzgVs64PbgXtM5x/KU9jV5E7SXkcCmoVQ4xEmTueKO5KBah' + '    \n' + \
    '3IlhwIbM/JDCSB0dkvStsQKBgQC2ABJKft9Xmly17TowL4vLbKnYUEjKVxRdOE91' + '    \n' + \
    'bSKWRX9XVVc8d7o10qoB+lgyNok/T3tGBboGRuYVPEUUZYfOU4Elj36tIT4oBC/n' + '    \n' + \
    'T+WJNbLqU/CwwIJtHdsv4ei+QJ+bpyy+fSHSATwAjgN8FV7bzdLWBeygsxojlK41' + '    \n' + \
    'q584IQKBgC9x/8xH4PX5IzX1CdgoNGU9OLNmhcyL21rL6IKfCku0dXiDep6g4hE0' + '    \n' + \
    '91ktCJRcmMpRl22/erzNhfLLZJRsuzmgEvdp3ROcV6z3LsOURHDt20KQB7JIKGqO' + '    \n' + \
    '9jyBtKiPBeHIg2wIc3yhVd7I807nMGrXPzzgOJtTbNw/k5R4D6cc' + '    \n' + \
    '-----END RSA PRIVATE KEY-----' + '    \n'
  publicKeyData = \
    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5rrKYQpl1rdfiYPKkx4eqdFm' + \
    'nbpULflZgHdD6c/Xanlw1xikZOvmfEjZIKZan73jFmhRG9H9x8Oj1IXRPKd+orK' + \
    '8kQ8ykE4+DgWQcdY4DkAkKso+laFS6K4wbYJU//vBBgc+aOPRZzfy4i0Uc/K+kj' + \
    '1cowNLLzT2uxtZ/2bawjLDd2Vxu7J/soi8GHbcfS4+h1WVqL1gSGxCyKqtaeC9t' + \
    'zS/hlrvIHaKpR4xL7FN+KCgP+RwkATk2Uctcwv1TSpNyDUjmJv++pOjEzoXjRLi' + \
    'epM1MEoORA2O+UwY/MlQru7SiEm2wtlPS4P42G2Wg6AfUm998n5reA1meSSwffd' + \
    '5N imported-openssh-key'
  privateKeyFileName = writeTemporary(privateKeyData)
  publicKeyFileName = writeTemporary(publicKeyData)
  return [privateKeyFileName, publicKeyFileName]

# This routine takes one line of the Apache access log and builds a log entry
# class instance from it
def buildLogEntryApacheAccess(line):
  lineOff = 0
  # Get the client IP address that preceeds the 
  # Get the first set of characters in square brackets
  firstOff = line.find('[', lineOff)
  if firstOff < 0:
    raise ValueError('First left square bracket not found')
  if firstOff == 0:
    raise ValueError('First left square bracket not found in the correct place')
  # The client IP address preceeds the access date and time
  clientString = line[0:firstOff]
  clientSplit = clientString.split()
  clientString = clientSplit[0]
  # The access date and time are in the first set of square brackets
  lastOff = line.find(']', lineOff)
  if lastOff < 0:
    raise ValueError('First right square bracket not found')
  timeString = line[firstOff+1:lastOff]
  timeDay = int(timeString[0:2])
  timeMonth = timeString[3:6]
  timeMonth = timeMonth.lower()
  timeMonth = ('jan feb mar apr may jun jul aug sep oct nov dec'.index(timeMonth))//4+1
  timeYear = int(timeString[7:11])
  timeHHMMSS = timeString[12:20]
  timeHour = int(timeHHMMSS[0:2])
  timeMinute = int(timeHHMMSS[3:5])
  timeSecond = int(timeHHMMSS[6:8])
  timeStamp = datetime.datetime(timeYear, timeMonth, timeDay, \
                                timeHour, timeMinute, timeSecond)
  lineOff = lastOff + 1
  # Get the rest of the line
  text = line[lineOff:]
  text = text.strip()
  # Build the final log file entry instance
  logEntry = LogEntry(timeStamp, None, None, \
                      clientString, None, text, line)
  return logEntry

# This routine takes one line of the Apache error log and builds a log entry
# class instance from it. As it turns out, the error can contain lines
# that don't have a standard format. We need to handle those as well. 
def buildLogEntryApacheError(line, checkName, logType):
  lineOff = 0
  # Get the first set of characters in square brackets
  firstOff = line.find('[', lineOff)
  if firstOff < 0:
    raise ValueError('First left square bracket not found')
  if firstOff != 0:
    raise ValueError('First left square bracket not found in the correct place')
  lastOff = line.find(']', lineOff)
  if lastOff < 0:
    raise ValueError('First right square bracket not found')
  timeString = line[firstOff+1:lastOff]
  timeSplit = timeString.split()
  timeDayOfWeek = timeSplit[0]
  timeMonth = timeSplit[1]
  timeMonth = timeMonth.lower()
  timeMonth = ('jan feb mar apr may jun jul aug sep oct nov dec'.index(timeMonth))//4+1
  timeDay = int(timeSplit[2])
  timeHHMMSS = timeSplit[3]
  timeHour = int(timeHHMMSS[0:2])
  timeMinute = int(timeHHMMSS[3:5])
  timeSecond = int(timeHHMMSS[6:8])
  timeMicroseconds = int(timeHHMMSS[9:15])
  timeYear = int(timeSplit[4])
  timeStamp = datetime.datetime(timeYear, timeMonth, timeDay, \
                                timeHour, timeMinute, timeSecond, timeMicroseconds)
  lineOff = lastOff + 1
  # Get the second set of characters in brackets
  firstOff = line.find('[', lineOff)
  if firstOff < 0:
    raise ValueError('Second left square bracket not found')
  lastOff = line.find(']', lineOff)
  if lastOff < 0:
    raise ValueError('Second right square bracket not found')
  typeString = line[firstOff+1:lastOff]
  typeSplit = typeString.split(':')
  typeString = typeSplit[1]
  lineOff = lastOff + 1
  # Get the third set of characters in brackets
  firstOff = line.find('[', lineOff)
  if firstOff < 0:
    raise ValueError('Third left square bracket not found')
  lastOff = line.find(']', lineOff)
  if lastOff < 0:
    raise ValueError('Third right square bracket not found')
  pidString = line[firstOff+1:lastOff]
  pidSplit = pidString.split()
  pidInt = int(pidSplit[1])
  lineOff = lastOff + 1
  # Get the fourth set of characters in brackets
  firstOff = line.find('[', lineOff)
  # Check if we really found a fourth set of characters in brackets.
  # This will not always be true. In some cases, we don't have a client
  # string at all. For example, some error mesages look line,
  #
  #   [Thu Dec 19 03:05:36.365345 2019] [ssl:warn] [pid 1441] 
  #   AH01909: oneworldobservatory.com:443:0 server certificate 
  #
  # In this case, we have no client string and no client port number.
  # Both values are set to None in this case.
  if firstOff < 0:
    clientString = None
    clientPortInt = None
  # If we were able to get the left bracket offset for the client
  # string, then we should be able to get the right bracket offset
  # for the client string
  else:
    lastOff = line.find(']', lineOff)
    if lastOff < 0:
      raise ValueError('Fourth right square bracket not found')
    clientString = line[firstOff+1:lastOff]
    clientSplit = clientString.split()
    if len(clientSplit) > 1:
      clientString = clientSplit[1]
    else:
      clientString = clientSplit[0]
    clientSplit = clientString.split(':')
    clientString = clientSplit[0]
    clientPortInt = int(clientSplit[1])
    lineOff = lastOff + 1
  # Get the rest of the line
  text = line[lineOff:]
  text = text.strip()
  # Build the final log file entry instance
  logEntry = LogEntry(timeStamp, typeString, pidInt, \
                      clientString, clientPortInt, text, line)
  return logEntry

# This routine takes one line of the Java log and builds a log entry
# class instance from it. This will only work for lines that are not part 
# of some exception. Lines that are part of an exception are handled by a 
# different set of code. The log file with the current entry could have 
# come from anyone of several machines using Java logging.
def buildLogEntryJavaLog4j(line):
  # Check if the date/time has a 'T' in it. If it does, then we have a
  # modern data/time. Some of the values below need to be adjusted.
  dateTimeAdjust = 0
  if line[10] == 'T':
    dateTimeAdjust = 1
  lineSplit = line.split() 
  # Get the timestamp from the line
  timeYear = int(line[0:4])
  timeMonth = int(line[5:7])
  timeDay = int(line[8:10])
  timeHour = int(line[11:13])
  timeMinute = int(line[14:16])
  timeSecond = int(line[17:19])
  timeMicroseconds = int(line[20:23])*1000
  timeStamp = datetime.datetime(timeYear, timeMonth, timeDay, \
                                timeHour, timeMinute, timeSecond, \
                                timeMicroseconds)
  # Get the thread ID. This value is not used for now.
  threadString = lineSplit[2-dateTimeAdjust]
  threadStringLen = len(threadString)
  threadString = threadString[1:threadStringLen]
  # Get the log entry type value
  typeString = lineSplit[3-dateTimeAdjust]
  # Get the text part of the log entry
  text = None
  textOff = line.find(' - ')
  if textOff > 0:
    text = line[textOff+3:]
    text = text.strip()
  # Build the final log file entry instance
  logEntry = LogEntry(timeStamp, typeString, None, \
                      None, None, text, line)
  return logEntry

# This routine takes one line of the info log and builds a log entry
# class instance from it
def buildLogEntryInfo(line):
  lineObj = json.loads(line)
  # Try to get the timestamp from the JSON
  if 'timestamp' in lineObj:
    timeString = lineObj['timestamp']
    timeYear = int(timeString[0:4])
    timeMonth = int(timeString[5:7])
    timeDay = int(timeString[8:10])
    timeHHMMSS = timeString[11:26]
    timeHour = int(timeHHMMSS[0:2])
    timeMinute = int(timeHHMMSS[3:5])
    timeSecond = int(timeHHMMSS[6:8])
    timeMicroseconds = int(timeHHMMSS[9:15])
    timeStamp = datetime.datetime(timeYear, timeMonth, timeDay, \
                                  timeHour, timeMinute, timeSecond, \
                                  timeMicroseconds)
  else:
    timeStamp = None
  # Try to get the client IP address and port from the JSON
  if 'client' in lineObj:
    clientString = lineObj['client']
    clientSplit = clientString.split(':')
    clientIpString = clientSplit[0]
    if len(clientSplit) > 1:
      clientPortInt = int(clientSplit[1])
    else:
      clientPortInt = None
  else:
    clientIpString = None
    clientPortInt = None
  # Try to use the reason as the type string 
  if 'reason' in lineObj:
    typeString = lineObj['reason']
  else:
    typeString = None
  # The entire JSON object is the text
  text = line
  # Build the final log file entry instance
  logEntry = LogEntry(timeStamp, typeString, None, \
                      clientIpString, clientPortInt, text, line)
  return logEntry

# Build a set of log entries for (from) an error log file. The format of
# an error log file is different. Some entries hava a non-standard format.
# Some entries have a standard format. The log type is an actual log type. 
# The log may have come from any one of several machines. For example, an 
# error log may have come from any one of several different machines. The 
# log type in this case, should always be 'ApacheError'.
def buildLogFileApacheError(checkName, logType, fileLines):
  logEntries = []
  for line in fileLines:
    # Check if the current line is a simple log entry. If thie current line
    # is a simple log entry, just handle it and skip to the next line.
    if re.search('^\[\D{3}\s\D{3}\s\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6}\s\d{4}', line) != None:
      logEntry = buildLogEntryApacheError(line, checkName, logType)
    # We now have a line that does not start with a timestamp
    else:
      logEntry = LogEntry(None, 'none', None, \
                          None, None, line, line)
    logEntries.append(logEntry)
  return logEntries

# Build a set of log entries for (from) a Java log file. The format of
# a Java log file is different. Some entries span many lines. Some entries
# are entirely on one line. The log type is an actual log type. The log 
# may have come from any one of several machines. For example, an error
# log may have come from any one of several different machines. The log
# type in this case, should always be 'log4j'.
def buildLogFileJavaLog4j(logType, fileLines):
  logEntries = []
  fileLinesLen = len(fileLines)
  i = 0
  while i < fileLinesLen:
    # Check if the current line is a simple log entry. If thie current line
    # is a simple log entry, just handle it and skip to the next line.
    curLine = fileLines[i]
    if re.search('^\d{4}\-\d{2}\-\d{2}', curLine) != None:
      logEntry = buildLogEntryJavaLog4j(curLine)
      logEntries.append(logEntry)
      i += 1
      continue
    # We now have a line that does not start with a timestamp. We 
    # need to add all of the subsequent lines that don't start 
    # with a timestamp.
    errorLineCount = 1
    text = curLine
    i += 1
    # Try to add additional lines to the current line. This process
    # continues until we run out of lines or find a line that can not
    # be added to the current line.
    while True:
      if i >= fileLinesLen:
        break
      laterLine = fileLines[i]
      if re.search('^\d{4}\-\d{2}\-\d{2}', laterLine) != None:
        break 
      text += laterLine
      errorLineCount += 1
      i += 1
    # Add the extended line to the set of log entries
    logEntry = LogEntry(None, 'EXCEPTION', None, \
                        None, None, text, curLine)
    logEntries.append(logEntry)
  return logEntries

# This routine takes a log level string and breaks it down into 
# separate components. The first part of the log level is the
# actual level. The level is returned as a string (the original
# string value is returned). The second part of the log level 
# indicates if detailed messages should be generated. This value
# becomes either True or False.
def checkLogLevelKeys(logLevel):
  logLevelSplit = logLevel.split()
  logSplitLen = len(logLevelSplit)
  # Report an error, if the log level string can not found
  if logSplitLen == 0:
    raise ValueError('Log level not found')
  # Get the actual level value and convert it to an integer
  level = logLevelSplit[0]
  levelLower = level.lower()
  if levelLower not in glbLogLevels:
    raise ValueError('Log level value ({}) is invalid'.format(level))
  # Handle, if found, the list value
  listValue = False
  if logSplitLen > 1:
    listValue = logLevelSplit[1]
    listValueLower = listValue.lower()
    if listValueLower == 'list':
      listValue = True
  # Return the final values to the caller
  return [levelLower, listValue]

# This routine takes a log level string and breaks it down into 
# separate components. The first part of the log level is the
# actual level. The level is returned as a number (0 for debug,
# 1 for info, 2 for warn, 3 for error, etc.). The second part 
# of the log level indicates if detailed messages should be 
# generated. This value becomes either True or False.
def checkLogLevelValues(logLevel):
  logLevelSplit = logLevel.split()
  logSplitLen = len(logLevelSplit)
  # Report an error, if the log level string can not found
  if logSplitLen == 0:
    raise ValueError('Log level not found')
  # Get the actual level value and convert it to an integer
  level = logLevelSplit[0]
  levelLower = level.lower()
  if levelLower not in glbLogLevels:
    raise ValueError('Log level value ({}) is invalid'.format(level))
  levelValue = glbLogLevels[levelLower]
  # Handle, if found, the list value
  listValue = False
  if logSplitLen > 1:
    listValue = logLevelSplit[1]
    listValueLower = listValue.lower()
    if listValueLower == 'list':
      listValue = True
  # Return the final values to the caller
  return [levelValue, listValue]

# This routine converts a log level string to a log level number
# if possible. If the log level string is not recognized, then
# the Python None value is returned.
def convertLogLevelString(logLevel):
  return glbLogLevels.get(logLevel.lower(), None)

# Get the Allocation ID for an IP address. The IP address
# must be passed in as a string (such as '3.14.54.178' 
# without the quotes). The return value is either None 
# or a string.
def getAllocIdFromIp(ipAddress):
  ec2 = boto3.client('ec2')
  response = ec2.describe_addresses()  
  addresses = response['Addresses']
  for address in addresses:
    publicIp = address['PublicIp']
    if publicIp == ipAddress:
      allocId = address['AllocationId']
      return allocId
  return None

# Get the resource id of the current instance. This 
# is the resource id of the server that is currently
# active.
def getCurrentServerResourceId():
  # Get the current server
  currentServer = getParameterValue('/Test1/CurrentServer')
  # Get the resource id from the tag name
  tagName = currentServer
  resourceType = 'instance'
  rId = getResourceIdFromTag(tagName, resourceType)
  return rId

# Get the directory name from the file name
def getDirectoryName(fileName):
  fileNameLen = len(fileName)
  # Set the slash character based on whether we are running
  # under Windows or not
  if isWindows():
    slashChar = '\\'
  else:
    slashChar = '/'
  # Check if the last character of the file name is a slash.
  # That is a serious error.
  if fileName[fileNameLen-1] == slashChar:
    raise ValueError('File name ends with a slash')
  # Look backwards from the end for the last slash
  lastOff = fileName.rfind(slashChar)
  if lastOff < 0:
    raise ValueError('File name does not have slash')
  dirName = fileName[0:lastOff+1]
  return dirName

# Get some bytes from a file. This a low-level routine tht only
# assumes that we can get bytes from the target file. This is 
# always true for all types of files (images, text, etc.). 
#
# Note that the file range value can be set or it can be none.
# If the value is positive, then only the last set of bytes are 
# returned to the caller. The size of the last set is the value 
# passed by the caller. If the value is negative, then it is 
# passed to pycurl as an option.
# 
# File range is actually an object. The file range numeric value
# is stored inside the object.
def getFileBytes(hostName, fileName, fileRange = None):
  keyFileNames = buildKeyFiles()
  ftpBytes = getFtpBytes(hostName, fileName, keyFileNames, 'ubuntu', fileRange)
  return ftpBytes

# Get the last part of a file name from a full file name. For example,
# if the caller passes /test/log, this routine will return log.
def getFileLastName(fileName):
  fileNameLen = len(fileName)
  # Set the slash character based on whether we are running
  # under Windows or not
  if isWindows():
    slashChar = '\\'
  else:
    slashChar = '/'
  # Check if the last character of the file name is a slash.
  # That is a serious error.
  if fileName[fileNameLen-1] == slashChar:
    raise ValueError('File name ends with a slash')
  # Look backwards from the end for the last slash
  lastOff = fileName.rfind(slashChar)
  lastName = fileName[lastOff+1:]
  return lastName

# Get some lines from a file. This routine will only work if the
# target file actually contains lines. If thie file is an image,
# this routine will not work. 
#
# Note that the file range value can be set or it can be none.
# If the value is positive, then only the last set of bytes are 
# returned to the caller. The size of the last set is the value 
# passed by the caller. If the value is negative, then it is 
# passed to pycurl as an option.
# 
# File range is actually an object. The file range numeric value
# is stored inside the object.
def getFileLines(hostName, fileName, fileRange = None):
  ftpBytes = getFileBytes(hostName, fileName, fileRange)
  ftpString = ftpBytes.decode('iso-8859-1')
  # Split the headers into separate lines 
  ftpLines = ftpString.splitlines()
  return ftpLines

# Get the file size. The file size is obtained from the directory
# containing the file. If the file size can not be obtained, this
# routine will return a Python None value. The log type is an 
# actual log type. The log may have come from any one of several 
# machines. For example, an error log may have come from any one
# of several different machines.
def getFileSizeFromDirectory(fileName, checkName, logType):
  dirName = getDirectoryName(fileName)
  lastName = getFileLastName(fileName)
  fileDirectory = buildDirectory(dirName, checkName, logType)
  fileDirectoryEntry = fileDirectory.getDirEntry(lastName)
  # Check if we really got a directory entry back of if we
  # got a Python None value
  if fileDirectoryEntry != None:
    fileSize = fileDirectoryEntry.getFileSize()
  else:
    fileSize = None
  return fileSize

# Get some binary data with FTP (actually SFTP). Note that the file range
# value can be set or it can be None. If the value is positive, then only
# the last set of bytes are returned to the caller. The size of the last
# set is the value passed by the caller. If the value is negative, then
# it is passed to pycurl as an option.
# 
# File range is actually an object. The file range numeric value
# is stored inside the object.
def getFtpBytes(hostName, fileName, keyFileNames, userid = None, fileRange = None):
  # Build the complete FTP string
  ftpString = 'sftp://' + hostName + '/' + fileName
  buffer = BytesIO()
  c = pycurl.Curl()
  c.setopt(c.URL, ftpString)
  if isWindows():
    c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(c.WRITEDATA, buffer)
  # Check if we are running under Windows. If this is correct, then 
  # a fixed userid and password are used. Otherwise, we use the userid
  # passed by the caller.
  if isWindows():
    c.setopt(c.USERPWD, glbWindowsUserid + ':' + glbWindowsPassword)
  else:
    if userid != None:
      c.setopt(c.USERNAME, userid)
  if fileRange != None:
    fileRangeValue = fileRange.getFileRange()
    if fileRangeValue < 0:
      c.setopt(c.RANGE, str(fileRangeValue))
  c.setopt(c.SSH_PRIVATE_KEYFILE, keyFileNames[0])
  c.setopt(c.SSH_PUBLIC_KEYFILE, keyFileNames[1])
  c.perform()
  c.close()
  bodyBytes = buffer.getvalue()
  # Check if need to return just some of the bytes to the caller
  if fileRange != None:
    fileRangeValue = fileRange.getFileRange()
    if fileRangeValue >= 0 and fileRangeValue < len(bodyBytes):
      fileRange.setRemoveFirst(True)
      if fileRangeValue > 0:
        bodyBytes = bodyBytes[-fileRangeValue:]
      else:
        bodyBytes = b''
  return bodyBytes

# Get some information from an HTTP header. The name of the 
# header will always be returned to the caller. The value 
# will be returned if the header has a value. This code
# should be able to deal with multi-line headers, but 
# probably does not. 
def getHeaderInfo(httpHeader):
  name = None
  value = None
  colonOff = httpHeader.find(':')
  # Check if the HTTP header has a value
  if colonOff < 0:
    # Generally, we want to convert the header name to lower case.
    # However, the status line is something of an exception.
    name = httpHeader.strip()
    nameLower = name.lower()
    if nameLower[0:4] == 'http':
      pass
    else:
      name = name.lower()
  else:
    name = httpHeader[0:colonOff]
    name = name.strip().lower().lower()
    value = httpHeader[colonOff+1:]
    value = value.strip()
  return [name, value]

# Get a set of HTTP headers from a set of hTTP header bytes.
# This routine converts the HTTP header bytes to a string and
# then extracts the HTTP headers from the HTTP lines. 
def getHeadersFromBytes(headerBytes):
  outMap = dict()
  headerString = headerBytes.decode('iso-8859-1')
  # Split the headers into separate lines 
  headerLines = headerString.splitlines()
  # Process each header line
  for line in headerLines:
    if len(line.strip()) == 0:
      continue
    [name, value] = getHeaderInfo(line)
    # Check if we have already processed this header name
    if name not in outMap:
      outMap[name] = []
    outMap[name].append(value)
  return outMap

# Get the HTTP headers for a URL in the form of a Python map.
# This code should be able to deal with multi-line header, but
# probably does not. Note that some headers can be duplicated
# (such as Set-Cookie). As a consequence, the value will always
# be a list. In other words, this routine will return a map 
# where each value (not key) is a Python list. 
def getHeadersUrl(urlString):
  outMap = dict()
  # Get the HTTP headers for the URL
  buffer = BytesIO()
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  if isWindows():
    c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(c.HEADER, True)
  c.setopt(c.NOBODY, True)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  headerBytes = buffer.getvalue()
  return getHeadersFromBytes(headerBytes)

# Get the HTML body for a log type value passed by the
# caller. Of course, the log type in this case, isn't a 
# real log type. Note that this routine returns a set of
# lines to the caller. The log type in this case, should
# always be 'html'.
def getHttpHtmlResponse(checkName, logType, seconds):
  [httpCode, httpStatusLine, httpHeaders, bodyBytes] = getHttpHtmlResponseInfo(checkName, logType, seconds) 
  # We can only decode the HTTP body in some cases
  if isinstance(httpCode, int):
    htmlString = bodyBytes.decode('utf-8')
    # Split the headers into separate lines. Generally this
    # can be done in a very simplistic way. However, Jetty 
    # servers, return a response that can't be split as easily.
    if logType == 'JettyHigh' or \
       logType == 'JettyStatus':
      htmlLines = splitHtmlTag(htmlString)
    else:       
      htmlLines = htmlString.splitlines()
  else:
    htmlLines = None
  # Build the HTTP/HTML response object
  response = HtmlResponse(httpCode, httpStatusLine, httpHeaders, htmlLines)
  return response

# Get some HTTP/HTML information for a log type value 
# passed by the caller. Of course, the log type in this 
# case, isn't a real log type. Note that this routine 
# returns a list of information to the caller. Some of 
# the information is stored in byte arrays. The caller
# must handle the conversion to a string, if that is 
# required. The log type in this case, should always be
# 'htnl'.
def getHttpHtmlResponseInfo(checkName, logType, seconds):
  fileName = getLogFileName(checkName)
  hostName = getLogHostName(checkName)
  urlString = 'https://' + hostName + fileName
  [httpCode, httpStatusLine, httpHeaders, bodyBytes] = getInfoFromUrl(urlString, seconds)
  return [httpCode, httpStatusLine, httpHeaders, bodyBytes]

# Get a response from a URL. The response includes a 
# variety of information. The body (probably HTML) of
# the response is returned as an array of bytes. Note, 
# that this code sets the follow location flag to true. 
# This causes Curl to follow certain types of responses.
#
# The HTTP code returned by this routine may be an actual
# HTTP code (such as 200 or 404) or it may be a string
# with Curl connection information in it. The later case
# is always a failure of some kind.
def getInfoFromUrl(urlString, seconds):
  # Get the HTTP headers and HTML body for a URL
  headerBuffer = BytesIO()
  bodyBuffer = BytesIO()
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  if isWindows():
    c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(c.FOLLOWLOCATION, True)
  c.setopt(pycurl.HEADERFUNCTION, headerBuffer.write)
  c.setopt(pycurl.WRITEFUNCTION, bodyBuffer.write)
  # Check if we have a valid maximum time value
  if seconds != None:
    c.setopt(c.TIMEOUT, seconds)
  # Running the actual Curl request may cause an exception. We need
  # to catch the exception and handle it. The numeric HTTP code is 
  # only available if the Curl request was handled properly. 
  try:
    c.perform()
    httpCode = c.getinfo(c.HTTP_CODE)
    headerBytes = headerBuffer.getvalue()
    httpHeaders = getHeadersFromBytes(headerBytes)
    bodyBytes = bodyBuffer.getvalue()
    # For now we really don't have the HTTP status line. At some point
    # we will get it. Use an empty string for now.
    httpStatusLine = ''
  # The Curl request failed with some type of error. The code below
  # tries to handle the error. 
  except pycurl.error as e:
    # Copy the error information into more convenient variables
    errorArgs = e.args
    errorCode = errorArgs[0]
    errorString = errorArgs[1]
    # Check for a specific error and set the HTTP code accordingly
    if errorCode == 7 and errorString.endswith('Connection refused'):
      httpCode = 'Connection failed'
    else:
      httpCode = errorString
    # Since the connection did not work, we have no other information
    # to return
    httpHeaders = None
    bodyBytes = None
    httpStatusLine = None
  # The code below should trap all other exceptions. We try to use
  # the error message associated with the exception. This may or may
  # not be possible. 
  except Exception as e:
    # Get the error description, if any
    if e == None:
      errorString = 'Exception'  
    else:
      errorArgs = e.args
      if len(errorArgs)> 0:
        errorString = errorArgs[-1]
      else:
        errorString = 'Exception'   
    # Use the error string as the HTTP code
    httpCode = errorString
    # Since the connection did not work, we have no other information
    # to return
    httpHeaders = None
    bodyBytes = None
    httpStatusLine = None
  # Close the Curl object. This causes resources to be released as
  # need be. 
  c.close()
  return [httpCode, httpStatusLine, httpHeaders, bodyBytes]

# Get the last part of a URL response. This code was not 
# completed.
def getLastUrl(urlString, desiredSize):
  # Check if the URL supports getting the last part of the response
  [size, ranges] = getSizeInfoUrl(urlString)
  if ranges != 'bytes':
    raise RuntimeError("URL doesn't support ranges")
  # Check if actual size is less than the desired size
  if size < desiredSize:
    desiredSize = size

# This routine gets some lines from a log file of some kind.
# The caller specifies the range in bytes. In other words, the
# last block of bytes are obtained from the file and they are 
# used to build a set of lines. Note that the first line is 
# almost certainly a partial line and is discarded. 
#
# Note that the file range value can be set or it can be none.
# If the value is positive, then only the last set of bytes are 
# returned to the caller. The size of the last set is the value 
# passed by the caller. If the value is negative, then it is 
# passed to pycurl as an option.
# 
# File range is actually an object. The file range numeric value
# is stored inside the object.
def getLogFile(checkName, logType, fileRange):
  fileName = getLogFileName(checkName)
  hostName = getLogHostName(checkName)
  logEntries = []
  # Get some lines from the log file  
  fileLines = getFileLines(hostName, fileName, fileRange)
  lenFileLines = len(fileLines)
  # We may or may not want to get rid of the first line from 
  # the file. In some cases, the first line is a partial line
  # that we can not process. However, this will not always be
  # the case. 
  removeFirst = fileRange.getRemoveFirst()
  if lenFileLines > 0 and removeFirst == True:
    fileLines.pop(0)
    lenFileLines -= 1
  # Convert each of the lines to a log entry class instance. This
  # code will only work for some types of logs. Other types of logs
  # require a different code path.
  if logType == 'ApacheAccess' or \
     logType == 'info':
    for line in fileLines:
      if logType == 'ApacheAccess':
        logEntry = buildLogEntryApacheAccess(line)
      elif logType == 'info':
        logEntry = buildLogEntryInfo(line)
      else:
        raise ValueError('Invalid log type specified')
      logEntries.append(logEntry)
  # Error log files must be handled separately. They have entries
  # that have a non-standard format. Some entries have a standard
  # formst. Other entires do not. We must handle both cases. 
  if logType == 'ApacheError':
    logEntries = buildLogFileApacheError(checkName, logType, fileLines)
  # Java log files must be handled separately. They have entries
  # that span many lines.
  if logType == 'JavaLog4jAccess' or \
     logType == 'JavaLog4jError' or \
     logType == 'JavaLog4jLog':
    logEntries = buildLogFileJavaLog4j(logType, fileLines)
  # Build the log file class instance
  logFile = LogFile(fileName, logEntries)
  return logFile

# Get the file name for a log file. The type of the log
# file is passed by the caller. The actual log file name
# is returned to the caller. Note that the log file name
# is actually a path name in some cases. The log type passed
# by the caller is actually a log type. The same log type
# can exist on any one of several machines. 
def getLogFileName(checkName):
  if checkName == 'javaproxyaaccess':
    if isWindows():
      fileName = 'C:\\Users\\pscha\\HeadlampJetty\\workspace-4.33.0\\ProxyServerA\\HDLmLog.log'
    else:
      fileName = '/home/ubuntu/HeadlampJetty/workspace/ProxyServer/HDLmLog.log'
  elif checkName == 'javaproxyaerror':
    if isWindows():
      fileName = 'C:\\Users\\pscha\\HeadlampJetty\\4.23.0\\ProxyServerA\\HDLmLog.log'
    else:
      fileName = '/home/ubuntu/HeadlampJetty/workspace/ProxyServer/HDLmLog.log'
  elif checkName == 'javaproxyahigh':
    fileName = '/server-status'
  elif checkName == 'javaproxyainfo':
    if isWindows():
      fileName = 'C:\\Users\\pscha\\HeadlampJetty\\workspace-4.33.0\\ProxyServerA\\info.log'
    else:
      fileName = '/var/www/html/example.com/public_html/info.log' 
  elif checkName == 'javaproxyalog':
    if isWindows():
      fileName = 'C:\\Users\\pscha\\HeadlampJetty\\workspace-4.33.0\\ProxyServerA\\HDLmLog.log'
    else:
      fileName = '/home/ubuntu/HeadlampJetty/workspace/ProxyServer/HDLmLog.log'
  elif checkName == 'javaproxyastatus':
    fileName = '/server-status'
  elif checkName == 'owotest2':
    fileName = '/'
  elif checkName == 'owotest3':
    fileName = '/'
  elif checkName == 'owotest4':
    fileName = '/zh-CN/'
  elif checkName == 'owotest5':
    fileName = '/zh-CN/'
  elif checkName == 'owotest6':
    fileName = '/'
  elif checkName == 'checkanomalies':
    fileName = '/events-checkAnomalies'
  elif checkName == 'checkexceptcmd':
    fileName = '/events-checkExceptions'
  elif checkName == 'checkexceptlog':
    if isWindows():
      fileName = 'C:\\Users\\pscha\\HeadlampJetty\\workspace-4.33.0\\ProxyServerA\\HDLmLog.log'
    else:
      fileName = '/home/ubuntu/HeadlampJetty/workspace/ProxyServer/HDLmLog.log'
  elif checkName == 'checkstatus':
    fileName = '/'
  else:
    raise ValueError('Invalid check name and/or log file specified')
  return fileName

# Get the host name for a log file. The type of the log
# file is passed by the caller. The actual log file host 
# name is returned to the caller.
def getLogHostName(checkName):
  if checkName == 'javaproxyaaccess':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'javaproxyaerror':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'javaproxyahigh':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'javaproxyainfo':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'javaproxyalog':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'javaproxyastatus':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'owotest2':
    hostName = 'oneworldobservatory.com'
  elif checkName == 'owotest3':
    hostName = 'www.oneworldobservatory.com'
  elif checkName == 'owotest4':
    hostName = 'oneworldobservatory.com'
  elif checkName == 'owotest5':
    hostName = 'www.oneworldobservatory.com'
  elif checkName == 'owotest6':
    hostName = 'owo.dnsalias.com'
  elif checkName == 'checkanomalies':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'checkexceptcmd':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'checkexceptlog':
    hostName = 'javaproxya.dnsalias.com'
  elif checkName == 'checkstatus':
    hostName = 'javaproxya.dnsalias.com'
  else:
    raise ValueError('Invalid check name and/or log type specified')
  return hostName

# This routine gets some lines from a log file of some kind.
# The caller specifies the time period needed in seconds. The
# callers also specifies the log file name and type. Note that
# in some cases, we don't actually want to get a log file. In
# some cases, an HTML response is returned as the 'log file'.
def getLogLast(checkName, logType, seconds):
  # Check if we should just return an HTML reponse as the 
  # 'log file' to the caller
  if logType == 'ApacheHigh':
    highResponse = getHttpHtmlResponse(checkName, logType, seconds)
    return highResponse
  # Check if we should just return an status reponse as the 
  # 'log file' to the caller
  elif logType == 'ApacheStatus':
    statusResponse = getHttpHtmlResponse(checkName, logType, seconds)
    return statusResponse
  # Check if we should just return an HTML reponse as the 
  # 'log file' to the caller
  elif logType == 'html':
    htmlResponse = getHttpHtmlResponse(checkName, logType, seconds)
    return htmlResponse
  # Check if we should just return an status reponse as the 
  # 'log file' to the caller. Note that the server is tested
  # twice here. We only recognize a failure if both tests fail.
  elif logType == 'htmlCheckStatus':
    # Test the server twice
    htmlResponseA = getHttpHtmlResponse(checkName, logType, seconds)
    httpCodeA = htmlResponseA.httpCode
    htmlResponseB = getHttpHtmlResponse(checkName, logType, seconds)
    httpCodeB = htmlResponseB.httpCode
    # Check the responses we got back from the server
    if httpCodeA != 200 and httpCodeB != 200:
      return htmlResponseB
    else:
      if httpCodeA == 200:
        return htmlResponseA
      else:
        return htmlResponseB
  # Check if we should just return an HTML reponse as the 
  # 'log file' to the caller
  if logType == 'JettyHigh':
    highResponse = getHttpHtmlResponse(checkName, logType, seconds)
    return highResponse
  # Check if we should just return an status reponse as the 
  # 'log file' to the caller
  elif logType == 'JettyStatus':
    statusResponse = getHttpHtmlResponse(checkName, logType, seconds)
    return statusResponse
  # Check if we should return a process list response as the
  # 'log file' to the caller
  elif logType == 'process':
    processResponse = getProcessResponse(checkName, logType, seconds)
    return processResponse    
  # Get part or all of a log file
  if isWindows():
    dateTimeNow = datetime.datetime.now()
  else:
    dateTimeNow = datetime.datetime.utcnow()
  fileName = getLogFileName(checkName)
  # Get the file size. We need this value later to make sure
  # that we are not asking for too much data.
  fileSize = getFileSizeFromDirectory(fileName, checkName, logType)
  if fileSize == None:
    fileSize = 0
  # The function used to get the file size should never fail. However,
  # you never know.
  testSize = 1000000
  # We may need to try more than once (sad to say)
  while True:
    # Check if we are asking for too much data. The amount of data
    # requested should never exceed the file size.
    testSize = min(testSize, fileSize)
    # Check if we are asking for the entire file. If this is true,
    # then we do not need to remove the first line. However, if we
    # are not requesting the entire file, the first line might be a
    # partial line that we can not handle. This doesn't work as well
    # as one might hope. The size of the file can change. Even if we
    # think we are requesting the entire file, this might not be true.
    # The file may actually get bigger as we attempt to get it.
    removeFirst = (fileSize != testSize)
    if removeFirst == True:
      fileRange = FileRange(-testSize, removeFirst)
    else:
      fileRange = FileRange(testSize, removeFirst)
    logFile = getLogFile(checkName, logType, fileRange)
    # Get the first timestamp from the log file class instance. The log  
    # file class instance may not actually have a first timestamp value
    # that can be used. 
    oldestDateTime = getLogOldestDateTime(logFile)
    # Check if actually got a first timestamp value back. This will
    # not always be true. The oldest entry might not have a valid 
    # timestamp value. In that is true, then we should retry and
    # ask for more data. 
    if oldestDateTime == None:
      pass
    # The oldest entry appears to have had a valid timestamp value.
    # This means that we can check to see if we have found enough
    # data.
    else:
      timeSecondsFloat = datetime.timedelta.total_seconds(dateTimeNow - \
                                                          oldestDateTime) 
      # Check if we found all of the data we need 
      if timeSecondsFloat >= seconds:
        break 
    # Check if we have already obtained as much data as we can  
    if testSize == fileSize:
      break 
    # We don't have enough data yet. Double the number of bytes
    # to get. Note that this might happen more than once.
    testSize = testSize << 1
  # We can check all of the log file entrie too see which ones are too
  # old. The entries that are too old are discarded. The good one are 
  # added to the final log list entry list. 
  addToLogList = False
  logList = []
  logEntries = logFile.getLogEntries()
  for entry in logEntries:
    # Check if we looking for the first log entry that can be
    # added to the final list of log entries
    if addToLogList == False:
      # Get the timestamp for the current log list entry. Not
      # all log list entries have timestamp values.
      entryDateTime = entry.getTimeStamp()
      # Check if the log entry date and time is not set. We can not
      # use this entry if the date and time are not set.
      if entryDateTime != None:      
        timeSecondsFloat = datetime.timedelta.total_seconds(dateTimeNow - \
                                                            entryDateTime) 
        # Check if this entry is too old
        if timeSecondsFloat < seconds:
          addToLogList = True
    if addToLogList == True:
      logList.append(entry)
  # Build the final file log file instance
  logFileName = logFile.getLogFileName()
  logFile = LogFile(logFileName, logList)
  return logFile

# This routine gets a character string log level (such as 'all') from a 
# numeric log level (such as '1'). Note that this routine will not always
# work as intended. Log levels may not be unqiue. Log key values (dict keys)
# are always unique. However, dictionary values may not be unique.
def getLogKey(logLevel):
  for key, value in glbLogLevels.items():
    if logLevel == value:
      return key
  return None

# Get the oldest timestamp value from a log file. The log file may not
# have any log entries with timestamps. In that case a Python value of
# None will be returned. It is assumed that the first log entry that 
# actually has a timestamp is the oldest. Basically, this routine amounts
# to scanning the log file entries for an entry with a valid timestamp.
# The timestamp from the first entry that has a timestamp is returned 
# to the caller.
def getLogOldestDateTime(logFile):
  # Assume that we can't get a valid oldest data and time value
  oldestDateTime = None
  # Check all of entries in the current log file
  logEntries = logFile.getLogEntries()
  for entry in logEntries:
    # Get the timestamp for the current log list entry. Not
    # all log list entries have timestamp values.
    entryDateTime = entry.getTimeStamp()
    # Check if the log entry date and time is not set. We can not
    # use this entry if the date and time are not set.
    if entryDateTime != None:  
      oldestDateTime = entryDateTime
      break
  return oldestDateTime

# Get the log type associated with a name of something that needs
# to be checked. The name is passed by the caller. This routine 
# determines the type of thing that needs to be checked. Many of
# the types are actual log types. However, some are other types 
# of checks, such as 'html'.
def getLogType(checkName):
  # Based on the name of the thing we are supposed to process
  # we can set the type of log (not really a log in the case  
  # of HTTP/HTML) the we need to process
  if checkName == 'javaproxyaaccess':
    logType = 'JavaLog4jAccess'
  elif checkName == 'javaproxyaerror':
    logType = 'JavaLog4jError'
  elif checkName == 'javaproxyahigh':
    logType = 'JettyHigh'
  elif checkName == 'javaproxyainfo':
    logType = 'info'
  elif checkName == 'javaproxyalog':
    logType = 'JavaLog4jLog'
  elif checkName == 'javaproxyastatus':
    logType = 'JettyStatus'
  elif checkName == 'owotest2':
    logType = 'html'
  elif checkName == 'owotest3':
    logType = 'html'
  elif checkName == 'owotest4':
    logType = 'html'
  elif checkName == 'owotest5':
    logType = 'html'
  elif checkName == 'owotest6':
    logType = 'html'
  elif checkName == 'checkanomalies':
    logType = 'html'
  elif checkName == 'checkexceptcmd':
    logType = 'html'
  elif checkName == 'checkexceptlog':
    logType = 'JavaLog4jLog'
  elif checkName == 'checkstatus':
    logType = 'htmlCheckStatus'
  else:
    raise ValueError('Invalid check name specified')
  return logType

# Get the next server from the server list. This 
# routine does not actually change anything. It
# does determine what server to use next.
def getNextServer():
  # Get the current server
  currentServer = getParameterValue('/Test1/CurrentServer')
  # Get and fix the list of servers
  serverList = getParameterValue('/Test1/ServerList')
  serverList = serverList.split(',')
  listCounter = 0
  for server in serverList:
    listCounter += 1 
    serverList[listCounter-1] = server.strip()
  # Search the list for the currnet server
  if currentServer not in serverList:
    return None
  # Get the index of the current server in the server list  
  currentIndex = serverList.index(currentServer)
  # Check if we have reached the end of the server list
  if (currentIndex+1) >= listCounter:
    return serverList[0]
  else:
    return serverList[currentIndex+1]

# Get the value of a stored parameter. The caller provides 
# the parameter name. This routine does the rest. 
def getParameterValue(paramName):
  ssm = boto3.client('ssm')
  response = ssm.get_parameter(Name=paramName)
  parameter = response['Parameter'] 
  paramValue = parameter['Value']  
  return paramValue

# Get the pubilc eip (such as '3.14.54.178' without the quotes)
# (if any) associated with an instance. This may not always
# be possible. Some instances may not have a public eip attached 
# to them.
def getPublicEipForInstance(instanceId):
  ec2 = boto3.client('ec2')
  response = ec2.describe_instances( \
    InstanceIds=[ instanceId ] )
  reservations = response['Reservations']
  reservation = reservations[0]
  groups = reservation['Groups']
  instances = reservation['Instances']
  instance = instances[0]
  nameValue = 'PublicIpAddress'
  if nameValue in instance:
    publicEip = instance[nameValue]
    return publicEip
  else:
    return None

# Get the resource id for a tag value. This routine 
# supports a number of resource types. The caller just
# provides the tag name and the resource type. This
# routine does the rest.
def getResourceIdFromTag(tagName, resourceType):
  ec2 = boto3.client('ec2')
  response = ec2.describe_tags(                \
    Filters=[ { 'Name': 'resource-type',       \
                'Values': [ resourceType ]  }, \
              { 'Name': 'tag:' + 'Name',       \
                'Values': [ tagName ] }
                
            ] )
  # Get all of the tag values                
  tags = response['Tags']
  # Get the first tag value
  tag = tags[0]
  # Get and return the resource id we are looking for
  rId = tag['ResourceId']
  return rId

# Obtain some size information from a URL
def getSizeInfoUrl(urlString):
  headerMap = getHeadersUrl(urlString)
  ranges = headerMap['accept-ranges'][0]
  size = headerMap['content-length'][0]
  return [size, ranges]

# Get the tag value for a given resource. This routine 
# supports a number of resource types. The caller just
# provides the resource string. This routine does the 
# rest.
def getTagfromResourceId(resourceId):
  ec2 = boto3.client('ec2')
  response = ec2.describe_tags(        \
    Filters=[ { 'Name': 'resource-id', \
                'Values': [            \
                  resourceId ]  } ] )
  # Get all of the tag values                
  tags = response['Tags']
  # Get the first tag value
  tag = tags[0]
  # Get and return the tag name we are looking for
  tagName = tag['Value']
  return tagName

# Build a Python dictionary with the count of each type of entry
def getTypeCount(logFile):
  outCounts = dict()
  # Check each entry in the log file object for an error
  logFileEntries = logFile.getLogEntries()
  for entry in logFileEntries:
    type = entry.getType()
    if type in outCounts:
      outCounts[type] = outCounts[type] + 1
    else:
      outCounts[type] = 1
  return outCounts

# Build a string with all of the count values
def getTypeString(outCounts):
  outCountsLen = len(outCounts)
  # Format each of type with a non-zero coun
  typeCountsStr = ''
  if outCountsLen > 0:
    for key in sorted(outCounts.keys()):
      if typeCountsStr != '':
        typeCountsStr += ' ' 
      typeCountsStr += key.capitalize() + ' entries ' + str(outCounts[key])
  return typeCountsStr

# This routine handles the current event and build a object
# from it. The returned event has the current check name, log 
# type, the number of seconds, the output targets (phone numbers 
# and/or Email addresses in a list) and some details. Note that
# the output targets will always be returned as a Python list, 
# even they were not specified as a JSON array.
def handleEvent(jsonString):
  newObj = EmptyObject()
  jsonObj = json.loads(jsonString)
  for key, value in jsonObj.items():
    # Convert the key and value to lower case to make matching
    # easier
    keyLower = key.lower()
    if isinstance(value, str):
      valueLower = value.lower()
    else:
      valueLower = value
    # Check if we have found the name of the thing to process
    if keyLower == 'check' or \
       keyLower == 'log' or \
       keyLower == 'logtype' or \
       keyLower == 'type': 
      newObj.check = valueLower
      continue
    # Check if we have found the number of seconds
    if keyLower == 'second' or \
       keyLower == 'seconds':
      newObj.time = valueLower
      continue
    # Check if we have found who should be notified
    if keyLower == 'notify':
      if isinstance(valueLower, list):
        newObj.notify = valueLower
      else:
        newObj.notify = [valueLower]
      continue
    # Check if we have found some details. The details are
    # used as the error level at present. They may be used
    # for other things in the future.
    if keyLower == 'detail' or \
       keyLower == 'details' or \
       keyLower == 'level':
      newObj.details = valueLower
      continue
    # Report an error if they JSON key was not matched
    raise ValueError('Invalid JSON key({}) detected'.format(key))
  return newObj

# Return a boolean showing if we are running under Windows
def isWindows():
  curPlatform = sys.platform
  return curPlatform.startswith('win')

# This is the actual entry point when this code is run using
# AWS Lambda. The event below is actually a Python dictionary.
# The code below converts the Python dictionary to a string.
def lambda_handler(event, context):
  glbLambdaHandler = True
  eventStr = json.dumps(event)
  # Use the event passed by the caller to get some information
  eventInfo = handleEvent(eventStr)
  checkName = eventInfo.check
  logType = getLogType(checkName)
  logSeconds = eventInfo.time
  logTargets = eventInfo.notify
  logLevel = eventInfo.details
  # Try to check the log specified by the event
  logObj = getLogLast(checkName, logType, logSeconds)
  outMsgs = analyzeLog(checkName, logObj, logType, logLevel)
  # Send SMS message(s) to the specified target(s) 
  awsSendTargets(outMsgs, logTargets)

# Move to the next server in the server list. 
# This routine finds the current server and 
# moves to the next server in the list. This 
# routine does all of the work needed to move
# to the next server in the server list.
def moveToNextServer(eipTagName):
  # Get the current server
  currentServer = getParameterValue('/Test1/CurrentServer')
  # Get the name of the next server
  nextServer = getNextServer()
  # Get the resource id for the next server
  nextServerId = getResourceIdFromTag(nextServer, 'instance') 
  # Get the resoruce id for the EIP
  eipId = getResourceIdFromTag(eipTagName, 'elastic-ip') 
  # Assign the eip to the next server 
  assignEipToInstance(eipId, nextServerId)
  # Update the current server parameter
  setParameterValue('/Test1/CurrentServer', nextServer)
  return

# Remove all HTML tags (if any) from a string. A string may
# contain more than one HTML tag. This routine removes them
# all, and returns the input string without the HTML tags.
def removeHtmlTags(inStr):
  # A string may have more than one HTML tag. We need to remove
  # them all. Hence the loop below.
  while True:
    # Search for the less than sign (start of an HTML tag)
    firstIndex = inStr.find('<')
    if firstIndex < 0:
      break
    # Search for a greater than sign. This may not be found. It is 
    # common for HTML tags to span several lines. 
    lastIndex = inStr.find('>', firstIndex+1)
    if lastIndex < 0:
      lastIndex = len(inStr) - 1
    # Build a new string without the current HTML tag  
    inStr = inStr[0:firstIndex] + inStr[lastIndex+1:]
  return inStr

# This routine sets a bunch of AWS access global values
def setAwsAccessGlobals():
  # Set some of the AWS access global values. The AWS 
  # access values are stored in AWS Secrets Manager.
  global glbAwsAccessKeyId
  glbAwsAccessKeyId = HDLmConfigInfo.getAwsAccessKeyId()
  global glbAwsSecretAccessKey
  glbAwsSecretAccessKey = HDLmConfigInfo.getAwsSecretAccessKey()
  return

# Set the value of a stored parameter. The caller provides 
# the parameter name and the new value. This routine does
# the rest. 
def setParameterValue(paramName, paramValue):
  ssm = boto3.client('ssm')
  response = ssm.put_parameter(Name=paramName,   \
                               Value=paramValue, \
                               Overwrite=True)
  return 

# Split an HTML response into separate lines. In some cases, the
# HTmL response is all one line with no separators between the 
# lines. This code handles that case. Basically, we split at the
# start of eaching opening tag. This routine does not do a good job
# of splitting HTML. The last line will include all of the HTML 
# closing tag. Of course, these closing tags finish HTML lines that
# started much earlier.
def splitHtmlTag(htmlString):
  currentHtmlIndex = 0
  lineStartIndex = 0
  htmlLines = []
  htmlStringLen = len(htmlString)
  # Check if the input string has a zero length. We can exit
  # immediately in that case.
  if htmlStringLen == 0:
    return htmlLines
  # Look for the next opening HTML tag. An opening tag is the
  # '<' character when it is not followed by an '/' character.
  while currentHtmlIndex < htmlStringLen:
    findIndex = htmlString.find('<', currentHtmlIndex)
    # Check if the input string starts with a '<' character. This
    # is actually rather likely. Just skip the leading character.
    if findIndex == 0:
      currentHtmlIndex = 1
    # Check if we found a closing HTML tag of some kind. We can
    # just skip HTML closing tags.
    elif findIndex > 0 and (findIndex+1) < htmlStringLen and \
         htmlString[findIndex+1] == '/':
      currentHtmlIndex = findIndex + 2
    # Check if we found an opening HTML tag. We can now add a 
    # new line to the list of output lines.
    elif findIndex > 0:
      newLine = htmlString[lineStartIndex:findIndex]
      htmlLines.append(newLine)
      lineStartIndex = findIndex
      currentHtmlIndex = findIndex + 1
    # Check if we didn't find a '<' character. The rest
    # of the string, is the current line in this case.
    elif findIndex < 0:
      newLine = htmlString[lineStartIndex:]
      htmlLines.append(newLine)
      currentHtmlIndex = htmlStringLen
  return htmlLines

# Handle startup 
def startup():
  # Switch to the current working directory we need
  # os.chdir(glbWorkPath)   
  pass

# Write out to a file
def writeDataFile(outFile, outData):
  f = open(outFile, 'w')
  f.write(outData)
  f.close()

# Write data out to a temporary file. Return the temporary
# file name to the caller for later use.
def writeTemporary(outData):
  tempFileObject = tempfile.NamedTemporaryFile(mode='w')
  tempFileName = tempFileObject.name
  tempFileObject.close()
  writeDataFile(tempFileName, outData)
  return tempFileName
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Build a secrets manager client
  secretsClient = HDLmAwsUtility.buildAwsSecretsManagerClient()
  # Start merging files 
  startup() 
  glbLambdaHandler = False
  # Set a few global values
  glbWindowsPassword = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'WindowsPasswordPds')
  glbWindowsUserid = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'WindowsUseridPds')  
  # Set a few AWS access values for use later
  setAwsAccessGlobals()
  # eventInfo = handleEvent('{"Check":"JavaProxyA", "seconds": 900, "notify": ["+12817990319"], "Level": "all"}')
  # eventInfo = handleEvent('{"Check":"error", "seconds": 20, "notify": ["+12817990319"], "Level": "all"}')
  # eventInfo = handleEvent('{"Check":"error", "seconds": 900, "notify": \
  #                           ["+12817990319"], \
  #                           "Level": "error list"}')
  # eventInfo = handleEvent('{"Check":"owotest5", "seconds": 15, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "error"}')
  # eventInfo = handleEvent('{"Check":"javaproxyalog", "seconds": 900, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "error"}')
  # eventInfo = handleEvent('{"Check":"owotest6", "seconds": 15, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "error"}')
  # eventInfo = handleEvent('{"Check":"javaproxyaaccess", "seconds": 19090, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "info"}')
  # eventInfo = handleEvent('{"Check":"javaproxyaerror", "seconds": 199000, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "info"}')
  # eventInfo = handleEvent('{"Check":"javaproxyainfo", "seconds": 19900, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "info"}')
  # eventInfo = handleEvent('{"Check":"javaproxyalog", "seconds": 190900, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "error"}')
  # eventInfo = handleEvent('{"Check":"javaproxyahigh", "seconds": 15, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "error"}')
  # eventInfo = handleEvent('{"Check":"javaproxyastatus", "seconds": 15, "notify": \
  #                         ["+12817990319"], \
  #                          "Level": "all"}')
  # eventInfo = handleEvent('{"Check":"owotest6", "seconds": 15, "notify": 
  #                         ["+12817990319"], 
  #                         "Level": "all"}')
  # eventInfo = handleEvent('{"Check":"checkanomalies", "seconds": 15, "notify": \
  #                         ["+12817990319"], "Level": \
  #                         "error list"}')
  # eventInfo = handleEvent('{"Check":"checkexceptcmd", "seconds": 15, "notify": \
  #                         ["+12817990319"], "Level": \
  #                         "error list"}')
  eventInfo = handleEvent('{"Check":"checkexceptlog", "seconds": 15, "notify": \
                          ["+12817990319"], "Level": \
                          "error list"}')
  # eventInfo = handleEvent('{"Check":"checkstatus", "seconds": 15, "notify": \
  #                         ["+12817990319"], \
  #                         "Level": "error"}')
  checkName = eventInfo.check 
  logType = getLogType(checkName)
  logSeconds = eventInfo.time
  logTarget = eventInfo.notify
  logLevel = eventInfo.details
  logObj = getLogLast(checkName, logType, logSeconds)
  outMsgs = analyzeLog(checkName, logObj, logType, logLevel)
  print(outMsgs)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()