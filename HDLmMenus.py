# Class for providing a set of menu functions. No instances of this
# class are ever created.  

from HDLmGlobals  import *
from HDLmGXE      import *
from HDLmMod      import *
from HDLmPass     import *
from HDLmString   import *
from HDLmTree     import *
from HDLmUtility  import *

class HDLmMenus(object):
  # The next method will adjust a new tree node name as need
  # be. The basic idea is that every tree node name must be
  # unique (at least under a specific site node). The routine
  # will build a unique tree node name and return it to the
  # caller if need be. 
  #
  # This check is caseless and any file numbers are potentially
  # stripped from each node name. That means that FONT and font
  # are treated as equal. It also means that Font (2) and font
  # are potentially treated as equal. Note that this conversion 
  # is only done for tree node name checking. Mixed case tree node
  # names are stored in mixed case. That means that name checking
  # is caseless, while names are actually stored in their original
  # case (which may be mixed case).
  #
  # Note that file numbers (such as (2)) are really only removed if 
  # the caller set the remove tails value to true. If this value is
  # set to false, then file numbers will not be removed.  
  @staticmethod
  def adjustTreeNodeName(newNodeName, 
                         parentTreeNode, 
                         removeTails,
                         forceSuffix=False):
    # print('In HDLmMenus.adjustTreeNodeName', newNodeName, parentTreeNode, removeTails) 
    #
    # Get a count of how many times the new tree node name 
    # is already used. Hopefully, this count will be zero. 
    # However, it might not be zero. 
    currentTreeNodeNone = None
    matchObj = HDLmTree.countSubNodeNames(newNodeName, parentTreeNode,
                                          currentTreeNodeNone, removeTails)
    # print(matchObj)     
    # Get and adjust the match count 
    matchCount = matchObj.matchCount
    if forceSuffix:
      matchCount = 1
    # Check if a suffix must be added to the name passed by the caller
    if matchCount > 0:
      childList = parentTreeNode.children
      integerList = HDLmTree.buildIntegerListName(newNodeName, childList)
      # Get the next available tree node number 
      nextInteger = HDLmUtility.getNextInteger(integerList)
      newNodeName += ' (' + str(nextInteger) + ')'
    # abcd = newNodeName 
    # print(abcd) 
    return newNodeName
  # The next method builds a new modification base name using a set  
  # of information passed by the caller. This routine does not store
  # the new modification name anywhere. However, it (the new name)
  # is returned to the caller. The returned name may or may not be 
  # unqiue. The name may or may not already be in use. 
  @staticmethod
  def buildModificationBase(newUrlValueStr, newDetailsType):
    defaultShortModName = HDLmDefines.getString('HDLMSHORTMODNAME')
    # We now have enough information to build the final modification name. 
    # Of course, the final modification name is just a guess. The user will
    # probably have to change the modification name by hand after the new
    # modification has been added. The URL value passed to this routine may
    # already be just a path value. In other words, the protocol and host 
    # name may have already been removed. 
    newModName = defaultShortModName
    # Use the path value to help build the modification name 
    if newUrlValueStr != None:
      newPathString = HDLmUtility.getPathString(newUrlValueStr)
      # Replace all occurences of '-' (without the quotes) with a blank 
      newPathString = newPathString.replace('-', ' ')
      # Replace all occurences of '/' (without the quotes) with a blank 
      newPathString = newPathString.replace('/', ' ')
      newPathString = newPathString.strip()
      if newPathString != '':
        newModName += ' ' + newPathString 
    # Use the modification type to help build the modification name 
    newModName += ' ' + newDetailsType
    # Change the first character of each word to uppercase 
    newModName = HDLmString.ucFirstSentence(newModName)
    return newModName
  # The next method builds a new modification name using a set of 
  # information passed by the caller. This routine does not store
  # the new modification name anywhere. However, it (the new name)
  # is returned to the caller. The returned name will always be
  # unique. A numeric suffix is added as need be to make sure that
  # the name is unique. The URL value passed to this routine may
  # already be just a path value. In other words, the protocol and
  # host name may have already been removed. 
  @staticmethod
  def buildModificationName(parentTreeNode,  
                            newUrlValueStr,  
                            newDetailsType,  
                            removeTails = False):
    # print('In HDLmMenus.buildModificationName') 
    # print(parentTreeNode) 
    # print(newUrlValueStr) 
    # print(newDetailsType) 
    # Get the initial new modification name. This name may be altered
    # by adding a suffix below. 
    newModName = HDLmMenus.buildModificationBase(newUrlValueStr, newDetailsType)
    # print(newModName) 
    #
    # Adjust the modification name (by adding a numeric suffix in parenthesis), if
    # need be 
    newModName = HDLmMenus.adjustTreeNodeName(newModName, parentTreeNode, removeTails)
    # print(newModName) 
    # Return the final (possibly adjusted) modification name to the caller 
    return newModName 
  # The next method clears any pending values showing that we were in 
  # the process of adding a new tree node. This routine must be called
  # to cleanup after a new tree node has been added. It can be called
  # in other cases as well.  
  @staticmethod
  def clearPending():
    # Clear the error message text 
    errorStringEmpty = ''
    HDLmUtility.setErrorText(errorStringEmpty)
    # Clear the global values that show we were adding a new tree node
    # of some type 
    HDLmGlobals.setActiveNodeType(None)
    # Remove the new tree node information from the web page 
    HDLmMod.removeEntries() 
  # The next method adds a data field to the details of a modification
  # as need. A new field does not always need to be added. In some cases,
  # all we really need to do is to delete an old field. This routine
  # returns a value showing if a new field was actually added or not. 
  @staticmethod
  def dataFieldAdd(currentTreeNode, modificationType, invokedBy):
    # We need to reset the tool tip at this point. This is only 
    # possible in some cases. We need to reset the tooltip 
    # because the modification type may have (probably has)
    # changed. 
    if currentTreeNode  != None and \
       modificationType != None:
      # print('s1') 
      # Check if this routine was run out of the modify type list code.
      # This is the only case where the Fancytree node can be obtained. 
      currentFancytreeNode = None
      if invokedBy == 'typelist possible change' and \
         HDLmGlobals.activeEditorType != HDLmEditorTypes.gxe:
        currentFancytreeNode = HDLmTree.locateFancyNode(currentTreeNode.nodePath)
        # Report an error if the Fancytree node could not be found 
        if currentFancytreeNode == None:
          nodeString = str(currentTreeNode.nodePath)
          HDLmError.buildError('Error', 'Locate', 25, nodeString)
          return
      newTreeTooltip = HDLmTree.getTooltip(modificationType)
      # print(newTreeTooltip) 
      # print(modificationType) 
      currentTreeNode.tooltip = newTreeTooltip
      # Reset the Fancytree tooltip if possible 
      if invokedBy == 'typelist possible change':
        if currentFancytreeNode != None:
          currentFancytreeNode.tooltip = newTreeTooltip
          currentFancytreeNode.renderTitle()
      # Remove the parameter property, if the new modification type
      # does not use parameter numbers. 
      if HDLmMod.getModificationTypeParmNumberUsed(modificationType) == False:
        if hasattr(currentTreeNode, 'details') and \
           hasattr(currentTreeNode.details, 'parameter'):
          del currentTreeNode.details.parameter
    # Get the complete set of modification information. Note that this
    # information is used for all tree node types, including companies,
    # divisions, sites, and modifications. 
    modTypeInfo = HDLmMod.getModTypeInfo()
    # print(modTypeInfo) 
    if modificationType == 'newcompproxy' or \
       modificationType == 'inject'       or \
       modificationType == 'HTML':
      # The following code should never be executed in the Python 
      # environment. Report an error, if this code is ever reached.
      errorText = 'This code should neve be executed. HDLmProxy has not been ported.'
      HDLmAssert(False, errorText)
      # modTypeInfo = HDLmProxy.HDLmProxyInfo
    # Get the array of fields for the current node 
    modTypeData = modTypeInfo[modificationType]
    modFields = modTypeData['fields']
    modFieldsLength = len(modFields)
    # Get the name of the last field in the field array 
    modSource = modFields[modFieldsLength - 1]['source']
    # We need to create an empty field in current modification node 
    # in some cases. Of course, if the field already exists, we do 
    # not need to create it. We must also take care to create the 
    # right kind of field, if the field does not exist. 
    newFieldAddedDeleted = False
    # print(currentTreeNode.details, modSource) 
    # print(modFields, modFieldsLength) 
    # print(currentTreeNode.details.hasOwnProperty(modSource)) 
    # print(modFields[modFieldsLength - 1].hasOwnProperty('datatype')) 
    if (hasattr(currentTreeNode.details, modSource) == False) and \
       hasattr(modFields[modFieldsLength - 1], 'datatype'):
      dataType = modFields[modFieldsLength - 1].datatype
      # print(dataType)  
      if dataType == 'array':
        setattr(currentTreeNode.details, modSource, [])
        newFieldAddedDeleted = True 
      elif dataType == 'number':
        setattr(currentTreeNode.details, modSource, None)
        newFieldAddedDeleted = True
      elif dataType == 'text':
        setattr(currentTreeNode.details, modSource, '')
        newFieldAddedDeleted = True 
      # Report an error if the data type did not match one of the expected choices 
      else: 
        errorString = dataType
        HDLmError.buildError('Error', 'Invalid data type', 19, errorString)   
    return newFieldAddedDeleted
  # At this point we may be able to do some work on a new tree node of
  # some type. Of course, we may not be handling a new tree node at this
  # point. However, in some cases work on a new tree node is possible. 
  # The call below will do the work on the new tree node (if one exists)
  # if possible. 
  # 
  # This routine always returns a string to the caller. In some cases, 
  # the string indicates that the required work has been completed and
  # the current modification (which may be a company, division, site, or
  # actual modification) should not be redrawn. This code (in some cases)
  # removes the modification from the web page. In these cases, we don't 
  # want later code to redraw the modification.
  #
  # In at least one case, this routine is used to finish adding a new rule
  # to the database without any user intervention. In at least one case, a
  # new rule was built using node identifier values provided by a browser 
  # extension. Ths new rule may have all of the required fields set. This 
  # code is used to add the new rule to the rule database with any user 
  # intervention or even a display of the new rule.
  # 
  # This routine can be (and is) invoked in several different editor 
  # environments. The editor environment is check in several places 
  # below and different code is use for different environments.   
  @staticmethod
  def finishTreeNode(currentTreeNode, containerAvailable, 
                     possibleRuleTypes, currentDomElement,
                     newTreeEntry, handlingCmdInsert,
                     callFromCallback, needUserInput): 
    # print('In HDLmMenus.finishTreeNode') 
    # rint(containerAvailable) 
    # print(possibleRuleTypes)
    # print(currentDomElement)
    # print(newTreeEntry)
    # print(handlingCmdInsert)
    # print(callFromCallback)
    # print(needUserInput)  
    # print('s15') 
    # print('s14', HDLmGlobals.activeNodeType) 
    # Check if we are debugging the GUI eXtended Editor (GXE). If we are
    # then a special flag is set to true than can be tested below. 
    gxeDebug = False
    if HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe and \
       HDLmGlobals.checkDebuggerStatus() == True:
      gxeDebug = True
    # print(currentTreeNode.details.extra) 
    # Set the return value string to a default value 
    rvStr = '' 
    # We assume that we are not going to be using the WebSocket
    # addTreeNode request type 
    addTreeNodeDone = False
    # We assume that we are not going to insert a new tree node 
    insertIntoDone = False
    # Check if we are really handling a new tree node. If not just
    # return immediately to the caller. This check blocks all of  
    # the code below if we are not handling a new tree node.
    if HDLmGlobals.activeNodeType != 'newcompgem'     and \
       HDLmGlobals.activeNodeType != 'newcompgxe'     and \
       HDLmGlobals.activeNodeType != 'newcompignore'  and \
       HDLmGlobals.activeNodeType != 'newcompmod'     and \
       HDLmGlobals.activeNodeType != 'newcomppass'    and \
       HDLmGlobals.activeNodeType != 'newcomppopup'   and \
       HDLmGlobals.activeNodeType != 'newcompproxy'   and \
       HDLmGlobals.activeNodeType != 'newcompsimple'  and \
       HDLmGlobals.activeNodeType != 'newcompstore'   and \
       HDLmGlobals.activeNodeType != 'newconfig'      and \
       HDLmGlobals.activeNodeType != 'newdivision'    and \
       HDLmGlobals.activeNodeType != 'newignore'      and \
       HDLmGlobals.activeNodeType != 'newlist'        and \
       HDLmGlobals.activeNodeType != 'newmod'         and \
       HDLmGlobals.activeNodeType != 'newsite'        and \
       HDLmGlobals.activeNodeType != 'newstore'       and \
       HDLmGlobals.activeNodeType != 'newvalue':
      return [insertIntoDone, addTreeNodeDone, rvStr]       
    # print('s13') 
    # print('s1') 
    # Get the complete set of modification information. Note that this
    # information is used for all tree node types, including companies,
    # divisions, sites, and modifications. 
    modTypeInfo = HDLmMod.getModTypeInfo()
    # Get the current node type 
    modificationType = currentTreeNode.details.type
    # abcd = modificationType 
    # print(abcd) 
    # The code block below (the dummy loop) is used to handle
    # the case where a new modification node has just been 
    # changed from a type of 'newmod' to an actual types. 
    # We may need to add one or more fields at this point. 
    # The code below does this. 
    # The dummy loop below is used to allow break to work 
    # print('s2', HDLmGlobals.activeNodeType, modificationType) 
    while (True): 
      # print(currentTreeNode.details.extra) 
      # Set an initial value for redisplay modification. The initial
      # value is false. It may be set to true in several cases below. 
      redisplayModification = False
      # This block of code is really only used for one purpose. If we
      # are handling a new modification node, then only some of the 
      # fields can be displayed at the outset. At least one field
      # can only be displayed later. This field depends on the type
      # of the new modification. The user selects the type of the
      # new modification from a select list. After the user picks
      # the new modification type, the new field(s) can be added. 
      # print(HDLmGlobals.activeNodeType) 
      if HDLmGlobals.activeNodeType != 'newmod' and \
         HDLmGlobals.activeNodeType != 'newvalue':
        break
      # print('s12') 
      # print('s3')  
      # print(modificationType) 
      # Check if node type is still 'newmod'. If this is true, then
      # the new modification type has not been specified so far. If 
      # this is true, then we don't want to run the code below. The 
      # code below is only run to handling the case where the node
      # type is specified. This is only done once for each new 
      # modification.  
      # print(modificationType) 
      if modificationType == 'newmod'or \
         modificationType == 'newvalue':
        break 
      # Check if we have detailed information for the current node type.
      # We always should, but you never know. 
      if modificationType not in modTypeInfo:
        errorString = modificationType
        HDLmError.buildError('Error', 'Lookup', 10, errorString)
        return [insertIntoDone, addTreeNodeDone, rvStr] 
      # print(currentTreeNode.details.extra) 
      # print('s4') 
      # We need to create an empty field in current modification node 
      # in some cases. Of course, if the field already exists, we do 
      # not need to create it. We must also take care to create the 
      # right kind of field, if the field does not exist. In some 
      # case, we actually need to delete a field, not add one. 
      newFieldAddedDeleted = HDLmMenus.dataFieldAdd(currentTreeNode,
                                                    modificationType,
                                                    "finish tree node")
      # print(newFieldAddedDeleted) 
      # In some cases, we need to delete a field from the newly created tree
      # node. Certain type of tree nodes aren't allowed to have a parameter
      # number field. For these types of nodes, the parameter number field
      # must be deleted, if it exists. 
      if hasattr(currentTreeNode.details, 'type') and \
         hasattr(currentTreeNode.details, 'parameter'):
        nodeDetailsType = currentTreeNode.details.type
        if HDLmMod.getModificationTypeParmNumberUsed(nodeDetailsType) == False:
          del currentTreeNode.details.parameter
          newFieldAddedDeleted = True
      # print(currentTreeNode.details.extra) 
      #
      # Some special code is needed for the GUI eXtended Editor (GXE).
      # We need to set the extra information field in some cases. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
        # print(redisplayModification) 
        # The dummy loop below is only used to allow break to work 
        while (True):
          # Check if we can go any further 
          if currentDomElement == None or \
             currentTreeNode   == None or \
             hasattr(currentTreeNode, 'details') == False:
            break
          # Check if the parameter number is already properly set 
          if hasattr(currentTreeNode.details, 'parameter') and \
             str(type(currentTreeNode.details.parameter)) == "<class 'int'>":      
            break
          # Check if a parameter number is used with the current type
          # of rule. This is true in some cases, but not in others. 
          newDetailsType = currentTreeNode.details.type 
          if HDLmMod.getModificationTypeParmNumberUsed(newDetailsType) == False:
            break
          # Set the parameter number field, if need be 
          newParameterNumber = HDLmTree.getParameterNumber(currentTreeNode)
          currentTreeNode.details.parameter = newParameterNumber
          break
        # The dummy loop below is only used to allow break to work 
        while (True):
          # print(currentTreeNode.details.extra) 
          # Set the extra information field, if need be 
          if currentDomElement == None or \
             currentTreeNode   == None or \
             hasattr(currentTreeNode, 'details') == False:
            break
          if currentTreeNode.details.type != 'textchecked':
            break
          if hasattr(currentTreeNode.details, 'extra') and \
             len(currentTreeNode.details.extra) > 0:
            break
          elementText = currentDomElement.innerText
          maxNodeIdenTextLength = HDLmDefines.getNumber('HDLMMAXIDENTEXTLEN')
          if len(elementText) > maxNodeIdenTextLength:
            elementText = elementText.substring(0, maxNodeIdenTextLength)
          currentTreeNode.details.extra = elementText
          break
        if callFromCallback == False and \
           needUserInput    == True  and \
           gxeDebug         == False:
          redisplayModification = True 
        # print(currentTreeNode, callFromCallback, needUserInput, gxeDebug, redisplayModification) 
      # print('s5') 
      # We need to check for one very special case here. In some cases, we 
      # need to set the value of the extra information field. This is not
      # generally true, but in some cases it is true. 
      # print(currentTreeNode.details.extra) 
      if HDLmGlobals.checkForInlineEditor()                      and \
         currentTreeNode.details.type == 'textchecked'           and \
         hasattr(currentTreeNode.details, 'extra') == True       and \
         currentTreeNode.details.extra == ''                     and \
         hasattr(currentTreeNode.details, 'nodeiden') == True:
        # Extract the inner text value from the node identifier. This is the
        # default value of the extra information field. 
        nodeIdenInnerText = currentTreeNode.details.nodeiden.attributes.innertext
        nodeIdenInnerText = HDLmString.ucFirstSentence(nodeIdenInnerText)
        currentTreeNode.details.extra = nodeIdenInnerText
        redisplayModification = True
      # print(redisplayModification) 
      # Check if a new field was actually added or deleted. We only need to
      # redisplay the current modification if a new field was really addeded
      # or deleted. 
      if newFieldAddedDeleted == True:
        redisplayModification = True
      # print(redisplayModification) 
      if redisplayModification:
        # print('In finishTreeNode', 'About to use HDLmMod.displayMod', redisplayModification) 
        divDescriptions = HDLmDefines.getString('HDLMENTRYDESCRIPTIONS')
        divValues = HDLmDefines.getString('HDLMENTRYVALUES')
        newTreeEntryLocal = True
        # print('about to displaymod') 
        callSource = 'HDLmMenus.finishTreeNode'
        inlineStartupFlag = False
        HDLmMod.displayMod(divDescriptions, divValues, currentTreeNode,
                           possibleRuleTypes, currentDomElement,
                           HDLmGlobals.activeEditorType, newTreeEntryLocal,
                           inlineStartupFlag, handlingCmdInsert,
                           callSource)
      break
    # print('s6') 
    # print('s11') 
    # The code block below (the dummy loop) is used to handle
    # the case where a new modification node or some other type  
    # of node is finally complete. At this point the complete node
    # can actually be inserted into the tree of nodes and the
    # Fancytree hierachy (in some cases) as well. The node that
    # may be inserted below may or may not be a modification node.
    # Other types of nodes are handled by this code as well. 
    # The dummy loop below is used to allow break to work 
    while (True):
      # print(currentTreeNode.details.extra) 
      # This code finishes the new tree node and inserts the new 
      # tree node into the node tree 
      newTooltip = None
      # Try to get the error text from the container if the 
      # container is available. If the container is not available,
      # then no error text can be used. Set the error text to an
      # empty string. 
      if containerAvailable:
        containerWidgetCurrent = currentTreeNode.containerWidget
        errorText = containerWidgetCurrent.getErrorText()
      else:
        errorText = ''
      # Check if the error text is an empty string or not. if the error text is 
      # actually set, then more work needs to be done on the new tree node. We
      # can just exit at this point. 
      # print(errorText) 
      if errorText != '':
        break
      # print('s7') 
      # Collect a set of information from the new node. This information
      # is used to finish updating the new tree node. 
      newName = currentTreeNode.details.name
      newNodePathLen = len(currentTreeNode.nodePath)
      newModificationType = currentTreeNode.details.type
      # For some of the editors, we may want to change the modification
      #  name at this point. The modification name probably uses to the 
      #  path name at this point for some of the editors. We would really
      # prefer to use the rule type as part of the modification name. 
      if HDLmGlobals.checkForInlineEditor():
        # Try to obtain (locate) the parent node of the current child node 
        nodePath = currentTreeNode.nodePath
        parentTreeNode = HDLmTree.locateTreeParentNode(nodePath)
        # Report an error if the parent node could not be found 
        if parentTreeNode == None:
          nodeString = str(nodePath)
          errorText = HDLmError.buildError('Error', 'Locate', 9, nodeString)
          HDLmAssert(False, errorText)
        # The following code should never be executed in the Python 
        # environment. Report an error, if this code is ever reached.
        errorText = 'This code should neve be executed. HDLmPopup has not been ported.'
        HDLmAssert(False, errorText)
        # newName = HDLmPopup.getUpdatedModName(parentTreeNode, newModificationType)
        currentTreeNode.details.name = newName
        nodePath[newNodePathLen - 1] = newName
        # print(currentTreeNode) 
      # print('s10') 
      # Check if we are running the GUI editor or the GUI extended editor. If we 
      # are running the GUI editor or the GUI extended editor, set the new type 
      # to a special value that will retrieve the correct tooltip value. In at 
      # least one case, we need to reset the type value as well. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
        newModificationType = newModificationType
        # Check if we just created a new company 
        if newModificationType == 'newcompgem' or \
           newModificationType == 'newcompgxe':
          currentTreeNode.nodePath[newNodePathLen - 1] = newName
          currentTreeNode.details.type = 'company'
          # Build the standard/required subnodes of the company node
          # and add them to the company node 
          updateDatabase = False
          HDLmMenus.buildCompanyNode(currentTreeNode, updateDatabase)
        # Check if we just created a new data value 
        # print(newModificationType) 
        if newModificationType == 'value':
          currentTreeNode.tooltip = HDLmTree.getTooltip('newvalue')
          newTooltip = currentTreeNode.tooltip
      # print(currentTreeNode.details.extra) 
      # print('s8') 
      # Check if we are running the ignore (ignore-lists) editor.
      # If we are running the ignore (ignore-lists) editor, set the new 
      # type to a special value that will retrieve the correct tooltip
      # value. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.ignore:
        newModificationType = newModificationType
      # Check if we are running the pass-through editor.
      # If we are running the pass-through editor, set the new 
      # type to a special value that will retrieve the correct
      # tooltip value. In at least one case, we need to reset
      # the type value as well. 
      # print('s9') 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.passEnum:
        newModificationType = newModificationType
        # Check if we just created a new company 
        if newModificationType == 'newcomppass':
          currentTreeNode.nodePath[newNodePathLen - 1] = newName
          currentTreeNode.details.type = 'company'
          # Build the standard/required subnodes of the company node
          # and add them to the company node 
          updateDatabase = True
          HDLmMenus.buildCompanyNode(currentTreeNode, updateDatabase)
        # Check if we just created a new data value 
        # print(newModificationType) 
        if newModificationType == 'value':
          currentTreeNode.tooltip = HDLmTree.getTooltip('newvalue')
          newTooltip = currentTreeNode.tooltip
      # print('s9') 
      # Check if we are running the Popup editor. If we are running 
      # the Popup editor, set the new type to a special value that
      # will retrieve the correct tooltip value. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.popup:
        newModificationType = newModificationType
      # Check if we are running the company proxy definitions editor. If
      # we are running the proxy definitions editor, set the new type to
      # a special value that will retrieve the correct tooltip value. 
      # The actual modification type (for the proxy definitions editor) 
      # is something like 'inject' or 'HTML'. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.proxy:
        newModificationType = 'newcompproxy'
      # Check if we are running the Simple editor. If we are running 
      # the Simple editor, set the new type to a special value that
      # will retrieve the correct tooltip value. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.simple:
        newModificationType = newModificationType
      # Check if we are running the company store (stored value) editor.
      # If we are running the store (stored value) editor, set the new 
      # type to a special value that will retrieve the correct tooltip
      # value. 
      # print(currentTreeNode.details.extra) 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.store:
        newModificationType = newModificationType
      if newTooltip == None:
        newTooltip = HDLmTree.getTooltip(newModificationType)
      # print('s8') 
      # For most editor types, the modification type will have been 
      # reset (set) at this point to something like 'fontcolor or 
      # 'inject'. However, the configuration editor, the store 
      # editor, and the ignore (ignore-lists) editor does not do 
      # this. We must fix the modification type directly. 
      if newModificationType == 'newconfig':
        newModificationType = 'config'
        currentTreeNode.details.type = 'config'
      if newModificationType == 'newignore':
        newModificationType = 'ignore'
        currentTreeNode.details.type = 'ignore'
      if newModificationType == 'newpass':
        newModificationType = 'pass'
        currentTreeNode.details.type = 'pass'
      if newModificationType == 'newstore':
        newModificationType = 'store'
        currentTreeNode.details.type = 'store'
      if newModificationType == 'newvalue':
        # We need to check for a very special case. It is possible
        # that the data value node name is not set. The node name 
        # must be set to create new node. 
        if newName == '':
          break
        newModificationType = 'value'
        currentTreeNode.details.type = 'value'
      # Set a few fields in the tree node using information obtained
      # from the new tree node 
      currentTreeNode.nodePath[newNodePathLen - 1] = newName
      currentTreeNode.tooltip = newTooltip
      # print('s10') 
      # At this point we want to delete the details property for all 
      #  nodes other than ignore (ignore-list entry) nodes. However, 
      #  we really only want to do this if we are running the ignore
      #  (ignore-lists) editor. This step can not be done for any other
      #  type of editor. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.ignore and \
         currentTreeNode.type != 'ignore'                       and \
         hasattr(currentTreeNode, 'details'):
        del currentTreeNode.details
      # At this point we want to delete the details property for all 
      # nodes other than modification nodes. However, we really only
      # want to do this if we are running the modiications editor. 
      # This step can not be done for any other type of editor. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.mod and \
          currentTreeNode.type != 'mod'                       and \
          hasattr(currentTreeNode, 'details'):
        del currentTreeNode.details
      # print('s7') 
      # At this point we want to delete the details property for 
      # some nodes if we are running the GUI editor or the GUI 
      # extended editor or the pass-through editor or one of the 
      # inline editors. The pass-through editor and the inline editors
      # are somewhat different in that many types (levels) of nodes 
      # have details that we need to keep. As a consequence, the code 
      # below is quite selective. 
      # print(currentTreeNode.details.extra) 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.passEnum or \
         HDLmGlobals.checkForInlineEditorOrGems():
        # Check if we are creating a leaf node for the pass-through
        # editor. We don't want to keep any details, at least for now. 
        if currentTreeNode.type != 'company' and \
           currentTreeNode.type != 'ignore'  and \
           currentTreeNode.type != 'line'    and \
           currentTreeNode.type != 'mod'     and \
           currentTreeNode.type != 'value':
          if hasattr(currentTreeNode, 'details'):
            del currentTreeNode.details
      # print('s11') 
      # At this point we want to delete the details property for all 
      # nodes other than modification nodes and top nodes. However, 
      # we really only want to do this if we are running one of the 
      # inline editors. This step can not be done for any other type
      # of editor. 
      if HDLmGlobals.checkForInlineEditor() and \
         currentTreeNode.type != 'mod'      and \
         currentTreeNode.type != 'top'      and \
         hasattr(currentTreeNode, 'details'):
        del currentTreeNode.details
      # At this point we want to delete the details property for all 
      # nodes other than store (stored value) nodes. However, we really
      # only want to do this if we are running the store (stored value)
      # editor. This step can not be done for any other type of editor. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.store and \
         currentTreeNode.type != 'store'                       and \
         hasattr(currentTreeNode, 'details'):
        del currentTreeNode.details
      # print('s6') 
      # We need to handle one very complex case here. It is possible that the
      # path value value for the details of a modification node will be set to 
      # an empty string here. This is actually an error. The correct value is
      # a string, one character long containing a slash. This appears to 
      # happen when a new modification node is inserted into the overall
      # tree structure, but the path value field is never touched (left with a 
      # default value). 
      if currentTreeNode.type == 'mod'                 and \
         hasattr(currentTreeNode, 'details')           and \
         hasattr(currentTreeNode.details, 'pathvalue') and \
         currentTreeNode.details.pathvalue == '':
        currentTreeNode.details.pathvalue = '/'
      # Get the parent Fancytree node for use below. We should always be
      # able to find the parent Fancytree node at this point. This is only
      # really possible if we are running the standard rule editor. If we
      # are running the GUI rule editor or the GUI extended editor, this
      # can not be done. Note that if we are running the GUI extended
      # editor (GXE) under the debugger than we can get the parent 
      # Fancytree node. 
      # print(currentTreeNode.details.extra) 
      parentFancyNode = None
      needParentFancyNode = True
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.simple:
        needParentFancyNode = False
      # print(HDLmGlobals.activeEditorType, gxeDebug, needParentFancyNode) 
      if gxeDebug == True:
        needParentFancyNode = True
      # In the Python environment, we have no Fancytree to update
      needParentFancyNode = False
      # Check if we need the parent Fancytree node
      if needParentFancyNode == True:
        # Some special code is needed hear to handle any or the inline 
        # editors. The parent Fancytree node in this case will always 
        # be the Top (top) level node. 
        fancyNodePath = currentTreeNode.nodePath
        if HDLmGlobals.activeEditorType == HDLmEditorTypes.popup:
          fancyNodePath = currentTreeNode.nodePath[0:2]
        # Try to locate the parent Fancytree node here. This may or may 
        # not work because the parent Fancytree node may or may not be
        # displayed at this point. 
        reportFancyLocateErrors = False
        # The following code should never be executed in the Python 
        # environment. Report an error, if this code is ever reached.
        errorText = 'This code should neve be executed. We have no Fancytree under Python.'
        HDLmAssert(False, errorText)
        parentFancyNode = HDLmTree.locateFancyParentNode(fancyNodePath, reportFancyLocateErrors)
        if parentFancyNode == None and \
           parentFancyNode != None:
          nodeString = str(currentTreeNode.nodePath)
          errorText = f'Parent Fancytree node not located (${nodeString})'
          HDLmAssert(False, errorText)
        # print(parentFancyNode) 
      # print('s5') 
      # In at least one very important case, the parent Fancytree node will
      # be known at this point. In this case, the parent Fancytree node is
      # actually, the Fancytree root node. All Fancytree subnodes are 
      # inserted directly under the Fancytree root node, if the Simple
      # editor is active. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.simple:
        parentFancyNode = HDLmTree.locateFancyRootNode() 
      # If we are running the GUI rule editor or the GUI extended editor, 
      # then we don't have Fancytree to update. We just set the Fancytree 
      # node reference to None in this case. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
        if gxeDebug == False:
          parentFancyNode = None
      # Add an insert event to the undo / redo array. Note that the node being 
      # added is identified using the complete path to the node. This path
      # (minus the last element) also identifies the Fancytree parent of the
      # node being added. Of course, a copy of the node path is made. The 
      # original node path is not used. The data to be pasted is also converted
      # to JSON to force a copy to be made.  
      #
      # The code below is not used under Python and has been disabled
      # for now
      if 1 == 2                                              and \
         HDLmGlobals.activeEditorType != HDLmEditorTypes.gem and \
         HDLmGlobals.activeEditorType != HDLmEditorTypes.gxe:
        # The following code should never be executed in the Python 
        # environment. Report an error, if this code is ever reached.
        errorText = 'This code should neve be executed. HDLmUnRe has not been ported.'
        HDLmAssert(False, errorText)
        currObj = HDLmTree.copyNode(currentTreeNode)
        addInsertEventNone = None
        addInsertDataNone = None
        # HDLmUnRe.addInsert(addInsertEventNone, addInsertDataNone,
        #                    list(currentTreeNode.nodePath),
        #                    json.dumps(currObj))
      # print(currentTreeNode.details.extra) 
      # print('s4') 
      # We need to decide if an actual insert should be done, at this 
      # point or if an insert should just be added to the array of 
      # pending inserts. In most cases, we really want to do a real 
      # insert at this point. However, if we are using the GEM editor  
      # or if we are using the GXE editor or if one of the inline editors
      # is in use, then we really want to add to the pending inserts list.
      # These comments are now out-of-date. The current comments follow.  
      # We need to decide if an actual insert should be done at this
      # point or if an insert should just be added to the array of
      # pending inserts. In all cases, we now create a pending insert. 
      usePendingInserts = True
      if HDLmGlobals.checkForInlineEditorOrGems():
        usePendingInserts = True
      # In the Python environment, we really don't want to 
      # use pending inserts, at least for now
      usePendingInserts = False
      # Check if the GEM or GXE environments are active. If the GEM or 
      # GXE environments are active, then we must (should) make sure 
      # that all of the parent nodes to the modification node really 
      # exist. If we are handling a new company, these nodes will not 
      # exist and must be created. 
      # print('s3') 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe:
        siteNodePath = currentTreeNode.nodePath[0:6]
        updateDatabase = False
        HDLmTree.buildSiteNode(siteNodePath, updateDatabase, HDLmTreeTypes.rules)
      # print(currentTreeNode.details.extra) 
      # Try to add the new rule to the rule tree and the Fancytree node
      # tree. Note that if we are handling the GUI rule editor or the 
      # GUI extended editor, the parent Fancytree node will be None at
      # this point because we have no Fancytree to update. The None value 
      # tells the routine below not to update the Fancytree. 
      try:
        processSubNodes = False
        # In the Python environment, we really don't want to 
        # update the database, at least for now
        updateDatabase = False
        # For a couple of types of editors we really don't want to
        # update the database. The database will be actually be
        # updated when the new modification is sent to the server
        # using web sockets. 
        if HDLmGlobals.checkForInlineEditorOrGems() == True: 
          updateDatabase = False
        # Check for a very special case here. If we using debugger 
        # to debug the GXE code, then we really do want to update
        # the database. 
        if gxeDebug == True:
          updateDatabase = True
        # print('s2') 
        # print(parentFancyNode) 
        # print(currentTreeNode)         
        insertIntoDone = True
        # print(currentTreeNode.details.extra) 
        HDLmMenus.insertIntoBothTrees(parentFancyNode, 
                                      currentTreeNode, 
                                      usePendingInserts,
                                      processSubNodes,
                                      updateDatabase,
                                      handlingCmdInsert)
        # print(currentTreeNode.details.extra) 
        # print('about to call processPendingInserts()') 
        HDLmTree.processPendingInserts()
        # print(currentTreeNode) 
        # print(usePendingInserts) 
      except Exception as errorObj: 
        print(errorObj)
      # print('s1') 
      # Clear the global values that show we were adding a new tree node
      # of some type. This can only be done for the standard rule editor
      # and can not be done for the GUI rule editor or the GUI extended
      # editor. Why this check was added is not clear. Note that this 
      # check is effectively bypassed by the else clause below. 
      if HDLmGlobals.activeEditorType != HDLmEditorTypes.gem and \
         HDLmGlobals.activeEditorType != HDLmEditorTypes.gxe:
        HDLmMenus.clearPending()
      else:
        HDLmMenus.clearPending()
      # print(currentTreeNode.details.extra) 
      # Send any pending inserts to the server database 
      # print('about to call processPendingInserts()') 
      HDLmTree.processPendingInserts()
      # At this point we may want to update the nodes inside the server. 
      # This is done by sending a message to the server telling it to 
      # reload all of the nodes. 
      if HDLmGlobals.checkForInlineEditorOrGems():
        # print('In HDLmMenus.finishTreeNode', newTreeEntry)  
        # If we are running under the debugger and we are using
        # the GUI eXtended Editor (GXE) then we really don't want 
        # to add a tree node here 
        sendAddRequest = True
        if gxeDebug == True:
          sendAddRequest = False
        if sendAddRequest == True:
          addTreeNodeDone = True
          HDLmWebSockets.sendAddTreeNodeRequest(currentTreeNode)
          HDLmGXE.rulesUpdatedSet()
      # At this point we need to consider a very special case. We may have
      # just added a company using the GUI editor or the GUI extended editor
      # or the pass-through editor. In that case, we need to create four more 
      # nodes from scratch. They are the data node and the lists node and the 
      # reports node and the rules node. 
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe or \
         HDLmGlobals.activeEditorType == HDLmEditorTypes.passEnum:
        # Check if we just created a new company. This code will never 
        # execute because of the false clause below. 
        if 1 == 2 and currentTreeNode.type == 'company':
          updateDatabase = True
          HDLmMenus.buildCompanyNode(currentTreeNode, updateDatabase)
        # Add some missing fields to the new node 
        if 1 == 2:
          HDLmPass.addMissingPassObject(currentTreeNode)
        # In some cases, we may need to update a count field in a parent
        # node. This is not always true. 
        if 1 == 2:
          fieldName = 'nodePath'
          nodePath = currentTreeNode[fieldName]
          HDLmTree.resetCountField(nodePath)
      rvStr = 'finished'
      break
    return [insertIntoDone, addTreeNodeDone, rvStr] 
  # This method gets a URL value from an image string. If the image
  # string does not contain a proper URL value, then this routine 
  # returns an empty (zero-length) string. Note that the returned
  # URL string will always start with two slashes if it is a network
  # (HTTP or HTTPS) URL. It will start with 'data:' if it is a data
  # URL. This code supports both network URLs and data URLs. The leading 
  # protocol (if any) and the leading colon (if one exists) are always
  # removed from network URLs.  
  @staticmethod
  def getUrlFromImage(imageStr):
    urlStr = ''
    # What follows is a dummy loop used only to allow break to work 
    while True:
      if imageStr == None or \
         imageStr == '':
        break
      # At this point we need to analyze the image string    
      imageStrTokens = HDLmString.getTokens(imageStr, '"')
      # Make sure we have enough tokens  
      imageStrTokensLength = len(imageStrTokens)
      if imageStrTokensLength < 4:
        break
      # Check the first token for a special value. If the special value
      # is found, then a special path is needed.  
      imageStrToken = imageStrTokens[0]
      if imageStrToken.value == 'data':
        # Check the second token  
        imageStrToken = imageStrTokens[1]
        if imageStrToken.value != ':':
          break
        # We now need to scan forwards looking for the comma token.
        # The comma token will be followed by the data URL value.  
        for i in range(2, imageStrTokensLength): 
          imageStrToken = imageStrTokens[i]
          if imageStrToken.value != ',':
            continue
          if (i + 1) >= imageStrTokensLength:
            break
          # The needed URL value is actually the entire image string 
          urlStr = imageStr
          break
      # We can now check for a fairly standard network URL 
      elif imageStrToken.value == 'http' or \
           imageStrToken.value == 'https': 
        # Check the second token 
        imageStrToken = imageStrTokens[1]
        if imageStrToken.value != ':':
          break
        # Check the third token 
        imageStrToken = imageStrTokens[2]
        if imageStrToken.value != '/':
          break
        else:
          startOfUrl = imageStrToken.pos
        # Check the fourth token 
        imageStrToken = imageStrTokens[3]
        if imageStrToken.value != '/':
          break
        # The needed URL value is actually the entire image string 
        urlStr = imageStr[startOfUrl:]
        break 
      break 
    return urlStr 
    # This method gets a URL value from a style string. If the style
    # string does not contain a proper URL value, then this routine 
    # returns an empty (zero-length) string. Note that the returned
    # URL string will always start with two slashes if it is a network
    # (HTTP or HTTPS) URL. It will start with 'data:' if it is a data
    # URL. This code supports both network URLs and data URLs. The leading 
    # protocol (if any) and the leading colon (if one exists) are always
    # removed from network URLs. The style must be a background-image style. 
  @staticmethod 
  def getUrlFromStyle(styleStr):
    urlStr = ''
    # What follows is a dummy loop used only to allow break to work 
    while True:
      if styleStr == None or \
         styleStr == '':
        break
      # At this point we need to analyze the style string. The style
      # string may specific a background image URL. This type of style
      # can be used.  
      styleStrTokens = HDLmString.getTokens(styleStr, '"')
      # Make sure we have enough tokens 
      if len(styleStrTokens) < 9:
        break
      # Check the first token 
      styleStrToken = styleStrTokens[0]
      if styleStrToken.value != 'background':
        break
      # Check the second token 
      styleStrToken = styleStrTokens[1]
      if styleStrToken.value != '-':
        break
      # Check the third token 
      styleStrToken = styleStrTokens[2]
      if styleStrToken.value != 'image':
        break
      # Check the fourth token 
      styleStrToken = styleStrTokens[3]
      if styleStrToken.value != ':':
        break
      # Check the fifth token 
      styleStrToken = styleStrTokens[4]
      if styleStrToken.tokType != HDLmTokenTypes.space:
        break
      # Check the sixth token 
      styleStrToken = styleStrTokens[5]
      if styleStrToken.value != 'url':
        break
      # Check the seventh token 
      styleStrToken = styleStrTokens[6]
      if styleStrToken.value != '(':
        break
      # The URL will be in the eigth token. The URL may be a 
      # traditional HTTP/HTTPS URL or it may be a data URL 
      # value. At least for now, we can not handle data values.
      # This has been changed we do support data URLs now.
      styleStrToken = styleStrTokens[7]
      urlStr = styleStrToken.value
      # Check if we have a data value at this point. We can not
      # handle data values for now. This has been changed. We do
      # support data URLs at this point. 
      if urlStr.startswith('data'):
        urlStr = urlStr
      # Remove a set of prefixes from the URL string. Note that
      # the code below changes (a lot) network URLs, but does not
      # change data URLs at all. 
      if urlStr.startswith('https'):
        urlStr = urlStr[5:]
      if urlStr.startswith('http'):
        urlStr = urlStr[4:]
      if urlStr.startswith(':'):
        urlStr = urlStr[1:]
      break
    return urlStr
  # Add the new tree node to the Fancytree and the standard tree. 
  # The caller passed the new tree node and Fancytree node that 
  # should serve as the parent of the new tree node. Note that 
  # this routine also updates the node tree as well as the 
  # Fancytree node tree. The Fancytree node may not exist, in 
  # which case we will not update the Fancytree. 
  @staticmethod 
  def insertIntoBothTrees(parentFancyNode, childTreeNode, 
                          usePendingInserts = False,
                          processSubNodes = False,
                          updateDatabase = False,
                          handlingCmdInsert = False):
    # print('HDLmMenus.insertIntoBothTrees') 
    # Get the node path associated with the tree of one or more
    # nodes that are going to be inserted  
    nodePath = childTreeNode.nodePath
    # print(parentFancyNode) 
    # print(childTreeNode) 
    # print(usePendingInserts) 
    # Insert all (one or more) rows associated with the node tree.
    # This is only really done if the use pending inserts flag is
    # set to false. If this flag is set to true, then the child
    # tree node is added to the list of pending inserts. 
    if updateDatabase == True:
      if usePendingInserts == False: 
        HDLmTree.passInsertOneTreePos(childTreeNode)
      else: 
        HDLmTree.addPendingInserts(childTreeNode, processSubNodes) 
    # The next step is to add the current tree node to the children
    # array of the parent of the current tree node. 
    addBool = HDLmTree.addToParentTree(childTreeNode)
    if addBool == False:
      nodePathString = str(nodePath)
      errorText = f'Child node (${nodePathString}) not added to parent node'
      HDLmAssert(False, errorText)
    # Perform some related operatons. We may need to update some count
    # values at this point. We clearly need to set the update status flag.
    # If any of the inline editors are in use, we need to update the server
    # and reload the current page. 
    HDLmTree.updateRelatedOperations(nodePath) 
    # Check if the Fancytree node exists or not. Just return if the Fancytree
    # node does not exist. 
    if parentFancyNode != None:
      # Some of the new tree nodes we need to add are actually folders. However,
      # some are not. Set a boolean field showing if the new tree node is a folder
      # of not. 
      newLazy = True
      newNodeFolder = True
      if HDLmGlobals.activeEditorType == HDLmEditorTypes.config:
        newLazy = False
        newNodeFolder = False 
      elif (HDLmGlobals.activeEditorType == HDLmEditorTypes.gem or \
            HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe) and \
            (childTreeNode.type == 'line'   or \
             childTreeNode.type == 'ignore' or \
             childTreeNode.type == 'mod'    or \
             childTreeNode.type == 'value'):
        newLazy = False
        newNodeFolder = False
      elif HDLmGlobals.activeEditorType == HDLmEditorTypes.ignore and \
           childTreeNode.type == 'ignore':
        newLazy = False
        newNodeFolder = False
      elif HDLmGlobals.activeEditorType == HDLmEditorTypes.mod and \
           childTreeNode.type == 'mod':
        newLazy = False
        newNodeFolder = False
      elif HDLmGlobals.activeEditorType == HDLmEditorTypes.passEnum and \
           (childTreeNode.type == 'line'   or \
            childTreeNode.type == 'ignore' or \
            childTreeNode.type == 'mod'    or \
            childTreeNode.type == 'value'):
        newLazy = False
        newNodeFolder = False
      elif HDLmGlobals.checkForInlineEditor() and \
           childTreeNode.type == 'mod':
        newLazy = False
        newNodeFolder = False
      elif HDLmGlobals.activeEditorType == HDLmEditorTypes.proxy:
        newLazy = False
        newNodeFolder = False
      elif HDLmGlobals.activeEditorType == HDLmEditorTypes.store and \
           childTreeNode.type == 'store':
        newLazy = False
        newNodeFolder = False
      # Build the new Fancytree node that we need to add to the fancy
      # tree. We may need to add this node in one of several places. 
      # The code below determines where to add the new Fancytree node. 
      lastNodePathValue = childTreeNode.nodePath[len(childTreeNode.nodePath) - 1]
      # The following code should never be executed in the Python 
      # environment. Report an error, if this code is ever reached.
      errorText = 'This code should neve be executed. We have no Fancytree under Python.'
      HDLmAssert(False, errorText)
      # newFancyNode = {                  
      #   title: lastNodePathValue,        
      #   tooltip: childTreeNode.tooltip, 
      #   folder: newNodeFolder,          
      #   lazy: newLazy                   
      # }
      # print('In HDLmMenus.insertIntoBothTrees', parentFancyNode) 
      # print(newFancyNode) 
      # print(childTreeNode) 
      #
      # The following code should never be executed in the Python 
      # environment. Report an error, if this code is ever reached.
      errorText = 'This code should neve be executed. We have no Fancytree under Python.'
      HDLmAssert(False, errorText)
      # We can now add the new Fancytree tree node to the Fancytree 
      # HDLmTree.addToParentFancy(parentFancyNode, newFancyNode, 
      #                           childTreeNode, handlingCmdInsert) 
    return 