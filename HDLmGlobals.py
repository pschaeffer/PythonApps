# The methods of this class return global information to the
# caller
#
# The HDLmGlobals class doesn't actually do anything. However, it
# does serve to hold a set of global values. Note that the HDLmGlobals
# class does have at least one static method for setting the current editor
# type.  

from HDLmEnums import *

class HDLmGlobals(object):
  # The debugger below is the JavaScript debugger. Of course,
  # this debugger is never active under Python.
  activeDebugger = False
  # Set the default editor type. In the Python environment
  # this value should not change.
  activeEditorType = HDLmEditorTypes.passEnum
  # Of course, we don't have any extension windows in Python.
  # The field is set for compatibility with other code. 
  activeExtensionWindow = False
  # The active node value shows what kind of node we 
  # are currently creating
  activeNodeType = None
  # This routine checks the active extension status flag. This routine
  # checks the active extension window status flag and returns a True 
  # or False value to the caller. The returned value will only be True
  # if we are running in the Popup or Simple extension windows.  
  #
  # Of course, we don't have any extension windows in Python.
  # The field is set for compatibility with other code. 
  @classmethod
  def checkActiveExtensionWindow(cls):
    return HDLmGlobals.activeExtensionWindow
  # This routine checks the debugger status flag. This routine checks
  # the debugger status flag and returns a true or false value to the
  # caller. 
  def checkDebuggerStatus():
    return HDLmGlobals.activeDebugger
  # This routine checks if one of the inline editors is in use.
  # At present, the inline editors are the Popup editor and the
  # Simple editor. If any inline editor is in use, this routine 
  # returns true. Otherwise, this routine returns false. 
  #
  # Of course, we don't have any inline editors in Python.
  # This method is provided for compatibility with other code. 
  @classmethod
  def checkForInlineEditor(cls):
    if HDLmGlobals.activeEditorType == HDLmEditorTypes.popup or \
       HDLmGlobals.activeEditorType == HDLmEditorTypes.simple:
      return True
    else:
      return False
  # This routine checks if one of the inline editors is in use
  # or if we are using one of the GUI editors (GEMs). At present,
  # the inline editors are the Popup editor and the Simple editor.
  # If any inline editor or one of the GUI editors is in use,
  # this routine returns true. Otherwise, this routine returns 
  # false. 
  #
  # Of course, we don't have any inline editors or GEMs in Python.
  # This method is provided for compatibility with other code. 
  @classmethod
  def checkForInlineEditorOrGems(cls): 
    if HDLmGlobals.activeEditorType == HDLmEditorTypes.popup  or \
       HDLmGlobals.activeEditorType == HDLmEditorTypes.simple or \
       HDLmGlobals.activeEditorType == HDLmEditorTypes.gem    or \
       HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
      return True
    else:
      return False
  # Get the active editor type and return it to the caller
  #
  # Of course, we only have one active editor type in Python.
  # This method is provided for compatibility with other code. 
  @classmethod
  def getActiveEditorType(cls):
    return HDLmGlobals.activeEditorType
  # Set the active editor type from a value passed by the caller
  #
  # Of course, we only have one active editor type in Python.
  # This method is provided for compatibility with other code. 
  @classmethod
  def setActiveEditorType(cls, newEditorEnumtype):
    HDLmGlobals.activeEditorType = newEditorEnumtype
    return
  # This routine set the active node type value to something
  # passed by the caller 
  @classmethod
  def setActiveNodeType(cls, newValue):
    # print(newValue); 
    HDLmGlobals.activeNodeType = newValue; 