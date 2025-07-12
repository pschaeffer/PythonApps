from   HDLmUtility  import *
import os
import time

glbDebug = True
glbWorkPath = '../../../../../HeadlampJetty/workspace-4.33.0/ProxyServerA/src/com/headlamp' 

# Fix one file
def fixFile(fileEntry):
  lines = fileEntry.getLines()
  linesLenInput = len(lines)
  outLines = []
  outErrors = 0
  lineCounter = 0
  for line in lines:
    lineCounter += 1
    assertOff = line.find('assertEquals(') 
    exectOff = line.find('execMsg')
    # Check if the current line must be modified. If not, just
    # copy the current line to the output lines list.
    if assertOff < 0 or exectOff < 0:
      outLines.append(line)
      continue
    # Convert the current line to a vector of tokens
    inStrVec = getTokensFromString(line, '"')
    # Check if the vector of tokens is None, which indicates
    # that an error was detected while trying to get the tokens.
    if inStrVec is None:
      print('Error - Unable to get tokens from string') 
      print(fileEntry.getFileName(), lineCounter, line)
      outErrors += 1
      continue
    # Try to find the left parenthesis in the vector of tokens
    leftParenOff = -1
    for i in range(len(inStrVec)):
      if inStrVec[i].value == '(':
        leftParenOff = i
        break
    # Report an error if the left parenthesis was not found
    if leftParenOff < 0:
      print('Error - Unable to find left parenthesis in token vector') 
      print(fileEntry.getFileName(), lineCounter, line)
      outErrors += 1
      continue
    # Check if the left parenthesis is followed by 'execMsg'
    if inStrVec[leftParenOff + 1].value != 'execMsg':
      outLines.append(line)
      continue
    # Check if 'execMsg' is followed by a comma and a blank
    if inStrVec[leftParenOff + 1].value != 'execMsg':
      print('Error - Expected execMsg after left parenthesis') 
      print(fileEntry.getFileName(), lineCounter, line)
      outErrors += 1
      continue
    if inStrVec[leftParenOff + 2].value != ',':
      print('Error - Expected comma after execMsg')
      print(fileEntry.getFileName(), lineCounter, line)
      outErrors += 1
      continue
    if inStrVec[leftParenOff + 3].value != ' ':
      print('Error - Expected blank after comma') 
      print(fileEntry.getFileName(), lineCounter, line)
      outErrors += 1
      continue
    # Try to find the second comma in the vector of tokens
    commaOff = -1
    commaCounter = 0
    for i in range(len(inStrVec)):
      if inStrVec[i].value == ',':
        commaCounter += 1
      if commaCounter == 2:
        commaOff = i
        break
    # Report an error if the comma was not found
    if commaOff < 0:
      # print('Error: - Unable to find second comma in token vector')
      print(fileEntry.getFileName(), lineCounter, line)
      outErrors += 1
      continue
    # Save a few tokens for use later 
    tokenExecMsg = inStrVec[leftParenOff + 1]
    tokenComma = inStrVec[leftParenOff + 2]
    tokenBlank = inStrVec[leftParenOff + 3] 
    # Insert the tokens into the output line
    inStrVec.insert(commaOff + 2, tokenExecMsg) 
    inStrVec.insert(commaOff + 2, tokenBlank) 
    inStrVec.insert(commaOff + 4, tokenComma)
    # Remove the leading tokens
    del inStrVec[leftParenOff + 1]
    del inStrVec[leftParenOff + 1]
    del inStrVec[leftParenOff + 1]
    # Convert the vector of tokens back to a string
    line = HDLmString.convertTokens(inStrVec)
    # print(fileEntry.getFileName(), lineCounter, 'Line - ', line)
    outLines.append(line)
    continue
  linesLenOutput = len(outLines)
  # Check if any errors were detected
  if outErrors == 0:
    # Make sure that the number of output lines is the same
    # as the number of input lines. If not, then report an error.
    if linesLenInput != linesLenOutput:
      print('Input lines:', linesLenInput)
      print('Output lines:', linesLenOutput)
    else:
      fileEntry.replaceLines(outLines)
  else: 
    print(fileEntry.getFileName(), 'Errors - ', outErrors)    

# Fix all of the files in the list passed by the caller.
def fixFiles(fileList):
  # Handle each output file
  for fileEntry in fileList:
    fixFile(fileEntry)
  return

# This routine gets a set of tokens from a string. The caller 
# provides the string and the quote character (more than one
# quote character can be passed). A vector is returned to the
# caller unless an exception is detected. If an exception is 
# detected, then None is return to the caller.
def getTokensFromString(inStr, quoteChar):
  errorDetected = False 
  try:
    inStrVec = HDLmString.getTokens(inStr, quoteChars = quoteChar)
  except:
    errorDetected = True
  if errorDetected:
    return None
  return inStrVec

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
  fileList = HDLmUtility.readFiles(fileNameList)
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