# Class for building complex sets of strings (such as a program)
# 
# Each instance of this class is used to build a set of complex strings.
# For example, one instance of this class might be used to build a full
# JavaScript program. Each instance has the accumulated text (so far)
# and the current indentation level. 

from HDLmUtility  import *

class HDLmBuildLines(object):
  # The __init__ method creates an instance of the class
  def __init__(self):
    # Each of the lines is stored in the array below
    self.lines = [] 
    self.outputFileName = None
  # Add a new line to the set of lines 
  def addLine(self, newLine):
    # The original line is added to the lines array 
    self.lines.append(newLine)
  # Return the number of lines which may be zero, or more
  # than zero
  def getLineCount(self):
    return len(self.lines)
  # Return the complete set of accumulated lines as a list
  def getLines(self):
    return self.lines 
  # Get the output file name 
  def getFileName(self):
    return self.outputFileName
  # Set the output file name
  def setFileName(self, fileName):
    self.outputFileName = fileName
  # Write out all of the collected lines
  def writeOutputFile(self):
    outputLines = self.getLines()
    outputFileName = self.getFileName()
    HDLmUtility.writeOutputFile(outputLines, outputFileName)