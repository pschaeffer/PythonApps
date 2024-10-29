# The methods of this class return state information
# to the caller
#
# The HDLmStateInfo class doesn't actually do anything. However, 
# it does serve to hold a set of state values and get/set those
# values as need be.

from HDLmAssert import *
from HDLmEnums  import *

class HDLmStateInfo(object):
  systemValue = None
  # Get the system suffix value that follows the standard
  # suffix. This is typically just one character, such as
  # 'b' or 'c' (without the quotes). The system suffix is
  # returned to the caller as Python string, not as a 
  # Python character. 
  #   
  # This value is used to build the key that is used to 
  # obtain data from a database. This value follows the 
  # standard suffix.  
  @classmethod
  def getSystemValue(cls):
    return HDLmStateInfo.systemValue
  # Set the system suffix value that follows the standard
	# suffix. This is typically just one character, such as
	# 'b' or 'c' (without the quotes). The system suffix is
	# set from the string passed by the caller. The actual 
	# value is a Python string, not a Python character. 
	# 
	# This value is used to build the key that is used to 
	# obtain data from a database. This value follows the 
	# standard suffix. 
  @classmethod
  def setEntriesSystemValue(cls, newValue):
    # Set a few values for use below
    newValueLen = len(newValue)
    newValueType = str(type(newValue))
    # Make sure the value passed by the caller is a string 
    if newValueType != "<class 'str'>":
      errorText = f'State ({newValue}) value passed to setEntriesSystemValue method is not a string'
      HDLmAssert(False, errorText)
    # Make sure the length of the value passed by the caller is valid
    if newValueLen != 1:
      errorText = f'State ({newValue}) value passed to setEntriesSystemValue method has an invalid length'
      HDLmAssert(False, errorText)
    # Store the new value passed by the caller
    HDLmStateInfo.systemValue = newValue  