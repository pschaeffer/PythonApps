# Some general notes. This code uses indexes and positions. Indexes can be used to 
# acceess Python list instances. Indexes are typically in the range of 0 to 8 or
# 0 to 80. Positions are more user friendly. Positions are typically in the range
# of 1 to 9 or 1 to 81.

from   tkinter import Tk, Canvas, Frame, BOTH, ttk, Toplevel
import bisect
import copy
import datetime
import math
import time

glbBoxCount = 9
glbBoxMax   = 9
glbBoxMin   = 1
glbColCount = 9
glbColMax   = 9
glbColMin   = 1
glbRowCount = 9
glbRowMax   = 9
glbRowMin   = 1
glbCellsCount = glbRowCount * glbColCount
glbCellsLen = 9
glbValueMax = 9
glbValueMin = 1
glbValueOff = 25

# Each instance of this class has all of the information about one Sudoku board
class Board(object):
  # The __init__ method creates an instance of the class      
  def __init__(self):
    self.cells = [None] * glbCellsCount
    self.cellsFilledIn = 0
    # Build all of the cells
    for rowPos in range(1, glbRowCount + 1):
      rowIndex = rowPos - 1
      for colPos in range(1, glbColCount + 1):
        colIndex = colPos - 1
        rowOffsetIndex = rowIndex * glbColCount
        newCell = Cell(rowPos, colPos)  
        self.cells[rowOffsetIndex + colIndex] = newCell
  # Make a complete clone of an instance of this class
  def clone(self):
    return copy.deepcopy(self)
  # Get references to all of the cells in one box. A box is 3X3 set of 
  # cells. The values passed to this routine are in the range of 1 to 9,
  # not zero to 8.
  def getBox(self, boxNumber):
    # Check the box number
    if boxNumber < glbBoxMin or \
       boxNumber > glbBoxMax:
      errorText = 'Box number ({0}) is out-of-range'
      errorText = errorText.format(boxNumber)
      raise ValueError(errorText)
    # Get references to all of the cells in the box
    rv = [] 
    boxIndex = boxNumber - 1
    startingRowIndex = (boxIndex // 3) * 3
    startingColIndex = (boxIndex % 3) * 3
    for rowIndex in range(startingRowIndex, startingRowIndex + 3):
      rowOffsetIndex = rowIndex * glbColCount
      for colIndex in range(startingColIndex, startingColIndex + 3):
        rv.append(self.cells[rowOffsetIndex + colIndex])
    # Return the row to the caller
    return rv
  # Get references to all of the cells in one column. The value passed
  # to this call is a position (1-9), not an index (0-8)
  def getCol(self, colPos):
    # Check the column number
    if colPos < glbColMin or \
       colPos > glbColMax:
      errorText = 'Column number (really a position) ({0}) is out-of-range'
      errorText = errorText.format(colPos)
      raise ValueError(errorText)
    # Get references to all of the cells in the column
    rv = []
    colIndex = colPos - 1
    for rowIndex in range(glbRowCount):
      rowOffsetIndex = rowIndex * glbColCount
      rv.append(self.cells[rowOffsetIndex + colIndex])
    # Return the column to the caller
    return rv
  # Get the number of cells that have been filled in and return the
  # value to the caller
  def getFilledIn(self):
    return self.cellsFilledIn
  # Get references to all of the cells in one row. The value passed
  # to this call is a position (1-9), not an index (0-8)
  def getRow(self, rowPos):
    # Check the row number
    if rowPos < glbRowMin or \
       rowPos > glbRowMax:
      errorText = 'Row number (really a position) ({0}) is out-of-range'
      errorText = errorText.format(rowPos)
      raise ValueError(errorText)
    # Get references to all of the cells in the row
    rv = []
    rowIndex = rowPos - 1
    rowOffsetIndex = rowIndex * glbColCount
    for colIndex in range(glbColCount):
      rv.append(self.cells[rowOffsetIndex + colIndex])
    # Return the row to the caller
    return rv
  # Store value on the board. The caller provides the row position,
  # the column position, and the new value. All values are checked
  # before they are used. The new value must be an integer value in
  # the correct range. 
  def storeValue(self, rowPos, colPos, newValue):
    # Check the values passed by the calle
    checkRow(rowPos)
    checkCol(colPos)
    checkValue(newValue)
    # Convert the row and column values to indexes
    rowIndex = rowPos - 1
    colIndex = colPos - 1
    rowOffsetIndex = rowIndex * glbColCount
    # Get a reference to the target cell
    oldCell = self.cells[rowOffsetIndex + colIndex]
    # The old value must be None or a list of possible values. The 
    # old value can not be an single (final) value.
    if isinstance(oldCell.value, int) == True:
      oldValue = oldCell.value
      errorText = 'Value ({0}) for row ({1}) column ({2}) is not None or a list'
      errorText = errorText.format(oldValue, rowPos, colPos)
      raise ValueError(errorText)
    # Store the new value
    oldCell.storeValue(newValue)
    self.cellsFilledIn = self.cellsFilledIn + 1

# Each instance of this class has all of the information about one cell 
class Cell(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, rowPos, colPos):
    # The value field below will always contain one of three types
    # of values. The first type is None which means that nothing 
    # has been assigned to the current cell. The second type is 
    # a specific integer value. The third type is a list. Each 
    # element in the list (there will be at least two) will be 
    # a integer value that could be assigned to the current cell. 
    self.value = None
    # The block list is a list of numbers (positions, not indexes) that 
    # can not occur at a given location. The block list will be empty if
    # an actual integer value is stored in the cell or if a list of values
    # is stored in the cell.
    self.blockList = []  
    # The allow (allowed) list is a list of numbers (positions, not indexes)
    # that can occur at a given location. This list will always be a direct
    # complement of the block list. The allow list will be empty if an 
    # actual integer value is stored in the cell or if a list of values
    # is stored in the cell.
    self.allowList = []
    # Check the row number
    checkRow(rowPos)
    # Check the column number
    checkCol(colPos)
    # Store the row and column numbers
    self.rowPosition = rowPos
    self.colPosition = colPos 
    # Calculate and store the box number
    rowIndex = rowPos - 1
    colIndex = colPos - 1 
    boxRowIndex = (rowIndex // 3) * 3
    boxColIndex = colIndex // 3
    boxPosIndex = boxRowIndex + boxColIndex
    boxPos = boxPosIndex + 1
    # This is the overall box position. In other words,
    # what box a given cell is in. This is not the location
    # of the cell in the box.
    self.boxPosition = boxPos
    # This is the box location. In other words, this is the
    # location of current cell in the current box. This is
    # not the box position. 
    boxLocIndex = (rowIndex % 3) * 3 + (colIndex % 3)
    boxLoc = boxLocIndex + 1
    self.boxLocation = boxLoc
  # This method stores a list of possible values in a cell
  def storeList(self, newList):
    # Check the new cell List passed by the caller
    checkList(newList)
    # Check if the old value is None. The old value must be 
    # none. In all other cases, an error has occurred. 
    if isinstance(self.value, (int, list)) == True:
      oldCol = self.colPosition
      oldRow = self.rowPosition
      oldValue = self.value
      errorText = 'Value ({0}) for row ({1}) column ({2}) is not None'
      errorText = errorText.format(oldValue, oldRow, oldCol)
      raise ValueError(errorText)
    # Store the new List
    self.value = newList
    self.blockList = []
    self.allowList = []
  # This method stores a value in a cell
  def storeValue(self, newValue):
    # Check the new cell value passed by the caller
    checkValue(newValue)
    # Check if the old value is None or a list of possible
    # values. The old value must be none or a list of values. 
    # In all other cases, an error has occurred. 
    if isinstance(self.value, int) == True:
      oldCol = self.colPosition
      oldRow = self.rowPosition
      oldValue = self.value
      errorText = 'Value ({0}) for row ({1}) column ({2}) is not None or a list'
      errorText = errorText.format(oldValue, oldRow, oldCol)
      raise ValueError(errorText)
    # Store the new value
    self.value = newValue
    self.blockList = []
    self.allowList = []

# Do all of the allowing (allow processing) based on the cells 
# that have not already been filled in. A cell is skipped if it 
# has already been filled in. Note that this routine only handles 
# cells that don't have a single final value for the cell in question.
# The set (really a list) of allowed values is the complement of the 
# set (really a list) of blocked values. In other words, a value is 
# allowed if it not blocked. 
def allowValues(boardCopy):
  # Build the list of allowed values. This list is exactly
  # as long as the cell list
  for curCell in boardCopy.cells:
    # Check if the current cell has a single integer value 
    # or a list of possible values. If the current cell has 
    # been set to a specific integer value or a list of values,
    # we can just ignore it.
    if isinstance(curCell.value, (int, list)) == True:
      continue
    allowValuesSet = set(range(1, glbValueMax+1)) - set(curCell.blockList)
    allowValuesList = list(allowValuesSet)
    allowValuesList.sort()
    curCell.allowList = allowValuesList
  # return allowedCells
  return
 
# Do all of the blocking based on the cells that have already
# been filled in. A cell is skipped if it has not already been
# filled in. Note that this routine only handles cells that have
# a single final value for the cell in question.
def blockValues(boardCopy):
  # Process all of the cell in the board
  for curCell in boardCopy.cells:
    # Check if the current cell has one specific value. If the
    # current cell has not been set to one specific value, we
    # can just ignore it.
    if isinstance(curCell.value, int) == False:
      continue
    # The current cell has one specific value. This value is 
    # blocked for the rest of the current row, column, and box.
    curValue = curCell.value
    curCol = curCell.colPosition
    curRow = curCell.rowPosition
    curBox = curCell.boxPosition
    # Mark all of the unfilled in cells in the row as blocked
    rowCells = boardCopy.getRow(curRow)
    for rowCell in rowCells:
      if rowCell.value == None and \
         curValue not in rowCell.blockList: 
        bisect.insort(rowCell.blockList, curValue)
    # Mark all of the unfilled in cells in the column as blocked
    colCells = boardCopy.getCol(curCol)
    for colCell in colCells:
      if colCell.value == None and \
         curValue not in colCell.blockList: 
        bisect.insort(colCell.blockList, curValue)
    # Mark all of the unfilled in cells in the box as blocked
    boxCells = boardCopy.getBox(curBox)
    for boxCell in boxCells:
      if boxCell.value == None and \
         curValue not in boxCell.blockList:
        bisect.insort(boxCell.blockList, curValue)

# Add the allow lists from all of the cells of a board
# to a canvas
def canvasAddAllows(curBoard, curCanvas):
  # Process all of the cell in the board
  for curCell in curBoard.cells:
    # Check if the current cell has a value or a list of possible
    # values. If the current cell has been set to a specific value
    # or has been set to a list of possible values, we can just 
    # ignore it. It won't have any allows and even if it did, we
    # already have the final value of a list of possible values. 
    if isinstance(curCell.value, (int, list)) == True:
      continue
    # Get the row and column position of the current call
    curCol = curCell.colPosition
    curRow = curCell.rowPosition
    # Get the x and y location of where the first allow
    # value should be placed
    xPos = (curCol-1) * 100 + 25 + glbValueOff
    yPos = (curRow-1) * 100 + 25 + glbValueOff
    # Process all of the possible values
    index = 0
    for curValue in range(glbValueMin, glbValueMax+1):
      index += 1 
      # Create some text for the current value, if the value is 
      # in the current allow list
      curText = str(curValue) if (curValue in curCell.allowList) else ' '
      curCanvas.create_text(xPos, yPos, text=curText, fill="green", font=('Helvetica 15'))
      # Every three values, shft down and left as need be
      if (index % 3) == 0:
        xPos = xPos - glbValueOff * 2
        yPos = yPos + glbValueOff
      else:
        xPos += glbValueOff

# Add the values from a board to a canvas
def canvasAddValues(curBoard, curCanvas):
  # Process all of the cell in the board
  for curCell in curBoard.cells:
    # Check if the current cell has been set to a specific value. 
    # If the current cell has not been set to a specific value,
    # we can just ignore it.
    if isinstance(curCell.value, int) == False:
      continue
    curValue = curCell.value
    curCol = curCell.colPosition
    curRow = curCell.rowPosition
    xPos = (curCol-1) * 100 + 75 
    yPos = (curRow-1) * 100 + 75
    curText = str(curValue)
    curCanvas.create_text(xPos, yPos, text=curText, fill="black", font=('Helvetica 45 bold'))

# Draw a set of line in a canvas
def canvasDrawLines(curCanvas):
  # Create the horizontal lines
  xPos = 25
  yPos = 25
  # Create all of the horizontal lines
  for i1 in range(4):
    curCanvas.create_line(xPos, yPos, xPos+900, yPos, fill="black", width=3)
    yOffset = 0
    # Create the minor horizontal lines
    if i1 != 3:
      for i2 in range(2):
        yOffset = yOffset + 100
        curCanvas.create_line(xPos, yPos+yOffset, xPos+900, yPos+yOffset, fill="black", width=1)
    yPos = yPos + 300
  # Create the vertical lines
  xPos = 25
  yPos = 25
  # Create all of the vertical lines
  for i1 in range(4):
    curCanvas.create_line(xPos, yPos, xPos, yPos+900, fill="black", width=3)
    xOffset = 0
    # Create the minor vertical lines
    if i1 != 3:
      for i2 in range(2):
        xOffset = xOffset + 100
        curCanvas.create_line(xPos+xOffset, yPos, xPos+xOffset, yPos+900, fill="black", width=1)
    xPos = xPos + 300

# Show a set of values on a canvas (a Tkinter canvas).
# This routine create a canvas and draws a set of lines
# on the canvas. Optionally a set of values are addded
# to the canvas.
def canvasShowValues(curBoard):
  # Create a Tkinter window
  winOne = Toplevel()
  # Set the size of the Tkinter window
  winOne.geometry("950x950")
  # Create a Tkinter canvas 
  canvasOne = Canvas(winOne, width=950, height=950)
  canvasOne.pack()
  # Add a set of lines to each canvas widget
  canvasDrawLines(canvasOne)
  if curBoard != None:
    canvasAddValues(curBoard, canvasOne)
    canvasAddAllows(curBoard, canvasOne)
  return winOne

# This routine merges a set of lists. Sets
# are used to do the merge. This means that
# the output list will have exactly one copy
# of each values.
def cellMergeList(*args):
  # Build the initial empty set
  outputSet = set()
  # Process all of the lists
  for arg in args:
    tempSet = set(arg)
    outputSet = outputSet | tempSet
  # Return the final list to the caller
  rv = list(outputSet)
  return rv

# Make sure that all of the allowed values for all of
# the cells are in the allowed list (of values) passed
# by the caller
def checkCellList(cellsList, allowedValuesList):
  # Assume that we will return false to the caller
  rv = False
  # Process all of the cells in the cell list
  for cell in cellsList:
    # Check all of the allowed values for each cell. Make
    # sure that each allowed value is allowed values list.
    for allowValue in cell.allowList:
      if allowValue not in allowedValuesList:
        return rv
  # Return a true value to the caller
  rv = True
  return rv

# Make sure that every cell in the cell list has two or three
# of the allowed values
def checkCellListAllowed(cellsList, allowedValuesList):
  rv = False
  # Process all of the cells in the cell list
  for cell in cellsList:
    # Check all of the allowed values for each cell. Make
    # sure that each allowed value is allowed values list.
    count = 0
    for allowValue in cell.allowList:
      if allowValue in allowedValuesList:
        count += 1
    # Check if the count is two or three
    if count != 2 and \
       count != 3:
      return rv
  # Return a true value to the caller
  rv = True
  return rv

# Check a column position, the column position must be
# in range or an exception is raised
def checkCol(colPos):
  # Check if the column position is set
  if colPos == None:
    errorText = 'Column number is not set'
    raise ValueError(errorText)
  # Make sure the column number passed by the caller is an integer
  if isinstance(colPos, int) == False:
    errorText = 'Column number is not an integer'
    raise ValueError(errorText)
  # Check the column number
  if colPos < glbColMin or \
     colPos > glbColMax:
    errorText = 'Column number (really a position) ({0}) is out-of-range'
    errorText = errorText.format(colPos)
    raise ValueError(errorText)
  return

# Check if the current location and value are already in the 
# result set. This routine returns true, if the current location
# and value is a duplicate and false if not.
def checkForDuplicates(resultsList, curCell, curValue):
  # set the default output value
  rv = True
  # Scan the results list looking for a match. If the
  # current result has already been added, skip the 
  # current location.
  countRv = 0
  for result in resultsList:
    # Get some information about the current result
    tempCell = result[0]
    tempRow = tempCell.rowPosition
    tempCol = tempCell.colPosition
    tempValue = result[1]
    # Check if the current result matches the result we just
    # found
    if tempRow == curCell.rowPosition and \
       tempCol == curCell.colPosition and \
       tempValue == curValue:
      countRv = countRv + 1
  # If no result matches were found, return false
  if countRv == 0:
    rv = False
  return rv

# Check a list of values, the list must be valid and all
# of the entries in the list must be valid. 
def checkList(valuesList):
  # Check if the list of values is set
  if valuesList == None:
    errorText = 'List of values is not set'
    raise ValueError(errorText)
  # Make sure the list of values passed by the caller is a list
  if isinstance(valuesList, list) == False:
    errorText = 'List of values is not a list'
    raise ValueError(errorText)
  # Make sure the length of the list of values is correct
  if len(valuesList) < 2:
    valuesListLen = len(valuesList)
    errorText = 'List of values is not long ({0}) enough'
    errorText = errorText.format(valuesListLen)
    raise ValueError(errorText)
  # Check each entry in the list of values
  for value in valuesList:
    checkValue(value)
  return

# Check if two or more lists match. Lists are only deemed 
# to match if they have exactly the same length and they 
# have exactly the same contents.
def checkListsMatch(list1, *args):
  rv = False
  for arg in args:
    if len(list1) != len(arg):
      return rv
  # Check if the contents of the lists match
  for arg in args:
    index = 0
    while index < len(list1):
      if list1[index] != arg[index]:
        return rv
      index += 1
  # Since everything matched, we must return true
  rv = True
  return rv

# Check a row position, the row position must be
# in range or an exception is raised
def checkRow(rowPos):
  # Check if the row position is set
  if rowPos == None:
    errorText = 'Row number is not set'
    raise ValueError(errorText)
  # Make sure the row number passed by the caller is an integer
  if isinstance(rowPos, int) == False:
    errorText = 'Row number is not an integer'
    raise ValueError(errorText)
  # Check the row number
  if rowPos < glbRowMin or \
     rowPos > glbRowMax:
    errorText = 'Row number (really a position) ({0}) is out-of-range'
    errorText = errorText.format(rowPos)
    raise ValueError(errorText)
  return

# Check a value, the value must be in range or an 
# exception is raised
def checkValue(value):
  # Check if the value is set
  if value == None:
    errorText = 'Value is not set'
    raise ValueError(errorText)
  # Make sure the value passed by the caller is an integer
  if isinstance(value, int) == False:
    errorText = 'Value is not an integer'
    raise ValueError(errorText)
  # Check the value
  if value < glbValueMin or \
     value > glbValueMax:
    errorText = 'Value ({0}) is out-of-range'
    errorText = errorText.format(value)
    raise ValueError(errorText)
  return

# Check if one of the values passed by the caller appears 
# in a cell that is not automatically bypassed. If such a 
# cell is found, then return false to the caller. otherwise,
# return true to the caller.
def checkValuesSkipList(curCells, valueList, skipList):
  # Assume that we will return false to the caller
  rv = False
  # Get the length of the list of cells passed to this routine
  curCellsLen = len(curCells)
  for value in valueList:
    indexCellList = 0
    while indexCellList < curCellsLen:
      tempCellFromList = curCells[indexCellList]
      indexCellList += 1
      if tempCellFromList in skipList: 
        continue
      if value in tempCellFromList.allowList:
        return rv
  # Return a true value to the caller
  rv = True
  return rv

# This routine is passed a list of cells and a value.
# This routine returns the number of times the value
# is allowed in the list of cells. This routine also
# returns a list of cells (the list may be empty) where
# the current value can be placed. The current cells 
# passed to this routine must be a complete row, column,
# or box. In other words, all of the cells of a unit 
# must be passed.
def countAllowed(curCells, curValue):
  outCells = []
  # Check the values passed by the caller
  if curCells == None:
    errorText = 'Cell list is not set'
    raise ValueError(errorText)
  # Check the cell list length
  curCellsLen = len(curCells)
  if curCellsLen !=  glbCellsLen: 
    errorText = 'Cell list length ({0}) is invalid'
    errorText = errorText.format(curCellsLen)
    raise ValueError(errorText)
  checkValue(curValue)
  count = 0
  # Check for the value passed by the caller in all
  # of the cells in the cell list
  for curCell in curCells:
    if curValue in curCell.allowList:
      count += 1
      outCells.append(curCell)
  return count, outCells

# This routine is passed a list of cells and a value.
# This routine returns the number of times the value
# is allowed in the list of cells. This routine also
# returns a list of index values (the list may be empty)
# where the current value can be placed. The current
# cells passed to this routine must be a complete row, 
# column, or box. In other words, all of the cells of 
# a unit must be passed.
def countAllowedIndexes(curCells, curValue):
  outIndexes = []
  # Check the values passed by the caller
  if curCells == None:
    errorText = 'Cell list is not set'
    raise ValueError(errorText)
  # Check the cell list length
  curCellsLen = len(curCells)
  if curCellsLen !=  glbCellsLen: 
    errorText = 'Cell list length ({0}) is invalid'
    errorText = errorText.format(curCellsLen)
    raise ValueError(errorText)
  checkValue(curValue)
  count = 0
  # Check for the value passed by the caller in all
  # of the cells in the cell list
  for curIndex in range(curCellsLen):
    curCell = curCells[curIndex]
    if curValue in curCell.allowList:
      count += 1
      outIndexes.append(curIndex)
  return count, outIndexes

# This routine is passed a list of cells and a value.
# This routine returns the number of times the value
# is allowed in the list of cells. This routine also
# returns a list of cells (the list may be empty) where
# the current value can be placed. The current cells 
# passed to this routine may not be a complete row,
# column, or box. 
def countAllowedList(curCells, curValue):
  outCells = []
  # Check the values passed by the caller
  if curCells == None:
    errorText = 'Cell list is not set'
    raise ValueError(errorText)
  # Get the cell list length
  curCellsLen = len(curCells)
  checkValue(curValue)
  count = 0
  # Check for the value passed by the caller in all
  # of the cells in the cell list
  for curCell in curCells:
    if curValue in curCell.allowList:
      count += 1
      outCells.append(curCell)
  return count, outCells

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. 
def defaultValues1(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 8)
  boardCopy.storeValue(1, 5, 6)
  boardCopy.storeValue(1, 8, 2)
  boardCopy.storeValue(2, 4, 8)
  boardCopy.storeValue(3, 1, 7)
  boardCopy.storeValue(3, 2, 5)
  boardCopy.storeValue(3, 3, 1)
  boardCopy.storeValue(3, 8, 6)
  boardCopy.storeValue(4, 1, 9)
  boardCopy.storeValue(4, 4, 2)
  boardCopy.storeValue(4, 7, 1)
  boardCopy.storeValue(5, 1, 2)
  boardCopy.storeValue(5, 2, 4)
  boardCopy.storeValue(5, 3, 6)
  boardCopy.storeValue(5, 4, 9)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(7, 4, 1)
  boardCopy.storeValue(7, 8, 3)
  boardCopy.storeValue(8, 2, 1)
  boardCopy.storeValue(8, 3, 3)
  boardCopy.storeValue(8, 7, 9)
  boardCopy.storeValue(8, 8, 7)
  boardCopy.storeValue(9, 5, 7)
  boardCopy.storeValue(9, 9, 6)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. 
def defaultValues2(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 4)
  boardCopy.storeValue(1, 9, 5)
  boardCopy.storeValue(2, 1, 9)
  boardCopy.storeValue(2, 4, 6)
  boardCopy.storeValue(2, 5, 8)
  boardCopy.storeValue(2, 6, 3)
  boardCopy.storeValue(3, 1, 2)
  boardCopy.storeValue(3, 4, 9)
  boardCopy.storeValue(3, 6, 5)
  boardCopy.storeValue(4, 3, 7)
  boardCopy.storeValue(4, 4, 5)
  boardCopy.storeValue(4, 8, 8)
  boardCopy.storeValue(5, 2, 9)
  boardCopy.storeValue(5, 7, 4)
  boardCopy.storeValue(6, 3, 5)
  boardCopy.storeValue(6, 5, 9)
  boardCopy.storeValue(6, 9, 6)
  boardCopy.storeValue(7, 8, 6)
  boardCopy.storeValue(7, 9, 4)
  boardCopy.storeValue(8, 5, 3)
  boardCopy.storeValue(8, 6, 7)
  boardCopy.storeValue(9, 2, 1)
  boardCopy.storeValue(9, 3, 8)
  boardCopy.storeValue(9, 7, 7)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. 
def defaultValues3(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 8, 3)
  boardCopy.storeValue(1, 9, 9)
  boardCopy.storeValue(2, 5, 6)
  boardCopy.storeValue(2, 7, 5)
  boardCopy.storeValue(3, 2, 3)
  boardCopy.storeValue(3, 5, 4)
  boardCopy.storeValue(3, 9, 7)
  boardCopy.storeValue(5, 1, 9)
  boardCopy.storeValue(5, 4, 7)
  boardCopy.storeValue(5, 9, 5)
  boardCopy.storeValue(6, 1, 4)
  boardCopy.storeValue(6, 2, 7)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(6, 5, 1)
  boardCopy.storeValue(6, 7, 6)
  boardCopy.storeValue(7, 7, 3)
  boardCopy.storeValue(7, 8, 5)
  boardCopy.storeValue(8, 3, 2)
  boardCopy.storeValue(8, 6, 6)
  boardCopy.storeValue(9, 1, 1)
  boardCopy.storeValue(9, 3, 8)
  boardCopy.storeValue(9, 4, 2)
  boardCopy.storeValue(9, 7, 9)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# hidden pair. See https://www.sudoku-solutions.com/index.php?
# section=solvingHiddenSubsets
def defaultValues4(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 4)
  boardCopy.storeValue(1, 2, 6)
  boardCopy.storeValue(1, 3, 5)
  boardCopy.storeValue(1, 5, 8)
  boardCopy.storeValue(1, 7, 3)
  boardCopy.storeValue(1, 8, 2)
  boardCopy.storeValue(2, 1, 7)
  boardCopy.storeValue(2, 2, 9)
  boardCopy.storeValue(2, 3, 8)
  boardCopy.storeValue(2, 5, 3)
  boardCopy.storeValue(2, 6, 2)
  boardCopy.storeValue(2, 7, 6)
  boardCopy.storeValue(2, 9, 5)
  boardCopy.storeValue(3, 1, 1)
  boardCopy.storeValue(3, 2, 2)
  boardCopy.storeValue(3, 3, 3)
  boardCopy.storeValue(3, 4, 5)
  boardCopy.storeValue(3, 5, 6)
  boardCopy.storeValue(3, 8, 9)
  boardCopy.storeValue(3, 9, 8)
  boardCopy.storeValue(4, 1, 8)
  boardCopy.storeValue(4, 4, 2)
  boardCopy.storeValue(4, 6, 5)
  boardCopy.storeValue(4, 8, 3)
  boardCopy.storeValue(5, 3, 2)
  boardCopy.storeValue(5, 7, 5)
  boardCopy.storeValue(6, 1, 5)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(6, 6, 6)
  boardCopy.storeValue(6, 7, 2)
  boardCopy.storeValue(6, 8, 8)
  boardCopy.storeValue(7, 2, 8)
  boardCopy.storeValue(7, 3, 4)
  boardCopy.storeValue(7, 5, 5)
  boardCopy.storeValue(7, 6, 3)
  boardCopy.storeValue(7, 7, 1)
  boardCopy.storeValue(7, 8, 7)
  boardCopy.storeValue(7, 9, 2)
  boardCopy.storeValue(8, 5, 2)
  boardCopy.storeValue(8, 7, 8)
  boardCopy.storeValue(8, 8, 5)
  boardCopy.storeValue(8, 9, 4)
  boardCopy.storeValue(9, 1, 2)
  boardCopy.storeValue(9, 2, 5)
  boardCopy.storeValue(9, 3, 7)
  boardCopy.storeValue(9, 5, 1)
  boardCopy.storeValue(9, 7, 9)
  boardCopy.storeValue(9, 8, 6)
  boardCopy.storeValue(9, 9, 3)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find 
# a naked triple. See https://www.sudokuwiki.org/Naked
# _Candidates
def defaultValues5(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 2, 1)
  boardCopy.storeValue(1, 3, 7)
  boardCopy.storeValue(1, 4, 9)
  boardCopy.storeValue(1, 6, 3)
  boardCopy.storeValue(1, 7, 6)
  boardCopy.storeValue(2, 5, 8)
  boardCopy.storeValue(3, 1, 9)
  boardCopy.storeValue(3, 7, 5)
  boardCopy.storeValue(3, 9, 7)
  boardCopy.storeValue(4, 2, 7)
  boardCopy.storeValue(4, 3, 2)
  boardCopy.storeValue(4, 5, 1)
  boardCopy.storeValue(4, 7, 4)
  boardCopy.storeValue(4, 8, 3)
  boardCopy.storeValue(5, 4, 4)
  boardCopy.storeValue(5, 6, 2)
  boardCopy.storeValue(5, 8, 7)
  boardCopy.storeValue(6, 2, 6)
  boardCopy.storeValue(6, 3, 4)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(6, 5, 7)
  boardCopy.storeValue(6, 7, 2)
  boardCopy.storeValue(6, 8, 5)
  boardCopy.storeValue(7, 1, 7)
  boardCopy.storeValue(7, 3, 1)
  boardCopy.storeValue(7, 8, 6)
  boardCopy.storeValue(7, 9, 5)
  boardCopy.storeValue(8, 5, 3)
  boardCopy.storeValue(9, 3, 5)
  boardCopy.storeValue(9, 4, 6)
  boardCopy.storeValue(9, 6, 1)
  boardCopy.storeValue(9, 7, 7)
  boardCopy.storeValue(9, 8, 2)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a naked triple. See https://www.sudokuwiki.org/Naked 
# _Candidates
def defaultValues6(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 2, 7)
  boardCopy.storeValue(1, 4, 4)
  boardCopy.storeValue(1, 6, 8)
  boardCopy.storeValue(1, 8, 2)
  boardCopy.storeValue(1, 9, 9)
  boardCopy.storeValue(2, 3, 2)
  boardCopy.storeValue(2, 9, 4)
  boardCopy.storeValue(3, 1, 8)
  boardCopy.storeValue(3, 2, 5)
  boardCopy.storeValue(3, 3, 4)
  boardCopy.storeValue(3, 5, 2)
  boardCopy.storeValue(3, 9, 7)
  boardCopy.storeValue(4, 3, 8)
  boardCopy.storeValue(4, 4, 3)
  boardCopy.storeValue(4, 5, 7)
  boardCopy.storeValue(4, 6, 4)
  boardCopy.storeValue(4, 7, 2)
  boardCopy.storeValue(5, 2, 2)
  boardCopy.storeValue(6, 3, 3)
  boardCopy.storeValue(6, 4, 2)
  boardCopy.storeValue(6, 5, 6)
  boardCopy.storeValue(6, 6, 1)
  boardCopy.storeValue(6, 7, 7)
  boardCopy.storeValue(7, 5, 9)
  boardCopy.storeValue(7, 6, 3)
  boardCopy.storeValue(7, 7, 6)
  boardCopy.storeValue(7, 8, 1)
  boardCopy.storeValue(7, 9, 2)
  boardCopy.storeValue(8, 1, 2)
  boardCopy.storeValue(8, 7, 4)
  boardCopy.storeValue(8, 9, 3)
  boardCopy.storeValue(9, 1, 1)
  boardCopy.storeValue(9, 2, 3)
  boardCopy.storeValue(9, 4, 6)
  boardCopy.storeValue(9, 5, 4)
  boardCopy.storeValue(9, 6, 2)
  boardCopy.storeValue(9, 8, 7)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a hidden triple. See https://www.sudokuwiki.org/Hidden
# _Candidates
def defaultValues7(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 6, 1)
  boardCopy.storeValue(1, 8, 3)
  boardCopy.storeValue(2, 1, 2)
  boardCopy.storeValue(2, 2, 3)
  boardCopy.storeValue(2, 3, 1)
  boardCopy.storeValue(2, 5, 9)
  boardCopy.storeValue(3, 2, 6)
  boardCopy.storeValue(3, 3, 5)
  boardCopy.storeValue(3, 6, 3)
  boardCopy.storeValue(3, 7, 1)
  boardCopy.storeValue(4, 1, 6)
  boardCopy.storeValue(4, 2, 7)
  boardCopy.storeValue(4, 3, 8)
  boardCopy.storeValue(4, 4, 9)
  boardCopy.storeValue(4, 5, 2)
  boardCopy.storeValue(4, 6, 4)
  boardCopy.storeValue(4, 7, 3)
  boardCopy.storeValue(5, 1, 1)
  boardCopy.storeValue(5, 3, 3)
  boardCopy.storeValue(5, 5, 5)
  boardCopy.storeValue(5, 9, 6)
  boardCopy.storeValue(6, 4, 1)
  boardCopy.storeValue(6, 5, 3)
  boardCopy.storeValue(6, 6, 6)
  boardCopy.storeValue(6, 7, 7)
  boardCopy.storeValue(7, 3, 9)
  boardCopy.storeValue(7, 4, 3)
  boardCopy.storeValue(7, 5, 6)
  boardCopy.storeValue(7, 7, 5)
  boardCopy.storeValue(7, 8, 7)
  boardCopy.storeValue(8, 3, 6)
  boardCopy.storeValue(8, 5, 1)
  boardCopy.storeValue(8, 6, 9)
  boardCopy.storeValue(8, 7, 8)
  boardCopy.storeValue(8, 8, 4)
  boardCopy.storeValue(8, 9, 3)
  boardCopy.storeValue(9, 1, 3)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# hidden pair. See https://www.thonky.com/sudoku/hidden-pairs
# -triples-quads
def defaultValues8(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 4)
  boardCopy.storeValue(1, 4, 3)
  boardCopy.storeValue(1, 5, 7)
  boardCopy.storeValue(1, 6, 2)
  boardCopy.storeValue(1, 7, 1)
  boardCopy.storeValue(1, 8, 9)
  boardCopy.storeValue(1, 9, 6)
  boardCopy.storeValue(2, 3, 2)
  boardCopy.storeValue(2, 7, 8)
  boardCopy.storeValue(2, 8, 7)
  boardCopy.storeValue(3, 1, 9)
  boardCopy.storeValue(3, 2, 7)
  boardCopy.storeValue(3, 7, 4)
  boardCopy.storeValue(4, 1, 5)
  boardCopy.storeValue(4, 3, 3)
  boardCopy.storeValue(4, 6, 1)
  boardCopy.storeValue(4, 7, 7)
  boardCopy.storeValue(4, 8, 6)
  boardCopy.storeValue(5, 2, 9)
  boardCopy.storeValue(5, 5, 3)
  boardCopy.storeValue(5, 6, 7)
  boardCopy.storeValue(5, 7, 5)
  boardCopy.storeValue(5, 9, 4)
  boardCopy.storeValue(6, 1, 2)
  boardCopy.storeValue(6, 3, 7)
  boardCopy.storeValue(6, 7, 3)
  boardCopy.storeValue(7, 1, 6)
  boardCopy.storeValue(7, 6, 3)
  boardCopy.storeValue(7, 7, 9)
  boardCopy.storeValue(7, 9, 7)
  boardCopy.storeValue(8, 3, 9)
  boardCopy.storeValue(8, 4, 7)
  boardCopy.storeValue(8, 7, 2)
  boardCopy.storeValue(8, 8, 4)
  boardCopy.storeValue(9, 1, 7)
  boardCopy.storeValue(9, 2, 2)
  boardCopy.storeValue(9, 4, 9)
  boardCopy.storeValue(9, 5, 5)
  boardCopy.storeValue(9, 7, 6)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a hidden triple. See https://www.thonky.com/sudoku/hidden
# -pairs-triples-quads
def defaultValues9(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 7, 2)
  boardCopy.storeValue(1, 8, 6)
  boardCopy.storeValue(2, 3, 9)
  boardCopy.storeValue(2, 5, 8)
  boardCopy.storeValue(2, 8, 4)
  boardCopy.storeValue(2, 9, 3)
  boardCopy.storeValue(3, 1, 5)
  boardCopy.storeValue(3, 5, 3)
  boardCopy.storeValue(3, 8, 9)
  boardCopy.storeValue(4, 4, 2)
  boardCopy.storeValue(4, 5, 1)
  boardCopy.storeValue(4, 6, 5)
  boardCopy.storeValue(5, 1, 3)
  boardCopy.storeValue(5, 2, 5)
  boardCopy.storeValue(5, 7, 1)
  boardCopy.storeValue(5, 9, 9)
  boardCopy.storeValue(6, 1, 1)
  boardCopy.storeValue(6, 2, 8)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(6, 5, 7)
  boardCopy.storeValue(6, 6, 9)
  boardCopy.storeValue(6, 9, 4)
  boardCopy.storeValue(7, 1, 8)
  boardCopy.storeValue(7, 5, 5)
  boardCopy.storeValue(7, 6, 4)
  boardCopy.storeValue(7, 7, 9)
  boardCopy.storeValue(8, 3, 4)
  boardCopy.storeValue(9, 3, 5)
  boardCopy.storeValue(9, 5, 2)
  boardCopy.storeValue(9, 6, 3)
  boardCopy.storeValue(9, 7, 4)
  boardCopy.storeValue(9, 8, 1)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a naked pair. See https://www.sudoku-solutions.com/index.
# php?section=solvingNakedSubsets
def defaultValues10(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 1)
  boardCopy.storeValue(1, 3, 4)
  boardCopy.storeValue(1, 5, 9)
  boardCopy.storeValue(1, 8, 6)
  boardCopy.storeValue(1, 9, 8)
  boardCopy.storeValue(2, 1, 9)
  boardCopy.storeValue(2, 2, 5)
  boardCopy.storeValue(2, 3, 6)
  boardCopy.storeValue(2, 5, 1)
  boardCopy.storeValue(2, 6, 8)
  boardCopy.storeValue(2, 8, 3)
  boardCopy.storeValue(2, 9, 4)
  boardCopy.storeValue(3, 3, 8)
  boardCopy.storeValue(3, 4, 4)
  boardCopy.storeValue(3, 6, 6)
  boardCopy.storeValue(3, 7, 9)
  boardCopy.storeValue(3, 8, 5)
  boardCopy.storeValue(3, 9, 1)
  boardCopy.storeValue(4, 1, 5)
  boardCopy.storeValue(4, 2, 1)
  boardCopy.storeValue(4, 8, 8)
  boardCopy.storeValue(4, 9, 6)
  boardCopy.storeValue(5, 1, 8)
  boardCopy.storeValue(5, 4, 6)
  boardCopy.storeValue(5, 8, 1)
  boardCopy.storeValue(5, 9, 2)
  boardCopy.storeValue(6, 1, 6)
  boardCopy.storeValue(6, 2, 4)
  boardCopy.storeValue(6, 5, 8)
  boardCopy.storeValue(6, 8, 9)
  boardCopy.storeValue(6, 9, 7)
  boardCopy.storeValue(7, 1, 7)
  boardCopy.storeValue(7, 2, 8)
  boardCopy.storeValue(7, 3, 1)
  boardCopy.storeValue(7, 4, 9)
  boardCopy.storeValue(7, 5, 2)
  boardCopy.storeValue(7, 6, 3)
  boardCopy.storeValue(7, 7, 6)
  boardCopy.storeValue(7, 8, 4)
  boardCopy.storeValue(7, 9, 5)
  boardCopy.storeValue(8, 1, 4)
  boardCopy.storeValue(8, 2, 9)
  boardCopy.storeValue(8, 3, 5)
  boardCopy.storeValue(8, 5, 6)
  boardCopy.storeValue(8, 7, 8)
  boardCopy.storeValue(8, 8, 2)
  boardCopy.storeValue(8, 9, 3)
  boardCopy.storeValue(9, 2, 6)
  boardCopy.storeValue(9, 4, 8)
  boardCopy.storeValue(9, 5, 5)
  boardCopy.storeValue(9, 6, 4)
  boardCopy.storeValue(9, 7, 1)
  boardCopy.storeValue(9, 8, 7)
  boardCopy.storeValue(9, 9, 9)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a naked pair. See https://www.sudokuwiki.org/Naked_Candidates.
def defaultValues11(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 4)
  boardCopy.storeValue(1, 7, 9)
  boardCopy.storeValue(1, 8, 3)
  boardCopy.storeValue(1, 9, 8)
  boardCopy.storeValue(2, 2, 3)
  boardCopy.storeValue(2, 3, 2)
  boardCopy.storeValue(2, 5, 9)
  boardCopy.storeValue(2, 6, 4)
  boardCopy.storeValue(2, 7, 1)
  boardCopy.storeValue(3, 2, 9)
  boardCopy.storeValue(3, 3, 5)
  boardCopy.storeValue(3, 4, 3)
  boardCopy.storeValue(3, 7, 2)
  boardCopy.storeValue(3, 8, 4)
  boardCopy.storeValue(4, 1, 3)
  boardCopy.storeValue(4, 2, 7)
  boardCopy.storeValue(4, 4, 6)
  boardCopy.storeValue(4, 6, 9)
  boardCopy.storeValue(4, 9, 4)
  boardCopy.storeValue(5, 1, 5)
  boardCopy.storeValue(5, 2, 2)
  boardCopy.storeValue(5, 3, 9)
  boardCopy.storeValue(5, 6, 1)
  boardCopy.storeValue(5, 7, 6)
  boardCopy.storeValue(5, 8, 7)
  boardCopy.storeValue(5, 9, 3)
  boardCopy.storeValue(6, 1, 6)
  boardCopy.storeValue(6, 3, 4)
  boardCopy.storeValue(6, 4, 7)
  boardCopy.storeValue(6, 6, 3)
  boardCopy.storeValue(6, 8, 9)
  boardCopy.storeValue(7, 1, 9)
  boardCopy.storeValue(7, 2, 5)
  boardCopy.storeValue(7, 3, 7)
  boardCopy.storeValue(7, 6, 8)
  boardCopy.storeValue(7, 7, 3)
  boardCopy.storeValue(8, 3, 3)
  boardCopy.storeValue(8, 4, 9)
  boardCopy.storeValue(8, 7, 4)
  boardCopy.storeValue(9, 1, 2)
  boardCopy.storeValue(9, 2, 4)
  boardCopy.storeValue(9, 5, 3)
  boardCopy.storeValue(9, 7, 7)
  boardCopy.storeValue(9, 9, 9)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a naked pair. See https://www.sudokuwiki.org/Naked_Candidates.
def defaultValues12(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 2, 8)
  boardCopy.storeValue(1, 5, 9)
  boardCopy.storeValue(1, 8, 3)
  boardCopy.storeValue(2, 2, 3)
  boardCopy.storeValue(2, 8, 6)
  boardCopy.storeValue(2, 9, 9)
  boardCopy.storeValue(3, 1, 9)
  boardCopy.storeValue(3, 3, 2)
  boardCopy.storeValue(3, 5, 6)
  boardCopy.storeValue(3, 6, 3)
  boardCopy.storeValue(3, 7, 1)
  boardCopy.storeValue(3, 8, 5)
  boardCopy.storeValue(3, 9, 8)
  boardCopy.storeValue(4, 2, 2)
  boardCopy.storeValue(4, 4, 8)
  boardCopy.storeValue(4, 6, 4)
  boardCopy.storeValue(4, 7, 5)
  boardCopy.storeValue(4, 8, 9)
  boardCopy.storeValue(5, 1, 8)
  boardCopy.storeValue(5, 2, 5)
  boardCopy.storeValue(5, 3, 1)
  boardCopy.storeValue(5, 4, 9)
  boardCopy.storeValue(5, 6, 7)
  boardCopy.storeValue(5, 8, 4)
  boardCopy.storeValue(5, 9, 6)
  boardCopy.storeValue(6, 1, 3)
  boardCopy.storeValue(6, 2, 9)
  boardCopy.storeValue(6, 3, 4)
  boardCopy.storeValue(6, 4, 6)
  boardCopy.storeValue(6, 6, 5)
  boardCopy.storeValue(6, 7, 8)
  boardCopy.storeValue(6, 8, 7)
  boardCopy.storeValue(7, 1, 5)
  boardCopy.storeValue(7, 2, 6)
  boardCopy.storeValue(7, 3, 3)
  boardCopy.storeValue(7, 5, 4)
  boardCopy.storeValue(7, 7, 9)
  boardCopy.storeValue(7, 8, 8)
  boardCopy.storeValue(7, 9, 7)
  boardCopy.storeValue(8, 1, 2)
  boardCopy.storeValue(8, 8, 1)
  boardCopy.storeValue(8, 9, 5)
  boardCopy.storeValue(9, 2, 1)
  boardCopy.storeValue(9, 5, 5)
  boardCopy.storeValue(9, 8, 2)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a hidden pair. See https://www.sudokuwiki.org/Hidden_Candidates.
def defaultValues13(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(2, 1, 9)
  boardCopy.storeValue(2, 3, 4)
  boardCopy.storeValue(2, 4, 6)
  boardCopy.storeValue(2, 6, 7)
  boardCopy.storeValue(3, 2, 7)
  boardCopy.storeValue(3, 3, 6)
  boardCopy.storeValue(3, 4, 8)
  boardCopy.storeValue(3, 6, 4)
  boardCopy.storeValue(3, 7, 1)
  boardCopy.storeValue(4, 1, 3)
  boardCopy.storeValue(4, 3, 9)
  boardCopy.storeValue(4, 4, 7)
  boardCopy.storeValue(4, 6, 1)
  boardCopy.storeValue(4, 8, 8)
  boardCopy.storeValue(5, 1, 7)
  boardCopy.storeValue(5, 3, 8)
  boardCopy.storeValue(5, 7, 3)
  boardCopy.storeValue(5, 9, 1)
  boardCopy.storeValue(6, 2, 5)
  boardCopy.storeValue(6, 3, 1)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(6, 6, 8)
  boardCopy.storeValue(6, 7, 7)
  boardCopy.storeValue(6, 9, 2)
  boardCopy.storeValue(7, 3, 7)
  boardCopy.storeValue(7, 4, 5)
  boardCopy.storeValue(7, 6, 2)
  boardCopy.storeValue(7, 7, 6)
  boardCopy.storeValue(7, 8, 1)
  boardCopy.storeValue(8, 3, 5)
  boardCopy.storeValue(8, 4, 4)
  boardCopy.storeValue(8, 6, 3)
  boardCopy.storeValue(8, 7, 2)
  boardCopy.storeValue(8, 9, 8)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find
# a hidden pair. See https://www.sudokuwiki.org/Hidden_Candidates.
def defaultValues14(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 7)
  boardCopy.storeValue(1, 2, 2)
  boardCopy.storeValue(1, 4, 4)
  boardCopy.storeValue(1, 6, 8)
  boardCopy.storeValue(1, 8, 3)
  boardCopy.storeValue(2, 2, 8)
  boardCopy.storeValue(2, 8, 4)
  boardCopy.storeValue(2, 9, 7)
  boardCopy.storeValue(3, 1, 4)
  boardCopy.storeValue(3, 3, 1)
  boardCopy.storeValue(3, 5, 7)
  boardCopy.storeValue(3, 6, 6)
  boardCopy.storeValue(3, 7, 8)
  boardCopy.storeValue(3, 9, 2)
  boardCopy.storeValue(4, 1, 8)
  boardCopy.storeValue(4, 2, 1)
  boardCopy.storeValue(4, 4, 7)
  boardCopy.storeValue(4, 5, 3)
  boardCopy.storeValue(4, 6, 9)
  boardCopy.storeValue(5, 4, 8)
  boardCopy.storeValue(5, 5, 5)
  boardCopy.storeValue(5, 6, 1)
  boardCopy.storeValue(6, 4, 2)
  boardCopy.storeValue(6, 5, 6)
  boardCopy.storeValue(6, 6, 4)
  boardCopy.storeValue(6, 8, 8)
  boardCopy.storeValue(7, 1, 2)
  boardCopy.storeValue(7, 3, 9)
  boardCopy.storeValue(7, 4, 6)
  boardCopy.storeValue(7, 5, 8)
  boardCopy.storeValue(7, 7, 4)
  boardCopy.storeValue(7, 8, 1)
  boardCopy.storeValue(7, 9, 3)
  boardCopy.storeValue(8, 1, 3)
  boardCopy.storeValue(8, 2, 4)
  boardCopy.storeValue(8, 9, 8)
  boardCopy.storeValue(9, 1, 1)
  boardCopy.storeValue(9, 2, 6)
  boardCopy.storeValue(9, 3, 8)
  boardCopy.storeValue(9, 4, 9)
  boardCopy.storeValue(9, 5, 4)
  boardCopy.storeValue(9, 6, 3)
  boardCopy.storeValue(9, 7, 2)
  boardCopy.storeValue(9, 8, 7)
  boardCopy.storeValue(9, 9, 5)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.sudokuwiki.org/Naked_Candidates.SS
def defaultValues15(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 2)
  boardCopy.storeValue(1, 2, 9)
  boardCopy.storeValue(1, 3, 4)
  boardCopy.storeValue(1, 4, 5)
  boardCopy.storeValue(1, 5, 1)
  boardCopy.storeValue(1, 6, 3)
  boardCopy.storeValue(1, 9, 6)
  boardCopy.storeValue(2, 1, 6)
  boardCopy.storeValue(2, 4, 8)
  boardCopy.storeValue(2, 5, 4)
  boardCopy.storeValue(2, 6, 2)
  boardCopy.storeValue(2, 7, 3)
  boardCopy.storeValue(2, 8, 1)
  boardCopy.storeValue(2, 9, 9)
  boardCopy.storeValue(3, 1, 3)
  boardCopy.storeValue(3, 4, 6)
  boardCopy.storeValue(3, 5, 9)
  boardCopy.storeValue(3, 6, 7)
  boardCopy.storeValue(3, 7, 2)
  boardCopy.storeValue(3, 8, 5)
  boardCopy.storeValue(3, 9, 4)
  boardCopy.storeValue(4, 5, 5)
  boardCopy.storeValue(4, 6, 6)
  boardCopy.storeValue(5, 2, 4)
  boardCopy.storeValue(5, 5, 8)
  boardCopy.storeValue(5, 8, 6)
  boardCopy.storeValue(6, 4, 4)
  boardCopy.storeValue(6, 5, 7)
  boardCopy.storeValue(7, 1, 7)
  boardCopy.storeValue(7, 2, 3)
  boardCopy.storeValue(7, 4, 1)
  boardCopy.storeValue(7, 5, 6)
  boardCopy.storeValue(7, 6, 4)
  boardCopy.storeValue(7, 9, 5)
  boardCopy.storeValue(8, 1, 9)
  boardCopy.storeValue(8, 4, 7)
  boardCopy.storeValue(8, 5, 3)
  boardCopy.storeValue(8, 6, 5)
  boardCopy.storeValue(8, 9, 1)
  boardCopy.storeValue(9, 1, 4)
  boardCopy.storeValue(9, 4, 9)
  boardCopy.storeValue(9, 5, 2)
  boardCopy.storeValue(9, 6, 8)
  boardCopy.storeValue(9, 7, 6)
  boardCopy.storeValue(9, 8, 3)
  boardCopy.storeValue(9, 9, 7)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.sudoku-solutions.com/index.php
# ?section=solvingNakedSubsets
def defaultValues16(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 7)
  boardCopy.storeValue(1, 2, 1)
  boardCopy.storeValue(1, 3, 9)
  boardCopy.storeValue(1, 5, 3)
  boardCopy.storeValue(1, 7, 8)
  boardCopy.storeValue(1, 8, 6)
  boardCopy.storeValue(2, 1, 2)
  boardCopy.storeValue(2, 2, 4)
  boardCopy.storeValue(2, 3, 3)
  boardCopy.storeValue(2, 5, 8)
  boardCopy.storeValue(2, 6, 6)
  boardCopy.storeValue(2, 7, 1)
  boardCopy.storeValue(2, 9, 9)
  boardCopy.storeValue(3, 1, 5)
  boardCopy.storeValue(3, 2, 6)
  boardCopy.storeValue(3, 3, 8)
  boardCopy.storeValue(3, 4, 9)
  boardCopy.storeValue(3, 5, 1)
  boardCopy.storeValue(3, 8, 4)
  boardCopy.storeValue(3, 9, 3)
  boardCopy.storeValue(4, 1, 3)
  boardCopy.storeValue(4, 4, 6)
  boardCopy.storeValue(4, 6, 9)
  boardCopy.storeValue(4, 8, 8)
  boardCopy.storeValue(5, 3, 6)
  boardCopy.storeValue(5, 7, 9)
  boardCopy.storeValue(6, 1, 9)
  boardCopy.storeValue(6, 4, 8)
  boardCopy.storeValue(6, 6, 1)
  boardCopy.storeValue(6, 7, 6)
  boardCopy.storeValue(6, 8, 3)
  boardCopy.storeValue(7, 2, 3)
  boardCopy.storeValue(7, 3, 7)
  boardCopy.storeValue(7, 5, 9)
  boardCopy.storeValue(7, 6, 8)
  boardCopy.storeValue(7, 7, 5)
  boardCopy.storeValue(7, 8, 2)
  boardCopy.storeValue(7, 9, 6)
  boardCopy.storeValue(8, 5, 6)
  boardCopy.storeValue(8, 7, 3)
  boardCopy.storeValue(8, 8, 9)
  boardCopy.storeValue(8, 9, 7)
  boardCopy.storeValue(9, 1, 6)
  boardCopy.storeValue(9, 2, 9)
  boardCopy.storeValue(9, 3, 2)
  boardCopy.storeValue(9, 5, 5)
  boardCopy.storeValue(9, 7, 4)
  boardCopy.storeValue(9, 8, 1)
  boardCopy.storeValue(9, 9, 8)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.thonky.com/sudoku/naked-pairs
# -triples-quads.
def defaultValues17(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 1)
  boardCopy.storeValue(1, 2, 2)
  boardCopy.storeValue(1, 3, 6)
  boardCopy.storeValue(1, 6, 9)
  boardCopy.storeValue(1, 8, 7)
  boardCopy.storeValue(1, 9, 3)
  boardCopy.storeValue(2, 3, 5)
  boardCopy.storeValue(2, 4, 6)
  boardCopy.storeValue(2, 5, 2)
  boardCopy.storeValue(2, 6, 7)
  boardCopy.storeValue(2, 8, 9)
  boardCopy.storeValue(3, 1, 7)
  boardCopy.storeValue(3, 3, 8)
  boardCopy.storeValue(3, 6, 3)
  boardCopy.storeValue(3, 8, 2)
  boardCopy.storeValue(4, 2, 7)
  boardCopy.storeValue(4, 5, 9)
  boardCopy.storeValue(4, 6, 2)
  boardCopy.storeValue(4, 7, 6)
  boardCopy.storeValue(5, 1, 8)
  boardCopy.storeValue(5, 6, 6)
  boardCopy.storeValue(5, 8, 1)
  boardCopy.storeValue(5, 9, 9)
  boardCopy.storeValue(6, 2, 6)
  boardCopy.storeValue(6, 4, 3)
  boardCopy.storeValue(6, 6, 5)
  boardCopy.storeValue(6, 7, 7)
  boardCopy.storeValue(6, 8, 4)
  boardCopy.storeValue(7, 3, 9)
  boardCopy.storeValue(7, 4, 2)
  boardCopy.storeValue(7, 5, 6)
  boardCopy.storeValue(7, 6, 4)
  boardCopy.storeValue(7, 7, 1)
  boardCopy.storeValue(7, 8, 8)
  boardCopy.storeValue(7, 9, 7)
  boardCopy.storeValue(8, 2, 8)
  boardCopy.storeValue(8, 6, 1)
  boardCopy.storeValue(9, 4, 9)
  boardCopy.storeValue(9, 6, 8)
  boardCopy.storeValue(9, 8, 6)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# hidden triple. See https://sudoku.com/sudoku-rules/hidden
# -triples/.
def defaultValues18(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 3, 8)
  boardCopy.storeValue(1, 6, 7)
  boardCopy.storeValue(1, 7, 9)
  boardCopy.storeValue(2, 2, 4)
  boardCopy.storeValue(2, 3, 2)
  boardCopy.storeValue(2, 6, 5)
  boardCopy.storeValue(3, 4, 6)
  boardCopy.storeValue(3, 8, 5)
  boardCopy.storeValue(4, 3, 3)
  boardCopy.storeValue(4, 6, 6)
  boardCopy.storeValue(4, 7, 8)
  boardCopy.storeValue(4, 9, 1)
  boardCopy.storeValue(5, 9, 6)
  boardCopy.storeValue(6, 1, 9)
  boardCopy.storeValue(6, 5, 7)
  boardCopy.storeValue(7, 2, 8)
  boardCopy.storeValue(7, 4, 1)
  boardCopy.storeValue(7, 5, 3)
  boardCopy.storeValue(7, 7, 4)
  boardCopy.storeValue(7, 8, 7)
  boardCopy.storeValue(8, 5, 9)
  boardCopy.storeValue(9, 2, 1)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.sudokuoftheday.com/techniques/
# naked-pairs-triples
def defaultValues19(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 4)
  boardCopy.storeValue(1, 4, 3)
  boardCopy.storeValue(1, 5, 9)
  boardCopy.storeValue(1, 9, 2)
  boardCopy.storeValue(2, 1, 2)
  boardCopy.storeValue(2, 2, 6)
  boardCopy.storeValue(2, 5, 5)
  boardCopy.storeValue(2, 6, 8)
  boardCopy.storeValue(2, 7, 3)
  boardCopy.storeValue(2, 8, 9)
  boardCopy.storeValue(3, 1, 5)
  boardCopy.storeValue(3, 2, 9)
  boardCopy.storeValue(3, 3, 3)
  boardCopy.storeValue(3, 4, 6)
  boardCopy.storeValue(3, 7, 1)
  boardCopy.storeValue(3, 8, 8)
  boardCopy.storeValue(4, 1, 1)
  boardCopy.storeValue(4, 4, 8)
  boardCopy.storeValue(4, 5, 6)
  boardCopy.storeValue(4, 9, 9)
  boardCopy.storeValue(5, 1, 6)
  boardCopy.storeValue(5, 3, 5)
  boardCopy.storeValue(5, 4, 9)
  boardCopy.storeValue(5, 7, 2)
  boardCopy.storeValue(6, 2, 3)
  boardCopy.storeValue(6, 3, 9)
  boardCopy.storeValue(6, 4, 2)
  boardCopy.storeValue(6, 5, 4)
  boardCopy.storeValue(6, 6, 5)
  boardCopy.storeValue(6, 8, 1)
  boardCopy.storeValue(6, 9, 6)
  boardCopy.storeValue(7, 2, 5)
  boardCopy.storeValue(7, 3, 6)
  boardCopy.storeValue(7, 6, 9)
  boardCopy.storeValue(7, 8, 2)
  boardCopy.storeValue(8, 2, 1)
  boardCopy.storeValue(8, 3, 4)
  boardCopy.storeValue(8, 4, 7)
  boardCopy.storeValue(8, 7, 9)
  boardCopy.storeValue(8, 9, 5)
  boardCopy.storeValue(9, 1, 9)
  boardCopy.storeValue(9, 4, 5)
  boardCopy.storeValue(9, 5, 3)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.sudokuoftheday.com/techniques/
# naked-pairs-triples
def defaultValues20(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 5)
  boardCopy.storeValue(1, 4, 7)
  boardCopy.storeValue(1, 6, 6)
  boardCopy.storeValue(1, 7, 9)
  boardCopy.storeValue(1, 9, 2)
  boardCopy.storeValue(2, 3, 9)
  boardCopy.storeValue(2, 5, 1)
  boardCopy.storeValue(2, 7, 8)
  boardCopy.storeValue(2, 8, 7)
  boardCopy.storeValue(2, 9, 5)
  boardCopy.storeValue(3, 1, 2)
  boardCopy.storeValue(3, 2, 7)
  boardCopy.storeValue(3, 4, 8)
  boardCopy.storeValue(3, 5, 9)
  boardCopy.storeValue(3, 6, 5)
  boardCopy.storeValue(3, 7, 3)
  boardCopy.storeValue(3, 9, 6)
  boardCopy.storeValue(4, 1, 3)
  boardCopy.storeValue(4, 2, 4)
  boardCopy.storeValue(4, 3, 7)
  boardCopy.storeValue(4, 4, 6)
  boardCopy.storeValue(4, 5, 8)
  boardCopy.storeValue(4, 6, 9)
  boardCopy.storeValue(4, 9, 1)
  boardCopy.storeValue(5, 1, 9)
  boardCopy.storeValue(5, 2, 1)
  boardCopy.storeValue(5, 3, 5)
  boardCopy.storeValue(5, 7, 7)
  boardCopy.storeValue(5, 8, 6)
  boardCopy.storeValue(5, 9, 8)
  boardCopy.storeValue(6, 1, 8)
  boardCopy.storeValue(6, 2, 2)
  boardCopy.storeValue(6, 3, 6)
  boardCopy.storeValue(6, 4, 5)
  boardCopy.storeValue(6, 5, 7)
  boardCopy.storeValue(6, 6, 1)
  boardCopy.storeValue(6, 7, 4)
  boardCopy.storeValue(6, 8, 3)
  boardCopy.storeValue(6, 9, 9)
  boardCopy.storeValue(7, 3, 2)
  boardCopy.storeValue(7, 4, 1)
  boardCopy.storeValue(7, 9, 7)
  boardCopy.storeValue(8, 1, 7)
  boardCopy.storeValue(8, 7, 1)
  boardCopy.storeValue(8, 9, 3)
  boardCopy.storeValue(9, 1, 1)
  boardCopy.storeValue(9, 3, 3)
  boardCopy.storeValue(9, 4, 9)
  boardCopy.storeValue(9, 6, 7)
  boardCopy.storeValue(9, 9, 4)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.sudokuoftheday.com/techniques/
# naked-pairs-triples
def defaultValues21(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 8)
  boardCopy.storeValue(1, 2, 9)
  boardCopy.storeValue(1, 3, 1)
  boardCopy.storeValue(1, 6, 5)
  boardCopy.storeValue(1, 7, 7)
  boardCopy.storeValue(1, 8, 6)
  boardCopy.storeValue(2, 1, 5)
  boardCopy.storeValue(2, 2, 3)
  boardCopy.storeValue(2, 3, 7)
  boardCopy.storeValue(2, 4, 6)
  boardCopy.storeValue(2, 5, 9)
  boardCopy.storeValue(2, 7, 2)
  boardCopy.storeValue(2, 9, 8)
  boardCopy.storeValue(3, 1, 4)
  boardCopy.storeValue(3, 2, 6)
  boardCopy.storeValue(3, 3, 2)
  boardCopy.storeValue(3, 9, 5)
  boardCopy.storeValue(4, 1, 2)
  boardCopy.storeValue(4, 2, 4)
  boardCopy.storeValue(4, 3, 3)
  boardCopy.storeValue(4, 4, 5)
  boardCopy.storeValue(4, 5, 1)
  boardCopy.storeValue(4, 7, 8)
  boardCopy.storeValue(4, 9, 6)
  boardCopy.storeValue(5, 1, 1)
  boardCopy.storeValue(5, 2, 5)
  boardCopy.storeValue(5, 3, 6)
  boardCopy.storeValue(5, 7, 4)
  boardCopy.storeValue(6, 1, 9)
  boardCopy.storeValue(6, 2, 7)
  boardCopy.storeValue(6, 3, 8)
  boardCopy.storeValue(6, 5, 4)
  boardCopy.storeValue(6, 6, 6)
  boardCopy.storeValue(6, 7, 5)
  boardCopy.storeValue(7, 1, 3)
  boardCopy.storeValue(7, 2, 1)
  boardCopy.storeValue(7, 3, 9)
  boardCopy.storeValue(7, 5, 5)
  boardCopy.storeValue(7, 7, 6)
  boardCopy.storeValue(7, 8, 8)
  boardCopy.storeValue(7, 9, 7)
  boardCopy.storeValue(8, 1, 6)
  boardCopy.storeValue(8, 2, 8)
  boardCopy.storeValue(8, 3, 4)
  boardCopy.storeValue(8, 8, 5)
  boardCopy.storeValue(8, 9, 2)
  boardCopy.storeValue(9, 1, 7)
  boardCopy.storeValue(9, 2, 2)
  boardCopy.storeValue(9, 3, 5)
  boardCopy.storeValue(9, 4, 8)
  boardCopy.storeValue(9, 5, 6)
  boardCopy.storeValue(9, 7, 3)
  return


# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# naked triple. See https://www.sudokuoftheday.com/techniques/
# naked-pairs-triples
def defaultValues22(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 4)
  boardCopy.storeValue(1, 3, 6)
  boardCopy.storeValue(1, 5, 5)
  boardCopy.storeValue(1, 6, 1)
  boardCopy.storeValue(1, 7, 2)
  boardCopy.storeValue(2, 2, 3)
  boardCopy.storeValue(2, 5, 2)
  boardCopy.storeValue(2, 9, 9)
  boardCopy.storeValue(4, 2, 6)
  boardCopy.storeValue(4, 3, 4)
  boardCopy.storeValue(4, 4, 2)
  boardCopy.storeValue(4, 6, 5)
  boardCopy.storeValue(4, 7, 7)
  boardCopy.storeValue(4, 8, 9)
  boardCopy.storeValue(4, 9, 8)
  boardCopy.storeValue(5, 1, 7)
  boardCopy.storeValue(5, 7, 5)
  boardCopy.storeValue(5, 8, 2)
  boardCopy.storeValue(5, 9, 4)
  boardCopy.storeValue(6, 1, 2)
  boardCopy.storeValue(6, 2, 8)
  boardCopy.storeValue(6, 3, 5)
  boardCopy.storeValue(6, 4, 7)
  boardCopy.storeValue(6, 5, 4)
  boardCopy.storeValue(6, 6, 9)
  boardCopy.storeValue(6, 7, 6)
  boardCopy.storeValue(6, 8, 3)
  boardCopy.storeValue(6, 9, 1)
  boardCopy.storeValue(7, 7, 9)
  boardCopy.storeValue(8, 1, 9)
  boardCopy.storeValue(8, 5, 6)
  boardCopy.storeValue(8, 8, 4)
  boardCopy.storeValue(9, 2, 4)
  boardCopy.storeValue(9, 3, 7)
  boardCopy.storeValue(9, 4, 5)
  boardCopy.storeValue(9, 5, 9)
  boardCopy.storeValue(9, 7, 1)
  boardCopy.storeValue(9, 9, 2)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to find a
# hidden triple. See https://www.sudokuoftheday.com/techniques/
# naked-pairs-triples
def defaultValues23(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 1, 3)
  boardCopy.storeValue(1, 2, 7)
  boardCopy.storeValue(1, 4, 4)
  boardCopy.storeValue(1, 6, 8)
  boardCopy.storeValue(1, 7, 1)
  boardCopy.storeValue(2, 4, 9)
  boardCopy.storeValue(2, 6, 3)
  boardCopy.storeValue(2, 7, 7)
  boardCopy.storeValue(2, 9, 4)
  boardCopy.storeValue(3, 1, 9)
  boardCopy.storeValue(3, 2, 4)
  boardCopy.storeValue(3, 4, 1)
  boardCopy.storeValue(3, 8, 8)
  boardCopy.storeValue(3, 9, 3)
  boardCopy.storeValue(4, 1, 4)
  boardCopy.storeValue(4, 2, 2)
  boardCopy.storeValue(4, 9, 5)
  boardCopy.storeValue(5, 4, 5)
  boardCopy.storeValue(5, 6, 4)
  boardCopy.storeValue(6, 1, 8)
  boardCopy.storeValue(6, 8, 4)
  boardCopy.storeValue(6, 9, 6)
  boardCopy.storeValue(7, 2, 1)
  boardCopy.storeValue(7, 5, 4)
  boardCopy.storeValue(7, 6, 9)
  boardCopy.storeValue(8, 1, 5)
  boardCopy.storeValue(8, 3, 9)
  boardCopy.storeValue(8, 4, 6)
  boardCopy.storeValue(8, 7, 4)
  boardCopy.storeValue(9, 3, 4)
  boardCopy.storeValue(9, 4, 2)
  boardCopy.storeValue(9, 7, 9)
  boardCopy.storeValue(9, 8, 3)
  boardCopy.storeValue(9, 9, 1)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to test
# X-Wings. See https://www.sudokuwiki.org/sudoku.htm?bd=
# 000400602006000100090500080050300000301206405000007020030002060004000900507009000
def defaultValues24(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 4, 4)
  boardCopy.storeValue(1, 7, 6)
  boardCopy.storeValue(1, 9, 2)
  boardCopy.storeValue(2, 3, 6)
  boardCopy.storeValue(2, 7, 1)
  boardCopy.storeValue(3, 2, 9)
  boardCopy.storeValue(3, 4, 5)
  boardCopy.storeValue(3, 8, 8)
  boardCopy.storeValue(4, 2, 5)
  boardCopy.storeValue(4, 4, 3)
  boardCopy.storeValue(5, 1, 3)
  boardCopy.storeValue(5, 3, 1)
  boardCopy.storeValue(5, 4, 2)
  boardCopy.storeValue(5, 6, 6)
  boardCopy.storeValue(5, 7, 4)
  boardCopy.storeValue(5, 9, 5)
  boardCopy.storeValue(6, 6, 7)
  boardCopy.storeValue(6, 8, 2)
  boardCopy.storeValue(7, 2, 3)
  boardCopy.storeValue(7, 6, 2)
  boardCopy.storeValue(7, 8, 6)
  boardCopy.storeValue(8, 3, 4)
  boardCopy.storeValue(8, 7, 9)
  boardCopy.storeValue(9, 1, 5)
  boardCopy.storeValue(9, 3, 7)
  boardCopy.storeValue(9, 6, 9)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to test
# X-Wings. See https://www.sudokuwiki.org/sudoku.htm?bd=
# 005000400020940000900700008003000290100203007079000300400008001000014060006000700
def defaultValues25(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 3, 5)
  boardCopy.storeValue(1, 7, 4)
  boardCopy.storeValue(2, 2, 2)
  boardCopy.storeValue(2, 4, 9)
  boardCopy.storeValue(2, 5, 4)
  boardCopy.storeValue(3, 1, 9)
  boardCopy.storeValue(3, 4, 7)
  boardCopy.storeValue(3, 9, 8)
  boardCopy.storeValue(4, 3, 3)
  boardCopy.storeValue(4, 7, 2)
  boardCopy.storeValue(4, 8, 9)
  boardCopy.storeValue(5, 1, 1)
  boardCopy.storeValue(5, 4, 2)
  boardCopy.storeValue(5, 6, 3)
  boardCopy.storeValue(5, 9, 7)
  boardCopy.storeValue(6, 2, 7)
  boardCopy.storeValue(6, 3, 9)
  boardCopy.storeValue(6, 7, 3)
  boardCopy.storeValue(7, 1, 4)
  boardCopy.storeValue(7, 6, 8)
  boardCopy.storeValue(7, 9, 1)
  boardCopy.storeValue(8, 5, 1)
  boardCopy.storeValue(8, 6, 4)
  boardCopy.storeValue(8, 8, 6)
  boardCopy.storeValue(9, 3, 6)
  boardCopy.storeValue(9, 7, 7)
  return

# Store a set of default values on the board. This routine
# is used for testing, so that the default values don't have
# to be entered by hand. This set of values is used to test
# X-Wings. See https://www.sudokuwiki.org/sudoku.htm?bd=
# 003910700000003400100040006060700000002109600000002010700080003008200000005071900
def defaultValues26(boardCopy):
  # Store a set of default values on the board
  boardCopy.storeValue(1, 3, 3)
  boardCopy.storeValue(1, 4, 9)
  boardCopy.storeValue(1, 5, 1)
  boardCopy.storeValue(1, 7, 7)
  boardCopy.storeValue(2, 6, 3)
  boardCopy.storeValue(2, 7, 4)
  boardCopy.storeValue(3, 1, 1)
  boardCopy.storeValue(3, 5, 4)
  boardCopy.storeValue(3, 9, 6)
  boardCopy.storeValue(4, 2, 6)
  boardCopy.storeValue(4, 4, 7)
  boardCopy.storeValue(5, 3, 2)
  boardCopy.storeValue(5, 4, 1)
  boardCopy.storeValue(5, 6, 9)
  boardCopy.storeValue(5, 7, 6)
  boardCopy.storeValue(6, 6, 2)
  boardCopy.storeValue(6, 8, 1)
  boardCopy.storeValue(7, 1, 7)
  boardCopy.storeValue(7, 5, 8)
  boardCopy.storeValue(7, 9, 3)
  boardCopy.storeValue(8, 3, 8)
  boardCopy.storeValue(8, 4, 2)
  boardCopy.storeValue(9, 3, 5)
  boardCopy.storeValue(9, 5, 7)
  boardCopy.storeValue(9, 6, 1)
  boardCopy.storeValue(9, 7, 9)
  return

# Display a set of locations where exactly one
# value can be placed
def displayOneValues(prefixStr, locations, iterationCount):
  if iterationCount > 1:
    print()
  # Display a location
  for location in locations:
    curCell = location[0]
    curRow = curCell.rowPosition
    curCol = curCell.colPosition
    curValue = location[1]
    print('Algo', prefixStr, 'Row', curRow, 'Column', curCol, 'Value', curValue)

# Find all of the locations where a value can be placed. A 
# value can be placed in a location (a cell) if the location 
# does not have a value currently and if the location is not
# blocked for some reason. This routine is no longer in use.
def findLocations(curBoard):
  rv = []
  # Process all of the cell in the board
  for curCell in curBoard.cells:
    # Check if the current cell has a value or a list of possible
    # values. If the current cell been set to a specific value or
    # if it has been set to a list of possible values, we can just 
    # ignore it.
    if isinstance(curCell.value, (int, list)) == True:
      continue
    # Check all of the possible values
    for i in range(glbValueMin, glbValueMax+1):
      # Check if the current value is blocked 
      if i in curCell.blockList:
        continue
      # Build a tuple with the current cell and value
      curTuple = (curCell, i)
      rv.append(curTuple)
  return rv

# This routine looks for locations where a value can be
# placed. An acceptable location (in this routine) will
# be the only place in a row, column, and box where 
# the value can be placed. This routine is no longer 
# in use.
def findOner(locs):
  rv = []
  # Check all of the possible locations
  for loc1 in locs:
    # Extract some values from the current tuple
    temp1Cell = loc1[0]
    temp1Value = loc1[1]
    temp1Row = temp1Cell.rowPosition
    temp1Col = temp1Cell.colPosition
    temp1Box = temp1Cell.boxPosition
    count = 0
    if temp1Row == 4 and \
       temp1Col == 2 and \
       temp1Value == 3:
      rv = rv
    # Scan all of the locations looking for match
    for loc2 in locs:
      temp2Cell = loc2[0]
      temp2Value = loc2[1]
      temp2Row = temp2Cell.rowPosition
      temp2Col = temp2Cell.colPosition
      temp2Box = temp2Cell.boxPosition
      if temp1Row == temp2Row and \
         temp1Value == temp2Value:
        count = count + 1
      if temp1Col == temp2Col and \
         temp1Value == temp2Value:
        count = count + 1
      if temp1Box == temp2Box and \
         temp1Value == temp2Value:
        count = count + 1
    # If three result matches were found, add the current location
    if count == 3:
      curTuple = (temp1Cell, temp1Value)
      rv.append(curTuple)
  # Return the final list of locations where a value can be placed
  return rv

# Look for pairs of values. A pair of values is something like 
# 1 and 9 being allowed in exacty two places. One of the places
# must end up as a 1 and the other one must end up as a 9. We 
# don't know which is which, but that doesn't matter for some
# purposes. If the 1 and 9 are in the same box, then 1 and 9
# can not appear anywhere else in the same box. If the 1 and 9
# are on the same row, then 1 and 9 can not be anywhere else on 
# the same row. If the 1 and 9 are in the same column, then 1 
# and 9 can not be anywhere else in the same column. 
def findPairsValues(curBoard):
  pairCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a row where the 
  # current value has just two (and only two) possible
  # locations.
  for row in range(glbRowMin, glbRowMax+1):
    # break
    tempCells = curBoard.getRow(row)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2:
          continue
        # Make sure the cell lists match
        cells1 = curTuple1[1]
        cells2 = curTuple2[1]
        if checkListsMatch(cells1, cells2) == False:
          continue
        # At this point we have a pair of values. We can now adjust
        # the allow and block lists for every cell in the unit.
        pairCount += 1
        colIndex1 = cells1[0].colPosition - 1
        colIndex2 = cells1[1].colPosition - 1
        allowList = [value1, value2]
        # Remove allows from the rest of the row
        cellsColIndexList = [colIndex1, colIndex2]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellsColIndexList) 
        totalRemoveAllowsCount += removeCount
        # Remove all other allows from the list pair
        removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
        totalRemoveAllowsCount += removeCount
  # Scan all of the columns looking for a column where the 
  # current value has just two (and only two) possible
  # locations.
  for col in range(glbColMin, glbColMax+1):
    # break
    tempCells = curBoard.getCol(col)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2:
          continue
        # Make sure the cell lists match
        cells1 = curTuple1[1]
        cells2 = curTuple2[1]
        if checkListsMatch(cells1, cells2) == False:
          continue
        # At this point we have a pair of values. We can now adjust
        # the allow and block lists for every cell in the unit.
        pairCount += 1
        rowIndex1 = cells1[0].rowPosition - 1
        rowIndex2 = cells1[1].rowPosition - 1
        allowList = [value1, value2]
        # Remove allows from the rest of the column
        cellsColIndexList = [rowIndex1, rowIndex2]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellsColIndexList) 
        totalRemoveAllowsCount += removeCount
        # Remove all other allows from the list pair
        removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
        totalRemoveAllowsCount += removeCount
  # Scan all of the boxes looking for a box where the 
  # current value has just two (and only two) possible
  # locations. Boxes are scanned first because a pair 
  # inside a box may be on the same row or in the same
  # column. 
  for box in range(glbBoxMin, glbBoxMax+1):
    # break
    tempCells = curBoard.getBox(box)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2:
          continue
        # Make sure the cell lists match
        cells1 = curTuple1[1]
        cells2 = curTuple2[1]
        if checkListsMatch(cells1, cells2) == False:
          continue
        # At this point we have a  pair of values. We can 
        # now adjust the allow and block lists for every 
        # cell in the unit
        pairCount += 1
        boxIndex1 = cells1[0].boxPosition - 1
        boxIndex2 = cells2[1].boxPosition - 1
        boxLocation1 = cells1[0].boxLocation - 1
        boxLocation2 = cells2[1].boxLocation - 1
        colIndex1 = cells1[0].colPosition - 1
        colIndex2 = cells2[1].colPosition - 1
        rowIndex1 = cells1[0].rowPosition - 1
        rowIndex2 = cells2[1].rowPosition - 1
        allowList = [value1, value2]
        # Remove allows from the rest of the box
        cellBoxIndexList = [boxLocation1, boxLocation2]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellBoxIndexList) 
        totalRemoveAllowsCount += removeCount
        # Remove all other allows from the list pair
        removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
        totalRemoveAllowsCount += removeCount
        # Store the list of possible values in each cell. For reasons
          # that I do not understand, this loop causes error later.
        for cell in cells1:
          break
          removeCount = len(cell.allowList)
          totalRemoveAllowsCount += removeCount
          cell.storeList(allowList)
        # We can now check if the hidden pair was in the same row.
        # If this is true, then the rest of the row can be adjusted
        # to remove the allowed values.
        if rowIndex1 == rowIndex2:
          tempCellsRow = curBoard.getRow(rowIndex1+1)
          # Remove allows from the rest of the row
          cellsColIndexList = [colIndex1, colIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
        # We can now check if the hidden pair was in the same column.
        # If this is true, then the rest of the column can be adjusted
        # to remove the allowed values.
        if colIndex1 == colIndex2:
          tempCellsCol = curBoard.getCol(colIndex1+1)
          # Remove allows from the rest of the column
          cellsRowIndexList = [rowIndex1, rowIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellsRowIndexList) 
          totalRemoveAllowsCount += removeCount
  # Return the final pair count and the number of allows that were
  # removed
  return [pairCount, totalRemoveAllowsCount]

# This routine looks for locations where a value can be
# placed. An acceptable location (in this routine) will
# be the only place in a row, column, or box where 
# the value can be placed. This routine is no longer
# in use.
def findSingleLocationsOne(locs):
  rv = []
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):
    # Scan all of the rows looking for a row where the 
    # current value has just one (and only one) possible
    # location.
    for row in range(glbRowMin, glbRowMax+1):
      countRow = 0
      for loc in locs:
        # Extract some values from the current tuple
        tempCell = loc[0]
        tempValue = loc[1]
        tempRow = tempCell.rowPosition
        tempCol = tempCell.colPosition
        tempBox = tempCell.boxPosition
        # Check if the current location is a possible location 
        # for the current row and current value
        if row != tempRow or \
           value != tempValue:
          continue
        countRow = countRow + 1 
        curCell = Cell(tempRow, tempCol)
      # If the current value occurred once and only once in
      # the current row, then we have a place where the current
      # value can be placed
      if countRow == 1:
        curTuple = (curCell, value)
        # Scan the results list looking for a match. If the
        # current result has already been added, skip the 
        # current location.
        countRv = 0
        for result in rv:
         # Get some information about the current result
          tempCell = result[0]
          tempRow = tempCell.rowPosition
          tempCol = tempCell.colPosition
          tempValue = result[1]
          # Check if the current result matches the result we just
          # found
          if tempRow == curCell.rowPosition and \
             tempCol == curCell.colPosition and \
             tempValue == value:
            countRv = countRv + 1
        # If no result matches were found, add the current location
        if countRv == 0:
          rv.append(curTuple)
    # Scan all of the columns looking for a column where the 
    # current value has just one (and only one) possible
    # location.
    for col in range(glbColMin, glbColMax+1):
      countCol = 0
      for loc in locs:
        # Extract some values from the current tuple
        tempCell = loc[0]
        tempValue = loc[1]
        tempRow = tempCell.rowPosition
        tempCol = tempCell.colPosition
        tempBox = tempCell.boxPosition
        # Check if the current location is a possible location 
        # for the current column and current value
        if col != tempCol or \
           value != tempValue:
          continue
        countCol = countCol + 1 
        curCell = Cell(tempRow, tempCol)
      # If the current value occurred once and only once in
      # the current column, then we have a place where the current
      # value can be placed
      if countCol == 1:
        curTuple = (curCell, value)
        # Scan the results list looking for a match. If the
        # current result has already been added, skip the 
        # current location.
        countRv = 0
        for result in rv:
          # Get some information about the current result
          tempCell = result[0]
          tempRow = tempCell.rowPosition
          tempCol = tempCell.colPosition
          tempValue = result[1]
          # Check if the current result matches the result we just
          # found
          if tempRow == curCell.rowPosition and \
             tempCol == curCell.colPosition and \
             tempValue == value:
            countRv = countRv + 1
        # If no result matches were found, add the current location
        if countRv == 0:
          rv.append(curTuple)
    # Scan all of the boxes looking for a box where the 
    # current value has just one (and only one) possible
    # location.
    for box in range(glbBoxMin, glbBoxMax+1):
      countBox = 0
      for loc in locs:
        # Extract some values from the current tuple
        tempCell = loc[0]
        tempValue = loc[1]
        tempRow = tempCell.rowPosition
        tempCol = tempCell.colPosition
        tempBox = tempCell.boxPosition
        # Check if the current location is a possible location 
        # for the current box and current value
        if box != tempBox or \
           value != tempValue:
          continue
        countBox = countBox + 1 
        curCell = Cell(tempRow, tempCol)
      # If the current value occurred once and only once in
      # the current box, then we have a place where the current
      # value can be placed
      if countBox == 1:
        curTuple = (curCell, value)
        # Scan the results list looking for a match. If the
        # current result has already been added, skip the 
        # current location.
        countRv = 0
        for result in rv:
          # Get some information about the current result
          tempCell = result[0]
          tempRow = tempCell.rowPosition
          tempCol = tempCell.colPosition
          tempValue = result[1]
          # Check if the current result matches the result we just
          # found
          if tempRow == curCell.rowPosition and \
             tempCol == curCell.colPosition and \
             tempValue == value:
            countRv = countRv + 1
        # If no result matches were found, add the current location
        if countRv == 0:
          rv.append(curTuple)
  # Return the final list of locations where a value can be placed
  return rv

