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
glbOldRemoteDatabase  = ''
glbOldRemoteHost      = ''
glbOldRemotePassword  = ''
glbOldRemoteTableName = 'main_9'
glbOldRemoteUser      = ''
glbNewRemoteDatabase  = ''
glbNewRemoteHost      = ''
glbNewRemotePassword  = ''
glbNewRemoteTableName = 'test_1'
glbNewRemoteUser      = ''

# Get some data from a table. This routine returns a 
# tuple. Each element of the tuple is a row from the table.
def getSomeData(connection, tableName):
  sqlStr = "SELECT * FROM" + " " + tableName + " " + "ORDER BY id"
  # Create a cursor and execute the select statement
  cur = connection.cursor()
  # Run a query with the cursor we just created
  with cur:
    cur.execute(sqlStr)
    result = cur.fetchall()
  return result

# Add a result set to a table
def insertSomeData(connection, tableName, results):
  resultsLen = len(results)
  # Get a cursor for use later
  currentCursor = connection.cursor()
  # Run a query with the cursor we just created
  with currentCursor:
    # Loop through the results
    for i in range(resultsLen):
      # Get the row
      row = results[i]
      # Get the name, content, info, and company from the row
      name = row[1]
      content = row[2]
      info = row[3]
      company = row[4]
      # Insert the row into the new table
      mySqlInsertIntoTable(currentCursor, tableName, name, content, info, company)
  return

# MySQL create table code
def mySqlCreateTable(connection, tableName):
  # Build the drop table string
  tableStr = "DROP TABLE `" + tableName + "`"
  # drop the table
  cur = connection.cursor()
  try:
    cur.execute(tableStr)
  except BaseException as e:
    print(e)
  # Build the create table string. Note that TEXT is 
  # used below rather than JSON, because TEXT is more
  # editable using the MySQL workbench.
  tableStr = "CREATE TABLE `" + tableName + "` ("
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
  sqlStr = "COMMIT"
  # Execute the commit    
  currentCursor.execute(sqlStr) 
  return 

# MySQL get connection code
def mySqlGetConnection(remoteHost, remoteUser, remotePassword, remoteDatabase):
  # Connect to the database
  connection = pymysql.connect(host=remoteHost,
                               user=remoteUser,
                               password=remotePassword,
                               database=remoteDatabase,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.Cursor)  
  return connection

# MySQL insert into table code
def mySqlInsertIntoTable(cursor, tableName, name, content, info, company):
  # Build the insert into table string      
  tableStr = "INSERT INTO `" + tableName + "` (`name`, `content`, `info`, `company`) VALUES (%s, %s, %s, %s)"
  # Execute the insert into table statement   
  cursor.execute(tableStr, (name, content, info, company)) 
  return 

# MySQL version code for now
def mySqlVersionCode(remoteHost, remoteUser, remotePassword, remoteDatabase):
  # Connect to the database
  connection = pymysql.connect(host=remoteHost,
                               user=remoteUser,
                               password=remotePassword,
                               database=remoteDatabase,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.Cursor)  
  # Use the connection to get the version
  with connection:
    cur = connection.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))
  return

# This routine sets a bunch of new database global values
def setNewDatabaseGlobals():
  # Set some of the global values
  global glbNewRemoteDatabase
  glbNewRemoteDatabase = HDLmConfigInfo.getEntriesDatabaseDatabaseNameTest()
  global glbNewRemoteHost
  glbNewRemoteHost = HDLmConfigInfo.getEntriesDatabaseDomainNameTest() 
  global glbNewRemotePassword
  glbNewRemotePassword = HDLmConfigInfo.getEntriesDatabasePassword()
  global glbNewRemoteUser
  glbNewRemoteUser = HDLmConfigInfo.getEntriesDatabaseUserid()
  return

# This routine sets a bunch of old database global values
def setOldDatabaseGlobals():
  # Set some of the global values
  global glbOldRemoteDatabase
  glbOldRemoteDatabase = HDLmConfigInfo.getEntriesDatabaseDatabaseNameProd()
  global glbOldRemoteHost
  glbOldRemoteHost = HDLmConfigInfo.getEntriesDatabaseDomainNameProd() 
  global glbOldRemotePassword
  glbOldRemotePassword = HDLmConfigInfo.getEntriesDatabasePassword()
  global glbOldRemoteUser
  glbOldRemoteUser = HDLmConfigInfo.getEntriesDatabaseUserid()
  return
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Set the new and database globals
  setNewDatabaseGlobals()
  setOldDatabaseGlobals()
  mySqlVersionCode(glbOldRemoteHost, glbOldRemoteUser, glbOldRemotePassword, glbOldRemoteDatabase)
  mySqlVersionCode(glbNewRemoteHost, glbNewRemoteUser, glbNewRemotePassword, glbNewRemoteDatabase)
  # Get a connection to the old database and the new database
  oldConnection = mySqlGetConnection(glbOldRemoteHost, glbOldRemoteUser, glbOldRemotePassword, glbOldRemoteDatabase)
  newConnection = mySqlGetConnection(glbNewRemoteHost, glbNewRemoteUser, glbNewRemotePassword, glbNewRemoteDatabase)
  mySqlCreateTable(newConnection, glbNewRemoteTableName)
  oldResults = getSomeData(oldConnection, glbOldRemoteTableName)  
  insertSomeData(newConnection, glbNewRemoteTableName, oldResults)
  mySqlCommit(newConnection)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()