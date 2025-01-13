from   HDLmUtility import *
import reprlib
import time

# This program appears to have been written to read lists of files.
# The lists of files are compared to each other..

# All of the input files are in the directory below
glbInDirName = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\PHPApps\\PHPWebProject1\\PHPWebProject1'
# The input Linux and Windows files are specified below
glbInLinuxFile = 'Linuxm3Find'
glbInWindowsFileA = 'WindowsDirMyapptest3-2024-01-01' 
glbInWindowsFileB = 'WindowsDirMyapptest1-2024-01-02'
glbInWindowsFileC = 'WindowsDirMyapptest2-2024-01-02'
glbInWindowsFileD = 'WindowsDirMyapptest3-2024-01-02'

# Compare two maps. This routine checks that every entry in the 
# first map is also in the second map. If not, then the entry is
# displayed.
def compareMaps(map1, map2):
  # Set a few values
  notFoundCount = 0
  notFoundList = []
  # Loop through the first map
  for key1 in map1:
    # Check if the key is in the second map
    if key1 not in map2:
      # The key is not in the second map. Display the value.
      value1 = map1[key1]
      notFoundList.append(value1)
      notFoundCount += 1
  # Return the number of keys not found and the list of value not found
  return [notFoundCount, notFoundList]
    
# Compare two maps. This routine checks that every entry in each
# map is also in the other map. If not, then the entry is displayed.
def compareTwoMaps(map1, map2):
  # Compare the first map to the second map
  [notFoundCount1, notFoundList1] = compareMaps(map1, map2)
  if notFoundCount1 > 0:
    print('The following files were not found in the second map')
    print(notFoundList1)
  # Compare the second map to the first map  
  [notFoundCount2, notFoundList2] = compareMaps(map2, map1)
  if notFoundCount2 > 0:
    print('The following files were not found in the first map')
    print(notFoundList2)
  return

# Normalize a name (this might be a directory name or it 
# might be a file name). The name is normalized by changing
# all m* values to mx. 
def normalizeName(name):  
  # Make a few changes to the name
  if len(name) == 2:
    name = name[0:1] + 'x'
  # Use a regular expression to make a few changes to the name
  else:
    name = re.sub('[m-m]\d/', 'mx/', name) 
  return name

# Process a set of lines. How the lines are processed depends on
# the file name. The file name is used to determine the type of
# file. 
def processLines(inputFileName, linelist, fileMap): 
  # Check if the input file name has 'Linux' in it
  if inputFileName.find('Linux') >= 0:
    # Process the Linux files
    processLinuxFiles(linelist, fileMap)
  else:
    # Process the Windows files
    [dirCount, fileCount] = processWindowsFiles(linelist, fileMap)

# Process the Linux files. Each line is a file or a directory.
# Because we reallly can't tell which is which, we will assume 
# that all lines are files, and not directories.
def processLinuxFiles(linelist, fileMap):
  # Loop through the lines in the list
  for line in linelist:
    # Get the original file name
    orginalFileName = line
    normalizedFileName = normalizeName(orginalFileName)
    # Add the file name to the map
    fileMap[normalizedFileName] = orginalFileName 

# Process the Windows files. Each line must be checked. 
# Many types of lines will be found. 
def processWindowsFiles(linelist, fileMap):
  # Set a few values
  dirCount = 0
  fileCount = 0
  # Loop through the lines in the list
  for line in linelist:
    # Split the line using blanks as the delimiter
    lineSplit = line.split()
    # Skip blank lines
    if len(lineSplit) ==  0:
      continue 
    # Skip some other lines
    firstWord = lineSplit[0]
    if firstWord == 'Volume':
      continue  
    if firstWord == 'Total':
      continue
    secondWord = lineSplit[1]
    if secondWord == 'Dir(s)':
      continue
    if secondWord == 'File(s)':
      continue
    # Check for a directory line. We have lots of work to do
    # if this is a directory line.
    if firstWord == 'Directory':
      curOffset = line.find('5\\m')
      curDirectory = line[curOffset+2:]
      curDirectory = curDirectory.replace('\\', '/')
      dirCount += 1
      # Add the directory name to the map
      normalizedDirectoryName = normalizeName(curDirectory)
      fileMap[normalizedDirectoryName] = curDirectory
      continue
    # The current line might be a file line or a directory line
    fourthWord = lineSplit[3]
    # If the fourth word is a directory, then we just skip the 
    # directory here. The directory will be processed later.
    if fourthWord == '<DIR>':
      continue
    # At this point, we have an actual file. Process the file.
    fifthWord = lineSplit[4]
    fileName = curDirectory + '/' + fifthWord 
    # Add the file name to the map
    normalizedFileName = normalizeName(fileName)
    fileMap[normalizedFileName] = fileName 
    fileCount += 1
  # Return the results
  return [dirCount, fileCount]

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)  
  # Build the first and second file maps
  firstFileMap = {}
  secondFileMap = {}
  # Get the full first input file name
  inputFileName = glbInDirName + '\\' + glbInWindowsFileC
  # Read the input file list
  listInFile = HDLmUtility.readInputFile(inputFileName, 'iso-8859-1')
  # Process the list of lines 
  processLines(inputFileName, listInFile, firstFileMap)
  # Get the full second input file name
  inputFileName = glbInDirName + '\\' + glbInWindowsFileD
  # Read the input file list
  listInFile = HDLmUtility.readInputFile(inputFileName, 'iso-8859-1')
  # Process the list of lines
  processLines(inputFileName, listInFile, secondFileMap) 
  # Compare the two maps  
  compareTwoMaps(firstFileMap, secondFileMap)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__": 
  main()