# Look for triples of values. A triple of values is something like 
# 1, 5, and 9 being allowed in exacty three places. One of the places
# must end up as a 1. A different place must end up with a 5 and the
# other place must end up as a 9. We don't know which is which, 
# but that doesn't matter for some purposes. If the 1, 5, and 9 are
# in the same box, then 1, 5, and 9 can not appear anywhere else in
# the same box. If the 1, 5, and 9 are on the same row, then the 1, 5,
# and 9 can not be anywhere else on the same row. If the 1, 5, and 9
# are in the same column, then the 1, 5, and 9 can not be anywhere
# else in the same column. 
def findTriplesValues(curBoard):
  tripleCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a row where the 
  # current value has just three (and only three) possible
  # locations.
  for row in range(glbRowMin, glbRowMax+1):
    # break
    tempCells = curBoard.getRow(row)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 3:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 3:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 != 3:
            continue
          # Make sure the cell lists match
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          if checkListsMatch(cells1, cells2, cells3) == False:
            continue
          # At this point we have a triple of values. We can now adjust
          # the allow and block lists for every cell in the unit.
          tripleCount += 1
          colIndex1 = cells1[0].colPosition - 1
          colIndex2 = cells1[1].colPosition - 1
          colIndex3 = cells1[2].colPosition - 1
          allowList = [value1, value2, value3]
          # Remove allows from the rest of the row
          cellsColIndexList = [colIndex1, colIndex2, colIndex3]
          removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list triple
          removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
          totalRemoveAllowsCount += removeCount
  # Scan all of the columns looking for a column where the 
  # current value has just three (and only three) possible
  # locations.
  for col in range(glbColMin, glbColMax+1):
    # break
    tempCells = curBoard.getCol(col)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 3:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 3:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 != 3:
            continue
          # Make sure the cell lists match
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          if checkListsMatch(cells1, cells2, cells3) == False:
            continue
          # At this point we have a triple of values. We can now adjust
          # the allow and block lists for every cell in the unit.
          tripleCount += 1
          rowIndex1 = cells1[0].rowPosition - 1
          rowIndex2 = cells1[1].rowPosition - 1
          rowIndex3 = cells1[2].rowPosition - 1
          allowList = [value1, value2, value3]
          # Remove allows from the rest of the column
          cellsColIndexList = [rowIndex1, rowIndex2, rowIndex3]
          removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list triple
          removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
          totalRemoveAllowsCount += removeCount
  # Scan all of the boxes looking for a box where the 
  # current value has just three (and only three) possible
  # locations. Boxes are scanned first because a triple 
  # inside a box may be on the same row or in the same
  # column. 
  for box in range(glbBoxMin, glbBoxMax+1):
    # break
    tempCells = curBoard.getBox(box)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 3:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 3:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 != 3:
            continue
          # Make sure the cell lists match
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          if checkListsMatch(cells1, cells2, cells3) == False:
            continue
          # At this point we have a triple of values. We can 
          # now adjust the allow and block lists for every 
          # cell in the unit.
          tripleCount += 1
          boxIndex1 = cells1[0].boxPosition - 1
          boxIndex2 = cells2[1].boxPosition - 1
          boxIndex3 = cells3[2].boxPosition - 1
          boxLocation1 = cells1[0].boxLocation - 1
          boxLocation2 = cells2[1].boxLocation - 1
          boxLocation3 = cells3[2].boxLocation - 1
          colIndex1 = cells1[0].colPosition - 1
          colIndex2 = cells2[1].colPosition - 1
          colIndex3 = cells3[2].colPosition - 1
          rowIndex1 = cells1[0].rowPosition - 1
          rowIndex2 = cells2[1].rowPosition - 1
          rowIndex3 = cells3[2].rowPosition - 1
          allowList = [value1, value2, value3]
          # Remove allows from the rest of the box
          cellBoxIndexList = [boxLocation1, boxLocation2, boxLocation3]
          removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellBoxIndexList) 
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list triple
          removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
          totalRemoveAllowsCount += removeCount
          # Store the list of possible values in each cell. For reasons
          # that I do not understand, this loop causes error later.
          for cell in cells1:
            break
            removeCount = len(cell.allowList)
            totalRemoveAllowsCount += removeCount
            cell.storeList(allowList)
          # We can now check if the hidden triple was in the same row.
          # If this is true, then the rest of the row can be adjusted
          # to remove the allowed values.
          if rowIndex1 == rowIndex2 and \
             rowIndex2 == rowIndex3:
            tempCellsRow = curBoard.getRow(rowIndex1+1)
            # Remove allows from the rest of the row
            cellsColIndexList = [colIndex1, colIndex2, colIndex3]
            removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellsColIndexList) 
            totalRemoveAllowsCount += removeCount
          # We can now check if the hidden triple was in the same column.
          # If this is true, then the rest of the column can be adjusted
          # to remove the allowed values.
          if colIndex1 == colIndex2 and \
             colIndex2 == colIndex3:
            tempCellsCol = curBoard.getCol(colIndex1+1)
            # Remove allows from the rest of the column
            cellsRowIndexList = [rowIndex1, rowIndex2, rwoIndex3]
            removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellsRowIndexList) 
            totalRemoveAllowsCount += removeCount
  # Return the final triple count and the number of allows that were
  # removed
  return [tripleCount, totalRemoveAllowsCount]

