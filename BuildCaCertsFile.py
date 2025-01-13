from   HDLmString  import *
from   HDLmUtility import *
import base64
import dumpASN3
import os
import time

glbDebug = True
glbFirefoxPath = '../../../../../HeadlampJetty/FirefoxCerts'
glbBase64Length = 76
glbOutFile = 'combinedcacerts.pem'
glbWorkPath = glbFirefoxPath

# Each instance of this class has all of the information about
# one file
class FileObj(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, name, lines):
    self.bytes = bytearray()
    self.name = name
    self.lines = []
    self.lines.extend(lines)
  # Get the file bytes 
  def getBytes(self):
    return self.bytes
  # Get the file name
  def getFileName(self):
    return self.name
  # Get the file lines
  def getLines(self):
    return self.lines
  # Set the file bytes
  def setBytes(self, bytes):
    self.bytes = bytes

# Combine all of the files into one large file
def combineFiles(files):
  outLines = []
  for file in files:
    fileName = file.getFileName()
    fileName = HDLmString.removeSuffix(fileName, '.crt')
    lineList = file.getLines()
    outBytes = file.getBytes()
    # Get the certificate name from the bytes
    certificateName = dumpASN3.extractName(outBytes) 
    # Get the first and last lines
    firstLine = lineList[0]
    lastLine = lineList[-1]
    # Add a blank line
    outLines.append('')
    # Add the rest of the header
    outLines.append(certificateName)
    outLines.append('=' * len(certificateName))
    outLines.append(firstLine)
    # Get the Base 64 encoded lines
    bs64Lines = getBase64Lines(outBytes, glbBase64Length)
    # Add all of the lines
    for line in bs64Lines:
      outLines.append(line)
    # Add the last line
    outLines.append(lastLine)
  return outLines

# Get a list of base 64 encoded lines from a set of bytes 
def getBase64Lines(outBytes, lineLength):
  outLines = []
  # Get a binary array with Base 64 bytes in it
  bs64 = base64.b64encode(outBytes)
  # Get a regular string
  bs64 = bs64.decode('utf-8')
  bs64Len = len(bs64)
  for i in range(0, bs64Len, lineLength):
    endLine = min(bs64Len, i+lineLength)
    line = bs64[i:endLine]
    outLines.append(line)
  return outLines

# Read all of the files in the list passed by the caller.
# Create an object for each file.
def readFiles(fileNames, skipList):
  outFiles = []
  # Handle each file
  for fileName in fileNames:
    # Check if the current file should be skipped
    if fileName in skipList:
      continue
    # Read the file from the file system
    lineList = HDLmUtility.readInputFile(fileName)
    fileInstance = FileObj(fileName, lineList)
    # Build the binary bytes from the base 64 data
    bs64 = ''
    for line in lineList:
      line = line.strip()
      if line.startswith('----'):
        continue
      bs64 += line
    outBytes = base64.b64decode(bs64)
    fileInstance.setBytes(outBytes)
    # Add the file object to the list of file objects
    outFiles.append(fileInstance)
  return outFiles

# Handle startup 
def startup():
  os.chdir(glbWorkPath)   
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Start merging files 
  startup() 
  # Build the new CA Certs file
  fileNameList = HDLmUtility.getFileList('.')
  fileNameListLen = len(fileNameList)
  fileNamelist = sorted(fileNameList, key=lambda s: s.casefold())
  # Read all of the files
  skipList = [glbOutFile]
  fileList = readFiles(fileNameList, skipList)
  # Combine the files
  outLines = combineFiles(fileList)
  HDLmUtility.writeOutputFile(outLines, glbOutFile)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()