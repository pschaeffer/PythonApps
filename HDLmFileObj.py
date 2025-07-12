# Each instane of this class has all of the information about
# one file

class HDLmFileObj(object):
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