# Look for hidden pairs. We have a hidden pair if two (just 
# two) cells have two values that don't occur anywhere else.
def hiddenPairs(curBoard):
  pairCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a row where the 
  # current value has just two (and only two) possible
  # locations.
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = curBoard.getRow(row)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2:
          continue
        # Make sure the cell lists match
        cells1 = curTuple1[1]
        cells2 = curTuple2[1]
        if checkListsMatch(cells1, cells2) == False:
          continue
        # At this point we have a hidden pair. We can now adjust
        # the allow and block lists for every cell in the unit
        pairCount += 1
        colIndex1 = cells1[0].colPosition - 1
        colIndex2 = cells1[1].colPosition - 1
        allowList = [value1, value2]
        # Remove allows from the rest of the row
        cellsColIndexList = [colIndex1, colIndex2]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellsColIndexList) 
        totalRemoveAllowsCount += removeCount
        # Remove all other allows from the list pair
        removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
        totalRemoveAllowsCount += removeCount
        # Check if the two cells are in the same box
        if cells1[0].boxPosition == cells1[1].boxPosition:
          boxIndexList = [cells1[0].boxLocation-1, cells1[1].boxLocation-1]
          removeCount = removeAllowsBox(curBoard, cells1[0].boxPosition, allowList, boxIndexList)
          totalRemoveAllowsCount += removeCount 
  # Scan all of the columns looking for a column where the 
  # current value has just two (and only two) possible
  # locations.
  for col in range(glbColMin, glbColMax+1):
    tempCells = curBoard.getCol(col)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2:
          continue
        # Make sure the cell lists match
        cells1 = curTuple1[1]
        cells2 = curTuple2[1]
        if checkListsMatch(cells1, cells2) == False:
          continue
        # At this point we have a hidden pair. We can now adjust
        # the allow and block lists for every cell in the unit
        pairCount += 1
        rowIndex1 = cells1[0].rowPosition - 1
        rowIndex2 = cells1[1].rowPosition - 1
        allowList = [value1, value2]
        # Remove allows from the rest of the column
        cellsRowIndexList = [rowIndex1, rowIndex2]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellsRowIndexList) 
        totalRemoveAllowsCount += removeCount
        # Remove all other allows from the list pair
        removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
        totalRemoveAllowsCount += removeCount
        # Check if the two cells are in the same box
        if cells1[0].boxPosition == cells1[1].boxPosition:
          boxIndexList = [cells1[0].boxLocation-1, cells1[1].boxLocation-1]
          removeCount = removeAllowsBox(curBoard, cells1[0].boxPosition, allowList, boxIndexList)
          totalRemoveAllowsCount += removeCount
  # Scan all of the boxes looking for a box where the 
  # current value has just two (and only two) possible
  # location.
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = curBoard.getBox(box)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2:
          continue
        # Make sure the cell lists match
        cells1 = curTuple1[1]
        cells2 = curTuple2[1]
        if checkListsMatch(cells1, cells2) == False:
          continue
        # At this point we have a hidden pair. We can now adjust
        # the allow and block lists for every cell in the unit
        pairCount += 1
        boxIndex1 = cells1[0].boxPosition - 1
        boxIndex2 = cells2[1].boxPosition - 1
        colIndex1 = cells1[0].colPosition - 1
        colIndex2 = cells2[1].colPosition - 1
        rowIndex1 = cells1[0].rowPosition - 1
        rowIndex2 = cells2[1].rowPosition - 1
        index1 = (rowIndex1 % 3) * 3 + (colIndex1 % 3)
        index2 = (rowIndex2 % 3) * 3 + (colIndex2 % 3)
        allowList = [value1, value2]
        # Remove allows from the rest of the box
        cellIndexList = [index1, index2]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellIndexList) 
        totalRemoveAllowsCount += removeCount
        # Remove all other allows from the list pair
        removeCount = removeOtherAllowedValuesFromCells(cells1, allowList)
        totalRemoveAllowsCount += removeCount
        # We can now check if the hidden pair was in the same row.
        # If this is true, then the rest of the row can be adjusted
        # to remove the allowed values.
        if rowIndex1 == rowIndex2:
          tempCellsRow = curBoard.getRow(rowIndex1+1)
          # Remove allows from the rest of the row
          cellsColIndexList = [colIndex1, colIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
        # We can now check if the hidden pair was in the same column.
        # If this is true, then the rest of the column can be adjusted
        # to remove the allowed values.
        if colIndex1 == colIndex2:
          tempCellsCol = curBoard.getCol(colIndex1+1)
          # Remove allows from the rest of the column
          cellsRowIndexList = [rowIndex1, rowIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellsRowIndexList) 
          totalRemoveAllowsCount += removeCount
  # Return the final pair count and the number of allows that were
  # removed
  return [pairCount, totalRemoveAllowsCount]

# This routine looks for triples of locations where the same 
# values are allowed. This routine does not actually return
# any locations. However, it does (in some cases) modify 
# other locations by adding to the block(ed) list and 
# removing values from the allowed list. This routine 
# does return the number of triple counts that were found.
def hiddenTriples(copyBoard):
  tripleCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a triple of cells that 
  # have the correct allowed list
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2 and \
         count1 != 3:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2 and \
           count2 != 3:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 != 2 and \
             count3 != 3:
            continue
          # We now merge the cell lists for each of the values.
          # The merged list must have exactly three cells.
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          # Merge the cell lists and make sure we have exactly 
          # three cells
          cellsMergeList = cellMergeList(cells1, cells2, cells3)
          if len(cellsMergeList) != 3:
            continue
          # Increment the number of triples found
          tripleCount += 1  
          tripleList = [value1, value2, value3]
          # Remove all of the allowed values from the rest of the row
          tempCell1 = cellsMergeList[0]
          tempCell2 = cellsMergeList[1]
          tempCell3 = cellsMergeList[2]
          colIndex1 = tempCell1.colPosition - 1
          colIndex2 = tempCell2.colPosition - 1
          colIndex3 = tempCell3.colPosition - 1
          cellsIndexList = [colIndex1, colIndex2, colIndex3]
          removeCount = removeAllowsExcludingListCells(tempCells, tripleList, cellsIndexList)
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list triple
          removeCount = removeOtherAllowedValuesFromCells(cellsMergeList, tripleList)
          totalRemoveAllowsCount += removeCount
          # Check if the three cells are in the same box
          if tempCell1.boxPosition == tempCell2.boxPosition and \
             tempCell2.boxPosition == tempCell3.boxPosition:
            boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, tempCell3.boxLocation-1]
            removeCount = removeAllowsBox(copyBoard, cells1[0].boxPosition, tripleList, boxIndexList)
            totalRemoveAllowsCount += removeCount
  # Scan all of the columns looking for a triple of cells that 
  # have the correct allowed list
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2 and \
         count1 != 3:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2 and \
           count2 != 3:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 != 2 and \
             count3 != 3:
            continue
          # We now merge the cell lists for each of the values.
          # The merged list must have exactly three cells.
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          # Merge the cell lists and make sure we have exactly 
          # three cells
          cellsMergeList = cellMergeList(cells1, cells2, cells3)
          if len(cellsMergeList) != 3:
            continue
          # Increment the number of triples found
          tripleCount += 1  
          tripleList = [value1, value2, value3]
          # Remove all of the allowed values from the rest of the column
          tempCell1 = cellsMergeList[0]
          tempCell2 = cellsMergeList[1]
          tempCell3 = cellsMergeList[2]
          rowIndex1 = tempCell1.rowPosition - 1
          rowIndex2 = tempCell2.rowPosition - 1
          rowIndex3 = tempCell3.rowPosition - 1
          cellsIndexList = [rowIndex1, rowIndex2, rowIndex3]
          removeCount = removeAllowsExcludingListCells(tempCells, tripleList, cellsIndexList)
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list triple
          removeCount = removeOtherAllowedValuesFromCells(cellsMergeList, tripleList)
          totalRemoveAllowsCount += removeCount
          # Check if the three cells are in the same box
          if tempCell1.boxPosition == tempCell2.boxPosition and \
             tempCell2.boxPosition == tempCell3.boxPosition:
            boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, tempCell3.boxLocation-1]
            removeCount = removeAllowsBox(copyBoard, cells1[0].boxPosition, tripleList, boxIndexList)
            totalRemoveAllowsCount += removeCount
  # Scan all of the boxes looking for a triple of cells that 
  # have the correct allowed list
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 != 2 and \
         count1 != 3:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 != 2 and \
           count2 != 3:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 != 2 and \
             count3 != 3:
            continue
          # We now merge the cell lists for each of the values.
          # The merged list must have exactly three cells.
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          # Merge the cell lists and make sure we have exactly 
          # three cells
          cellsMergeList = cellMergeList(cells1, cells2, cells3)
          if len(cellsMergeList) != 3:
            continue
          # Increment the number of triples found
          tripleCount += 1  
          tripleList = [value1, value2, value3]
          # Remove all of the allowed values from the rest of the box
          tempCell1 = cellsMergeList[0]
          tempCell2 = cellsMergeList[1]
          tempCell3 = cellsMergeList[2]
          rowIndex1 = tempCell1.rowPosition - 1
          rowIndex2 = tempCell2.rowPosition - 1
          rowIndex3 = tempCell3.rowPosition - 1
          colIndex1 = tempCell1.colPosition - 1
          colIndex2 = tempCell2.colPosition - 1
          colIndex3 = tempCell3.colPosition - 1
          boxLocIndex1 = tempCell1.boxLocation - 1
          boxLocIndex2 = tempCell2.boxLocation - 1
          boxLocIndex3 = tempCell3.boxLocation - 1
          cellsIndexList = [boxLocIndex1, boxLocIndex2, boxLocIndex3]
          removeCount = removeAllowsExcludingListCells(tempCells, tripleList, cellsIndexList)
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list triple
          removeCount = removeOtherAllowedValuesFromCells(cellsMergeList, tripleList)
          totalRemoveAllowsCount += removeCount   
          # We can now check if the row positions match. If this
          # is true, then the rest of the row can be adjusted to
          # remove the allowed values.
          if rowIndex1 == rowIndex2 and \
             rowIndex2 == rowIndex3:
            tempCellsRow = copyBoard.getRow(rowIndex1+1)
            cellsColIndexList = [colIndex1, colIndex2, colIndex3]
            removeCount = removeAllowsExcludingListCells(tempCellsRow, tripleList, cellsColIndexList) 
            totalRemoveAllowsCount += removeCount
          # We can now check if the column positions match. If this
          # is true, then the rest of the column can be adjusted to 
          # remove the allowed values.
          if colIndex1 == colIndex2 and \
             colIndex2 == colIndex3:
            tempCellsCol = copyBoard.getCol(colIndex1+1)
            cellsRowIndexList = [rowIndex1, rowIndex2, rowIndex3]
            removeCount = removeAllowsExcludingListCells(tempCellsCol, tripleList, cellsRowIndexList)  
            totalRemoveAllowsCount += removeCount
  # Return the final triple count and the number of allows that were
  # removed
  return [tripleCount, totalRemoveAllowsCount]

