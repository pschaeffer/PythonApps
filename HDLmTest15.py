from   HDLmUtility import * 
import os
import time

glbDebug = True
glbIgnoreList = ['Fancytree event', 'errorObj']
glbIgnoreList.append('Item created successfully')
glbIgnoreList.append('Item removed successfully')
glbIgnoreList.append('`Error')
glbIgnoreList.append('`Redo')
glbIgnoreList.append('`Undo')
glbIgnoreList.append('`Add')
glbIgnoreList.append('`No')
glbWorkPath = '../WebApplication5/WebApplication5/js'

# Process all of the files in the list passed by the caller
def processFiles(fileNames, ignoreList): 
  # Handle each file
  for fileName in fileNames:
    # Check if the current file should be skipped
    if '.js' not in fileName:
      continue
    # Check if this is a jquery file
    if 'jquery' in fileName:
      continue
    # Read the file from the file system  
    lineList = HDLmUtility.readInputFile(fileName)
    # Process the lines in the file
    processLines(lineList, ignoreList, fileName)
  return  

# Process all of the lines in a file
def processLines(lineList, ignoreList, fileName):
  lineNumber = 0
  # Handle each line
  for currentLine in lineList:
    lineNumber = lineNumber + 1 
    # Try to find 'console.log' in the current line
    clindex = currentLine.find('console.log')
    # Check if 'console.log' was not found
    if clindex < 0:
      continue
    # Check if the 'console.log' is proceeded by the start
    # of a comment
    comStr = currentLine[clindex-3:clindex]
    if comStr == '/* ':
      continue     
    # Check if the 'console.log' is really OK
    ignoreFound = False
    for ignnoreStr in ignoreList:
      if ignnoreStr in currentLine:
        ignoreFound = True
        break
    if ignoreFound == False:
      print(fileName, lineNumber, currentLine)    

# Handle startup 
def startup():  
  os.chdir(glbWorkPath)   
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Start processing
  startup() 
  # Get the list of files in the JavaScript directory
  fileNameList = HDLmUtility.getFileList('.') 
  # Process each of the files
  processFiles(fileNameList, glbIgnoreList)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()