from   HDLmUtility  import *
import os
import time

glbDebug = True
glbWorkPath = '../../../../../HeadlampJetty/workspace/ProxyServer/src/com/headlamp'

# Each instane of this class has all of the information about
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
  # Replace the file lines
  def replaceLines(self, newLines):
    self.lines = newLines
  # Set the file bytes
  def setBytes(self, bytes):
    self.bytes = bytes

# Fix one file
def fixFile(fileEntry):
  lines = fileEntry.getLines()
  linesLen = len(lines)
  outLines = []
  for line in lines:
    assertOff = line.find('HDLmAssert(false, ')
    endOff = line.find(' is null");')
    # Check if the current line must be modified. If not, just
    # copy the current line to the output lines list.
    if assertOff < 0 or endOff < 0:
      outLines.append(line)
      continue
    # Change the current line, if need be
    line = line.replace('HDLmAssert(false, ', 'String  errorText = ')
    line = line.replace(' is null");', ' is null";')
    outLines.append(line)
    # Build a new output line and add it to the output lines
    newLine = ''
    newLine += line[0:assertOff]
    newLine += 'throw new NullPointerException(errorText);'
    outLines.append(newLine)
    outLinesLen = len(outLines)
  fileEntry.replaceLines(outLines)

# Fix all of the files in the list passed by the caller.
def fixFiles(fileList):
  # Handle each output file
  for fileEntry in fileList:
    fixFile(fileEntry)
  return

# Read all of the files in the list passed by the caller.
# Create an object for each file.
def readFiles(fileNames):
  outFiles = []
  # Handle each file
  for fileName in fileNames:
    # Read the file from the file system
    lineList = HDLmUtility.readInputFile(fileName, 'iso-8859-1')
    fileInstance = FileObj(fileName, lineList)
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
  fileList = readFiles(fileNameList)
  # Fix all of the files
  fixFiles(fileList)
  # Write out all of the files
  HDLmUtility.writeOutputFiles(fileList)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()