# This routine looks for triples of locations where the same 
# values are allowed. This routine does not actually return
# any locations. However, it does (in some cases) modify 
# other locations by adding to the block(ed) list and 
# removing values from the allowed list. This routine 
# does return the number of triple counts that were found.
def hiddenTriplesOld(copyBoard):
  tripleCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a triple of cells that 
  # have the correct allowed list
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    index1 = 0
    while index1 < glbColMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbColMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbColMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          cellsList = [tempCell1, tempCell2, tempCell3]
          # Merge the allowed value(s) lists
          allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3)
          allowedListMergeLen = len(allowedListMerge)
          # Check all of the allowed values
          for index4 in range(0, allowedListMergeLen):
            value4 = allowedListMerge[index4]
            curTuple4 = countAllowedList(cellsList, value4)
            count4 = curTuple4[0]
            # Check if the current value appeared two or three times
            # in the cell list
            if count4 != 2 and \
               count4 != 3: 
              continue
            # Check all of the allowed values
            for index5 in range(index4+1, allowedListMergeLen):
              value5 = allowedListMerge[index5]
              curTuple5 = countAllowedList(cellsList, value5)
              count5 = curTuple5[0]
              # Check if the current value appeared two or three times
              # in the cell list
              if count5 != 2 and \
                 count5 != 3: 
                continue
              # Check all of the allowed values
              for index6 in range(index5+1, allowedListMergeLen):
                value6 = allowedListMerge[index6]
                curTuple6 = countAllowedList(cellsList, value6)
                count6 = curTuple6[0]
                # Check if the current value appeared two or three times
                # in the cell list
                if count6 != 2 and \
                   count6 != 3: 
                  continue 
                tripleList = [value4, value5, value6]
                # At this point we need to make sure that every cell has
                # two or three of the triple values 
                if checkCellListAllowed(cellsList, tripleList) == False:
                  continue
                # Check if any of the allowed values appear outside of the three cells
                # we have found so far
                if checkValuesSkipList(tempCells, tripleList, cellsList) == False:
                  continue
                # Increment the number of triples
                tripleCount += 1  
                # Remove all of the allowed values from the rest of the row
                cellIndexList = [index1-1, index2-1, index3-1]
                removeCount = removeAllowsExcludingListCells(tempCells, tripleList, cellIndexList)
                totalRemoveAllowsCount += removeCount
                # Remove all other allows from the list triple
                removeCount = removeOtherAllowedValuesFromCells(cellsList, tripleList)
                totalRemoveAllowsCount += removeCount
                # Check if the three cells are in the same box
                if tempCell1.boxPosition == tempCell2.boxPosition and \
                   tempCell2.boxPosition == tempCell3.boxPosition:
                  boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, tempCell3.boxLocation-1]
                  removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, tripleList, boxIndexList)
                  totalRemoveAllowsCount += removeCount  
  # Scan all of the columns looking for a triple of cells that 
  # have the correct allowed list
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    index1 = 0
    while index1 < glbRowMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbRowMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbRowMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          cellsList = [tempCell1, tempCell2, tempCell3]
          # Merge the allowed value(s) lists
          allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3)
          allowedListMergeLen = len(allowedListMerge)
          # Check all of the allowed values
          for index4 in range(0, allowedListMergeLen):
            value4 = allowedListMerge[index4]
            curTuple4 = countAllowedList(cellsList, value4)
            count4 = curTuple4[0]
            # Check if the current value appeared two or three times
            # in the cell list
            if count4 != 2 and \
               count4 != 3: 
              continue
            # Check all of the allowed values
            for index5 in range(index4+1, allowedListMergeLen):
              value5 = allowedListMerge[index5]
              curTuple5 = countAllowedList(cellsList, value5)
              count5 = curTuple5[0]
              # Check if the current value appeared two or three times
              # in the cell list
              if count5 != 2 and \
                 count5 != 3: 
                continue
              # Check all of the allowed values
              for index6 in range(index5+1, allowedListMergeLen):
                value6 = allowedListMerge[index6]
                curTuple6 = countAllowedList(cellsList, value6)
                count6 = curTuple6[0]
                # Check if the current value appeared two or three times
                # in the cell list
                if count6 != 2 and \
                   count6 != 3: 
                  continue 
                tripleList = [value4, value5, value6]
                # At this point we need to make sure that every cell has
                # two or three of the triple values 
                if checkCellListAllowed(cellsList, tripleList) == False:
                  continue
                # Check if any of the allowed values appear outside of the three cells
                # we have found so far
                if checkValuesSkipList(tempCells, tripleList, cellsList) == False:
                  continue
                # Increment the number of triples
                tripleCount += 1  
                # Remove all of the allowed values from the rest of the row
                cellIndexList = [index1-1, index2-1, index3-1]
                removeCount = removeAllowsExcludingListCells(tempCells, tripleList, cellIndexList)
                totalRemoveAllowsCount += removeCount
                # Remove all other allows from the list triple
                removeCount = removeOtherAllowedValuesFromCells(cellsList, tripleList)
                totalRemoveAllowsCount += removeCount
                # Check if the three cells are in the same box
                if tempCell1.boxPosition == tempCell2.boxPosition and \
                   tempCell2.boxPosition == tempCell3.boxPosition:
                  boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, tempCell3.boxLocation-1]
                  removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, tripleList, boxIndexList)
                  totalRemoveAllowsCount += removeCount 
  # Scan all of the boxes looking for a triple of cells that 
  # have the correct allowed list
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    index1 = 0
    while index1 < glbBoxMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbBoxMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbBoxMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          cellsList = [tempCell1, tempCell2, tempCell3]
          # Merge the allowed value(s) lists
          allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3)
          allowedListMerge.sort()
          allowedListMergeLen = len(allowedListMerge)
          # Check all of the allowed values
          for index4 in range(0, allowedListMergeLen):
            value4 = allowedListMerge[index4]
            curTuple4 = countAllowedList(cellsList, value4)
            count4 = curTuple4[0]
            # Check if the current value appeared two or three times
            # in the cell list
            if count4 != 1 and \
               count4 != 2 and \
               count4 != 3: 
              continue
            # Check all of the allowed values
            for index5 in range(index4+1, allowedListMergeLen):
              value5 = allowedListMerge[index5]
              curTuple5 = countAllowedList(cellsList, value5)
              count5 = curTuple5[0]
              # Check if the current value appeared two or three times
              # in the cell list
              if count5 != 1 and \
                 count5 != 2 and \
                 count5 != 3: 
                continue
              # Check all of the allowed values
              for index6 in range(index5+1, allowedListMergeLen):
                value6 = allowedListMerge[index6]
                curTuple6 = countAllowedList(cellsList, value6)
                count6 = curTuple6[0]
                # Check if the current value appeared two or three times
                # in the cell list
                if count6 != 1 and \
                   count6 != 2 and \
                   count6 != 3: 
                  continue 
                tripleList = [value4, value5, value6]
                # At this point we need to make sure that every cell has
                # two or three of the triple values 
                if checkCellListAllowed(cellsList, tripleList) == False:
                  continue
                # Check if any of the allowed values appear outside of the three cells
                # we have found so far
                if checkValuesSkipList(tempCells, tripleList, cellsList) == False:
                  continue
                # Increment the number of triples
                tripleCount += 1  
                # Remove all of the allowed values from the rest of the box
                cellIndexList = [index1-1, index2-1, index3-1]
                removeCount = removeAllowsExcludingListCells(tempCells, tripleList, cellIndexList)
                totalRemoveAllowsCount += removeCount
                # Remove all other allows from the list triple
                removeCount = removeOtherAllowedValuesFromCells(cellsList, tripleList)
                totalRemoveAllowsCount += removeCount
                # All of the current cells may be in exactly one row or exactly one column 
                boxIndex1 = tempCell1.boxPosition - 1
                boxIndex2 = tempCell2.boxPosition - 1
                boxIndex3 = tempCell3.boxPosition - 1
                colIndex1 = tempCell1.colPosition - 1
                colIndex2 = tempCell2.colPosition - 1
                colIndex3 = tempCell3.colPosition - 1
                rowIndex1 = tempCell1.rowPosition - 1
                rowIndex2 = tempCell2.rowPosition - 1
                rowIndex3 = tempCell3.rowPosition - 1 
                # We can now check if the row positions match. If this
                # is true, then the rest of the row can be adjusted to
                # remove the allowed values.
                if rowIndex1 == rowIndex2 and \
                   rowIndex2 == rowIndex3:
                  tempCellsRow = copyBoard.getRow(rowIndex1+1)
                  cellsColIndexList = [colIndex1, colIndex2, colIndex3]
                  removeCount = removeAllowsExcludingListCells(tempCellsRow, tripleList, cellsColIndexList) 
                  totalRemoveAllowsCount += removeCount
                # We can now check if the column positions match. If this
                # is true, then the rest of the column can be adjusted to 
                # remove the allowed values.
                if colIndex1 == colIndex2 and \
                   colIndex2 == colIndex3:
                  tempCellsCol = copyBoard.getCol(colIndex1+1)
                  cellsRowIndexList = [rowIndex1, rowIndex2, rowIndex3]
                  removeCount = removeAllowsExcludingListCells(tempCellsCol, tripleList, cellsRowIndexList)  
                  totalRemoveAllowsCount += removeCount
  # Return the final triple count and the number of allows that were
  # removed
  return [tripleCount, totalRemoveAllowsCount]

