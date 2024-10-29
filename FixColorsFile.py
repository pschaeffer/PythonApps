from   HDLmUtility  import *
import os
import sys
import time

glbInColors    = 'inColors.txt'
glbOutColors   = 'outColors.txt'
glbWorkPath    = '/windows/temp/'   

# Build an output line from the color line passed by the caller
def buildLines(color):
  outLines = []
  # Build the first and only line
  line = ''
  data = color.split()
  name = data[0]
  hex = data[1]
  category = data[2]
  line += '  '
  outData = '"' + name.lower() + '"' + ': '
  outData = outData.ljust(24)
  line += outData
  line += '{ '
  outData = '"' + data[0] + '",'
  outData = outData.ljust(24)
  line += '"name": ' + outData
  line += '"hex": "' + data[1] + '", '
  line += '"category": "' + data[2] + '"'
  line += ' }'
  outLines.append(line)
  return outLines

# Build a set of output lines from the colors passed by the caller.
# One line is built for each color. The actual line construction
# is handled by another routine.
def buildLinesAll(colors):
  outLines = []
  colorLen = len(colors)
  i = 0
  for color in colors:
    i += 1
    lines = buildLines(color)
    if i < colorLen:
      lines[0] += ','
    outLines.extend(lines)
  return outLines

# Extract a set of lines from a file. The caller passes the starting 
# line and the ending line. All of the lines between the starting line
# and the ending line are returned to the caller.
def extractLines(lines, start, end):
  outList = []
  startFound = False
  for line in lines:
    lineLStrip = line.lstrip()
    # Look for the ending line. Terminate the loop if we find the ending
    # line.
    if startFound and lineLStrip.startswith(end):
      break
    # Look for the starting line, if need be
    if not startFound:
      if lineLStrip.startswith(start):
        startFound = True
    else:
      outList.append(line)
  return outList

# Load the input colors from a file
def getInputColors(fileName):
  inColors = []
  lines = readFile(fileName)
  for line in lines: 
    inColors.append(line)
  return inColors

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
  inColorsFileName = glbInColors
  # Read the input colors file
  inColorsList = getInputColors(inColorsFileName)
  outLines = buildLinesAll(inColorsList)
  outColorsFileName = glbOutColors
  HDLmUtility.writeOutputFile(outLines, outColorsFileName)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()