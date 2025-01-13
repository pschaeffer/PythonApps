# Class for building a node in the node / rule tree. Of course, some 
# nodes are not really for rules.
# 
# Each instance of this class is one node in the node tree. Most nodes (but 
# not all) are for rules.

from   HDLmAssert                   import * 
from   HDLmConfigInfo               import *
from   HDLmExtensionBothManageRules import *
from   HDLmIgnore                   import * 
from   HDLmMod                      import *
from   HDLmPass                     import * 
from   HDLmStore                    import *
from   HDLmString                   import *
from   HDLmUrl                      import *
from   HDLmUtility                  import *
from   HDLmWebSockets               import *
import copy 
import jsons
import math
import re
import types

class HDLmTree(object):
  # Set the tree top to a default value. The tree top will be
  # reset later to a more normal value when the tree is built.
  top = None
  # In the beginning, the pending inserts array (list) is empty
  pendingInserts = []
  # print('In class HDLmTree')
  # print(type(HDLmDefines))
  # print(type(HDLmGlobals))
  # print(type(HDLmMod))
  # print(type(HDLmPass))
  # print(type(HDLmTree))
  # The __init__ method creates an instance of the class
  def __init__(self, newType, newTooltip, newNodePath):
    # Each tree node nas a set of fields
    self.type = newType
    self.tooltip = newTooltip
    # The next field has all of the details for each rule
    # The details would appear to be a instance of the HDLmMod class. This may 
	  # be true. However, in some cases, the details will actually be a class that
	  # extends the HDLmMod class. For example, the details might actually be an
	  # instance of the HDLmProxy class.
    self.details = None
    # Set the node path of the new instance. Note that a deep copy
    # is used here so that the passed value can be changed without
    # impacting the new tree node.
    self.nodePath = newNodePath.copy()
    self.id = None
    self.children = []
  # This routine adds a set of pending inserts to the pending inserts
  # array. The caller passes a tree node (which may or may not have
  # children) that needs to be inserted. The passed tree node (which
  # may or may have children) is not modified by this call. The children
  # (which may or may not exist) are not modified by this call. The
  # tree node passed by the caller (and all of it's children) are added
  # to the pending inserts array. Eventually the passed tree node (and
  # the possible children) will be modified when the ID value(s) are returned
  # by the database server. A variety of unneeded information is (if present)
  # removed from the temporary copy of the tree node (and it's children)
  # passed by the caller. 
  @staticmethod
  def addPendingInserts(treePos, processSubNodes = False):
    tempDetails = types.SimpleNamespace()
    # Create a temporary copy of the current tree node. This is
    # done so that we can make changes to the temporary copy that
    # will not affect the original tree node. 
    # 
    # A fairly complex copy is used below so that class variables
    # are not copied into the temporary object. This allows that 
    # copy to be converted into a JSON string without recursion.
    tempPos = types.SimpleNamespace()
    treePosVars = vars(treePos)
    for var in treePosVars:
      setattr(tempPos, var, copy.deepcopy(getattr(treePos, var)))
    if hasattr(tempPos, 'children'):
      del tempPos.children
    if hasattr(tempPos, 'containerWidget'):
      del tempPos.containerWidget
    if hasattr(tempPos, 'id'):
      del tempPos.id
    # Remove the saved details from the current node, if need be 
    if hasattr(tempPos, 'savedDetails'):
      del tempPos.savedDetails
    # Fix the details (an HDLmMod) so that the stringify will work 
    if hasattr(tempPos, 'details'):
      tempDetails = copy.deepcopy(tempPos.details)
      if hasattr(tempDetails, 'pathValue'):
        tempDetails.path = tempDetails.pathvalue
        del tempDetails.pathvalue
        # print(tempDetails)  
      tempPos.details = tempDetails 
    # Convert the temporary object into a string 
    tempPosStr = jsons.dumps(tempPos)
    # print(tempPos) 
    # Add the string (created from the temporary node) to the
    # array of pending inserts 
    HDLmTree.pendingInserts.append(tempPosStr)
    # Check if subnodes should be handled or not 
    if processSubNodes == False:
      return
    # Handle all of the children of the tree node passed
    # by the caller 
    # print(treePos) 
    childArray = treePos.children
    childArraySize = len(childArray)
    for i in range(0, childArraySize):
      HDLmTree.addPendingInserts(childArray[i], processSubNodes)
  # Locate (find) the parent of a node using a node path. Add the
  # current node to the children array of the parent node. This
  # routine will return true if the current node was added to the
  # children array of the parent node. This routine will return false
  # if the current node was not added to the children array of the
  # parent node.
  #
  # This routine must be called with a node that has a parent. As
  # a consequence, this routine should not be called with the path
  # of the top node. 
  @staticmethod
  def addToParentTree(childTreeNode):
    # print('In HDLmTree.addToParentTree') 
    # print(childTreeNode) 
    rvBool = False
    # Try to obtain (locate) the parent node of the current child node 
    nodePath = childTreeNode.nodePath
    parentTreeNode = HDLmTree.locateTreeParentNode(nodePath)
    # print(parentTreeNode) 
    # Report an error if the parent node could not be found 
    if parentTreeNode == None:
      nodeString = str(nodePath)
      HDLmError.buildError('Error', 'Locate', 9, nodeString) 
      return rvBool
    # Check all of the subnodes of the parent tree node looking for a
    # tree node with a name higher (greater then) the current name. This
    # may not happen. The new tree node name may be greater than all of
    # the existing tree node names. 
    childrenArray = parentTreeNode.children
    # tempChildrenArray = list(childrenArray) 
    # print(tempChildrenArray) 
    # print(len(tempChildrenArray)) 
    childrenLength = len(childrenArray)
    # print(childrenLength) 
    i = 0
    for i in range(0, childrenLength):
      childEntry = childrenArray[i]
      childEntryNodePath = childEntry.nodePath
      childEntryNodePathLen = len(childEntryNodePath)
      childName = childEntryNodePath[childEntryNodePathLen - 1]
      if childEntryNodePath[childEntryNodePathLen - 1] < childName:
        break
    # Insert the new tree node into the correct place in the parent
    # tree node children array. This may be at the beginning of the
    # array, at the end of the array, or in the middle of the array. 
    #
    # tempChildrenArray = list(parentTreeNode.children) 
    # print(tempChildrenArray) 
    # print(len(tempChildrenArray)) 
    parentTreeNode.children.insert(i, childTreeNode)
    # temrChildrenArray = parentTreeNode.children.slice() 
    # print(temrChildrenArray) 
    # print(temrChildrenArray.length) 
    rvBool = True
    return rvBool 
  # Add the JSON returned to the caller to the node tree. This 
  # method may add many nodes to the node tree at many levels. 
  @staticmethod
  def addToTree(jsonStr):
    # print(type(HDLmMod))
    # print(jsonStr)  
    jsonStrLen = len(jsonStr)
    # The following code is just used to write to print.
    # The idea is that parts of a very long JSON string are
    # broken into pieces and the pieces are changed so that
    # the can be used to build a Java JSON literal. 
    if 1 == 2:
      # Set the initial new line location. This value makes
      # it appear that a new line was just before the first
      # character of the very long JSON string.  
      priorNewLine = -1
      strArray = []
      # Process every character in the very long JSON string 
      for index in range(0, jsonStrLen): 
        # Get the current character 
        charVal = jsonStr[index] 
        # Check if the current character is a new line character 
        if ord(charVal) == 10:
          # Get a part of the very long JSON string. The part is
          # the text between two new line characters. 
          tempStr = jsonStr[priorNewLine + 1 : index]
          strArray.append(tempStr)
          priorNewLine = index  
      # Add the last part of the very long JSON string. This
      # code handles the text after the last new line character. 
      tempStr = jsonStr[priorNewLine + 1 : jsonStrLen + 1]
      strArray.append(tempStr)
      # Process each text string that was obtained above 
      strArrayLen = len(strArray)
      consoleStart = 0
      consoleEnd = 3000
      # Process each text string in the text string array 
      for i in range(0, strArrayLen):
        # Get the current array entry 
        curStr = strArray[i]
        # Make a few changes needed to build a proper Java
        # JSON literal 
        curStr = curStr.replace('\\n', '')
        curStr = curStr.replace('"', '\\"')
        curStr = curStr.replace('\\\\"', '\\\\\\"')
        curStr = '"' + curStr + '" +'
        # print(curStr) 
        # Write the current string to the console log 
        if i >= consoleStart and i < consoleEnd:
          print(curStr) 
    # The HTTP request to the local server does not appear to fail.
    # However, the HTTP request to the remote server does appear to
    # fail if the network connection is not working. This can result
    # in an empty string being passed to this routine. We need to
    # check for this case and handle it. 
    if len(jsonStr) == 0:
      errorText = f'Nothing retrieved'
      HDLmError.buildError('Error',
                           'Retrieval failure',
                           16,
                           errorText)
      HDLmUtility.setErrorText(errorText)
      return 
    # Convert the JSON string to a Python dictionary and get some 
    # information from the dictionary  
    jsonObj = jsons.loads(jsonStr)
    # Get the number of data rows returned from the server. The number
    # of data rows will be equal to the number of tree nodes. 
    dataRows = jsonObj['rows_returned']
    if dataRows < 1:
      errorText = f'Invalid number of data rows ({dataRows}) returned from the server'
      HDLmAssert(False, errorText) 
    # The data may have returned in a new format. Handle the new format.
    # The new format has one row for each node in the node tree. 
    jsonData = jsonObj['data']  
    # The JSON data array may (or may not) contain bad entries.
    # Why the JSON data array can have bad entries is not clear.
    # However, it is empirically correct that bad entries can
    # be found in some cases. 
    #
    # Check if the JSON data entry is valid or not
    jsonFilterFunction = lambda curEntry : \
      False if curEntry['info'] == '' or \
               curEntry['name'] == '' else True 
    # Check if the JSON data entry is valid or not. Invalid
    # entries are removed here.
    filter(jsonFilterFunction, jsonData)
    # At this point, the info member of each object in the
    # array is just a string. This string must be converted
    # to a JSON object here. We also add the ID value so
    # that the corresponding row can be deleted/updated
    # later. 
    jsonDataLen = len(jsonData)
    # print(jsonDataLen) 
    # jsonDataLen = 40 
    for i in range(0, jsonDataLen): 
      # Get the current array entry 
      curEntry = jsonData[i]
      # print(curEntry) 
      # Get the info string and convert it to a JSON object 
      infoStr = curEntry['info']
      # At this point, the information string may actually be a string
      # or it might be an object. We need to handle both cases. 
      infoStrType = str(type(infoStr))
      if infoStrType == "<class 'str'>":
        infoJson = jsons.loads(infoStr) 
      # The information string may actually be an object at this
      # point. This is not an error condition. This will happen
      # when the string (not really a string) is obtained from
      # the server via web sockets. 
      else:
        # print('Inside addToTree') 
        # print(i) 
        # print(curEntry) 
        # print(str(type(curEntry['info']))) 
        infoJson = infoStr
        # print(infoJson) 
      # Get and store the ID value 
      infoJson['id'] = curEntry['id']
      curEntry['info'] = infoJson 
    # Define the sort function used below
    jsonSortFunction = lambda curEntry : curEntry['info']['nodePath'] \
                                         [len(curEntry['info']['nodePath']) - 1] 
    # Sort the JSON objects into ascending name order 
    jsonData.sort(key=jsonSortFunction)   
    # Build the entire node tree using the JSON data passed
    # to this routine as a JSON string 
    # print(jsonData) 
    currentTreeNodeNone = None
    treeTop = HDLmTree.buildNodeTree(jsonData, currentTreeNodeNone)
    HDLmTree.setTreeTop(treeTop)
    # print(treeTop) 
    # Add any missing fields to the modification level nodes or
    # company level nodes for proxy definitions 
    HDLmTree.addToTreeFix(HDLmTree.getTreeTop())
  # This routine fixes the node tree as need be. In some cases, we may
  # get a node tree from the database that is missing certain fields.
  # These fields are needed later. This routine checks for missing
  # fields and provides default values for them. 
  @staticmethod
  def addToTreeFix(node):
    # print(node.type)
    # if node.type == 'proxy':
    # node.type = node.type
    # Check if we are handling a companies level node or not. We
    # recursively call this routine for all nodes other than
    # companies level nodes and a few other node types. Companies
    # level nodes are fixed, as need be. 
    if node.type == 'companies':
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the 
      # GXE editor or the pass-through editor or one of the inline 
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling a company level node or not. We
    # recursively call this routine for all nodes other than
    # company level nodes and a few other node types. Company
    # level nodes are fixed, as need be. 
    if node.type == 'company':
      # Check if we are running the GUI editor or the GXE editor or 
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the 
      # GXE editor or the pass-through editor or one of the inline
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node)
      # Check if we are running the proxy editor. We may need to create
      # an additional set of fields, if we are running the proxy editor. 
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.proxy:
        # Add a default (empty) comments value, if need be 
        if hasattr(node.details, 'comments') == False: 
          node.details.comments = '' 
        # Add a default (empty) extra information value, if need be 
        if hasattr(node.details, 'extra') == False: 
          node.details.extra = '' 
        # Add a default (empty) backend type value, if need be 
        if hasattr(node.details, 'backendType') == False: 
          node.details.backendType = '' 
        # Add a default (empty) backend server value, if need be 
        if hasattr(node.details, 'backendServer') == False: 
          node.details.backendSever = '' 
        # Add a default (empty) secure server value, if need be 
        if hasattr(node.details, 'secureServer') == False: 
          node.details.secureSever = ''  
    # Check if we are handling a configuration data node or not.
    # We recursively call this routine for all nodes other than
    # configuration level nodes and a few other node types.
    # Configuration data nodes are fixed, as need be. 
    if node.type == 'config':
      # Check if we are running the configuration editor. We may need to create
      # an additional set of fields, if we are running the configuration editor. 
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.config:
        HDLmConfig.addMissingConfigObject(node.details) 
    # Check if we are handling a data (zero, one, or more
    # divisions) node or not. We recursively call this routine
    # for all nodes other than data (zero, one, or more divisions)
    # level nodes and a few other node types. Data (zero, one,
    # or more divisions) data nodes are fixed, as need be. 
    if node.type == HDLmDefines.getString('HDLMDATATYPE'):
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the
      # GXE editor or the pass-through editor or one of the inline 
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling an ignore-list entry node or not.
    #  We recursively call this routine for all nodes other than
    #  ignore-list entry nodes and a few other node types.
    #  Ignore-list entry nodes are fixed, as need be. 
    if node.type == 'ignore':
      # Check if we are running the ignore-lists editor. We may
      # need to create one or more additional fields, if we are
      # running the ignore-lists editor. 
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.ignore:
        HDLmIgnore.addMissingIgnoreObject(node.details)
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the GXE 
      # editor or the pass-through editor or one of the inline editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe       or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum  or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup     or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling a line (just one line) data
    # node or not. We recursively call this routine for all nodes
    # other than line (just one line) level nodes and a few
    # other node types. Line (just one line) data nodes are
    # fixed, as need be. 
    if node.type == 'line':
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the 
      # GXE editor or the pass-through editor or one of the inline 
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem       or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe       or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum  or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup     or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node)
    # Check if we are handling a lines (zero, one, or more
    # lines) data node or not. We recursively call this routine
    # for all nodes other than lines (zero, one, or more lines)
    # level nodes and a few other node types. Lines (zero, one,
    # or more lines) data nodes are fixed, as need be. 
    if node.type == 'lines':
      # Check if we are running the GUI editor or the GXE editor or 
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the 
      # GXE editor or the pass-through editor or one of the inline 
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling an ignore-list data node or not.
    # We recursively call this routine for all nodes other than
    # ignore-list level nodes and a few other node types.
    # Ignore-list data nodes are fixed, as need be. 
    if node.type == 'list':
      # Check if we are running the GUI editor or the GXE editor or 
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the
      # GXE editor of the pass-through editor or one of the inline 
      # editors.
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code. 
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling an ignore-lists data node or not.
    # We recursively call this routine for all nodes other than
    # ignore-lists level nodes and a few other node types.
    # Ignore-lists data nodes are fixed, as need be. 
    if node.type == 'lists':
      # Check if we are running the GUI editor or the GXE editor or 
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the
      # GXE editor or the pass-through editor or one of the inline 
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling a modification level node or not. We
    # recursively call this routine for all nodes other than modification
    # level nodes and a few other node types. Modification level nodes are
    # fixed, as need be. 
    if node.type == 'mod':
      # Check if we are running the modifications editor. We may need to create
      # an additional set of fields, if we are running the modifications editor,
      # the GUI editor or the GUI extended editor or the pass-through editor or 
      # one of the inline editors.
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.mod      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        # Create the node details, if need be
        if hasattr(node, 'details') == False or \
           node.details == None:
          node.details = HDLmMod.makeEmptyMod()
        # Add a default (empty) comments value, if need be 
        if hasattr(node.details, 'comments') == False: 
          node.details.comments = '' 
        # Add a default (empty) CSS selector value, if need be 
        if hasattr(node.details, 'cssselector') == False: 
          node.details.cssselector = '' 
        # Add a default (empty) Extra Information value, if need be 
        if hasattr(node.details, 'extra') == False: 
          node.details.extra = '' 
        # Add a default (empty) node identifier value, if need be 
        if 1 == 2 and hasattr(node.details, 'nodeiden') == True:
          jsonStrNodeIden = jsons.dumps(node.details.nodeiden)
          if jsonStrNodeIden.find('phash') >= 0:
            # print(node.details)  
            pass
        if hasattr(node.details, 'nodeiden') == False or \
           node.details.nodeiden == None:
          node.details.nodeiden = ''  
        # Add a default (empty) path value, if need be 
        if hasattr(node.details, 'path') == True:
          node.details.pathvalue = node.details.path
          # print(node.details.path]) 
          # print(node.details.pathvalue]) 
          del node.details.path
          # print(node.details)  
        # print(node.details.pathvalue']) 
        # print(node.details) 
        if hasattr(node.details, 'pathValue') == False: 
          node.details.pathvalue = ''  
          # print(node.details.pathvalue'])  
        # Add a default (empty) XPath search value, if need be 
        if hasattr(node.details, 'xpath') == False: 
          node.details.xpath = ''  
        # Fix a database error, if need be 
        if node.details.nodeiden == '{}':
          node.details.nodeiden = '' 
        # We may have a image, that does not have a perceptual
        # hash value. We need to fix this by getting the perceptual
        # hash value and adding it to the node identifier. 
        #
        # What follows is a dummy loop used only to allow break to work 
        while True:
          # Make sure we can use the node identifier object 
          if node.details.nodeiden == None or \
             node.details.nodeiden == '':
            break
          nodeIdenType = str(type(node.details.nodeiden))
          if nodeIdenType != "<class 'dict'>":
            break
          if 'attributes' not in node.details.nodeiden:
            break
          nodeAttributes = node.details.nodeiden['attributes']
          if nodeAttributes == None:
            break
          # Make sure we have a tag attribute and that it has the
          # correct value 
          if 'tag' not in nodeAttributes: 
            break
          if nodeAttributes['tag'] != 'img':
            break
          # Get the source value from the node identifier attributes 
          if 'src' not in nodeAttributes:
            break
          nodeSource = nodeAttributes['src']
          # Make sure we don't already have a perceptual hash value 
          if 'phash' in nodeAttributes:
            break
          # Get the URL from the image source, if possible  
          nodeUrl = HDLmUrl.getUrlFromImage(nodeSource)
          if nodeUrl == '':
            break
          # Get the node path for updating the node 
          localNodePath = node.nodePath.copy()
          # Run the code that updates the node with the perceptual  
          # hash data. Note that this actually occurs synchronously 
          # as the statements below are executed. 
          newString = HDLmUtility.getPerceptualHash(nodeUrl)
          HDLmUtility.usePerceptualString(newString, localNodePath)
          break 
        # We may have a style, with a background image, that does
        # not have a perceptual hash value. We need to fix this by
        # getting the perceptual hash value and adding it to the
        # node identifier. 
        #
        # What follows is a dummy loop used only to allow break to work 
        while True:
          # Make sure we can use the node identifier object 
          if node.details.nodeiden == None or \
             node.details.nodeiden == '':
            break
          nodeIdenType = str(type(node.details.nodeiden))
          if nodeIdenType != "<class 'dict'>":
            break
          if 'attributes' not in node.details.nodeiden:
            break
          nodeAttributes = node.details.nodeiden['attributes']
          if nodeAttributes == None:
            break
          # Get the style value from the node identifier attributes 
          if 'style' not in nodeAttributes:
            break
          nodeStyle = nodeAttributes['style']
          # Make sure we don't already have a perceptual hash value 
          if 'phash' in nodeAttributes:
            break
          # Get the URL from the style, if possible  
          nodeUrl = HDLmUrl.getUrlFromStyle(nodeStyle)
          if nodeUrl == '':
            break
          # Get the node path for updating the node 
          localNodePath = node.nodePath.copy() 
          # Run the code that updates the node with the perceptual 
          # hash data. Note that this actually occurs synchronously
          # as the statements below are executed. 
          newString = HDLmUtility.getPerceptualHash(nodeUrl)
          HDLmUtility.usePerceptualString(newString, localNodePath)
          break 
        # Remove an empty (unused) value suffix field, if need be 
        if hasattr(node.details, 'valueSuffix') == True:
          del node.details.valueSuffix 
        # Remove an empty (unused) values count field, if need be 
        if hasattr(node.details, 'valuesCount') == True:
          del node.details.valuesCount  
        # Remove an empty (unused) values field, if need be 
        if hasattr(node.details, 'values') == True:
          del node.details.values  
        # Remove an empty (unused) value field, if need be 
        if hasattr(node.details, 'value') == True:
          del node.details.value 
        # In a few cases, we want to remove the parameter number
        # field. This is true if the parameter number field is
        # present and the modification type does not allow/use
        # the parameter number field. 
        if hasattr(node.details, 'type') == True:
          nodeDetailsType = node.details.type
          if HDLmMod.getModificationTypeParmNumberUsed(nodeDetailsType) == False:
            if hasattr(node.details, 'parameter') == True:
              del node.details.parameter
    # Check if we are handling a report (just one report) data
    # node or not. We recursively call this routine for all nodes
    # other than report (just one report) level nodes and a few
    # other node types. Report (just one report) data nodes are
    # fixed, as need be. 
    if node.type == 'report':
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor or one of the inline editors. We
      # may need to create one or more additional fields, if we
      # are running the GUI editor or the GXE editor or the 
      # pass-through editor or one of the inline editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling a reports (zero, one, or more
    # reports) data node or not. We recursively call this routine
    # for all nodes other than reports (zero, one, or more reports)
    # level nodes and a few other node types. Reports (zero, one,
    # or more reports) data nodes are fixed, as need be. 
    if node.type == 'reports':
      # Check if we are running the GUI editor or the GXE editor or 
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the 
      # GXE editor or the pass-through editor or one of the inline
      # editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Check if we are handling a rules (zero, one, or more
    # divisions) data node or not. We recursively call this routine
    # for all nodes other than rules (zero, one, or more divisions)
    # level nodes and a few other node types. Rules (zero, one,
    # or more divisions) data nodes are fixed, as need be. 
    if node.type == HDLmDefines.getString('HDLMRULESTYPE'):
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor. We may need to create one or more 
      # additional fields, if we are running the GUI editor or the
      # GXE editor or the pass-through editor or one of the inline 
      # editors.
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code. 
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node)
    # Check if we are handling a store (stored value) node or not.
    # We recursively call this routine for all nodes other than
    # store (stored value) nodes. Store (stored value) nodes are
    # fixed, as need be. 
    if node.type == 'store':
      # Check if we are running the store (stored values) editor. We may
      # need to create one or more additional fields, if we are running
      # the store (stored value) editor. 
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.store:
        HDLmStore.addMissingStoreObject(node.details)    
    # Check if we are handling a top (top) node or not. We
    # recursively call this routine for all nodes other than
    # top (top) nodes and a few other types. Top nodes are
    # fixed, as need be. 
    if node.type == 'top':
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor or one of the inline editors. We may
      # need to create one or more additional fields, if we are running 
      # the GUI editor or the GXE editor or the pass-through editor or
      # one of the inline editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node)
    # Check if we are handling a value (data value) node or not. 
    # We recursively call this routine for all nodes other than
    # value (data value) nodes and a few other types. Top nodes are
    # fixed, as need be. 
    if node.type == HDLmDefines.getString('HDLMVALUETYPE'):
      # Check if we are running the GUI editor or the GXE editor or
      # the pass-through editor or one of the inline editors. We may
      # need to create one or more additional fields, if we are running 
      # the GUI editor or the GXE editor or the pass-through editor or
      # one of the inline editors. 
      #
      # Of course, we don't have any inline editors or GEMs in Python.
      # This code is provided for compatibility with other code.
      if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe      or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.passEnum or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.popup    or \
         HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.simple:
        HDLmPass.addMissingPassObject(node) 
    # Recursively invoke this routine on all of the children of the
    # curent node. These steps will have no effect if they current
    # node does not have any children. 
    children = node.children
    childrenLength = len(children)
    for i in range(0, childrenLength):
      child = children[i]
      HDLmTree.addToTreeFix(child)
  # This routine does all of the extra work needed to build a company
  # node. A company node has a fixed set of subnodes that must be 
  # built at this point. This routine does all of the work needed
  # to actually build a company node. 
  @staticmethod
  def buildCompanyNode(companyTreeNode, updateDatabase):
    # Get the node path for the node we just created 
    fieldName = 'nodePath'
    nodePathCompanyNode = getattr(companyTreeNode, fieldName)
    # Add the new Data child to the new company 
    nodePathData = list(nodePathCompanyNode)
    dataNodeName = HDLmDefines.getString('HDLMDATANODENAME')
    dataNodeType = HDLmDefines.getString('HDLMDATATYPE')
    nodePathData.append(dataNodeName)
    tooltip = HDLmModTreeInfo[dataNodeType]['tooltip']
    newData = HDLmTree.buildTreeNode(dataNodeName,    \
                                     dataNodeType,    \
                                     tooltip,         \
                                     nodePathData,    \
                                     companyTreeNode, \
                                     updateDatabase)
    # Add the new Lists child to the new company 
    nodePathLists = list(nodePathCompanyNode)
    nodePathLists.append('Ignore Lists')
    tooltip = HDLmModTreeInfo['lists']['tooltip']
    newLists = HDLmTree.buildTreeNode('Ignore Lists',  \
                                      'lists',         \
                                      tooltip,         \
                                      nodePathLists,   \
                                      companyTreeNode, \
                                      updateDatabase)
    # Add the new Reports child to the new company 
    nodePathReports = list(nodePathCompanyNode)
    nodePathReports.append('Reports')
    tooltip = HDLmModTreeInfo['reports']['tooltip'] 
    newReports = HDLmTree.buildTreeNode('Reports',       \
                                        'reports',       \
                                        tooltip,         \
                                        nodePathReports, \
                                        companyTreeNode, \
                                        updateDatabase)
    # Add the new Rules child to the new company 
    nodePathRules = list(nodePathCompanyNode)
    rulesNodeName = HDLmDefines.getString('HDLMRULESNODENAME')
    rulesNodeType = HDLmDefines.getString('HDLMRULESTYPE')
    nodePathRules.append(rulesNodeName)
    tooltip = HDLmModTreeInfo[rulesNodeType]['tooltip']
    newRules = HDLmTree.buildTreeNode(rulesNodeName,   \
                                      rulesNodeType,   \
                                      tooltip,         \
                                      nodePathRules,   \
                                      companyTreeNode, \
                                      updateDatabase)
    return [newData, newLists, newReports, newRules] 
  # This method builds a list of integers from the rule names in
  # the list of rules passed by the caller. Only rules with names
  # that begin with a value passed by the caller are considered.
  # These rules, may or may not, end with a 'nnnn' value. All other
  # rules are just ignored. The 'nnnn' values are extracted and
  # added to a list. The list is returned to the caller. Stated
  # differently, this routine builds a list of numbers used to
  # create unique rule names. 
  @staticmethod
  def buildIntegerListName(ruleNamePrefix, childList):
    childListLen = len(childList) 
    integerList = []
    rulePrefixLen = len(ruleNamePrefix) 
    for i in range(0, childListLen):
      # Get the current rule name 
      childEntry = childList[i]
      currentName = childEntry.nodePath[len(childEntry.nodePath) - 1]
      # Check if the rule name starts with the required prefix.
      # If the rule name does not start with the right prefix,
      # then we can just skip this rule. 
      if currentName.startswith(ruleNamePrefix) == False:
        continue
      # Strip the prefix from the rule name 
      currentName = currentName[rulePrefixLen:]
      # Check if we have anything left. If we don't have anything
      # left, then the rule name was just the prefix and we don't
      # have a numeric suffix (in parenthesis). We can just skip
      # this rule. 
      currentNameLength = len(currentName) 
      if currentNameLength == 0:
        continue
      # At this point the remaining string should consist only
      # of a blank, a left parenthesis, a number, and a right
      # parenthesis. If we have anything else, then we should
      # not use this name. 
      pattern = re.compile("^\\s\\(\\d+\\)$")
      testResult = pattern.search(currentName)
      if testResult == None:
        continue
      # We can now add the integer to the list 
      currentNameMatch = re.findall("\\d+", currentName)
      if currentNameMatch == None:
        continue
      if len(currentNameMatch) == 0:
        errorString = currentName
        HDLmError.buildError('Error', 'Current name did not match', 48, errorString)
        return integerList
      if len(currentNameMatch) > 1:
        errorString = currentName
        HDLmError.buildError('Error', 'Too many matches for current name', 48, errorString)
        return integerList
      currentNumber = int(currentNameMatch[0])
      integerList.append(currentNumber)
    return integerList
  # This routine builds the modification tree. Actually, most of the 
  # tree does not have any details. Of course, rule nodes have details
  # (the actual modifications). However, other node have details as
  # well. 
  #
  # This routine does not really build the tree. This routine returns
  # a set of bytes that can be used to build the tree after the bytes
  # are converted to a string and successfully used.
  #
  # This code is used to build the first part of the pass-through
  # display. A request is sent to a standard server to obtain informtion
  # about whatever companies have been defined so far. 
  #
  # This routine returns a list (two) of values. The first
  # value is binary and must be decoded to get a string. 
  @staticmethod
  def buildModificationTree():
    # Get the string used to load the modifications (rules)
    return HDLmTree.passReadAllRows()
  # This routine builds the node tree using the Python
  # data passed by the caller. The node tree is built
  # from the top (literally) down. When this routine is
  # first invoked, it is pass a None value for the current
  # node. The None value causes this routine to find and
  # build the top node. All other nodes are built as direct
  # and indirect children of the top node
  @staticmethod
  def buildNodeTree(jsonData, curTreeNode):
    # Declare and define a few variables 
    # If the current node is None, then this is the first
    # call to this routine. We need to find an build the
    # top node here. 
    if curTreeNode == None:
      getMatchingNodesTopList = ['Top']
      outArray = HDLmTree.getMatchingEntries(jsonData, 1, getMatchingNodesTopList)
      infoJson = outArray[0]['info']
      curTreeNode = HDLmTree.convertDictToTree(infoJson) 
    # Find all of the children of the current node 
    findLevel = len(curTreeNode.nodePath) + 1
    findNodes = curTreeNode.nodePath
    outArray = HDLmTree.getMatchingEntries(jsonData, findLevel, findNodes)
    outLen = len(outArray)
    # Each of the matching entries is a child of the current entry.
    # add each child entry. 
    curTreeNode.children = []
    for i in range(0, outLen): 
      curInfo = outArray[i]['info']
      curTreeSubNode = HDLmTree.convertDictToTree(curInfo)
      curTreeNode.children.append(curTreeSubNode)
      # tempCurTreeNode = curTreeNode.children.copy()
      # print(tempCurTreeNode) 
      # print(len(curTreeNode.children)) 
      HDLmTree.buildNodeTree(jsonData, curTreeSubNode)
    return curTreeNode
  # This method build a map (actually an object) with entries
  # for all of the parameter numbers that are actually in use.
  # The caller passes a list of child nodes that may or may not
  # have parameter numbers. This routine scans all of the child
  # nodes and uses the parameter numbers (if they can be found)
  # to build the parameter number usage map. For example, if the
  # child nodes used the parameter number 3, two times, then the
  # returned map would have an entry with a key of 3 and a value
  # of two. 
  @staticmethod
  def buildParameterMap(childList):
    # Get the number of children in the child list passed by
    # the caller 
    childListLen = len(childList)
    # Build a map that shows how many times each parameter number
    # is used 
    parmMapDict = dict()
    # Check all of the children of the parent node 
    for i in range(0, childListLen):
      # Get the current child 
      childEntry = childList[i]
      # Try to obtain the parameter number of the current rule 
      if hasattr(childEntry, 'details') == False:
        continue
      if hasattr(childEntry.details, 'parameter') == False:
        continue
      childParmNumber = childEntry.details.parameter
      # Check if the parameter map already has the current parameter
      # number. If the parameter map already has the current parameter
      # number, increment the count value. Otherwise, create the map
      # entry with a count of 1. 
      if (childParmNumber in parmMapDict) == False:
        parmMapDict[childParmNumber] = 1
      else:
        parmMapEntryCount = parmMapDict[childParmNumber]
        parmMapEntryCount += 1
        parmMapDict[childParmNumber] = parmMapEntryCount
    return parmMapDict 
  # This routine either finds (locates) or builds a site tree
  # node for a given node path. If new tree nodes need to be
  # created, they are added to the node tree and sent to the
  # server to be added to the database. It is assumed (and
  # checked) that the top node and companies node already
  # exist. The eventual site node is returned to the caller.
  # The caller must pass a complete node path all the way down
  # to the site node. 
  @staticmethod
  def buildSiteNode(passedNodePath, updateDatabase, treeNodeType):
    # Check the value(s) passed by the caller 
    if str(type(passedNodePath)) != "<class 'list'>":
      errorText = f'Node path value (${passedNodePath}) passed to buildSiteNode is not a list'
      HDLmAssert(False, errorText) 
    if (str(type(passedNodePath)) == "<class 'list'>") != True:
      errorText = f'Node path value (${passedNodePath}) passed to buildSiteNode is not a list'
      HDLmAssert(False, errorText) 
    # Make sure the passed node path length is correct 
    passedNodePathLen = len(passedNodePath)
    if passedNodePathLen != HDLmDefines.getNumber('HDLMSITENODEPATHLENGTH'): 
      errorText = f'Passed node path length (${passedNodePathLen}) is incorrect'
      HDLmAssert(False, errorText)
    # Build the node path for getting the companies node 
    nodePath = list(passedNodePath[0:2])
    # At this point we can try to locate the companies node. This
    # step should never fail. However, you never know what is going
    # to fail or not. 
    companiesTreeNode = HDLmTree.locateTreeNode(nodePath)
    # Report an error if the companies node could not be found 
    if companiesTreeNode == None:
      nodeString = str(nodePath)
      HDLmError.buildError('Error', 'Locate', 9, nodeString)
      return None
    # At this point we need to either locate or create the node
    # for the current company 
    hostName = passedNodePath[2]
    nodePath.append(hostName)
    companyTreeNode = HDLmTree.locateTreeNode(nodePath)
    # Create the company node, if the company node could not be found 
    if companyTreeNode == None:
      companyTreeNodeType = HDLmDefines.getString('HDLMCOMPANYTYPE')
      companyTooltip = HDLmTree.getTooltip('newcompmod')
      companyTreeNode = HDLmTree.buildTreeNode(hostName, companyTreeNodeType,
                                               companyTooltip, nodePath,
                                               companiesTreeNode, updateDatabase)
      # At this point we may (or may not) want to do a lot of work
      # to create a Fancytree node for the new company tree node 
      # print(HDLmGlobals.activeEditorType) 
      if not HDLmGlobals.checkForInlineEditorOrGems(): 
        HDLmTree.createCurrentFancytree(companyTreeNode)
    # At this point we should always be able to locate the
    # data or rules node. The data or rules node was created 
    # when the company node was created (if the company node
    # was created). 
    #
    # Check if we are building a node path for a rule or a data value 
    if treeNodeType == HDLmTreeTypes.data:
      nodePath.append(HDLmDefines.getString('HDLMDATANODENAME'))
    if treeNodeType == HDLmTreeTypes.rules:
      nodePath.append(HDLmDefines.getString('HDLMRULESNODENAME'))
    # At this point we can try to locate the rules node. This
    # step should never fail. However, you never know what is
    # going to fail or not. 
    rulesTreeNode = HDLmTree.locateTreeNode(nodePath)
    # Report an error if the rules node could not be found 
    if rulesTreeNode == None:
      nodeString = str(nodePath)
      HDLmError.buildError('Error', 'Locate', 9, nodeString)
      return None
    # Add the division and site nodes, if need be 
    divisionNodeName = HDLmDefines.getString('HDLMDIVISIONNODENAME')
    nodePath.append(divisionNodeName)
    # At this point we need to either locate or create the node
    # for the current division 
    divisionTreeNode = HDLmTree.locateTreeNode(nodePath)
    # Create the division node, if the division node could not be found 
    if divisionTreeNode == None:
      divisionTreeNodeType = HDLmDefines.getString('HDLMDIVISIONTYPE')
      divisionTooltip = HDLmTree.getTooltip('newdivision')
      divisionTreeNode = HDLmTree.buildTreeNode(divisionNodeName, divisionTreeNodeType,
                                                divisionTooltip, nodePath,
                                                rulesTreeNode, updateDatabase)
      # At this point we may (or may not) want to do a lot of work
      # to create a Fancytree node for the new divison tree node 
      # print(HDLmGlobals.checkForInlineEditorOrGems()) 
      # print(HDLmGlobals.activeEditorType) 
      if not HDLmGlobals.checkForInlineEditorOrGems():
        HDLmTree.createCurrentFancytree(divisionTreeNode)
    # Add the site node, if need be 
    siteNodeName = HDLmDefines.getString('HDLMSITENODENAME')
    nodePath.append(siteNodeName)
    # At this point we need to either locate or create the node
    # for the current site 
    siteTreeNode = HDLmTree.locateTreeNode(nodePath)
    # Create the site node, if the site node could not be found 
    if siteTreeNode == None:
      siteTreeNodeType = HDLmDefines.getString('HDLMSITETYPE')
      siteTooltip = HDLmTree.getTooltip('newsite')
      siteTreeNode = HDLmTree.buildTreeNode(siteNodeName, siteTreeNodeType,
                                            siteTooltip, nodePath,
                                            divisionTreeNode, updateDatabase)
      # At this point we may (or may not) want to do a lot of work
      # to create a Fancytree node for the new site tree node 
      if not HDLmGlobals.checkForInlineEditorOrGems():
        HDLmTree.createCurrentFancytree(siteTreeNode)
    return siteTreeNode
  # Build a new tree node and inserts it into the tree. The
  # caller provides all of the information about the new node.
  # The return value is always the new tree node. 
  @staticmethod
  def buildTreeNode(newNodeName,    
                    newNodeType,    
                    newNodeTooltip, 
                    newNodePath,    
                    parentTreeNode, 
                    updateDatabase):
    newNodeLevel = len(newNodePath)
    newTreeNode = HDLmTree(newNodeType, newNodeTooltip, newNodePath)
    newTreeNode.nodePath = list(newNodePath) 
    HDLmPass.addMissingPassObject(newTreeNode)
    # print('In HDLmTree.buildTreeNode') 
    # print(parentTreeNode) 
    # print(newNodeName) 
    #
    # Search for the first existing node with a name that is
    # greater than or equal to the current name. We must insert
    # the new subnode just before the node with a higher name. 
    subPos = -1
    childCounter = 0
    for childNode in parentTreeNode.children: 
      childCounter += 1
      if childNode.nodePath[len(childNode.nodePath) - 1] >= newNodeName:
        subPos = childCounter - 1
        break
    # If we did not find an existing node with a name that is
    # greater than or equal to the current name. We must insert
    # the new subnode at the end of the children array. Note
    # that the children array may be empty. 
    if subPos == -1:
      subPos = len(parentTreeNode.children)
    # Insert the new subnode in the correct position 
    parentTreeNode.children.insert(subPos, newTreeNode)
    if newNodeType == 'company':
      # Build the standard/required subnodes of the company node
      # and add them to the company node 
      HDLmTree.buildCompanyNode(newTreeNode, updateDatabase)
    HDLmPass.addMissingPassObject(parentTreeNode)
    # Add the new tree node to the list (actually an array) of
    # pending inserts. Eventually, all of these nodes will be
    # added to the nodes database maintained by the server. 
    if updateDatabase == True:
      processSubNodesFalse = False
      HDLmTree.addPendingInserts(newTreeNode, processSubNodesFalse) 
    return newTreeNode 
  # Convert a dictionary to an instance of the HDLmTree class.
  # The new instance is returned to the caller. Specific fields
  # are copied from the dictionary to the new HDLmTree instance. 
  @staticmethod
  def convertDictToTree(infoJsonDict):
    # Build the new tree node
    curTreeNode = HDLmTree(infoJsonDict['type'], infoJsonDict['tooltip'], [])
    # Finish building the new tree node
    if 'details' in infoJsonDict:
      curTreeNode.details = HDLmMod.convertDictToMod(infoJsonDict['details'])
    if 'id' in infoJsonDict:
      curTreeNode.id = infoJsonDict['id']
    if 'nodePath' in infoJsonDict:
      curTreeNode.nodePath = infoJsonDict['nodePath'].copy()
    return curTreeNode  
  # This routine checks all of the subnodes of the parent node passed
  # to it and counts the number of subnodes with matching names. The
  # number of subnodes with matching names may be zero or greater than
  # zero. The name matching algorithm is caseless. In other words, ABCD
  # is deemed to match abcd. Note that ABCD (2) will also match abcd if
  # the remove tails flag is set to true. If the remove tails flag is
  # set to false, then ABCD (2) will not match ABCD.
  #
  # A none value can be (and is in some cases) passed for current tree
  # node to force all of the children of the parent tree node to be
  # checked. Passing a none value for current tree node is not an error
  # condition.
  #
  # The removal of file number tails (such as (2)) is actually optional.
  # The caller passes a flag that controls this behavior. If the flag
  # is set to true, then file number tails are removed. If this flag
  # is set to false, then file number tails are not removed. 
  @staticmethod
  def countSubNodeNames(nodeName, parentTreeNode, currentTreeNode,
                        removeTails):
    # print('countSubNodeNames') 
    # tempParentTreeNode = Object.assign({}, parentTreeNode) 
    # tempParentTreeNodeChildren = list(parentTreeNode.children) 
    # print(tempParentTreeNode) 
    # print(tempParentTreeNodeChildren) 
    # print(len(tempParentTreeNodeChildren)) 
    # tempCurrentTreeNode = Object.assign({}, currentTreeNode) 
    # print(tempCurrentTreeNode) 
    # print(removeTails) 
    matchObj = types.SimpleNamespace()
    matchObj.matchCount = 0
    matchObj.matchArray = []
    # The code below will convert the file name passed by the caller
    # in two ways. First any numeric file number tail (such as (2)) will
    # be removed. The file name will then be converted to lower case. Note
    # that the file name may not have a file number tail. This is not an
    # error condition. 
    if removeTails:
      nodeName = HDLmString.removeFileNumberTail(nodeName)
    nodeName = nodeName.lower()
    # Check all of the names in the subnodes of the current parent node 
    # print(len(parentTreeNode.children)) 
    for i in range(0, len(parentTreeNode.children)): 
      # print(i) 
      # Check if the we are checking against ourself. We don't need to
      # check for a match in our own node. 
      if currentTreeNode != None and \
         currentTreeNode == parentTreeNode.children[i]:
        continue
      # print(len(parentTreeNode.children)) 
      # Get the subnode name with the file number tail removed (if any)
      # and converted to lower case 
      childEntry = parentTreeNode.children[i]
      siblingName = childEntry.nodePath[len(childEntry.nodePath) - 1]
      # print(i) 
      # print(siblingName) 
      # print(parentTreeNode) 
      # print(parentTreeNode.children[i]) 
      siblingNameSave = siblingName
      if removeTails:
        siblingName = HDLmString.removeFileNumberTail(siblingName)
      siblingName = siblingName.lower()
      # Check if the names match exactly 
      # print(i) 
      # print(siblingName) 
      # print(nodeName) 
      if siblingName == nodeName:
        matchObj.matchCount = matchObj.matchCount + 1
        matchObj.matchArray.append(siblingNameSave)
    return matchObj
  # Create a new Fancytree node and add it to the Fancytree 
  # node tree. This is only done in some cases. 
  #
  # Of course, we don't really have a Fancytree to work with 
  # in the Python environment. For Python just return to the 
  # caller. 
  @staticmethod
  def createCurrentFancytree(currentTreeNode):
    pass
  # This method scans a parameter number usage map to find the
  # parameter number that is used the least. The least used
  # parameter number is returned to the caller. Note that if
  # the parameter map does not have any information for a
  # parameter number, then the usage is assumed to be zero. 
  @staticmethod
  def findLowestParameter(parmMap):
    maxParameterCount = HDLmDefines.getNumber('HDLMMAXPARAMETERCOUNT')
    maxValue = math.inf
    # Check all of the parameter numbers looking for the one
    # that is used the least 
    for i in range(0, maxParameterCount):
      # Check if the parameter map passed by the caller has an
      # entry for the current parameter number 
      if i in parmMap:
        currentCount = parmMap[i]
      else:
        currentCount = 0
      # Check if the current count is less that lowest value
      # we have seen so far 
      if currentCount < maxValue:
        maxValue = currentCount
        minParm = i
        # If the current count is zero, then we really don't
        # need to keep searching. We are done at this point. 
        if currentCount == 0:
          break
    return minParm
  # This routine extracts all of the ID values from a set
  # of text passed by the caller and returns an array of
  # ID values The response text came from a read all
  # operation that returned all of the rows with a
  # specific content value. 
  @staticmethod
  def getIdArray(responseText):
    # Declare and define a few values 
    idArray = []
    # Extract all of the ID values from the response text 
    # print('getIdArray') 
    # print(responseText) 
    responseJson = jsons.loads(responseText)
    # print(responseJson) 
    responseData = responseJson['data']
    # print(responseData) 
    rowCount = len(responseData)
    # Process each of the rows 
    for i in range(0, rowCount):
      rowDict = responseData[i]
      rowId = rowDict['id']
      idArray.append(rowId)
    return idArray
  # This routine scans the input array and returns all
  # of the matching entries in the output array. For an
  # entry to match, the entry must have the correct
  # level number and the node array passed by the
  # caller must match the node array of the entry.
  # The node array passed by the caller is compared to
  # the node array of each entry by comparing each
  # entry in both arrays.
  @staticmethod
  def getMatchingEntries(inArray, level, matchingNodePath):
    # Declare and define a few values 
    inLen = len(inArray)
    nodesLen = len(matchingNodePath)
    outArray = []
    # Scan the input array looking for matches 
    for i in range(0, inLen): 
      # Get the current array entry 
      curEntry = inArray[i]
      # Check if the array entry is at the correct level 
      if level != len(curEntry['info']['nodePath']):
        continue
      entryNodeArray = curEntry['info']['nodePath']
      # Make sure that the node arrays match 
      nodeMismatch = False
      for j in range(0, nodesLen): 
        if matchingNodePath[j] != entryNodeArray[j]:
          nodeMismatch = True
          break 
      # Check if we found a node array mismatch 
      if nodeMismatch == True:
        continue
      # At this point, we have an array entry that
      # passed all of the tests 
      outArray.append(curEntry)
    return outArray
  # Get a parameter number for use by the caller. The parameter
  # number is typically used to build a new modification (rule).
  # This routine  will return a none value if a new parameter 
  # number can not be obtained for some reason. 
  @staticmethod
  def getParameterNumber(currentTreeNode):
    newParameterNumber = None
    # Try to locate the parent tree node 
    currentTreeNodePath = currentTreeNode.nodePath
    parentTreeNode = HDLmTree.locateTreeParentNode(currentTreeNodePath)
    # Report an error if the parent node could not be found 
    if parentTreeNode == None:
      nodeString = str(currentTreeNodePath)
      HDLmError.buildError('Error', 'Locate', 9, nodeString)
      return 
    # Build a map that shows how many times each parameter number 
    # is used 
    childList = parentTreeNode.children
    parmMapObj = HDLmTree.buildParameterMap(childList)
    if parmMapObj == None:
      return
    # Get the lowest parameter number 
    minParameterNumber = HDLmTree.findLowestParameter(parmMapObj)
    newParameterNumber = minParameterNumber
    return newParameterNumber 
  # Get the Tooltip value for the current node. This code is in a
  # separate routine so that it can be invoked from several places. 
  @staticmethod
  def getTooltip(type):
    if type == 'newauth':
      tooltip = HDLmModTreeInfo['auth']['tooltip']
    elif type == 'newcompgem':
      tooltip = HDLmModTreeInfo['compgem']['tooltip']
    elif type == 'newcompgxe':
      tooltip = HDLmModTreeInfo['compgxe']['tooltip']
    elif type == 'newcompignore':
      tooltip = HDLmModTreeInfo['compignore']['tooltip']
    elif type == 'newcompmod':
      tooltip = HDLmModTreeInfo['compmod']['tooltip']
    elif type == 'newcomppass':
      tooltip = HDLmModTreeInfo['comppass']['tooltip']
    elif type == 'newcomppopup':
      tooltip = HDLmModTreeInfo['comppopup']['tooltip']
    elif type == 'newcompproxy':
      tooltip = HDLmModTreeInfo['compproxy']['tooltip']
    elif type == 'newcompsimple':
      tooltip = HDLmModTreeInfo['compsimple']['tooltip']
    elif type == 'newcompstore':
      tooltip = HDLmModTreeInfo['compstore']['tooltip']
    elif type == 'newconfig':
      tooltip = HDLmModTreeInfo['config']['tooltip']
    elif type == 'newdivision':
      tooltip = HDLmModTreeInfo['division']['tooltip']
    elif type == 'newignore':
      tooltip = HDLmModTreeInfo['ignore']['tooltip']
    elif type == 'newlist':
      tooltip = HDLmModTreeInfo['list']['tooltip']
    elif type == 'newlists':
      tooltip = HDLmModTreeInfo['lists']['tooltip']
    elif type == 'newmod':
      tooltip = HDLmModTreeInfo['mod']['tooltip']
    elif type == 'newsite':
      tooltip = HDLmModTreeInfo['site']['tooltip']
    elif type == 'newstore':
      tooltip = HDLmModTreeInfo['store']['tooltip']
    elif type == 'newvalue':
      tooltip = HDLmModTreeInfo['value']['tooltip']
    else:
      # Build the Tooltip information
      typeInfo = HDLmMod.getModificationTypeInfo(type)
      if typeInfo != None:
        tooltip = typeInfo['longname']
      else:
        tooltip = type
      tooltip = HDLmString.ucFirst(tooltip) + ' ' + 'modification'
    return tooltip
  # This routine returns the rule tree top (if any) to caller 
  @classmethod
  def getTreeTop(cls):
    return HDLmTree.top
  # Locate (find) a Fancytree node using a node path
  #
  # We have no Fancytree in the Python environment 
  @staticmethod
  def locateFancyNode(nodePath):
    # The following code should never be executed in the Python 
    # environment. Report an error, if this code is ever reached.
    errorText = 'This code should neve be executed. We have no Fancytree under Python.' 
    HDLmAssert(False, errorText)
    return None
  # Locate (find) the parent of a Fancytree node using a node path 
  #
  # We have no Fancytree in the Python environment   
  @staticmethod
  def locateFancyParentNode(nodePath, reportFancyLocateErrors):
    # The following code should never be executed in the Python 
    # environment. Report an error, if this code is ever reached.
    errorText = 'This code should neve be executed. We have no Fancytree under Python.' 
    HDLmAssert(False, errorText)
    return None
    
  # This routine returns the root of the Fancytree
  #
  # We have no Fancytree in the Python environment   
  @staticmethod
  def locateFancyRootNode():
    # The following code should never be executed in the Python 
    # environment. Report an error, if this code is ever reached.
    errorText = 'This code should neve be executed. We have no Fancytree under Python.' 
    HDLmAssert(False, errorText)
    return None
  # Locate (find) a tree node using a node path. A node path is all of the
  # names that lead a node. The first entry in the tree node path is for
  # the top tree node. This is required so that this function can find
  # the top tree node. This routine will return the target node if it is
  # found. If the target node can not be found, this routine will return
  # a None value. 
  @classmethod
  def locateTreeNode(cls, nodePath):
    # Get and check the node path length
    nodePathLength = len(nodePath)
    if nodePathLength <= 0:
      errorText = f'Length of passed node path is less than or equal to zero'
      HDLmAssert(False, errorText)
    # Process all of the nodes in the node path
    for i in range(0, nodePathLength):
      currentName = nodePath[i]
      # Check if we are handling level 1. Level 1 is always the
      # top-level node and does not have to be found in the same
      # way.  
      if i == 0:
        currentNode = HDLmTree.getTreeTop()
        continue
      # print(i) 
      # print(currentName) 
      # print(currentNode) 
      # print(currentNode.children) 
      # We are not handling level 1. Use the current node to get
      # the array of child nodes. Search the array of child nodes. 
      childNodes = currentNode.children
      childNodesLen = len(childNodes)
      currentNode = None
      # Process (check for a matching name) all of the child nodes
      for j in range(0, childNodesLen):
        childNode = childNodes[j]
        childNodeNodePath = childNode.nodePath
        childNodeNodePathLen = len(childNodeNodePath)
        childNodeLastName = childNodeNodePath[childNodeNodePathLen-1]
        # Check if the last name in the node path matches or not
        if currentName != childNodeLastName:
          continue
        # The last name does match the name we are looking for 
        currentNode = childNode
        break
    return currentNode
  # Locate (find) the parent of a node using a node path. A node path
  # is all of the names that lead a node. The first entry in the node path
  # is for the top node. This is required so that this function can find
  # the top node. This routine will return the parent node if it is found
  # If the parent node can not be found, this routine will return a none
  # value. 
  @staticmethod
  def locateTreeParentNode(nodePath):
    parentNode = None
    nodePathLength = len(nodePath)
    # Report an error if the node path is not long enough 
    if nodePathLength < 2:
      nodePathString = str(nodePath)
      HDLmError.buildError('Error', 'Invalid', 21, nodePathString)
      return parentNode
    # Make a copy of the node path and remove the last element.
    # The remaining node path can be used to locate the parent
    # node of the current node. 
    parentPath = nodePath[0:nodePathLength - 1]
    # Search for the parent node in the node tree 
    parentNode = HDLmTree.locateTreeNode(parentPath)
    # Report an error if the node could not be found 
    if parentNode == None:
      parentNodeString = str(parentPath)
      HDLmError.buildError('Error', 'Locate', 9, parentNodeString)
      return parentNode 
    return parentNode 
  # This code inserts zero or more rows into the database. The caller
  # passes an array with zero or more entries. A string is returned
  # to the caller. 
  @staticmethod
  def passInsertRows(content, infoArray):
    # Declare and define one or more variables 
    infoLen = len(infoArray)
    newStr = ''
    # Process each entry in the data array 
    for i in range(0, infoLen):
      kvAdded = False
      # Separate each of the objects, if need be 
      if newStr != '':
        newStr += ', '
      # Start the current object 
      newStr += '{ '
      # Check and add the content string 
      if content != None and \
         content != '':
        if kvAdded:
          newStr += ', '
        newStr += '"content": ' + '"' + content + '"'
        kvAdded = True
      # Check the information JSON string. A string is passed
      # in this case. The conversion to JSON is done by the
      # server. 
      infoEntry = infoArray[i]
      if infoEntry != None and \
         infoEntry != '':
        if kvAdded:
          newStr += ', '
        newStr += '"info": ' + infoEntry
        kvAdded = True
      # Check the information name string. A string is passed
      # in this case. 
      if 1 == 1:
        infoEntryDict = jsons.loads(infoEntry)
        if infoEntryDict != None:
          infoEntryNodePath = infoEntryDict['nodePath']
          infoEntryNodePathLen = len(infoEntryNodePath)
          infoEntryDictName = infoEntryNodePath[infoEntryNodePathLen - 1]
          if infoEntryDictName != None                            and \
             str(type(infoEntryDictName)) != "<class 'NoneType'>" and \
             infoEntryDictName != '':
            if kvAdded:
              newStr += ', '
            newStr += '"name": ' + '"' + infoEntryDictName + '"'
            kvAdded = True
      # Finish the current object 
      newStr += ' }'
    # We can now try to insert the new nodes 
    URL = HDLmConfigInfo.getEntriesBridgeInternetMethod() + "://" + \
            HDLmConfigInfo.getEntriesBridgeInsertUrl() + "" +       \
            HDLmConfigInfo.getEntriesBridgeTableSeparate() + ""
    userid = HDLmConfigInfo.getEntriesBridgeUserid()
    password = HDLmConfigInfo.getEntriesBridgePassword()
    # print(newStr) 
    # Build the final insertion string 
    inStr = '{ "data": [ ' + newStr + ' ] }'
    # The call below returns a Promise. The Promise is not used at
    # this time. The data must be URI encoded before it is sent.
    # This step is required to preserve characters such as the
    # plus sign. Note that this code has been changed. The URI
    # encoding is now done by the call below in some cases. 
    requestAsyncTrue = True
    [responseBinary, responseCode] = HDLmUtility.runAJAX('URL', 
                                                         requestAsyncTrue, URL, 
                                                         userid, 
                                                         password, 
                                                         'post', 
                                                         inStr)
    responseTextStr = responseBinary.decode('UTF-8')
    return responseTextStr
  # This code reads all of the rows from the database and returns
  # the rows to the caller. When this call completes all of the
  # rows will be in the response text. The set of rows depends on
  # the current content type. The current content type depends on
  # the current editor type. 
  #
  # This routine returns a list (two) of values. The first
  # value is binary and must be decoded to get a string.
  @staticmethod
  def passReadAllRows():
    # We can now try to get the modifications or proxy definitions
    # or anything else 
    URL = HDLmConfigInfo.getEntriesBridgeInternetMethod() + "://" + \
          HDLmConfigInfo.getEntriesBridgeReadUrl() + "" +           \
          HDLmConfigInfo.getEntriesBridgeTableSeparate() + ""
    # The content type shows if we are handling modifications,
    # proxy definitions, or configurations. The value returned
    # below is a string, not a numeric value (such as enums
    # typically are).  
    queryStr = ''
    queryStr += '?'
    queryStr += HDLmUtility.buildBridgeRestQuery('content')
    URL += queryStr
    # print(queryStr) 
    # Get the userid and password from the configuration information 
    userid = HDLmConfigInfo.getEntriesBridgeUserid()
    password = HDLmConfigInfo.getEntriesBridgePassword()
    # Get the JSON that contains the modifications
    requestAsyncTrue = True
    return HDLmUtility.runAJAX('URL', requestAsyncTrue, URL, userid, password)
  # This code updates one row (one node) in the server. The node could
  # also be some other type of node. For example, it could be a report
  # node. 
  @staticmethod
  def passUpdateOneTreePos(treePos, newTreeEntryBoolean):
    # print('In HDLmTree.passUpdateOneTreePos', treePos, newTreeEntryBoolean) 
    #
    # Get the current ID value. This value may or may not be 
    # available. If this routine is invoked by one of the 
    # inline editor (indirectly), then we won't have an ID
    # value at this point. Of course, we can't do an update
    # of the database without an ID value. 
    idValue = None
    if hasattr(treePos, 'id'):
      idValue = treePos.id
    # Create a temporary copy of the current tree node. This is
    # done so that we can make changes to the temporary copy that
    # will not affect the original tree node. 
    tempPos = copy.deepcopy(treePos)
    if hasattr(tempPos, 'children'):
      del tempPos.children
    if hasattr(tempPos, 'containerWidget'):
      del tempPos.containerWidget
    if hasattr(tempPos, 'id'):
      del tempPos.id
    # Remove the saved details from the current node, if need be 
    if hasattr(tempPos, 'savedDetails'):
      del tempPos.savedDetails
    # Fix the details (an HDLmMod) so that the stringify will work 
    if hasattr(tempPos, 'details'):
      tempDetails = copy.deepcopy(tempPos.details)
      # If the current set of details are going to be sent to a server
      # using web sockets, then we really don't want to change the name
      # of the path field 
      if hasattr(tempDetails, 'pathValue') and \
         HDLmGlobals.checkForInlineEditorOrGems() == False:
        tempDetails.path = tempDetails.pathvalue
        del tempDetails.pathvalue
        # print(tempDetails)  
      tempPos.details = tempDetails 
    data = jsons.dumps(tempPos)
    # Check if we are actually using one of the inline editors or if
    # we are in the GEM environment or the GXE environment. If this 
    # is true, then we really don't want to update the database at 
    # this point. 
    if HDLmGlobals.checkForInlineEditorOrGems() == False:
      # print('passUpdateOneTreePos') 
      # Try to actually update the node (row) 
      # print('about to passUpdateRow') 
      # Check if we really have an ID value here. We can't
      # update the database without a valid ID value. 
      if idValue != None:
        HDLmTree.passUpdateRow(idValue, data)
      else:
        errorText = 'ID value is None in passUpdateOneTreePos'
        HDLmAssert(False, errorText) 
    # Since we are using one of the inline editors or we are running 
    # in the GEM environmentor or the GXE environment, we don't really
    # want to try to update the database here. We do want to send 
    # the update to the server for processing. 
    else:
      # print('newTreeEntryBoolean') 
      # print(newTreeEntryBoolean) 
      if HDLmGlobals.activeNodeType == None or \
         HDLmGlobals.activeNodeType.startswith('new') == False: 
        # print('passUpdateOneTreePos') 
        # This code is no longer in use. The divs are deleted when the 
        # user presses enter, not when an update is done. The update is
        # done as need be. However, the div is deleted when the user, 
        # uses the delete or esacpe key or when the mouse is clicked 
        # outside of the div. 
        if 1 == 2 and (HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
                       HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe):
          # print('In passUpdateOneTreePos, about to delete divs') 
          #
          # The following code should never be executed in the Python 
          # environment. Report an error, if this code is ever reached.
          errorText = 'This code should neve be executed. HDLmMenus can not be imported.' 
          HDLmAssert(False, errorText)
          # HDLmMenus.clearPending()
          # The following code should never be executed in the Python 
          # environment. Report an error, if this code is ever reached.
          errorText = 'This code should neve be executed. HDLmGEM has not been ported.'
          HDLmAssert(False, errorText)
          # HDLmGEM.deleteDivs()
        # print('sendUpdateTreeNodeRequest') 
        HDLmWebSockets.sendUpdateTreeNodeRequest(tempPos)
        if HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
           HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
          # The next statement forces the current window to reload.
          # This is needed so that the latest (possibly changed)
          # modifications will be used. This code is no longer in
          # use. The window is reloaded by other code, elsewhere. 
          # How and where and when the window is reloaded is not
          # clear. The above comment is of unknown origin. 
          # window.location.href = window.location.href 
          # treeTop = HDLmTree.getTreeTop() 
          # print(treeTop)  
          pass      
        # Check for the GUI extended editor  
        if HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
          # The next statement forces the current window to reload.
          # This is needed so that the latest (possibly changed)
          # modifications will be used.  
          pass
        # Set a flag (but only for the GXE editor) showing that 
        # at least one rule has been updated 
        HDLmExtensionBothManageRules.rulesUpdatedSet()  
    return  
  # This code updates one row (one node) in the server. The node could
  # also be some other type of node. For example, it could be a report
  # node. 
  @staticmethod
  def passUpdateRow(id, data):
    # Declare and define one or more variables 
    newStr = ''
    # Check the ID string 
    if id != None and \
       id != '':
      if newStr != '':
        newStr += ', '
      newStr += '"id": ' + '"' + id + '"' 
    # Check the data JSON string. A string is passed in this case.
    # The conversion to JSON is done by the server. 
    if data != None and \
       data != '':
      if newStr != '':
        newStr += ', '
      newStr += '"info": ' + data 
    # Check the data name string. A string is passed
    # in this case. 
    if 1 == 1:
      if data != None:
        dataObj = jsons.parse(data)
        dataNodePath = dataObj['nodePath']
        dataNodePathLength = len(dataNodePath)
        dataObjName = dataNodePath[dataNodePathLength - 1] 
        if dataObjName != None and \
           dataObjName != '':
          if newStr != '':
            newStr += ', '
    # We can now try to insert the new node 
    API = HDLmConfigInfo.getEntriesBridgeApi()
    URL = HDLmConfigInfo.getEntriesBridgeInternetMethod() + "://" + \
                HDLmConfigInfo.getEntriesBridgeUpdateUrl() + "" +   \
                HDLmConfigInfo.getEntriesBridgeTableSeparate() + ""
    if API == 'bucket':
      URL += ''
    userid = HDLmConfigInfo.getEntriesBridgeUserid()
    password = HDLmConfigInfo.getEntriesBridgePassword() 
    # Build the final insertion string 
    inStr = '{ "data": [ { ' + newStr + ' } ] }'
    # print(newStr) 
    # The call below returns a Promise. The Promise is not used at
    # this time. The data must be URI encoded before it is sent.
    # This step is required to preserve characters such as the
    # plus sign. Note that this code has been changed. The URI
    # encoding is now done by the call below in some cases. 
    requestAsyncTrue = True
    HDLmUtility.runAJAX('URL', requestAsyncTrue, URL, userid, password, 'post', inStr)
    return 
  # This code inserts zero or more rows into the database. One row
  # is created for each pending insert. The caller does not pass
  # anything. The array of pending inserts may be empty. This is
  # not an error condition. Of course, nothing will be done in
  # this case. When the server responds with a set of ID values,
  # the ID values are extracted and added to each tree node. 
  @staticmethod
  def processPendingInserts():
    # Declare and define a few variables  
    # Build the content string for use below. 
    content = HDLmUtility.getContentString()
    # Get the data values from the pending inserts. Note that
    # a shallow copy is made here so that the actual pending
    # inserts array can be cleared. 
    treeDataArray = list(HDLmTree.pendingInserts)
    HDLmTree.pendingInserts.clear()
    if len(treeDataArray) == 0:
      return  
    # print('processPendingInserts') 
    # Insert all of the rows associated with the tree 
    responseText = HDLmTree.passInsertRows(content, treeDataArray)
    # We can now wait from the Promise to complete 
    if responseText != None:
      treeIdArray = HDLmTree.getIdArray(responseText)
      # The ID values returned by the insert must be stored in each
      # node in the node tree 
      HDLmTree.resetIdValues(treeIdArray, treeDataArray)
    else:
      errorText = 'passInsertRows failed'
      # print(errorText) 
      HDLmError.buildError('Error', 'Pending inserts failure', 14, errorText) 
    return   
  # This routine resets a count field after a node is cut,
  # deleted, inserted, pasted, etc. The count is always
  # in the details of the parent node. The parent is the
  # parent of the node that was just deleted. 
  @staticmethod 
  def resetCountField(currentNodePath):
    # At this point, we must consider a very special case. The parent of
    # the deleted tree node, may have a count field that needs to be fixed
    # to take into account the restoration of the tree node. 
    if HDLmGlobals.activeEditorType != HDLmEditorTypes.passEnum and \
       HDLmGlobals.checkForInlineEditorOrGems() == False:
      return
    # Make a copy of the node path passed by the caller. Since we
    # need to changes to this node path, we must first make a copy. 
    localNodePath = list(currentNodePath)
    localNodePath.pop()
    # Try to find the parent node. This should never fail. 
    parentTreeNode = HDLmTree.locateTreeNode(localNodePath)
    # Report an error if the parent node could not be found 
    if parentTreeNode == None:
      nodeString = str(localNodePath)
      HDLmError.buildError('Error', 'Locate', 9, nodeString)
      return
    # Some parent nodes will not have any details and as a
    # consequence, they won't have any count fields that
    # need to be adjusted. If the parent node has no details,
    # then we are done at this point. 
    if (hasattr(parentTreeNode, 'details') == False):
      return
    # Make sure the parent node has details 
    if (hasattr(parentTreeNode, 'details') == False):
      errorString = 'details'
      HDLmError.buildError('Error', 'Missing field', 11, errorString)
      return
    # Make sure the parent node has children 
    if (hasattr(parentTreeNode, 'children') == False):
      errorString = 'children'
      HDLmError.buildError('Error', 'Missing field', 11, errorString)
      return 
    # Fix the count field in the parent object 
    HDLmPass.addMissingPassObject(parentTreeNode) 
  # This routine reset ID values in the node tree. We need to have
  # the actual ID values in each node so that the node can be deleted
  # and/or updated. This routine is passed an array of ID values and
  # an array of node information. The node information is used to find
  # the actual nodes that are then updated with current ID information. 
  @staticmethod
  def resetIdValues(idArray, infoArray):
    # Make sure the argument is an array 
    if (str(type(idArray)) == "<class 'list'>") == False:
      errorText = 'idArray passed to resetIdValues method is not an array'
      HDLmAssert(False, errorText) 
    # Make sure the argument is an array 
    if (str(type(idArray)) == "<class 'list'>") == False:
      errorText = 'infoArray passed to resetIdValues method is not an array'
      HDLmAssert(False, errorText)
    # Get the lengths of each array. The lengths must be equal. 
    idArrayLen = len(idArray)
    infoArrayLen = len(infoArray)
    if idArrayLen != infoArrayLen:
      errorText = f'idArray length (${idArrayLen}) is not equal to infoArray length (${infoArrayLen})'
      HDLmAssert(False, errorText)  
    # Process each entry in the info array 
    for i in range(0, infoArrayLen):
      infoArrayEntry = infoArray[i]
      infoArrayEntryDict = jsons.loads(infoArrayEntry)
      infoEntryNodePath = infoArrayEntryDict['nodePath']
      # Try to find the node in the node tree we are looking for 
      infoEntryNode = HDLmTree.locateTreeNode(infoEntryNodePath)
      # Report an error if the node could not be found 
      if infoEntryNode == None:
        nodeString = str(infoEntryNodePath)
        # print('HDLmTree.resetIdValues') 
        HDLmError.buildError('Error', 'Locate', 9, nodeString)
        return False 
      # Get the new and old ID values 
      oldIdValue = infoEntryNode.id
      newIdValue = idArray[i]
      infoEntryNode.id = newIdValue 
    return True 
  # This routine sets the rule tree top using a value passed
  # by the caller 
  @classmethod
  def setTreeTop(cls, newTreeTop):
    HDLmTree.top = newTreeTop
    return
  # This routine will perform a set of update related operations.
  # The operations depend on what editor is currently in use and
  # what type of node is being updated. 
  @staticmethod 
  def updateRelatedOperations(currentTreeNodePath):
    # print('In HDLmTree.updateRelatedOperations') 
    #
    # We only need to update count values if the GUI editor or the 
    # GXE editor or the pass-through editor or one of the inline
    # editors is in use 
    if HDLmGlobals.activeEditorType == HDLmEditorTypes.passEnum or \
       HDLmGlobals.checkForInlineEditorOrGems():
      # In some cases, we may heed to update a count field in a parent
      # node. This is not always true.  
      HDLmTree.resetCountField(currentTreeNodePath)
    # The call below will always update the rules on the server.
    # The current window will only be reloaded if we are running
    # one of the inline editors. 
    if HDLmGlobals.checkForInlineEditor():
      callFromCallbackFalse = False
      HDLmMod.handleUpdateReloadPageUnconditional(callFromCallbackFalse)
  # The method below is passed a string and a node path.
  # The node path uniquely identifies a node that should
  # be updated with the perceptual hash information. The
  # string provides the perceptual hash information when 
  # it is used. 
  @staticmethod
  def usePerceptualString(newString, nodePath):
    # Search for the current node in the node tree  
    currentTreeNode = HDLmTree.locateTreeNode(nodePath)
    # Report an error if the node could not be found  
    if currentTreeNode == None:
      nodeString = str(nodePath) 
      HDLmError.buildError('Error', 'Locate', 9, nodeString) 
      return
    # Make sure the current node can be updated properly. 
    # If the current node can be updated properly, then
    # save the perceptual hash value.  
    if hasattr(currentTreeNode, 'details')                 and \
       hasattr(currentTreeNode.details, 'nodeiden')        and \
       'attributes' in currentTreeNode.details.nodeiden:
      newDict = jsons.loads(newString) 
      perceptualHashStr = newDict['phash']
      currentTreeNode.details.nodeiden['attributes']['phash'] = perceptualHashStr
      # At this point we can and should send the updated tree node 
      # back to the server that owns and updates the database 
      newTreeEntryBooleanFalse = False
      updateOutput = HDLmTree.passUpdateOneTreePos(currentTreeNode, 
                                                   newTreeEntryBooleanFalse)   