# This routine looks for quads of locations where the same 
# values are allowed. This routine does not actually return
# any locations. However, it does (in some cases) modify 
# other locations by adding to the block(ed) list and 
# removing values from the allowed list. This routine 
# does return the number of quad counts that were found.
def hiddenQuads(copyBoard):
  quadCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a quad of cells that 
  # have the correct allowed list
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 < 2 or \
         count1 > 4:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 < 2 or \
           count2 > 4:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 < 2 or \
             count3 > 4:
            continue
          for value4 in range(value3+1, glbValueMax+1):
            curTuple4 = countAllowed(tempCells, value4)
            count4 = curTuple4[0]
            if count4 < 2 or \
               count4 > 4:
              continue
            # We now merge the cell lists for each of the values.
            # The merged list must have exactly four cells.
            cells1 = curTuple1[1]
            cells2 = curTuple2[1]
            cells3 = curTuple3[1]
            cells4 = curTuple4[1]
            # Merge the cell lists and make sure we have exactly 
            # four cells
            cellsMergeList = cellMergeList(cells1, cells2, cells3, cells4)
            if len(cellsMergeList) != 4:
              continue
            # Increment the number of quads found
            quadCount += 1  
            quadList = [value1, value2, value3, value4]
            # Remove all of the allowed values from the rest of the row
            tempCell1 = cellsMergeList[0]
            tempCell2 = cellsMergeList[1]
            tempCell3 = cellsMergeList[2]
            tempCell4 = cellsMergeList[3]
            colIndex1 = tempCell1.colPosition - 1
            colIndex2 = tempCell2.colPosition - 1
            colIndex3 = tempCell3.colPosition - 1
            colIndex4 = tempCell4.colPosition - 1
            cellsIndexList = [colIndex1, colIndex2, colIndex3, colIndex4]
            removeCount = removeAllowsExcludingListCells(tempCells, quadList, cellsIndexList)
            totalRemoveAllowsCount += removeCount
            # Remove all other allows from the list quad
            removeCount = removeOtherAllowedValuesFromCells(cellsMergeList, quadList)
            totalRemoveAllowsCount += removeCount
            # Check if the four cells are in the same box
            if tempCell1.boxPosition == tempCell2.boxPosition and \
               tempCell2.boxPosition == tempCell3.boxPosition and \
               tempCell3.boxPosition == tempCell4.boxPosition:
              boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, \
                              tempCell3.boxLocation-1, tempCell4.boxLocation-1]
              removeCount = removeAllowsBox(curBoard, cells1[0].boxPosition, quadList, boxIndexList)
              totalRemoveAllowsCount += removeCount
  # Scan all of the columns looking for a quad of cells that 
  # have the correct allowed list
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 < 2 or \
         count1 > 4:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 < 2 or \
           count2 > 4:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 < 2 or \
             count3 > 4:
            continue
          for value4 in range(value3+1, glbValueMax+1):
            curTuple4 = countAllowed(tempCells, value4)
            count4 = curTuple4[0]
            if count4 < 2 or \
               count4 > 4:
              continue
          # We now merge the cell lists for each of the values.
          # The merged list must have exactly four cells.
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          cells4 = curTuple4[1]
          # Merge the cell lists and make sure we have exactly 
          # four cells
          cellsMergeList = cellMergeList(cells1, cells2, cells3, cells4)
          if len(cellsMergeList) != 4:
            continue
          # Increment the number of quads found
          quadCount += 1  
          quadList = [value1, value2, value3, value4]
          # Remove all of the allowed values from the rest of the column
          tempCell1 = cellsMergeList[0]
          tempCell2 = cellsMergeList[1]
          tempCell3 = cellsMergeList[2]
          tempCell4 = cellsMergeList[3]
          rowIndex1 = tempCell1.rowPosition - 1
          rowIndex2 = tempCell2.rowPosition - 1
          rowIndex3 = tempCell3.rowPosition - 1
          rowIndex4 = tempCell4.rowPosition - 1
          cellsIndexList = [rowIndex1, rowIndex2, rowIndex3, rowIndex4]
          removeCount = removeAllowsExcludingListCells(tempCells, quadList, cellsIndexList)
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list quad
          removeCount = removeOtherAllowedValuesFromCells(cellsMergeList, quadList)
          totalRemoveAllowsCount += removeCount
          # Check if the four cells are in the same box
          if tempCell1.boxPosition == tempCell2.boxPosition and \
             tempCell2.boxPosition == tempCell3.boxPosition and \
             tempCell3.boxPosition == tempCell4.boxPosition:
            boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, \
                            tempCell3.boxLocation-1, tempCell4.boxLocation-1]
            removeCount = removeAllowsBox(curBoard, cells1[0].boxPosition, quadList, boxIndexList)
            totalRemoveAllowsCount += removeCount
  # Scan all of the boxes looking for a quad of cells that 
  # have the correct allowed list
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    # Check all of the possible values
    for value1 in range(glbValueMin, glbValueMax+1):
      curTuple1 = countAllowed(tempCells, value1)
      count1 = curTuple1[0]
      if count1 < 2 or \
         count1 > 4:
        continue
      for value2 in range(value1+1, glbValueMax+1):
        curTuple2 = countAllowed(tempCells, value2)
        count2 = curTuple2[0]
        if count2 < 2 or \
           count2 > 4:
          continue
        for value3 in range(value2+1, glbValueMax+1):
          curTuple3 = countAllowed(tempCells, value3)
          count3 = curTuple3[0]
          if count3 < 2 or \
             count3 > 4:
            continue
          for value4 in range(value3+1, glbValueMax+1):
            curTuple4 = countAllowed(tempCells, value4)
            count4 = curTuple4[0]
            if count4 < 2 or \
               count4 > 4:
              continue
          # We now merge the cell lists for each of the values.
          # The merged list must have exactly four cells.
          cells1 = curTuple1[1]
          cells2 = curTuple2[1]
          cells3 = curTuple3[1]
          cells4 = curTuple4[1]
          # Merge the cell lists and make sure we have exactly 
          # four cells
          cellsMergeList = cellMergeList(cells1, cells2, cells3, cells4)
          if len(cellsMergeList) != 4:
            continue
          # Increment the number of quads found
          quadCount += 1  
          quadList = [value1, value2, value3, value4]
          # Remove all of the allowed values from the rest of the box
          tempCell1 = cellsMergeList[0]
          tempCell2 = cellsMergeList[1]
          tempCell3 = cellsMergeList[2]
          tempCell4 = cellsMergeList[3]
          rowIndex1 = tempCell1.rowPosition - 1
          rowIndex2 = tempCell2.rowPosition - 1
          rowIndex3 = tempCell3.rowPosition - 1
          rowIndex4 = tempCell4.rowPosition - 1
          colIndex1 = tempCell1.colPosition - 1
          colIndex2 = tempCell2.colPosition - 1
          colIndex3 = tempCell3.colPosition - 1
          colIndex4 = tempCell4.colPosition - 1
          boxLocIndex1 = tempCell1.boxLocation - 1
          boxLocIndex2 = tempCell2.boxLocation - 1
          boxLocIndex3 = tempCell3.boxLocation - 1
          boxLocIndex4 = tempCell4.boxLocation - 1
          cellsIndexList = [boxLocIndex1, boxLocIndex2, boxLocIndex3, boxLocIndex4]
          removeCount = removeAllowsExcludingListCells(tempCells, quadList, cellsIndexList)
          totalRemoveAllowsCount += removeCount
          # Remove all other allows from the list quad
          removeCount = removeOtherAllowedValuesFromCells(cellsMergeList, quadList)
          totalRemoveAllowsCount += removeCount   
          # We can now check if the row positions match. If this
          # is true, then the rest of the row can be adjusted to
          # remove the allowed values.
          if rowIndex1 == rowIndex2 and \
             rowIndex2 == rowIndex3 and \
             rowIndex3 == rowIndex4:
            tempCellsRow = copyBoard.getRow(rowIndex1+1)
            cellsColIndexList = [colIndex1, colIndex2, colIndex3, colIndex4]
            removeCount = removeAllowsExcludingListCells(tempCellsRow, quadList, cellsColIndexList) 
            totalRemoveAllowsCount += removeCount
          # We can now check if the column positions match. If this
          # is true, then the rest of the column can be adjusted to 
          # remove the allowed values.
          if colIndex1 == colIndex2 and \
             colIndex2 == colIndex3 and \
             colIndex3 == colIndex4:
            tempCellsCol = copyBoard.getCol(colIndex1+1)
            cellsRowIndexList = [rowIndex1, rowIndex2, rowIndex3, rowIndex4]
            removeCount = removeAllowsExcludingListCells(tempCellsCol, quadList, cellsrowIndexList)  
            totalRemoveAllowsCount += removeCount
  # Return the final quad count and the number of allows that were
  # removed
  return [quadCount, totalRemoveAllowsCount]

