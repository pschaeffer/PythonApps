from   HDLmAssert     import *
from   HDLmConfig     import *
from   HDLmConfigInfo import *
from   io             import BytesIO
from   io             import StringIO
import json
import pycurl
import pymysql.cursors 
import time

glbCertifi = 'C:\\Users\\pscha\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\certifi\\cacert.pem'
glbRemoteDatabase  = ''
glbRemoteHost      = ''
glbRemotePassword  = ''
glbRemoteTableName = 'main_9'
glbRemoteUser      = ''

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
def getSomeData(mySqlConnection):
  bytesBuffer = BytesIO()
  stringBuffer = StringIO()
  protocol = 'https'
  hostName = 'headlamp.dreamtsoft.com'
  # This path value gets all of the rows
  pathValue = 'io/bucket/search/main_3?q=[[[\'content\',\'ne\',\'pass_javxx\',\'pass_javxx\']]]'
  urlString = protocol + '://' + hostName + '/' + pathValue 
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(c.WRITEDATA, bytesBuffer)
  c.setopt(c.USERPWD, 'admin:headlamp')
  c.perform()
  c.close()   
  bytesBody = bytesBuffer.getvalue()
  stringJson = bytesBody.decode('UTF-8')
  mainDict = json.loads(stringJson)
  # Get a MySQL cursor for use below
  mySqlCursor = mySqlConnection.cursor() 
  # Get the number of rows and process each row
  rowCount = mainDict['rows_returned']
  rowData = mainDict['data']
  # Handle all of the rows
  for i in range(rowCount):
    currentRow = rowData[i]
    # Get and check the current content value
    currentContent = currentRow['content']
    currentContentLen = len(currentContent) 
    if currentContentLen == 0:
      errorText = f'Content length is zero for row({i})'
      HDLmAssert(False, errorText)
    # Get and check the current info value
    currentInfo = currentRow['info']
    currentInfoLen = len(currentInfo)
    if currentInfoLen == 0:
      errorText = f'Info length is zero for row({i})'
      HDLmAssert(False, errorText)
    # Get and check the current name value
    currentName = currentRow['name']
    currentNameLen = len(currentName)
    if currentNameLen == 0:
      errorText = f'Name length is zero for row({i})'
      HDLmAssert(False, errorText)
    # Get and check the current company value
    currentCompany = None
    currentCompanyLen = None
    currentInfoStr = currentRow['info']
    currentInfoDict = json.loads(currentInfoStr)
    currentNodePath = currentInfoDict['nodePath']
    currentNodePathLen = len(currentNodePath)
    # We need separate code for proxy entries versus rule entries
    if currentContent == 'proxy_javaa':
      if currentNodePathLen >= 2 and \
         currentNodePath[0] == 'Top':
        currentCompany = currentNodePath[1]
        currentCompanyLen = len(currentCompany)
    if currentContent == 'pass_javaa':
      if currentNodePathLen >= 3 and \
         currentNodePath[0] == 'Top' and \
         currentNodePath[1] == 'Companies':
        currentCompany = currentNodePath[2]
        currentCompanyLen = len(currentCompany)
    if currentCompanyLen == 0:
      errorText = f'Company length is zero for row({i})'
      HDLmAssert(False, errorText)
    # Insert the data into the MySQL table
    mySqlInsertIntoTable(mySqlCursor, currentName, currentContent, currentInfo, currentCompany)
  return

# MySQL create table code
def mySqlCreateTable(connection):
  # Build the drop table string
  tableStr = "DROP TABLE `" + glbRemoteTableName + "`"
  # drop the table
  cur = connection.cursor()
  try:
    cur.execute(tableStr)
  except BaseException as e:
    print(e)
  # Build the create table string. Note that TEXT is 
  # used below rather than JSON, because TEXT is more
  # editable using the MySQL workbench.
  tableStr = "CREATE TABLE `" + glbRemoteTableName + "` ("
  tableStr += "`id` BIGINT NOT NULL AUTO_INCREMENT,"
  tableStr += "`name` NVARCHAR(255) NOT NULL,"
  tableStr += "`content` NVARCHAR(255) NOT NULL,"
  tableStr += "`info` JSON NOT NULL,"
  tableStr += "`company` NVARCHAR(255),"
  tableStr += "`report` NVARCHAR(255),"
  tableStr += " PRIMARY KEY (`id`)"
  tableStr += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin"
  # Create the table
  cur = connection.cursor()
  cur.execute(tableStr)
  return  

# MySQL commit              
def mySqlCommit(connection):
  # Get a cursor for use later
  currentCursor = connection.cursor()
  # Build the commit string      
  tableStr = "COMMIT"
  # Execute the commit    
  currentCursor.execute(tableStr) 
  return 

# MySQL get connection code
def mySqlGetConnection():
  # Connect to the database
  connection = pymysql.connect(host=glbRemoteHost,
                               user=glbRemoteUser,
                               password=glbRemotePassword,
                               database=glbRemoteDatabase,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.Cursor)  
  return connection

# MySQL insert into table code
def mySqlInsertIntoTable(cursor, name, content, info, company):
  # Build the insert into table string      
  tableStr = "INSERT INTO `" + glbRemoteTableName + "` (`name`, `content`, `info`, `company`) VALUES (%s, %s, %s, %s)"
  # Execute the insert into table statement   
  cursor.execute(tableStr, (name, content, info, company)) 
  return 

# MySQL version code for now
def mySqlVersionCode():
  # Connect to the database
  connection = pymysql.connect(host=glbRemoteHost,
                               user=glbRemoteUser,
                               password=glbRemotePassword,
                               database=glbRemoteDatabase,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.Cursor)  
  # Use the connection to get the version
  with connection:
    cur = connection.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))
    
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

# This routine sets a bunch of database global values
def setDatabaseGlobals():
  # Set some of the global values
  global glbRemoteDatabase
  glbRemoteDatabase = HDLmConfigInfo.getEntriesDatabaseDatabaseNameProd()
  global glbRemoteHost
  glbRemoteHost = HDLmConfigInfo.getEntriesDatabaseDomainNameProd()
  global glbRemotePassword
  glbRemotePassword = HDLmConfigInfo.getEntriesDatabasePassword()
  global glbRemoteUser
  glbRemoteUser = HDLmConfigInfo.getEntriesDatabaseUserid()
  return
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Set a few database globals
  setDatabaseGlobals()
  # mySqlVersionCode()
  connection = mySqlGetConnection()
  mySqlCreateTable(connection)
  getSomeData(connection)  
  mySqlCommit(connection)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()