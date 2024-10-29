from   HDLmUtility import *
import sys
import os
import time

glbInFile    = 'test6.txt'
glbOutFile   = 'outest6.txt'
glbWorkPath    = 'C:\\Users\\pscha\\Desktop'

# Build a set of output lines from the line(s) passed by the caller.
# One line is built for each part of the input line. The actual line
# construction is handled by another routine.
def buildLinesAll(inLines):
  # Get the first line 
  inLine = inLines[0]
  # Fix the line in several ways
  inLine = inLine.replace('\\\\\\\\\\\\"', 'ZYX6BSDQ') 
  inLine = inLine.replace('\\\\\\\\"',     'ZYX4BSDQ') 
  inLine = inLine.replace('\\\\"',         'ZYX2BSDQ') 
  inLine = inLine.replace('\\\\n',         'ZYX2BSN')
  inLine = inLine.replace('\\\\t',         'ZYX2BST')
  inLine = inLine.replace('ZYX2BSN',         '\\n')
  # Split the line
  inSplit = inLine.split('\\n')
  outLines = []
  splitLen = len(inSplit)
  i = 0
  for part in inSplit:
    # Escape all double quotes
    part = part.replace('"', '\\"')
    part = part.replace('ZYX6BSDQ', '\\\\\\\\\\\\\\"',)
    part = part.replace('ZYX4BSDQ', '\\\\\\\\\\"',)
    part = part.replace('ZYX2BSDQ', '\\\\\\"',)
    part = part.replace('ZYX2BST', '  ',)
    part = '"' + part + '"' 
    i += 1 
    if i < splitLen:
      part += ' +'
    else:
      part += ';'
    outLines.append(part)
  return outLines

# Load the input lines from a file
def getInputLines(fileName):
  inLines = []
  lines = readFile(fileName)
  for line in lines: 
    inLines.append(line)
  return inLines

# Read a file and return a list of lines
def readFile(fileName):
  rv =[]
  count = 0
  try:
    with open(fileName, encoding="UTF-8") as file:
      for line in file:
        count += 1
        line = line.rstrip()
        rv.append(line)
  except IOError as e:
    print('File did not open - ' + fileName + '\n  ' + str(e))
  return rv

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
  inFileName = glbInFile
  # Read the input file
  inList = getInputLines(inFileName)
  outLines = buildLinesAll(inList)
  outFileName = glbOutFile
  HDLmUtility.writeOutputFile(outLines, outFileName)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()