# Find a location where a single value can/must be placed. 
# This routine searches for cells where all but one potential
# value has been blocked. 
def lastPossibleNumber(curBoard):
  rv = []
  valueMaxM1 = glbValueMax - 1
  # Process all of the cell in the board
  for curCell in curBoard.cells:
    # Check if the current cell has a value or a list of possible
    # values. If the current cell has been set to one specific value
    # or the current cell has a list of possible values, we can just
    # ignore it.
    if isinstance(curCell.value, (int, list)) == True:
      continue 
    # Check the length of the block list. If the block
    # list is the wrong length, then we have no more work 
    # to do here on the current cell. If the length of the
    # block list is exactly equal to the total number 
    # of values minus 1, then the one missing value
    # must go in this cell / location.
    if len(curCell.blockList) != valueMaxM1:
      continue
    singleValue = curCell.allowList[0]
    # Build a tuple with the current cell and value
    curTuple = (curCell, singleValue)
    rv.append(curTuple)
    # Return to the caller with the first location
    return rv
  # Return to the caller with the (empty) list of
  # locations
  return rv 

# This routine looks for a location where a value can be
# placed. An acceptable location (in this routine) will
# be the only place in a row, column, or box where 
# the value can be placed. This is sometimes called
# the hidden single algoritm.
def lastRemainingCellInUnit(copyBoard):
  rv = []
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):
    # Scan all of the rows looking for a column where the 
    # current value has just one (and only one) possible
    # location.
    for row in range(glbRowMin, glbRowMax+1):
      tempCells = copyBoard.getRow(row)
      outTuple = countAllowed(tempCells, value)
      countRow = outTuple[0]
      if countRow > 0:
        curCell = outTuple[1][0]      
      # If the current value occurred once and only once in
      # the current row, then we have a place where the current
      # value can be placed
      if countRow == 1:
        curTuple = (curCell, value)
        # If no result matches were found, add the current location
        if checkForDuplicates(rv, curCell, value) == False:
          rv.append(curTuple)
          return rv
    # Scan all of the columns looking for a row where the 
    # current value has just one (and only one) possible
    # location.
    for col in range(glbColMin, glbColMax+1):
      tempCells = copyBoard.getCol(col)
      outTuple = countAllowed(tempCells, value)
      countCol = outTuple[0]
      if countCol > 0:
        curCell = outTuple[1][0]      
      # If the current value occurred once and only once in
      # the current column, then we have a place where the current
      # value can be placed
      if countCol == 1:
        curTuple = (curCell, value)
        # If no result matches were found, add the current location
        if checkForDuplicates(rv, curCell, value) == False:
          rv.append(curTuple)
          return rv
    # Scan all of the boxes looking for a box where the 
    # current value has just one (and only one) possible
    # location.
    for box in range(glbBoxMin, glbBoxMax+1):
      tempCells = copyBoard.getBox(box)
      outTuple = countAllowed(tempCells, value)
      countBox = outTuple[0]
      if countBox > 0:
        curCell = outTuple[1][0]      
      # If the current value occurred once and only once
      # in the current box, then we have a place where the 
      # current value can be placed
      if countBox == 1:
        curTuple = (curCell, value)
        # If no result matches were found, add the current location
        if checkForDuplicates(rv, curCell, value) == False:
          rv.append(curTuple)    
          return rv
  # Return the final list (presumably empty) of locations 
  # where a value can be placed
  return rv

# Merge the allowed lists for a set of cells
def mergeAllowedLists(*args):
  rv = []
  # Process all of the cells
  for arg in args:
    for allowedValue in arg.allowList:  
      if allowedValue not in rv:
        rv.append(allowedValue)
  return rv

# This routine looks for pairs of locations where the same 
# values are allowed. This routine does not actually return
# any locations. However, it does (in some cases) modify 
# other locations by adding to the block(ed) list and 
# removing values from the allow(ed) list. This routine 
# does return the number of pair counts that were found.
def nakedPairs(copyBoard):
  pairCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a pair of cells that 
  # have the same allowed list 
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    index1 = 0
    while index1 < glbColMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2: 
        continue
      # Scan all of the other cells looking for a matching 
      # allow list
      index2 = index1 
      while index2 < glbColMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2: 
          continue
        # Check if the allow lists match
        if checkListsMatch(tempCell1.allowList, tempCell2.allowList) == False:
          continue
        # At this point we have a naked pair. We can now adjust
        # the allow and block lists for every cell in the unit
        pairCount += 1
        allowList = tempCell1.allowList
        # Remove allows from the rest of the row
        cellIndexList = [index1-1, index2-1]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellIndexList)  
        totalRemoveAllowsCount += removeCount
        # Check if the two cells are in the same box
        if tempCell1.boxPosition == tempCell2.boxPosition:
          boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1]
          removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, allowList, boxIndexList)
          totalRemoveAllowsCount += removeCount    
  # Scan all of the columns looking for a pair of cells that 
  # have the same allowed list 
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    index1 = 0
    while index1 < glbRowMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2: 
        continue
      # Scan all of the other cells looking for a matching 
      # allow list
      index2 = index1 
      while index2 < glbRowMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2: 
          continue
        # Check if the allow lists match
        if checkListsMatch(tempCell1.allowList, tempCell2.allowList) == False:
          continue
        # At this point we have a naked pair. We can now adjust
        # the allow and block lists for every cell in the unit
        pairCount += 1
        allowList = tempCell1.allowList
        # Remove allows from the rest of the column
        cellIndexList = [index1-1, index2-1]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellIndexList)  
        totalRemoveAllowsCount += removeCount
        # Check if the two cells are in the same box
        if tempCell1.boxPosition == tempCell2.boxPosition:
          boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1]
          removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, allowList, boxIndexList)
          totalRemoveAllowsCount += removeCount 
  # Scan all of the boxes looking for a pair of cells that 
  # have the same allowed list 
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    index1 = 0
    while index1 < glbRowMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2: 
        continue
      # Scan all of the other cells looking for a matching 
      # allow list
      index2 = index1 
      while index2 < glbRowMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2: 
          continue
        # Check if the allow lists match
        if checkListsMatch(tempCell1.allowList, tempCell2.allowList) == False:
          continue
        # At this point we have a naked pair. We can now adjust
        # the allow and block lists for every cell in the unit
        pairCount += 1
        allowList = tempCell1.allowList
        # Remove allows from the rest of the box
        cellIndexList = [index1-1, index2-1]
        removeCount = removeAllowsExcludingListCells(tempCells, allowList, cellIndexList)  
        totalRemoveAllowsCount += removeCount
        # The two cells may be in the same row or column. We can now process
        # the rest of the row or column.
        boxIndex1 = tempCell1.boxPosition - 1
        boxIndex2 = tempCell2.boxPosition - 1
        colIndex1 = tempCell1.colPosition - 1
        colIndex2 = tempCell2.colPosition - 1
        rowIndex1 = tempCell1.rowPosition - 1
        rowIndex2 = tempCell2.rowPosition - 1
        # We can now check if the hidden pair was in the same row.
        # If this is true, then the rest of the row can be adjusted
        # to remove the allowed values.
        if rowIndex1 == rowIndex2:
          tempCellsRow = copyBoard.getRow(rowIndex1+1)
          # Remove allows from the rest of the row
          cellsColIndexList = [colIndex1, colIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
        # We can now check if the hidden pair was in the same column.
        # If this is true, then the rest of the column can be adjusted
        # to remove the allowed values.
        if colIndex1 == colIndex2:
          tempCellsCol = copyBoard.getCol(colIndex1+1)
          # Remove allows from the rest of the column
          cellsRowIndexList = [rowIndex1, rowIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellsRowIndexList)  
          totalRemoveAllowsCount += removeCount
  # Return the final pair count and the number of allows that were
  # removed
  return [pairCount, totalRemoveAllowsCount]

# This routine looks for locations (specific cells) in
# a unit where only one value can be placed. Since only
# one value is allowed, the one value must be correct. 
def nakedSingles(copyBoard):
  rv = []
  # Scan all of the rows looking for cells that can have
  # only one value 
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    for tempCell in tempCells:
      # Check if only one value is allowed for the current
      # cell
      if len(tempCell.allowList) != 1: 
        continue
      # Extract some values from the current cell
      tempValue = tempCell.allowList[0]        
      tempRow = tempCell.rowPosition
      tempCol = tempCell.colPosition
      # Build a cell using the current row and column
      curCell = Cell(tempRow, tempCol)
      # Build a tuple with the current cell and value
      curTuple = (curCell, tempValue)
      # If no result matches were found, add the current location
      if checkForDuplicates(rv, curCell, tempValue) == False:
        rv.append(curTuple)
        return rv
  # Scan all of the columns looking for cells that can have
  # only one value 
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    for tempCell in tempCells:
    # Check if only one value is allowed for the current
      # cell
      if len(tempCell.allowList) != 1: 
        continue
      # Extract some values from the current cell
      tempValue = tempCell.allowList[0]       
      tempRow = tempCell.rowPosition
      tempCol = tempCell.colPosition
      # Build a cell using the current row and column
      curCell = Cell(tempRow, tempCol)
      # Build a tuple with the current cell and value
      curTuple = (curCell, tempValue)
      # If no result matches were found, add the current location
      if checkForDuplicates(rv, curCell, tempValue) == False:
        rv.append(curTuple)
        return rv
  # Scan all of the boxes looking for cells that can have
  # only one value 
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    for tempCell in tempCells:
      # Check if only one value is allowed for the current
      # cell
      if len(tempCell.allowList) != 1: 
        continue
      # Extract some values from the current cell
      tempValue = tempCell.allowList[0]      
      tempRow = tempCell.rowPosition
      tempCol = tempCell.colPosition
      # Build a cell using the current row and column
      curCell = Cell(tempRow, tempCol)
      # Build a tuple with the current cell and value
      curTuple = (curCell, tempValue)
      # If no result matches were found, add the current location
      if checkForDuplicates(rv, curCell, tempValue) == False:
        rv.append(curTuple)
        return rv
  # Return the final list (presumable empty) of locations 
  # where a value can be placed
  return rv

# This routine looks for triples of locations where the same 
# values are allowed. This routine does not actually return
# any locations. However, it does (in some cases) modify 
# other locations by adding to the block(ed) list and 
# removing values from the allowed list. This routine 
# does return the number of triple counts that were found.
def nakedTriples(copyBoard):
  tripleCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a triple of cells that 
  # have the correct allowed list
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    index1 = 0
    while index1 < glbColMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two or three values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2 and \
         len(tempCell1.allowList) != 3: 
        continue
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbColMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two or three values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2 and \
           len(tempCell2.allowList) != 3: 
          continue
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbColMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          # Check if only two or three values are allowed for the current
          # cell
          if len(tempCell3.allowList) != 2 and \
             len(tempCell3.allowList) != 3: 
            continue
          cellsList = [tempCell1, tempCell2, tempCell3]
          # indexList = [index1-1, index2-1, index3-1]
          # Merge the allowed value(s) lists
          allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3)
          if len(allowedListMerge) != 3:
            continue
          # Make sure that the allowed lists for each cell only 
          # contain allowed values
          if checkCellList(cellsList, allowedListMerge) == False:
            continue
          # Increment the number of triples
          tripleCount += 1
          # Remove all of the allowed values from the rest of the row
          cellIndexList = [index1-1, index2-1, index3-1]
          removeCount = removeAllowsExcludingListCells(tempCells, allowedListMerge, cellIndexList)
          totalRemoveAllowsCount += removeCount
          # Check if the three cells are in the same box
          if tempCell1.boxPosition == tempCell2.boxPosition and \
             tempCell2.boxPosition == tempCell3.boxPosition:
            boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, tempCell3.boxLocation-1]
            removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, allowedListMerge, boxIndexList)
            totalRemoveAllowsCount += removeCount  
  # Scan all of the columns 
  # looking for a triple of cells that 
  # have the correct allowed list
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    index1 = 0
    while index1 < glbRowMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two or three values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2 and \
         len(tempCell1.allowList) != 3: 
        continue
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbRowMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two or three values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2 and \
           len(tempCell2.allowList) != 3: 
          continue
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbRowMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          # Check if only two or three values are allowed for the current
          # cell
          if len(tempCell3.allowList) != 2 and \
             len(tempCell3.allowList) != 3: 
            continue
          cellsList = [tempCell1, tempCell2, tempCell3]
          # indexList = [index1-1, index2-1, index3-1]
          # Merge the allowed value(s) lists
          allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3)
          if len(allowedListMerge) != 3:
            continue
          # Make sure that the allowed lists for each cell only 
          # contain allowed values
          if checkCellList(cellsList, allowedListMerge) == False:
            continue
          # Increment the number of triples
          tripleCount += 1
          # Remove all of the allowed values from the rest of the column
          cellIndexList = [index1-1, index2-1, index3-1]
          removeCount = removeAllowsExcludingListCells(tempCells, allowedListMerge, cellIndexList)
          totalRemoveAllowsCount += removeCount
          # Check if the three cells are in the same box
          if tempCell1.boxPosition == tempCell2.boxPosition and \
             tempCell2.boxPosition == tempCell3.boxPosition:
            boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, tempCell3.boxLocation-1]
            removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, allowedListMerge, boxIndexList)
            totalRemoveAllowsCount += removeCount  
  # Scan all of the boxes looking for a triple of cells that 
  # have the correct allowed list
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    index1 = 0
    while index1 < glbBoxMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two or three values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2 and \
         len(tempCell1.allowList) != 3: 
        continue
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbBoxMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two or three values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2 and \
           len(tempCell2.allowList) != 3: 
          continue
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbBoxMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          # Check if only two or three values are allowed for the current
          # cell
          if len(tempCell3.allowList) != 2 and \
             len(tempCell3.allowList) != 3: 
            continue
          cellsList = [tempCell1, tempCell2, tempCell3]
          # indexList = [index1-1, index2-1, index3-1]
          # Merge the allowed value(s) lists
          allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3)
          if len(allowedListMerge) != 3:
            continue
          # Make sure that the allowed lists for each cell only 
          # contain allowed values
          if checkCellList(cellsList, allowedListMerge) == False:
            continue
          # Increment the number of triples
          tripleCount += 1
          # Remove all of the allowed values from the rest of the box
          cellIndexList = [index1-1, index2-1, index3-1]
          removeCount = removeAllowsExcludingListCells(tempCells, allowedListMerge, cellIndexList)   
          totalRemoveAllowsCount += removeCount
          # All of the current cells may be exactly one row or exactly one column 
          boxIndex1 = tempCell1.boxPosition - 1
          boxIndex2 = tempCell2.boxPosition - 1
          boxIndex3 = tempCell3.boxPosition - 1
          colIndex1 = tempCell1.colPosition - 1
          colIndex2 = tempCell2.colPosition - 1
          colIndex3 = tempCell3.colPosition - 1
          rowIndex1 = tempCell1.rowPosition - 1
          rowIndex2 = tempCell2.rowPosition - 1
          rowIndex3 = tempCell3.rowPosition - 1 
          # We can now check if the row positions match. If this
          # is true, then the rest of the row can be adjusted to
          # remove the allowed values.
          if rowIndex1 == rowIndex2 and \
             rowIndex2 == rowIndex3:
            tempCellsRow = copyBoard.getRow(rowIndex1+1)
            cellsColIndexList = [colIndex1, colIndex2, colIndex3]
            removeCount = removeAllowsExcludingListCells(tempCellsRow, allowedListMerge, cellsColIndexList) 
            totalRemoveAllowsCount += removeCount
          # We can now check if the column positions match. If this
          # is true, then the rest of the column can be adjusted to 
          # remove the allowed values.
          if colIndex1 == colIndex2 and \
             colIndex2 == colIndex3:
            tempCellsCol = copyBoard.getCol(colIndex1+1)
            cellsRowIndexList = [rowIndex1, rowIndex2, rowIndex3]
            removeCount = removeAllowsExcludingListCells(tempCellsCol, allowedListMerge, cellsRowIndexList)  
            totalRemoveAllowsCount += removeCount
  # Return the final triple count and the number of removed allows
  return [tripleCount, totalRemoveAllowsCount]

