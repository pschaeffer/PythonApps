from   ctypes       import c_int16
from   HDLmString   import *
from   HDLmUtility  import *
import os
import time 

glbDebug = True 
glbWorkPath = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\projects\\PythonApps\\PythonApps'

# Check for a circular import error. The program calls itself recursively using all of 
# imports of the current file. This step is required to find recursive file import errors.
def checkForImportError(workCounter, fileNameFixedList, baseFileNameFixed, curFileName, fileImportDict):
  fileNameFixedList.append(curFileName)
  # Check for too much work. This will really happen if we have
  # circular imports. Worse, The code below won't detect the circular
  # import until later. Hence, the need for this code.
  if workCounter.value > 200:
    return
  # Remove the '.py' (without the quotes) from the file name
  curFileNameFixed = HDLmString.removeSuffix(curFileName, '.py')
  importList = fileImportDict[curFileNameFixed]
  # print(curFileNameFixed)
  # print(len(importList))
  # print(importList)
  # print()
  # print(baseFileNameFixed)
  # print(fileNameFixedList)
  # print(workCounter)
  # print(importList)
  # Check if we have a circular import error and report the error
  # using print
  if baseFileNameFixed in importList:
    print('We have an error')
    print(fileNameFixedList)
    return
  # Recursively check all of the current imports
  workCounter.value += 1
  for importEntry in importList:
    # Create a new list with all of the current entries in the list. 
    # The new list will be changed by the call below. Not the original
    # list.
    newFileNameFixedList = list(fileNameFixedList)
    checkForImportError(workCounter, newFileNameFixedList, baseFileNameFixed, importEntry, fileImportDict)
  return

# Check for possible import errors (circular imports)
def checkForImportErrors(fileImportDict):
  for inFileFixed in fileImportDict:
    # Get the list of imports for the current file
    inValue = fileImportDict[inFileFixed]
    inValueLen = len(inValue)
    if inValueLen == 0:
      continue
    # print(inFileFixed)
    # Note that the call below creates a mutable integer. 
    workCounter = c_int16(0)
    fileNameFixedList = []
    # fileNameFixedList.append(inFileFixed)
    checkForImportError(workCounter, fileNameFixedList, inFileFixed, inFileFixed, fileImportDict)
  return  

# Get the list of imports and return it to the caller
def getImportList(fileName, fileLines, fileList):
  # Create the import list 
  importList = []
  # Check each line
  lineCounter = 0
  for line in fileLines:
    lineCounter += 1
    lineTokens = []
    try:
      lineTokens = line.split()
      lineTokensLen = len(lineTokens)
      if lineTokensLen == 1 and fileName == 'HDLmBuildRules.py' and \
         line.strip() != 'continue' and line.strip() != 'else:' and \
         line.strip() != 'return'   and line.strip() != 'break' and \
         line.strip() != '#'        and line.strip() != '@staticmethod':
        # print(fileName) 
        # print(str(lineCounter) + ' ' + line)
        pass
      # Check for a from statement
      if lineTokensLen >= 4 and \
         lineTokens[0] == 'from':
        importName = lineTokens[1]  
        importNamePy = importName + '.py'
        if importNamePy in fileList:
          importList.append(importName) 
      # Check for an import statement
      if lineTokensLen >= 2 and \
         lineTokens[0] == 'import':
        importName = lineTokens[1]  
        importNamePy = importName + '.py'
        if importNamePy in fileList:
          importList.append(importName) 
    except Exception as e:
      print(str(e))
      # print(fileName) 
  return importList

# For each file, get the list of imports
def readFilesImport(fileList):
  # Create the initial file import dictionary
  fileImportDict = dict()
  # Process each file
  for inFile in fileList:
    if not inFile.endswith('.py'):
      continue
    fileLines = HDLmUtility.readInputFile(inFile, 'Latin-1')
    importList = getImportList(inFile, fileLines, fileList)
    # Add to the output dictionary
    inFileFixed = HDLmString.removeSuffix(inFile, '.py')
    fileImportDict[inFileFixed] = importList
  return fileImportDict

# Handle startup 
def startup():
  os.chdir(glbWorkPath)   
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Start the program
  startup() 
  # Get a list of files in the current directory
  fileNameFixedList = HDLmUtility.getFileList('.')
  fileNameFixedListLen = len(fileNameFixedList)
  fileNameFixedList = sorted(fileNameFixedList, key=lambda s: s.casefold())
  # Get the imports for each file 
  fileImportDict = readFilesImport(fileNameFixedList)
  # Check for possible circular import errors
  checkForImportErrors(fileImportDict)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()
