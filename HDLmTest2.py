from   io import BytesIO
from   io import StringIO
import json
import pycurl
import time

glbCertifi = 'C:\\Users\\pscha\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\certifi\\cacert.pem'

# This routine breaks a string into an list of substrings.
# The list is returned to the caller. The caller passes 
# the original string and the desired length of each substring.
# The last substring may be a short string (if need be). If the
# string passed by the caller is empty (zero-length), the list
#	will have zero elements. 
def createArrayListOfStrings(inStr, desiredLength):
  # Check the values passed by the caller 
  if inStr == None:
    errorText = 'Input string passed to createArrayListOfStrings is None'
    raise ValueError(errorText)
  if str(type(inStr)) != "<class 'str'>":
    errorText = 'Input string passed to createArrayListOfStrings is not a string'
    raise ValueError(errorText)
  if desiredLength == None:
    errorText = 'Desired length passed to createArrayListOfStrings is None'
    raise ValueError(errorText)
  if str(type(desiredLength)) != "<class 'int'>":
    errorText = 'Desired length passed to createArrayListOfStrings is not an integer'
    raise ValueError(errorText)
  # Check the desired length passed by the caller 
  if desiredLength <= 0:
    errorText = 'Desired length passed to createArrayListOfStrings is less than or equal to zero'
    raise ValueError(errorText)
  # Get the length of the string passed by the caller 
  inStrLen = len(inStr)
  # Allocate the ArrayList that is returned to the caller 
  localArray = [] 
  if localArray == None:
    errorText = 'List not allocated in createArrayListOfStrings'
    raise RuntimeError(errorText)	     
  # Build the ArrayList that is returned to the caller from each
  # substring 
  strOffset = 0
  while strOffset < inStrLen:
    remainingLen = inStrLen - strOffset
    if remainingLen > desiredLength:
      remainingLen = desiredLength
    tempStr = inStr[strOffset:strOffset + remainingLen]
    localArray.append(tempStr)	
    strOffset += desiredLength		
  return localArray

# Get some data
def getSomeData():
  bytesBuffer = BytesIO()
  stringBuffer = StringIO()
  protocol = 'https'
  hostName = 'headlamp.dreamtsoft.com'
  pathValue = 'io/bucket/search/main_3?q=[[[\'content\',\'eq\',\'pass_javaa\',\'pass_javaa\']]]'
  urlString = protocol + '://' + hostName + '/' + pathValue 
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(c.WRITEDATA, bytesBuffer)
  c.setopt(c.USERPWD, 'admin:headlamp')
  c.perform()
  c.close()   
  bytesBody = bytesBuffer.getvalue()
  stringBody = bytesBody.decode('UTF-8')
  printStringInParts('getSomeData', stringBody)
  print('Number of occurrence of a substring:', stringBody.count('headlamp'))
  return
    
# This routine takes a string (possibly very long) and breaks 
# into parts (substrings). Each part is printed. 	
def printStringInParts(whereStr, inStr):
  # Check the values passed by the caller   
  if whereStr == None:
    errorText = 'Where string passed to printStringInParts is None'
    raise ValueError(errorText)
  if str(type(whereStr)) != "<class 'str'>":
    errorText = 'Where string passed to createArrayListOfStrings is not a string'
    raise ValueError(errorText)
  if inStr == None:
    errorText = 'Input string passed to printStringInPart is None'
    raise ValueError(errorText)
  if str(type(inStr)) != "<class 'str'>":
    errorText = 'Input string passed to createArrayListOfStrings is not a string'
    raise ValueError(errorText)
  # Set a few values for use later. These values make sure we always
  # use the correct part length.
  partSize = 80
  partOffset = 0		
	# Break the passed string into a list of substrings and 
	# print each one
  strList = createArrayListOfStrings(inStr, partSize) 
	# Pass each part of the string passed by the caller to the string function 
  for strEntry in strList:
    print(whereStr + ' ' + str(partOffset) + ' ' + strEntry) 
    partOffset += partSize
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Start
  getSomeData()  
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()