# This routine looks for quads of locations where the same 
# values are allowed. This routine does not actually return
# any locations. However, it does (in some cases) modify 
# other locations by adding to the block(ed) list and 
# removing values from the allowed list. This routine 
# does return the number of quad counts that were found.
def nakedQuads(copyBoard):
  quadCount = 0
  totalRemoveAllowsCount = 0
  # Scan all of the rows looking for a quad of cells that 
  # have the correct allowed list
  for row in range(glbRowMin, glbRowMax+1):
    tempCells = copyBoard.getRow(row)
    index1 = 0
    while index1 < glbRowMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two or three or four values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2 and \
         len(tempCell1.allowList) != 3 and \
         len(tempCell1.allowList) != 4: 
        continue
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbRowMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two or three or four values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2 and \
           len(tempCell2.allowList) != 3 and \
           len(tempCell2.allowList) != 4: 
          continue
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbRowMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          # Check if only two or three or four values are allowed for the current
          # cell
          if len(tempCell3.allowList) != 2 and \
             len(tempCell3.allowList) != 3 and \
             len(tempCell3.allowList) != 4: 
            continue
          index4 = index3 
          while index4 < glbRowMax:
            tempCell4 = tempCells[index4]
            index4 += 1
            # Check if only two or three or four values are allowed for the current
            # cell
            if len(tempCell4.allowList) != 2 and \
               len(tempCell4.allowList) != 3 and \
               len(tempCell4.allowList) != 4: 
              continue
            cellsList = [tempCell1, tempCell2, tempCell3, tempCell4]
            cellsIndexList = [index1-1, index2-1, index3-1, index4-1]
            # Merge the allowed value(s) lists
            allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3, tempCell4)
            if len(allowedListMerge) != 4:
              continue
            # Make sure that the allowed lists for each cell only 
            # contain allowed values
            if checkCellList(cellsList, allowedListMerge) == False:
              continue
            # Increment the number of quads
            quadCount += 1
            # Remove all of the allowed values from the rest of the row
            removeCount = removeAllowsExcludingListCells(tempCells, allowedListMerge, cellsIndexList)
            totalRemoveAllowsCount += removeCount
            # Check if the four cells are in the same box
            if tempCell1.boxPosition == tempCell2.boxPosition and \
               tempCell2.boxPosition == tempCell3.boxPosition and \
               tempCell3.boxPosition == tempCell4.boxPosition:
              boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, \
                              tempCell3.boxLocation-1, tempCell4.boxLocation-1]
              removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, allowedListMerge, boxIndexList)
              totalRemoveAllowsCount += removeCount  
  # Scan all of the columns looking for a quad of cells that 
  # have the correct allowed list
  for col in range(glbColMin, glbColMax+1):
    tempCells = copyBoard.getCol(col)
    index1 = 0
    while index1 < glbColMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two or three or four values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2 and \
         len(tempCell1.allowList) != 3 and \
         len(tempCell1.allowList) != 4: 
        continue
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbColMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two or three or four values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2 and \
           len(tempCell2.allowList) != 3 and \
           len(tempCell2.allowList) != 4: 
          continue
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbColMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          # Check if only two or three or four values are allowed for the current
          # cell
          if len(tempCell3.allowList) != 2 and \
             len(tempCell3.allowList) != 3 and \
             len(tempCell3.allowList) != 4: 
            continue
          index4 = index3 
          while index4 < glbColMax:
            tempCell4 = tempCells[index4]
            index4 += 1
            # Check if only two or three or four values are allowed for the current
            # cell
            if len(tempCell4.allowList) != 2 and \
               len(tempCell4.allowList) != 3 and \
               len(tempCell4.allowList) != 4: 
              continue
            cellsList = [tempCell1, tempCell2, tempCell3, tempCell4]
            cellsIndexList = [index1-1, index2-1, index3-1, index4-1]
            # Merge the allowed value(s) lists
            allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3, tempCell4)
            if len(allowedListMerge) != 4:
              continue
            # Make sure that the allowed lists for each cell only 
            # contain allowed values
            if checkCellList(cellsList, allowedListMerge) == False:
              continue
            # Increment the number of quads
            quadCount += 1
            # Remove all of the allowed values from the rest of the column
            removeCount = removeAllowsExcludingListCells(tempCells, allowedListMerge, cellsIndexList)
            totalRemoveAllowsCount += removeCount
            # Check if the four cells are in the same box
            if tempCell1.boxPosition == tempCell2.boxPosition and \
               tempCell2.boxPosition == tempCell3.boxPosition and \
               tempCell3.boxPosition == tempCell4.boxPosition:
              boxIndexList = [tempCell1.boxLocation-1, tempCell2.boxLocation-1, \
                              tempCell3.boxLocation-1, tempCell4.boxLocation-1]
              removeCount = removeAllowsBox(copyBoard, tempCell1.boxPosition, allowedListMerge, boxIndexList)
              totalRemoveAllowsCount += removeCount  
  # Scan all of the boxes looking for a quad of cells that 
  # have the correct allowed list
  for box in range(glbBoxMin, glbBoxMax+1):
    tempCells = copyBoard.getBox(box)
    index1 = 0
    while index1 < glbBoxMax:
      tempCell1 = tempCells[index1]
      index1 += 1
      # Check if only two or three or four values are allowed for the current
      # cell
      if len(tempCell1.allowList) != 2 and \
         len(tempCell1.allowList) != 3 and \
         len(tempCell1.allowList) != 4: 
        continue
      # Scan all of the other cells 
      index2 = index1 
      while index2 < glbBoxMax:
        tempCell2 = tempCells[index2]
        index2 += 1
        # Check if only two or three or four values are allowed for the current
        # cell
        if len(tempCell2.allowList) != 2 and \
           len(tempCell2.allowList) != 3 and \
           len(tempCell2.allowList) != 4: 
          continue
        # Scan all of the other cells 
        index3 = index2 
        while index3 < glbBoxMax:
          tempCell3 = tempCells[index3]
          index3 += 1
          # Check if only two or three or four values are allowed for the current
          # cell
          if len(tempCell3.allowList) != 2 and \
             len(tempCell3.allowList) != 3 and \
             len(tempCell3.allowList) != 4: 
            continue
          index4 = index3 
          while index4 < glbBoxMax:
            tempCell4 = tempCells[index4]
            index4 += 1
            # Check if only two or three or four values are allowed for the current
            # cell
            if len(tempCell4.allowList) != 2 and \
               len(tempCell4.allowList) != 3 and \
               len(tempCell4.allowList) != 4: 
              continue
            cellsList = [tempCell1, tempCell2, tempCell3, tempCell4]
            cellsIndexList = [index1-1, index2-1, index3-1, index4-1]
            # Merge the allowed value(s) lists
            allowedListMerge = mergeAllowedLists(tempCell1, tempCell2, tempCell3, tempCell4)
            if len(allowedListMerge) != 4:
              continue
            # Make sure that the allowed lists for each cell only 
            # contain allowed values
            if checkCellList(cellsList, allowedListMerge) == False:
              continue
            # Increment the number of quads
            quadCount += 1
            # Remove all of the allowed values from the rest of the box
            removeCount = removeAllowsExcludingListCells(tempCells, allowedListMerge, cellsIndexList)
            totalRemoveAllowsCount += removeCount
            # All of the current cells may be exactly one row or exactly one column 
            boxIndex1 = tempCell1.boxPosition - 1
            boxIndex2 = tempCell2.boxPosition - 1
            boxIndex3 = tempCell3.boxPosition - 1
            boxIndex4 = tempCell4.boxPosition - 1
            colIndex1 = tempCell1.colPosition - 1
            colIndex2 = tempCell2.colPosition - 1
            colIndex3 = tempCell3.colPosition - 1
            colIndex4 = tempCell4.colPosition - 1
            rowIndex1 = tempCell1.rowPosition - 1
            rowIndex2 = tempCell2.rowPosition - 1
            rowIndex3 = tempCell3.rowPosition - 1 
            rowIndex4 = tempCell4.rowPosition - 1 
            # We can now check if the row positions match. If this
            # is true, then the rest of the row can be adjusted to
            # remove the allowed values.
            if rowIndex1 == rowIndex2 and \
               rowIndex2 == rowIndex3 and \
               rowIndex3 == rowIndex4:
              tempCellsRow = copyBoard.getRow(rowIndex1+1)
              cellsColIndexList = [colIndex1, colIndex2, colIndex3, colIndex4]
              removeCount = removeAllowsExcludingListCells(tempCellsRow, allowedListMerge, cellsColIndexList) 
              totalRemoveAllowsCount += removeCount
            # We can now check if the column positions match. If this
            # is true, then the rest of the column can be adjusted to 
            # remove the allowed values.
            if colIndex1 == colIndex2 and \
               colIndex2 == colIndex3 and \
               colIndex3 == colIndex4:
              tempCellsCol = copyBoard.getCol(colIndex1+1)
              cellsRowIndexList = [rowIndex1, rowIndex2, rowIndex3, rowIndex4]
              removeCount = removeAllowsExcludingListCells(tempCellsCol, allowedListMerge, cellsRowIndexList)  
              totalRemoveAllowsCount += removeCount
  # Return the final quad count and the number of removed allows
  return [quadCount, totalRemoveAllowsCount]

# Find all of the pointing pairs and triples and use 
# them. A pointing pair or triple is set of values
# that are the same, and in one row or column (in one 
# box). Since the values are the same and they are in 
# one row or column, the value can not occur anywhere 
# else in the row or column outside of the box.
def pointingPairsAndTriples(copyBoard):
  pairTripleCount = 0
  totalRemoveAllowsCount = 0
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):  
    allowList = [value]  
    # Scan all of the boxes looking for a box where the 
    # current value has just two or three possible
    # location.
    for box in range(glbBoxMin, glbBoxMax+1):
      tempCellsBox = copyBoard.getBox(box)
      curTuple = countAllowed(tempCellsBox, value)
      count = curTuple[0]
      # Check if a pair of values was found
      if count == 2:
        cell1 = curTuple[1][0] 
        cell2 = curTuple[1][1]
        boxIndex1 = cell1.boxPosition - 1
        boxIndex2 = cell2.boxPosition - 1
        colIndex1 = cell1.colPosition - 1
        colIndex2 = cell2.colPosition - 1
        rowIndex1 = cell1.rowPosition - 1
        rowIndex2 = cell2.rowPosition - 1
        # We can now check if the row positions match. If this
        # is true, then the rest of the row can be adjusted to
        # remove the allowed values.
        if rowIndex1 == rowIndex2:
          pairTripleCount += 1
          tempCellsRow = copyBoard.getRow(rowIndex1+1)
          # Remove allows from the rest of the row
          cellsColIndexList = [colIndex1, colIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
        # We can now check if the column positions match. If this
        # is true, then the rest of the column can be adjusted to 
        # remove the allowed values.
        if colIndex1 == colIndex2:
          pairTripleCount += 1
          tempCellsCol = copyBoard.getCol(colIndex1+1)
          # Remove allows from the rest of the column
          cellsRowIndexList = [rowIndex1, rowIndex2]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellsRowIndexList)  
          totalRemoveAllowsCount += removeCount
      # Check if three values were found
      if count == 3:
        cell1 = curTuple[1][0] 
        cell2 = curTuple[1][1]
        cell3 = curTuple[1][2]
        boxIndex1 = cell1.boxPosition - 1
        boxIndex2 = cell2.boxPosition - 1
        boxIndex3 = cell3.boxPosition - 1
        colIndex1 = cell1.colPosition - 1
        colIndex2 = cell2.colPosition - 1
        colIndex3 = cell3.colPosition - 1
        rowIndex1 = cell1.rowPosition - 1
        rowIndex2 = cell2.rowPosition - 1
        rowIndex3 = cell3.rowPosition - 1 
        # We can now check if the row positions match. If this
        # is true, then the rest of the row can be adjusted to
        # remove the allowed values.
        if rowIndex1 == rowIndex2 and \
           rowIndex2 == rowIndex3:
          pairTripleCount += 1
          tempCellsRow = copyBoard.getRow(rowIndex1+1)
          cellsColIndexList = [colIndex1, colIndex2, colIndex3]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellsColIndexList) 
          totalRemoveAllowsCount += removeCount
        # We can now check if the column positions match. If this
        # is true, then the rest of the column can be adjusted to 
        # remove the allowed values.
        if colIndex1 == colIndex2 and \
           colIndex2 == colIndex3:
          pairTripleCount += 1
          tempCellsCol = copyBoard.getCol(colIndex1+1)
          cellsRowIndexList = [rowIndex1, rowIndex2, rowIndex3]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellsRowIndexList) 
          totalRemoveAllowsCount += removeCount
  # Return the final pair and/or triple count and the number of allows removed
  return [pairTripleCount, totalRemoveAllowsCount]

# Remove a set of allows from a box. The caller
# provides the box number, the list of allows 
# that should be removed, and the index values
# of the cells that should be skipped. The index
# values are actually location values minus one.
def removeAllowsBox(copyBoard, boxNumber, allowsList, boxIndexList):
  # Get all of the cells for the current box
  boxCells = copyBoard.getBox(boxNumber)
  # Remove all of the allows
  removeCount = removeAllowsExcludingListCells(boxCells, allowsList, boxIndexList)
  return removeCount

# Remove a set of allow values from a list of cells.
# This is only done if the cell has the allow value
# and the cell is not in the excluded list. This routine
# returns a count of the number of allows that have
# been actually removed (of course, the count may be
# zero).
def removeAllowsExcludingListCells(curCells, allowList, cellIndexList):
  removedCount = 0
  # Get the length of the list of cells passed to this routine
  curCellsLen = len(curCells)
  for allowValue in allowList:
    index3 = 0
    while index3 < curCellsLen:
      tempCell3 = curCells[index3]
      index3 += 1
      if (index3-1) in cellIndexList:
        continue
      actuallyRemoved = removeAllowValue(tempCell3, allowValue)  
      # Check if the allow(ed) value was actually removed or not
      if actuallyRemoved:
        removedCount += 1
  return removedCount

# Try to remove an allow value and add the value to 
# the block list. This routine returns false if the 
# possible allow value is not removed from the allow
# list of the current cell and true if it is removed
# from the allow list of the current cell. 
def removeAllowValue(curCell, curValue):
  # Check if the current value is in the allow list. This 
  # may not be true.
  if curValue not in curCell.allowList:
    return False
  curCell.allowList.remove(curValue)
  # We now need to add the value to the block list
  bisect.insort(curCell.blockList, curValue)
  return True

# Remove a set of allow values from a set of cells. 
# The key idea is that some value may be allowed 
# one, two, or three times in the same box. If all
# of the allows are on the same row or column, then
# the allows for that value can be removed from the
# rest of the row or column outside of the box.
def removeBlockAllows(copyBoard):
  totalRemovedCount = 0
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):
    allowList = [value]
    # Scan all of the boxes looking for a box where the 
    # current value is allowed on just one row or column
    for box in range(glbBoxMin, glbBoxMax+1):
      # Get all of the cells of the current box
      tempCells = copyBoard.getBox(box)
      # Count the number of times the current value is allowed
      # in the current box
      outTuple = countAllowed(tempCells, value)
      countBox = outTuple[0]
      # The current value might be allowed one, two, three, or
      # more times. Check for each case. 
      if countBox == 1:
        curCell = outTuple[1][0]   
        curCellRow = curCell.rowPosition
        curCellCol = curCell.colPosition
        curCellBox = curCell.boxPosition
        # Get all of the cells of the current row
        tempCellsRow = copyBoard.getRow(curCellRow)
        cellIndexList = [curCellCol-1]
        removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellIndexList)
        totalRemovedCount += removeCount
        # Get all of the cells of the current column
        tempCellsCol = copyBoard.getCol(curCellCol)
        cellIndexList = [curCellRow-1]
        removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellIndexList)
        totalRemovedCount += removeCount
      # The current allow value may have occurred two times
      if countBox == 2:
        curCell1 = outTuple[1][0] 
        curCell2 = outTuple[1][1]  
        curCell1Row = curCell1.rowPosition
        curCell1Col = curCell1.colPosition
        curCell1Box = curCell1.boxPosition
        curCell2Row = curCell2.rowPosition
        curCell2Col = curCell2.colPosition
        curCell2Box = curCell2.boxPosition
        # Check if both allows were on the same row
        if curCell1Row == curCell2Row:
          # Get all of the cells of the current row
          tempCellsRow = copyBoard.getRow(curCell1Row)
          cellIndexList = [curCell1Col-1, curCell2Col-1]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellIndexList)
          totalRemovedCount += removeCount
        # Check if both allows were on the same column
        if curCell1Col == curCell2Col:
          # Get all of the cells of the current column
          tempCellsCol = copyBoard.getCol(curCell1Col)
          cellIndexList = [curCell1Row-1, curCell2Row-1]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellIndexList)
          totalRemovedCount += removeCount
      # The current allow value may have occurred three times
      if countBox == 3:
        curCell1 = outTuple[1][0] 
        curCell2 = outTuple[1][1]  
        curCell3 = outTuple[1][2] 
        curCell1Row = curCell1.rowPosition
        curCell1Col = curCell1.colPosition
        curCell1Box = curCell1.boxPosition
        curCell2Row = curCell2.rowPosition
        curCell2Col = curCell2.colPosition
        curCell2Box = curCell2.boxPosition
        curCell3Row = curCell3.rowPosition
        curCell3Col = curCell3.colPosition
        curCell3Box = curCell3.boxPosition
        # Check if both allows were on the same row
        if curCell1Row == curCell2Row and \
           curCell2Row == curCell3Row:
          # Get all of the cells of the current row
          tempCellsRow = copyBoard.getRow(curCell1Row)
          cellIndexList = [curCell1Col-1, curCell2Col-1, curCell3Col-1]
          removeCount = removeAllowsExcludingListCells(tempCellsRow, allowList, cellIndexList)
          totalRemovedCount += removeCount
        # Check if both allows were on the same column
        if curCell1Col == curCell2Col and \
           curCell2Col == curCell3Col:
          # Get all of the cells of the current column
          tempCellsCol = copyBoard.getCol(curCell1Col)
          cellIndexList = [curCell1Row-1, curCell2Row-1, curCell3Row-1]
          removeCount = removeAllowsExcludingListCells(tempCellsCol, allowList, cellIndexList)
          totalRemovedCount += removeCount
  # Return the number of times an allow was removed 
  return totalRemovedCount

# Remove all of the other values from a list of cells. 
# We know that the list of cells may only contain a set
# of two or more values. All of the other 'allowed' values 
# should be removed at this point. This routine
# returns a count of the number of allows that have
# been actually removed (of course, the count may be
# zero).
def removeOtherAllowedValuesFromCells(curCells, allowedList):
  removedCount = 0
  # Process all of the cells
  for cell in curCells:
    # A deep copy is used here because the code below 
    # changes the allowed list for each cell 
    dcAllowList = copy.deepcopy(cell.allowList)
    # Check each allowed value for each cell
    for allowValue in dcAllowList:
      if allowValue in allowedList:
        continue
      actuallyRemoved = removeAllowValue(cell, allowValue)  
      # Check if the allow(ed) value was actually removed or not
      if actuallyRemoved:
        removedCount += 1
  return removedCount

# This routine implements the Swordfish strategy. Thw Swordfish
# strategy looks for a rectangle of a specific value. If the
# rectangle is found, then the specific value is removed from
# each of thw rows of the rectangle.
def swordfish(curBoard):
  swordfishCount = 0
  totalRemoveAllowsCount = 0
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):
    allowList = [value]
    # Scan all of the rows looking for a row where the 
    # current value has just two (and only two) possible
    # locations
    for rowBase in range(glbRowMin, glbRowMax+1):
      # Get all of the cells for the current row
      rowBaseCells = curBoard.getRow(rowBase)
      # Get all of the cells where the current value occurs
      rowBaseTuple = countAllowed(rowBaseCells, value)
      rowBaseCount = rowBaseTuple[0]
      if rowBaseCount != 2:
        continue
      # Scan for another row where the current value 
      # has just two (and only two) possible
      # locations
      for rowOther in range(rowBase+1, glbRowMax+1):
        # Get all of the cells for the current row
        rowOtherCells = curBoard.getRow(rowOther)
        # Get all of the cells where the current value occurs
        rowOtherTuple = countAllowed(rowOtherCells, value)
        rowOtherCount = rowOtherTuple[0]
        if rowOtherCount != 2:
          continue
        # Get the specific cells where the value occurs
        rowBaseTupleCells = rowBaseTuple[1]
        # Get the two cells where the desired value occurs
        rowBaseCellFirst = rowBaseTupleCells[0]
        rowBaseCellSecond = rowBaseTupleCells[1]
        # Get the row and column values for each of the two cells 
        rowBaseColIndexFirst = rowBaseCellFirst.colPosition - 1
        rowBaseColIndexSecond = rowBaseCellSecond.colPosition - 1
        rowBaseRowIndexFirst = rowBaseCellFirst.rowPosition - 1
        rowBaseRowIndexSecond = rowBaseCellSecond.rowPosition - 1
        # Make sure the row positions match. We have a serious
        # error if these two values don't match.
        if rowBaseRowIndexFirst != rowBaseRowIndexSecond:
          errorText = 'Row index values ({0}) ({1}) do not match'
          errorText = errorText.format(rowBaseRowIndexFirst, rowBaseRowIndexSecond)
          raise RuntimeError(errorText)       
        # Get the specific cells where the value occurs
        rowOtherTupleCells = rowOtherTuple[1]
        # Get the two cells where the desired value occurs
        rowOtherCellFirst = rowOtherTupleCells[0]
        rowOtherCellSecond = rowOtherTupleCells[1]
        # Get the row and column values for each of the two cells 
        rowOtherColIndexFirst = rowOtherCellFirst.colPosition - 1
        rowOtherColIndexSecond = rowOtherCellSecond.colPosition - 1
        rowOtherRowIndexFirst = rowOtherCellFirst.rowPosition - 1
        rowOtherRowIndexSecond = rowOtherCellSecond.rowPosition - 1
        # Make sure the row positions match. We have a serious
        # error if these two values don't match.
        if rowOtherRowIndexFirst != rowOtherRowIndexSecond:
          errorText = 'Row index values ({0}) ({1}) do not match'
          errorText = errorText.format(rowOtherRowIndexFirst, rowOtherRowIndexSecond)
          raise RuntimeError(errorText)  
        # We can now make sure that the values were found in the 
        # correct columns
        if rowBaseColIndexFirst  != rowOtherColIndexFirst or \
           rowBaseColIndexSecond != rowOtherColIndexSecond:
          continue
        # We now have a rectangle. We can remove the row
        # value from the two columns except for the two rows.
        colFirstCells = curBoard.getCol(rowBaseCellFirst.colPosition)
        colSecondCells = curBoard.getCol(rowBaseCellSecond.colPosition) 
        # Get the index values for the base and other rows
        rowIndexList = [rowBaseRowIndexFirst, rowOtherRowIndexFirst]
        # We can now remove the current allow value from all
        # columns on the base and other rows except for where
        # it must be located
        removedCount = removeAllowsExcludingListCells(colFirstCells, allowList, rowIndexList)
        totalRemoveAllowsCount += removedCount
        if removedCount > 500:
          print('r1', value, rowBase, rowOther, rowBaseRowIndexFirst, rowOtherRowIndexFirst)
        removedCount = removeAllowsExcludingListCells(colSecondCells, allowList, rowIndexList)
        totalRemoveAllowsCount += removedCount
        if removedCount > 500:
          print('r1', value, rowBase, rowOther, rowBaseRowIndexFirst, rowOtherRowIndexFirst)
    # Scan all of the columns looking for a column where the 
    # current value has just two (and only two) possible
    # locations
    for colBase in range(glbColMin, glbColMax+1):
      # Get all of the cells for the current column
      colBaseCells = curBoard.getCol(colBase)
      # Get all of the cells where the current value occurs
      colBaseTuple = countAllowed(colBaseCells, value)
      colBaseCount = colBaseTuple[0]
      if colBaseCount != 2:
        continue
      # Scan for another column where the current value 
      # has just two (and only two) possible
      # locations
      for colOther in range(colBase+1, glbColMax+1):
        # Get all of the cells for the current column
        colOtherCells = curBoard.getCol(colOther)
        # Get all of the cells where the current value occurs
        colOtherTuple = countAllowed(colOtherCells, value)
        colOtherCount = colOtherTuple[0]
        if colOtherCount != 2:
          continue
        # Get the specific cells where the value occurs
        colBaseTupleCells = colBaseTuple[1]
        # Get the two cells where the desired value occurs
        colBaseCellFirst = colBaseTupleCells[0]
        colBaseCellSecond = colBaseTupleCells[1]
        # Get the row and column values for each of the two cells 
        colBaseColIndexFirst = colBaseCellFirst.colPosition - 1
        colBaseColIndexSecond = colBaseCellSecond.colPosition - 1
        colBaseRowIndexFirst = colBaseCellFirst.rowPosition - 1
        colBaseRowIndexSecond = colBaseCellSecond.rowPosition - 1
        # Make sure the column positions match. We have a serious
        # error if these two values don't match.
        if colBaseColIndexFirst != colBaseColIndexSecond:
          errorText = 'Column index values ({0}) ({1}) do not match'
          errorText = errorText.format(colBaseColIndexFirst, colBaseColIndexSecond)
          raise RuntimeError(errorText)       
        # Get the specific cells where the value occurs
        colOtherTupleCells = colOtherTuple[1]
        # Get the two cells where the desired value occurs
        colOtherCellFirst = colOtherTupleCells[0]
        colOtherCellSecond = colOtherTupleCells[1]
        # Get the row and column values for each of the two cells 
        colOtherColIndexFirst = colOtherCellFirst.colPosition - 1
        colOtherColIndexSecond = colOtherCellSecond.colPosition - 1
        colOtherRowIndexFirst = colOtherCellFirst.rowPosition - 1
        colOtherRowIndexSecond = colOtherCellSecond.rowPosition - 1
        # Make sure the column positions match. We have a serious
        # error if these two values don't match.
        if colOtherColIndexFirst != colOtherColIndexSecond:
          errorText = 'Column index values ({0}) ({1}) do not match'
          errorText = errorText.format(colOtherColIndexFirst, colOtherColIndexSecond)
          raise RuntimeError(errorText)  
        # We can now make sure that the values were found in the 
        # correct rows
        if colBaseRowIndexFirst  != colOtherRowIndexFirst or \
           colBaseRowIndexSecond != colOtherRowIndexSecond:
          continue
        # We now have a rectangle. We can remove the current
        # value from the two rows except for the two columns.
        rowFirstCells = curBoard.getRow(colBaseCellFirst.rowPosition)
        rowSecondCells = curBoard.getRow(colBaseCellSecond.rowPosition) 
        # Get the index values for the base and other columns
        colIndexList = [colBaseColIndexFirst, colOtherColIndexFirst]
        # We can now remove the current allow value from all
        # columns on the base and other rows except for where
        # it must be located
        removedCount = removeAllowsExcludingListCells(rowFirstCells, allowList, colIndexList)
        totalRemoveAllowsCount += removedCount
        if removedCount > 500:
          print('c1', value, colBase, colOther, colBaseColIndexFirst, colOtherColIndexFirst)
        removedCount = removeAllowsExcludingListCells(rowSecondCells, allowList, colIndexList)
        if removedCount > 500:
          print('c2', value, colBase, colOther, colBaseColIndexFirst, colOtherColIndexFirst)
        totalRemoveAllowsCount += removedCount
  # Return the final Swordfish count and the number of allows that were
	# removed
  return [swordfishCount, totalRemoveAllowsCount]

# Handle startup 
def startup():   
  pass

# Try to solve a Sudoku board using a set of algorithms.
# This routine returns true if the board was successfully 
# solved and false, if not.
def trySolve(winRoot, mainBoard, interactive):
  # win1 = canvasShowValues(mainBoard)   
  # winRoot.mainloop() 
  # Set the default return value
  rv = False
  # Make a deep copy of the current board
  copyBoard = mainBoard.clone()
  # win1 = canvasShowValues(copyBoard)   
  # winRoot.mainloop() 
  # This is the main loop. One or more values are 
  # added to board each time this loop is executed
  # (hopefully)
  iterationCount = 0
  while True:
    iterationCount = iterationCount + 1
    totalRemoveAllowsCount = 0
    # Check if we are done. We are done if the board 
    # is entirely filled in.
    filledIn = copyBoard.getFilledIn()
    if filledIn == glbCellsCount:
      break
    # Based on the current board, do all of the row, column, 
    # and box blocks. This step builds the block list for 
    # each cell. 
    blockValues(copyBoard)
    # Based on the current board, do all of the allow processing.
    # A value is allowed in a given cell if the cell has no value
    # and the value is not blocked.
    allowValues(copyBoard) 
    # win1 = canvasShowValues(copyBoard)   
    # winRoot.mainloop()
    # This was an attempt (successful) to have lists of values
    # stored in cells where only a certain list of values
    # could possible occur.
    if totalRemoveAllowsCount == 0:
      [pairCount, removeCount] = findPairsValues(copyBoard)
      totalRemoveAllowsCount += removeCount
    # This was an attempt (successful) to have lists of values
    # stored in cells where only a certain list of values
    # could possible occur.
    if totalRemoveAllowsCount == 0:
      [tripleCount, removeCount] = findTriplesValues(copyBoard)
      totalRemoveAllowsCount += removeCount
    # Remove all of the allows that can be found and invalidated
    # using the X-Wing strategy
    if totalRemoveAllowsCount == 0:
      [pairCount, removeCount] = xWing(copyBoard)
      totalRemoveAllowsCount += removeCount
    # Remove all of the allows outside of each where we known
    # that allows inside the box will take precedence
    if totalRemoveAllowsCount == 0:
      removeCount = removeBlockAllows(copyBoard)
      totalRemoveAllowsCount += removeCount
    # Find and use all of the naked pairs. Of course, the 
    # number of naked pairs may be zero
    if totalRemoveAllowsCount == 0:
      [pairCount, removeCount] = nakedPairs(copyBoard)
      totalRemoveAllowsCount += removeCount
      # print('Naked pairs remove count', removeCount)
      # totalRemoveAllowsCount = 0
    # Find and use all of the hidden pairs. Of course, the 
    # number of hidden pairs may be zero
    if totalRemoveAllowsCount == 0:
      [pairCount, removeCount] = hiddenPairs(copyBoard)
      totalRemoveAllowsCount += removeCount   
      # print('HIdden pairs remove count', removeCount)   
      # totalRemoveAllowsCount = 0
    # Find and use all of the pointing pairs and triples. 
    # Of course, the number of pointing pairs and triples 
    # may be zero
    if totalRemoveAllowsCount == 0:
      [pairTripleCount, removeCount] = pointingPairsAndTriples(copyBoard)
      totalRemoveAllowsCount += removeCount
      # print('Pointing pairs and triples remove count', removeCount)
      # totalRemoveAllowsCount = 0
    # Find and use all of the naked triples. Of course, 
    # the number of naked triples may be zero.
    if totalRemoveAllowsCount == 0:
      [tripleCount, removeCount] = nakedTriples(copyBoard)
      totalRemoveAllowsCount += removeCount
      # print('Naked triples remove count', removeCount)
      # totalRemoveAllowsCount = 0
    # Find and use all of the hidden triples. Of course, 
    # the number of hidden triples may be zero.
    if totalRemoveAllowsCount == 0:
      [tripleCount, removeCount] = hiddenTriples(copyBoard)
      totalRemoveAllowsCount += removeCount
      # print('Hidden triples remove count', removeCount)
      # totalRemoveAllowsCount = 0
    # Get a location where all but one value is blocked. 
    # Since only one value is allowed at this location, 
    # the value must be placed in this location. 
    lastPossibleLocations = lastPossibleNumber(copyBoard)
    if len(lastPossibleLocations) > 0:
      if interactive:
        displayOneValues('LPN', lastPossibleLocations, iterationCount)
      useLocationList(copyBoard, lastPossibleLocations)
      continue 
    # Get a location where only a single value is allowed. 
    # If the value can appear in multiple places in the 
    # current unit, then the value can not definitely be 
    # placed in just one location in the current unit.
    lastRemainingLocations = lastRemainingCellInUnit(copyBoard)
    if len(lastRemainingLocations) > 0:
      if interactive:
        displayOneValues('LRC', lastRemainingLocations, iterationCount)
      useLocationList(copyBoard, lastRemainingLocations)
      continue    
    # Get all of the locations in a unit where just one value
    # is allowed. Of course, the value must be placed at that 
    # location.
    nakedSingleLocations = nakedSingles(copyBoard)
    if len(nakedSingleLocations) > 0: 
      if interactive:
        displayOneValues('NSL', nakedSingleLocations, iterationCount)
      useLocationList(copyBoard, nakedSingleLocations)
      continue   
    # Check for too many iterations. At this point we may 
    # be in a loop
    if iterationCount > 200:
      break
  # Return to the caller showing if the board has been solved
  # or not
  if filledIn == glbCellsCount:
    rv = True
  return [rv, copyBoard]

# Use a set of locations where a value can be placed. These
# locations, are the only place where a value can be placed.
def useLocationList(curBoard, ones):
  for location in ones:
    curLocation = location[0]
    curRow = curLocation.rowPosition
    curCol = curLocation.colPosition
    curValue = location[1]
    curBoard.storeValue(curRow, curCol, curValue)
  return

# This routine implements the X-Wing strategy. Thw X-Wing
# strategy looks for a rectangle of a specific value. If the
# rectangle is found, then the specific value is removed from
# each of thw rows of the rectangle.
def xWinf(curBoard):
  xWingsCount = 0
  totalRemoveAllowsCount = 0
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):
    allowList = [value]
    # Scan all of the rows looking for a row where the 
    # current value has just two (and only two) possible
    # locations.
    for rowBase in range(glbRowMin, glbRowMax+1):
      # Get all of the cells for the current row
      rowBaseCells = curBoard.getRow(rowBase)
      # Get all of the cells where the current value occurs
      rowBaseTuple = countAllowed(rowBaseCells, value)
      rowBaseCount = rowBaseTuple[0]
      if rowBaseCount != 2:
        continue
      # Get the specific cells where the value occurs
      rowBaseTupleCells = rowBaseTuple[1]
      # Get the two cells where the desired value occurs
      rowBaseCellFirst = rowBaseTupleCells[0]
      rowBaseCellSecond = rowBaseTupleCells[1]
      # Get the row and column values for each of the two cells 
      colBaseIndexFirst = rowBaseCellFirst.colPosition - 1
      colBaseIndexSecond = rowBaseCellSecond.colPosition - 1
      rowBaseIndexFirst = rowBaseCellFirst.rowPosition - 1
      rowBaseIndexSecond = rowBaseCellSecond.rowPosition - 1
      # Make sure the row positions match. We have a serious
      # error if these two values don't match.
      if rowBaseIndexFirst != rowBaseIndexSecond:
        errorText = 'Row index values ({0}) ({1}) do not match'
        errorText = errorText.format(rowBaseIndexFirst, rowBaseIndexSecond)
        raise RuntimeError(errorText)        
      # We can now make sure the current value occurs twice 
      # (and exactly twice) in the first column
      colFirstCells = curBoard.getCol(colBaseIndexFirst+1)
      # Get all of the cells where the current value occurs
      colFirstTuple = countAllowed(colFirstCells, value)
      colFirstCount = colFirstTuple[0]
      if colFirstCount != 2:
        continue
      # We can now make sure the current value occurs twice 
      # (and exactly twice) in the second column
      colSecondCells = curBoard.getCol(colBaseIndexSecond+1)
      # Get all of the cells where the current value occurs
      colSecondTuple = countAllowed(colSecondCells, value)
      colSecondCount = colSecondTuple[0]
      if colSecondCount != 2:
        continue
      cellColIndexList = [colBaseIndexFirst, colBaseIndexSecond]
      # Get the row and column index values for the first column
      colFirstColCells = colFirstTuple[1]
      colFirstColCellFirst = colFirstColCells[0]
      colFirstColCellSecond = colFirstColCells[1]
      colFirstColIndexFirst = colFirstColCellFirst.colPosition - 1
      colFirstColIndexSecond = colFirstColCellSecond.colPosition - 1
      rowFirstColIndexFirst = colFirstColCellFirst.rowPosition - 1
      rowFirstColIndexSecond = colFirstColCellSecond.rowPosition - 1
      # Get the row and column index values for the second column
      colSecondColCells = colSecondTuple[1]
      colSecondColCellFirst = colSecondColCells[0]
      colSecondColCellSecond = colSecondColCells[1]
      colSecondColIndexFirst = colSecondColCellFirst.colPosition - 1
      colSecondColIndexSecond = colSecondColCellSecond.colPosition - 1
      rowSecondColIndexFirst = colSecondColCellFirst.rowPosition - 1
      rowSecondColIndexSecond = colSecondColCellSecond.rowPosition - 1
      # Get the index values for the first and second rows
      cellRowIndexList = [rowFirstColIndexFirst, rowFirstColIndexSecond]
      # Check if we should use the first match in each column
      # or the second. Both cases will occur. The check below
      # will return True if the search of the column first found
      # the current row.
      if rowBaseIndexFirst == rowFirstColIndexFirst:
        # If we did not find the value for the second time on
        # the same row, we are done
        if rowFirstColIndexSecond != rowSecondColIndexSecond:
          continue
        # We can now remove the current allow value from all
        # columns on the first and second rows except for where
        # it must be located
        removedCount = removeAllowsExcludingListCells(rowBaseCells, allowList, cellColIndexList)
        totalRemoveAllowsCount += removedCount
        rowSecondCells = curBoard.getRow(rowFirstColIndexSecond+1)
        removedCount = removeAllowsExcludingListCells(rowSecondCells, allowList, cellColIndexList)
        totalRemoveAllowsCount += removedCount
      # The 'second' row was actually the first row
      else:
        # If we did not find the value for the second time on
        # the same row, we are done
        if rowFirstColIndexFirst != rowSecondColIndexFirst:
          continue
        # We can now remove the current allow value from all
        # columns on the first and second rows except for where
        # it must be located  
        removedCount = removeAllowsExcludingListCells(rowBaseCells, allowList, cellColIndexList)
        totalRemoveAllowsCount += removedCount
        rowSecondCells = curBoard.getRow(rowFirstColIndexFirst+1)
        removedCount = removeAllowsExcludingListCells(rowSecondCells, allowList, cellColIndexList)
        totalRemoveAllowsCount += removedCount    
      # Increment the number of X-Wings found
      xWingsCount += 1
      # Remove the current value from the first and second columns
      removedCount = removeAllowsExcludingListCells(colFirstCells, allowList, cellRowIndexList)
      totalRemoveAllowsCount += removedCount
      removedCount = removeAllowsExcludingListCells(colSecondCells, allowList, cellRowIndexList)
      totalRemoveAllowsCount += removedCount
  # Return the final X-Wings count and the number of allows that were
	# removed
  return [xWingsCount, totalRemoveAllowsCount]

# This routine implements the X-Wing strategy. Thw X-Wing
# strategy looks for a rectangle of a specific value. If the
# rectangle is found, then the specific value is removed from
# each of thw rows of the rectangle.
def xWing(curBoard):
  xWingsCount = 0
  totalRemoveAllowsCount = 0
  # Check all of the possible values
  for value in range(glbValueMin, glbValueMax+1):
    allowList = [value]
    # Scan all of the rows looking for a row where the 
    # current value has just two (and only two) possible
    # locations
    for rowBase in range(glbRowMin, glbRowMax+1):
      # Get all of the cells for the current row
      rowBaseCells = curBoard.getRow(rowBase)
      # Get all of the cells where the current value occurs
      rowBaseTuple = countAllowed(rowBaseCells, value)
      rowBaseCount = rowBaseTuple[0]
      if rowBaseCount != 2:
        continue
      # Scan for another row where the current value 
      # has just two (and only two) possible
      # locations
      for rowOther in range(rowBase+1, glbRowMax+1):
        # Get all of the cells for the current row
        rowOtherCells = curBoard.getRow(rowOther)
        # Get all of the cells where the current value occurs
        rowOtherTuple = countAllowed(rowOtherCells, value)
        rowOtherCount = rowOtherTuple[0]
        if rowOtherCount != 2:
          continue
        # Get the specific cells where the value occurs
        rowBaseTupleCells = rowBaseTuple[1]
        # Get the two cells where the desired value occurs
        rowBaseCellFirst = rowBaseTupleCells[0]
        rowBaseCellSecond = rowBaseTupleCells[1]
        # Get the row and column values for each of the two cells 
        rowBaseColIndexFirst = rowBaseCellFirst.colPosition - 1
        rowBaseColIndexSecond = rowBaseCellSecond.colPosition - 1
        rowBaseRowIndexFirst = rowBaseCellFirst.rowPosition - 1
        rowBaseRowIndexSecond = rowBaseCellSecond.rowPosition - 1
        # Make sure the row positions match. We have a serious
        # error if these two values don't match.
        if rowBaseRowIndexFirst != rowBaseRowIndexSecond:
          errorText = 'Row index values ({0}) ({1}) do not match'
          errorText = errorText.format(rowBaseRowIndexFirst, rowBaseRowIndexSecond)
          raise RuntimeError(errorText)       
        # Get the specific cells where the value occurs
        rowOtherTupleCells = rowOtherTuple[1]
        # Get the two cells where the desired value occurs
        rowOtherCellFirst = rowOtherTupleCells[0]
        rowOtherCellSecond = rowOtherTupleCells[1]
        # Get the row and column values for each of the two cells 
        rowOtherColIndexFirst = rowOtherCellFirst.colPosition - 1
        rowOtherColIndexSecond = rowOtherCellSecond.colPosition - 1
        rowOtherRowIndexFirst = rowOtherCellFirst.rowPosition - 1
        rowOtherRowIndexSecond = rowOtherCellSecond.rowPosition - 1
        # Make sure the row positions match. We have a serious
        # error if these two values don't match.
        if rowOtherRowIndexFirst != rowOtherRowIndexSecond:
          errorText = 'Row index values ({0}) ({1}) do not match'
          errorText = errorText.format(rowOtherRowIndexFirst, rowOtherRowIndexSecond)
          raise RuntimeError(errorText)  
        # We can now make sure that the values were found in the 
        # correct columns
        if rowBaseColIndexFirst  != rowOtherColIndexFirst or \
           rowBaseColIndexSecond != rowOtherColIndexSecond:
          continue
        # Increment the number of X-Wings found
        xWingsCount += 1
        # We now have a rectangle. We can remove the current
        # value from the two columns except for the two rows.
        colFirstCells = curBoard.getCol(rowBaseCellFirst.colPosition)
        colSecondCells = curBoard.getCol(rowBaseCellSecond.colPosition) 
        # Get the index values for the base and other rows
        rowIndexList = [rowBaseRowIndexFirst, rowOtherRowIndexFirst]
        # We can now remove the current allow value from all
        # columns on the base and other rows except for where
        # it must be located
        removedCount = removeAllowsExcludingListCells(colFirstCells, allowList, rowIndexList)
        totalRemoveAllowsCount += removedCount
        if removedCount > 500:
          print('r1', value, rowBase, rowOther, rowBaseRowIndexFirst, rowOtherRowIndexFirst)
        removedCount = removeAllowsExcludingListCells(colSecondCells, allowList, rowIndexList)
        totalRemoveAllowsCount += removedCount
        if removedCount > 500:
          print('r1', value, rowBase, rowOther, rowBaseRowIndexFirst, rowOtherRowIndexFirst)
    # Scan all of the columns looking for a column where the 
    # current value has just two (and only two) possible
    # locations
    for colBase in range(glbColMin, glbColMax+1):
      # Get all of the cells for the current column
      colBaseCells = curBoard.getCol(colBase)
      # Get all of the cells where the current value occurs
      colBaseTuple = countAllowed(colBaseCells, value)
      colBaseCount = colBaseTuple[0]
      if colBaseCount != 2:
        continue
      # Scan for another column where the current value 
      # has just two (and only two) possible
      # locations
      for colOther in range(colBase+1, glbColMax+1):
        # Get all of the cells for the current column
        colOtherCells = curBoard.getCol(colOther)
        # Get all of the cells where the current value occurs
        colOtherTuple = countAllowed(colOtherCells, value)
        colOtherCount = colOtherTuple[0]
        if colOtherCount != 2:
          continue
        # Get the specific cells where the value occurs
        colBaseTupleCells = colBaseTuple[1]
        # Get the two cells where the desired value occurs
        colBaseCellFirst = colBaseTupleCells[0]
        colBaseCellSecond = colBaseTupleCells[1]
        # Get the row and column values for each of the two cells 
        colBaseColIndexFirst = colBaseCellFirst.colPosition - 1
        colBaseColIndexSecond = colBaseCellSecond.colPosition - 1
        colBaseRowIndexFirst = colBaseCellFirst.rowPosition - 1
        colBaseRowIndexSecond = colBaseCellSecond.rowPosition - 1
        # Make sure the column positions match. We have a serious
        # error if these two values don't match.
        if colBaseColIndexFirst != colBaseColIndexSecond:
          errorText = 'Column index values ({0}) ({1}) do not match'
          errorText = errorText.format(colBaseColIndexFirst, colBaseColIndexSecond)
          raise RuntimeError(errorText)       
        # Get the specific cells where the value occurs
        colOtherTupleCells = colOtherTuple[1]
        # Get the two cells where the desired value occurs
        colOtherCellFirst = colOtherTupleCells[0]
        colOtherCellSecond = colOtherTupleCells[1]
        # Get the row and column values for each of the two cells 
        colOtherColIndexFirst = colOtherCellFirst.colPosition - 1
        colOtherColIndexSecond = colOtherCellSecond.colPosition - 1
        colOtherRowIndexFirst = colOtherCellFirst.rowPosition - 1
        colOtherRowIndexSecond = colOtherCellSecond.rowPosition - 1
        # Make sure the column positions match. We have a serious
        # error if these two values don't match.
        if colOtherColIndexFirst != colOtherColIndexSecond:
          errorText = 'Column index values ({0}) ({1}) do not match'
          errorText = errorText.format(colOtherColIndexFirst, colOtherColIndexSecond)
          raise RuntimeError(errorText)  
        # We can now make sure that the values were found in the 
        # correct rows
        if colBaseRowIndexFirst  != colOtherRowIndexFirst or \
           colBaseRowIndexSecond != colOtherRowIndexSecond:
          continue
        # Increment the number of X-Wings found
        xWingsCount += 1
        # We now have a rectangle. We can remove the current
        # value from the two rows except for the two columns.
        rowFirstCells = curBoard.getRow(colBaseCellFirst.rowPosition)
        rowSecondCells = curBoard.getRow(colBaseCellSecond.rowPosition) 
        # Get the index values for the base and other columns
        colIndexList = [colBaseColIndexFirst, colOtherColIndexFirst]
        # We can now remove the current allow value from all
        # columns on the base and other rows except for where
        # it must be located
        removedCount = removeAllowsExcludingListCells(rowFirstCells, allowList, colIndexList)
        totalRemoveAllowsCount += removedCount
        if removedCount > 500:
          print('c1', value, colBase, colOther, colBaseColIndexFirst, colOtherColIndexFirst)
        removedCount = removeAllowsExcludingListCells(rowSecondCells, allowList, colIndexList)
        if removedCount > 500:
          print('c2', value, colBase, colOther, colBaseColIndexFirst, colOtherColIndexFirst)
        totalRemoveAllowsCount += removedCount
  # Return the final X-Wings count and the number of allows that were
	# removed
  return [xWingsCount, totalRemoveAllowsCount]
  
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Start the current program  
  startup() 
  # Create an instance of Tkinter frame or window
  root = Tk()
  # This is the main loop. This loop tests all of the 
  # saved boards.
  interactive = True
  interactive = False
  for boardNumber in range(26, 27):
    IterCpuTimeStart = time.process_time()
    mainBoard = Board()
    evalStr = 'defaultValues' + str(boardNumber) + '(mainBoard)'
    eval(evalStr)
    win1 = canvasShowValues(mainBoard)   
    root.mainloop() 
    # Make a deep copy of the current board
    copyBoard = mainBoard.clone() 
    # [tripleCount, removeCount] = hiddenTriplet(copyBoard)
    # Try to solve the current board
    [solved, copzBoard] = trySolve(root, copyBoard, interactive)
    IterCpuTimeEnd = time.process_time()
    IterCpuTimeUsed = IterCpuTimeEnd - IterCpuTimeStart
    print(boardNumber, solved, IterCpuTimeUsed)
    # Check if we are running in interactive mode
    if interactive:
      # Display the current board on a canvas
      win1 = canvasShowValues(copzBoard)   
      root.mainloop()    
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()