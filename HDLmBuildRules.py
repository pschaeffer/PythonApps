# Class for providing a set of functions for building rules. No instances
# of this class are ever created.
 
from bs4          import BeautifulSoup
from HDLmGlobals  import *
from HDLmGXE      import *
from HDLmMenus    import *
from HDLmMod      import *
from HDLmNodeIden import *
from HDLmTree     import *

class HDLmBuildRules(object):
  # Build a set of rules for the current web page. We start at
  # the top, by looking for a 'body' or 'html' tag (without the
  # quotes). We then process all of the elements under the top
  # level element. This routine builds a list of rules and 
  # returns the list to the caller. The caller can then use 
  # the list as need be. 
  @staticmethod
  def buildRules(wLHref, wLHostName, webPage):
    # print('In HDLmBuildRules.buildRules') 
    # Create the list that will contain all of the rules built 
    # by this routine and the routines that this routine calls
    outputRules = []
    # Convert the current web page into a Beautiful Soap object
    soup = BeautifulSoup(webPage, 'html.parser')
    # Get the adjusted host name all of the new rules will
    # be stored under
    hostNameWithSuffix = HDLmBuildRules.getUniqueHostName(wLHostName)
    # Create the site node as need be 
    hostNameWithSuffixSiteNode = HDLmGXE.buildSiteNode(hostNameWithSuffix, 
                                                       HDLmTreeTypes.rules)
    # Get the highest level element in the web page 
    topElement = None
    domHtmlElement = soup.html
    domBodyElement = soup.body
    # Check which high-level elements were actually found 
    if domBodyElement != None:
      topElement = domBodyElement
    # If the 'body' element (without the quotes) was not found,
    # look for the 'html' element (without the quotes) 
    elif domHtmlElement != None:
      topElement = domHtmlElement
      # Report an error if the top level element could not 
      # be found 
    else:
      errorStr = 'Html and body elements not found'
      errorText = HDLmError.buildError('Error', 'Find', 55, errorStr)
      HDLmAssert(False, errorText)
      return    
    # print('In HDLmBuildRules.buildRules') 
    # print(domHtmlElement) 
    # print(domBodyElement) 
    # print(topElement) 
    #
    # The dummy loop below is used to allow break to work 
    while True:
      # Check if the top elmeent is set or not 
      if topElement == None:
        break
      # Get all of the children of the top element 
      topElementChildren = topElement.children 
      # print(topElementChildren)  
      # Process all of the children of the top element 
      for topElementChild in topElementChildren: 
        if topElementChild == '\n':
          continue
        HDLmBuildRules.element(wLHref, 
                               wLHostName, 
                               hostNameWithSuffix,
                               hostNameWithSuffixSiteNode,
                               outputRules,
                               soup, 
                               topElementChild)        
      # Terminate the dummy loop 
      break
    return outputRules
  # Build the current tree node and modification 
  @staticmethod
  def build(soup,  
            hostNameWithSuffix,       
            hostNameWithSuffixSiteNode,
            currentElement,   
            urlStr,          
            extraValue,       
            newModType):
    # print('In HDLmBuildRules.build')  
    # print(currentElement)
    # print(urlStr) 
    # print(extraValue) 
    # print(newModType) 
    # Set a few values for use later 
    ruleTreeInfo = None
    newModTypeCapitalized = HDLmString.ucFirst(newModType)
    pathValue = HDLmUtility.getPathString(urlStr)
    urlObj = HDLmUrl(urlStr)
    hostName = urlObj.getHost() 
    # Set a few values for use later 
    newActiveNodeType = 'newmod'
    HDLmGlobals.activeEditorType = HDLmEditorTypes.passEnum
    # Get the node path from the site node 
    newNodePath = list(hostNameWithSuffixSiteNode.nodePath)
    # Build the path for the new rule 
    newUrlValueStr = 'https://' + hostNameWithSuffix + pathValue
    # At this point, we really don't know what the final rule name will be.
    # However, we do need to build an initial modification name. So we use
    # the rule type as part of the rule name. 
    removeTailsTrue = True
    newName = HDLmMenus.buildModificationName(hostNameWithSuffixSiteNode, 
                                              newUrlValueStr, 
                                              newModTypeCapitalized, 
                                              removeTailsTrue)
    newNodePath.append(newName)
    # print(newName) 
    newTreeType = HDLmTreeTypes.mod
    newTreeTypeStr = str(newTreeType).split('.')[1]
    newTooltip = HDLmTree.getTooltip(newActiveNodeType)
    # Build a node identifier JSON string for the current node.
    # The value is used below to try to find an existing rule
    # or to build a new rule. 
    nodeIdenObj = HDLmNodeIden.getNodeIdentifierObj(soup, currentElement)
    # If we don't have a valid node identification string, then we really
    # can't go any further. Just return to the caller, if need be. 
    if nodeIdenObj == None:
      return None
    # The creation of a new tree node below is OK because eventually (hopefully)
    # we call a routine that inserts the new tree node into the overall node 
    # tree. This routine also sends the new tree node to the server to add the
    # new tree node to the database. 
    ruleTreeInfo = HDLmTree(newTreeTypeStr, newTooltip, newNodePath)
    ruleTreeInfo.nodePath = list(newNodePath)
    # Build the details (the actual modification) for the new rule 
    modificationExtra = extraValue
    # print(extraValue) 
    modificationCssEmpty = ''
    modificationEnabledTrue = True
    modificationFindsEmpty = []
    modificationParameterNumberNone = None
    modificationXpathEmpty = ''
    ruleModInfo = HDLmMod.buildModificationObject(newName, pathValue,
                                                  modificationExtra, modificationEnabledTrue,
                                                  modificationCssEmpty, modificationXpathEmpty,
                                                  modificationFindsEmpty, nodeIdenObj,
                                                  newModType, modificationParameterNumberNone)
    # print(ruleModInfo.extra) 
    ruleTreeInfo.details = ruleModInfo
    return ruleTreeInfo
  # Check the tag value passed by the caller. If this is an image
  # try to get the image. If we can not get the image return false
  # to the caller. If the current element is not an image try to 
  # get the text. If we can not get the text, return false to the
  # caller. 
  @staticmethod
  def checkElement(currentElement, currentTagUpper):
    rv = False
    # Check if the caller passed a tag value showing that we have
    # an image 
    if currentTagUpper == 'IMG':
      # Get the image (if any) for the current element 
      currentImage = HDLmBuildRules.getImage(currentElement)
      if currentImage == None:
        return rv
      # Check if the image is OK. Some images appear not to be really images. 
      if HDLmBuildRules.checkImage(currentImage) == False:
        return rv
      # Show that the current image element appears to be OK 
      rv = True
      return rv
    # Since the current element is not an image, we need to make sure that we can
    # get some text for current element. If we can't get any text, then we just 
    # return false to the caller. 
    #
    # Get the text (if any) for the current element 
    currentText = HDLmBuildRules.getText(currentElement)
    if currentText == None:
      return rv
    # Show that the current element appears to be OK 
    rv = True
    return rv  
  # Check the image passed by the caller. The caller really doesn't 
  # pass an image. The caller really passes an image name. The name
  # is check and true or false is returned to the caller. The actual
  # image is not loaded by this routine. 
  @staticmethod
  def checkImage(currentImage):
    rv = False
    # Check if the caller passed a None value. Just return to 
    # caller in this case. 
    if currentImage == None:
      return rv
    if str(type(currentImage)) != "<class 'str'>":
      return rv
    # Get the suffix of the current image name 
    currentImageSuffix = None 
    currentImageSuffix = HDLmString.getFileNameSuffix(currentImage)
    if currentImageSuffix == None:
      return rv
    if str(type(currentImageSuffix)) != "<class 'str'>":
      return rv
    # Get the type of the current image. If they type is not
    # 'image' (without the quotes), then just return to the 
    # caller. 
    currentImageType = None
    currentImageType = HDLmString.getFileNameType(currentImageSuffix)
    if currentImageType == None:
      return rv
    if str(type(currentImageType)) != "<class 'str'>":
      return rv
    # Check if the type is actually correct     
    if currentImageType != 'image':
      return rv
    # Show that the current image element appears to be OK 
    rv = True
    return rv 
  # Check the tag value passed by the caller. If this is a tag
  # value, we just ignore, return false to the caller. Otherwise
  # return true to the caller. 
  @staticmethod
  def checkTag(currentElement, currentTagUpper):
    # Check if the caller passed a tag value, we just ignore 
    if currentTagUpper == 'BR'     or \
       currentTagUpper == 'SCRIPT':
      return False
    # Show that the tag value shows that the current element
    # should be processed 
    return True
  # Create one or more rules for the current element. The caller
  # passes the current element. The rule or rules are added to 
  # the rule tree. The new rules created by this routine are
  # returned to the caller. 
  @staticmethod
  def create(wLHref, 
             wLHostName, 
             hostNameWithSuffix,
             hostNameWithSuffixSiteNode,
             soup, 
             currentElement, 
             userUpdateRule, 
             allowBlankText):
    newRuleCount = 0
    newImageRule = None
    newTextRule = None
    # Get the image (if any) for the current element 
    currentImage = HDLmBuildRules.getImage(currentElement)
    # print(currentImage) 
    # print(currentElement) 
    if currentImage != None:
      newImageRule = HDLmBuildRules.createImage(wLHref, 
                                                wLHostName,
                                                hostNameWithSuffix,
                                                hostNameWithSuffixSiteNode,
                                                soup,
                                                currentElement, 
                                                userUpdateRule) 
      return [newImageRule]
    # Get the text (if any) for the current element 
    currentText = HDLmBuildRules.getText(currentElement)
    # print(allowBlankText) 
    # print(currentText) 
    currentTextLength = None
    currentTextTrimLength = None
    if currentText != None:
      currentTextLength = len(currentText)
      currentTextTrimLength = len(currentText.strip()) 
    # print(currentElement, currentTextLength, currentText) 
    # print(currentElement, currentText, currentTextTrimLength) 
    # Skip all None text values 
    if currentText == None:  
      return [None]
    # Check if blank text is allowed 
    if allowBlankText == False and \
       currentText.strip() == '':
      return [None]
    # print(currentElement, currentText) 
    if currentText != None:
      newTextRule = HDLmBuildRules.createText(wLHref, 
                                              wLHostName,
                                              hostNameWithSuffix,
                                              hostNameWithSuffixSiteNode,
                                              soup, 
                                              currentElement, 
                                              userUpdateRule) 
      return [newTextRule]
    return [None] 
  # Create one or more image rules for the current element. The 
  # caller passes the current element. The rule or rules are 
  # added to the rule tree. The image rule created by this 
  # routine is returned to the caller.  
  @staticmethod
  def createImage(wLHref, 
                  wLHostName,
                  hostNameWithSuffix, 
                  hostNameWithSuffixSiteNode,
                  soup, 
                  currentElement, 
                  userUpdateRule):
    newRuleCount = 0
    ruleTreeInfo = None
    # Get the image (if any) for the current element 
    currentImage = HDLmBuildRules.getImage(currentElement)
    # print(currentImage) 
    if currentImage == None:
      return None
    # Check the current image name 
    currentImageCheck = HDLmBuildRules.checkImage(currentImage)
    if currentImageCheck == None or \
       currentImageCheck == False:
      return None
    # Check if the current image starts with a dot and a slash. 
    # This is bad. The dot and the slash must be removed. 
    if currentImage != None   and \
       len(currentImage) >= 2 and \
       currentImage.startswith('./'):
      currentImage = currentImage[2:]
    # The image name may not start with a protocol and have a host
    # name in the image name. This needs to be fixed here. 
    startsWithProtocol = False
    if len(currentImage) >= 6 and \
       currentImage.startswith('https:'):
      startsWithProtocol = True
    elif len(currentImage) >= 5 and \
         currentImage.startswith('http:'):
      startsWithProtocol = True
    # If the current image name does not start with a protocol
    # then we need to fix the current image name 
    if startsWithProtocol == False:
      urlStr = wLHref 
      # let urlObj = new URL(urlStr)
      hostName = wLHostName
      currentImage = 'https://' + hostName + '/' + currentImage
      # print(currentImage) 
    # print(currentImage)
    startIndex = currentImage.find('://');
    if startIndex > 0:
      currentImage = currentImage[startIndex + 1:]
    # print(currentImage) 
    # print(currentElement, currentImage) 
    # Get the URL string from the current location 
    urlStr = wLHref
    # print(urlStr) 
    # Set a few values for use later 
    newModType = 'image'
    newActiveNodeType = 'newmod'
    ruleTreeInfo = HDLmBuildRules.build(soup,
                                        hostNameWithSuffix,
                                        hostNameWithSuffixSiteNode,
                                        currentElement,
                                        urlStr,
                                        '',
                                        newModType)
    # Check if we got a None value back. Just exit if need be. 
    if ruleTreeInfo == None:
      return None
    ruleModInfo = ruleTreeInfo.details
    ruleModInfo.images = [currentImage]
    ruleModInfo.parameter = HDLmTree.getParameterNumber(ruleTreeInfo)
    # print(ruleTreeInfo) 
    # Add the new modification to the rule tree 
    HDLmBuildRules.finish(currentElement, newActiveNodeType, ruleTreeInfo)
    # Check if we need to display the newly created rule. This is done
    # in some cases to the user modify the rule. 
    if userUpdateRule:
      HDLmBuildRules.display(currentElement, ruleTreeInfo)   
    # Show that a new rule was created 
    newRuleCount = 1
    return ruleTreeInfo
  # Create one or more text rules for the current element. The 
  # caller passes the current element. The rule or rules are 
  # added to the rule tree. The text rule created by this 
  # routine is returned to the caller.  
  @staticmethod
  def createText(wLHref, 
                 wLHostName, 
                 hostNameWithSuffix,
                 hostNameWithSuffixSiteNode,
                 soup, 
                 currentElement, 
                 userUpdateRule):
    newRuleCount = 0
    ruleTreeInfo = None
    # print('In HDLmBuildRules.createText') 
    # Get the text (if any) for the current element 
    currentText = HDLmBuildRules.getText(currentElement)
    # print(currentElement, currentText) 
    # Build a URL object from the URL passed by the caller.
    # Get the host name and path from it. 
    urlStr = wLHref
    # print(urlStr) 
    # Set a few values for use later 
    newModType = 'textchecked' 
    newActiveNodeType = 'newmod'
    # print(currentText) 
    ruleTreeInfo = HDLmBuildRules.build(soup,
                                        hostNameWithSuffix,
                                        hostNameWithSuffixSiteNode,
                                        currentElement,
                                        urlStr,  
                                        currentText,
                                        newModType)
    # print(ruleTreeInfo) 
    # Check if we got a None value back. Just exit if need be. 
    if ruleTreeInfo == None:
      return ruleTreeInfo
    # print(ruleTreeInfo.details.extra) 
    ruleModInfo = ruleTreeInfo.details
    ruleModInfo.newtexts = [currentText]
    ruleModInfo.parameter = HDLmTree.getParameterNumber(ruleTreeInfo)
    # Add the new modification to the rule tree    
    HDLmBuildRules.finish(currentElement, newActiveNodeType, ruleTreeInfo)
    # print(ruleTreeInfo.details.extra) 
    # Check if we need to display the newly created rule. This is done
    # in some cases to the user modify the rule. 
    #
    # print(userUpdateRule) 
    if userUpdateRule:
      HDLmBuildRules.display(currentElement, ruleTreeInfo)
      # print(ruleTreeInfo.details.extra)  
    # The code below is no longer in use. This code created a set of 
    # variations of the selected text and then sent the updated rule
    # back to the server.  
    if 1 == 2 and userUpdateRule: 
      # Get some text choice/variants from the server 
      response = HDLmWebSockets.getTextChoices(currentText) 
      # Get the node path for the current modification. This will only work
      # if the current modification is still displayed. If the current 
      # modification is gone, the call below will return None. 
      modificationNodePath = HDLmExtensionBothManageRules.getNodePathModification()
      if response != None and \
          modificationNodePath != None:
        responseObj = json.loads(response)
        choicesList = responseObj['choices']
        for choice in choicesList:
          # print(choice) 
          ruleModInfo['newtexts'].append(choice) 
        # Display the current modification with the additional text choices 
        HDLmBuildRules.display(currentElement, ruleTreeInfo)
        # Send the updated modifcation back to the server 
        HDLmWebSockets.sendUpdateTreeNodeRequest(ruleTreeInfo)
    # Show that a new rule was created 
    newRuleCount = 1
    return ruleTreeInfo
  # Display the current modification. The user may or may not 
  # make various changes to the current modification. The modification
  # has already been saved at this point.  
  @staticmethod
  def display(currentElement, ruleTreeInfo):
    divDescriptions = HDLmDefines.getString('HDLMENTRYDESCRIPTIONS')
    divValues = HDLmDefines.getString('HDLMENTRYVALUES')
    # The active node type is set to a standard value here. This value 
    # will allow normal finish tree node processing to happen, if we are
    # creating a new modification rule. 
    newTreeEntryTrue = True
    callSource = 'buildRulesDisplay'
    handlingCmdInsertFalse = False
    inlineStartupFlagFalse = False
    possibleRuleTypesNone = None
    HDLmMod.displayMod(divDescriptions, divValues, ruleTreeInfo,
                       possibleRuleTypesNone, currentElement,
                       HDLmGlobals.activeEditorType, newTreeEntryTrue,
                       inlineStartupFlagFalse, handlingCmdInsertFalse,
                       callSource)
  # Build zero or one rule for the current element. The current
  # element may just be ignored. This routine recursively calls
  # itself for all child elements of the current element. 
  @staticmethod
  def element(wLHref, 
              wLHostName, 
              hostNameWithSuffix,
              hostNameWithSuffixSiteNode,
              outputRules, 
              soup, 
              currentElement):
    # print('In HDLmBuildRules.element') 
    # print(currentElement) 
    #
    # Try to get the uppercase version of the current tag name.
    # This is not possible in all cases. Some elements don't  
    # have a tag we can accesss.
    currentElementName = currentElement.name
    if currentElementName != None:
      tagNameUpper = currentElement.name.upper()
    # Get and check the current element tag name. We just ignore quite
    # a few elements based on their tag names. 
    useCreate = True
    if currentElementName == None or \
       HDLmBuildRules.checkElement(currentElement, tagNameUpper) == False:
      useCreate = False
    # Create zero or more rules for the current element, if possible
    if useCreate:
      allowBlankTextFalse = False
      userUpdateRuleFalse = False
      newOutputRules = HDLmBuildRules.create(wLHref, 
                                             wLHostName,
                                             hostNameWithSuffix,
                                             hostNameWithSuffixSiteNode,
                                             soup,
                                             currentElement, 
                                             userUpdateRuleFalse,
                                             allowBlankTextFalse)
      if newOutputRules != [None] and newOutputRules != None:
        outputRules.extend(newOutputRules)
    # Check if we should skip the current element
    if currentElement == '\n':
      return outputRules
    if str(type(currentElement)) == "<class 'bs4.element.NavigableString'>":
      return outputRules
    # Get all of the child elements of the current element 
    currentElementChildren = currentElement.children
    # Process all of the child elmements of the current element  
    for childElement in currentElementChildren: 
       HDLmBuildRules.element(wLHref,     
                              wLHostName, 
                              hostNameWithSuffix,
                              hostNameWithSuffixSiteNode,
                              outputRules,
                              soup,       
                              childElement)
    # Always return all of the rules we have created so far, to the caller
    return outputRules
  # Finish the current modification. This code will cause the
  # current modification to be saved.  
  @staticmethod
  def finish(currentElement, newActiveNodeType, ruleTreeInfo):
    # print('In HDLmBuildRules.finish')
    # print(currentElement) 
    # print(newActiveNodeType) 
    # print(ruleTreeInfo)  
    # Add the new modification to the rule tree 
    callFromCallbackFalse = False
    containerAvailableFalse = False
    newTreeEntryFalse = False
    handlingCmdInsertFalse = False
    needUserInputFalse = False
    possibleRuleTypes = None
    # Set the system character to a standard value 
    systemCharacter = 'a'
    HDLmStateInfo.setEntriesSystemValue(systemCharacter)
    HDLmGlobals.activeEditorType = HDLmEditorTypes.passEnum
    HDLmGlobals.setActiveNodeType(newActiveNodeType)
    # print(ruleTreeInfo.details.extra) 
    [insertIntoDone, addTreeNodeDone, rvStr] = \
      HDLmMenus.finishTreeNode(ruleTreeInfo, containerAvailableFalse,
                               possibleRuleTypes, currentElement,
                               newTreeEntryFalse, handlingCmdInsertFalse,
                               callFromCallbackFalse, needUserInputFalse)
    # print(ruleTreeInfo.details.extra) 
  # Try to get the image associated with the current element.
  # This may not work. We may not have a valid image for the
  # current element. Note that an invalid image is just ignored. 
  @staticmethod
  def getImage(currentElement):
    # Set a few initial values 
    rvImage = None
    # Check for something that can not be an image
    if currentElement == '\n':
      return rvImage
    # Check for an image <img> tag 
    currentElementTag = currentElement.name
    if currentElementTag == None:
      return rvImage
    currentElementTagUpper = currentElementTag.upper()
    if currentElementTagUpper != 'IMG':
      return rvImage
    # Get the value of the source attribute 
    srcValue = currentElement['src']
    if srcValue == None:
      return rvImage
    rvImage = srcValue
    return rvImage
  # Try to get the text associated with the current element.
  # This may not work. We may not have any valid text for the
  # current element. Note that invalid text is just ignored. 
  @staticmethod
  def getText(currentElement):
    # Set a few initial values 
    rvText = None
    if currentElement == '\n':
      return rvText
    if currentElement.name == 'br':
      return rvText
    if hasattr(currentElement, 'children'):
      currentElementChildren = currentElement.children
      if currentElementChildren == None:
        return rvText
      # print('gt 1 ' + str(type(currentElement))) 
      # print(currentElement, currentElementChildren) 
      # Check all of the sub nodes of the current node. We 
      # are only interested in text sub nodes, and only some
      # of those. 
      for child in currentElementChildren:
        # Check for a navigable string node. Skip all other 
        # node types. 
        if str(type(child)) != "<class 'bs4.element.NavigableString'>":
          continue
        # Handle the sub nodes of the current element
        childText = child
        if childText == None:
          continue
        if childText.startswith('\n'):
          continue
        rvText = childText
        break 
    return rvText 
  # This method gets a unique host name from a host name passed to 
  # it. A unique host name is created by adding a suffix to the 
  # original host name. The suffix takes the form of a blank, a 
  # left parenthesis, a number, and a right parenthesis. The suffix
  # must be unique and never used before. 
  @staticmethod
  def getUniqueHostName(hostName):
    # Find the companies tree node
    newNodePath = []
    newNodePath.append(HDLmDefines.getString('HDLMTOPNODENAME'))
    newNodePath.append(HDLmDefines.getString('HDLMCOMPANIESNODENAME'))
    # At this point we can try to locate the companies node. This
    # step should never fail. However, you never know what is going
    # to fail or not. 
    companiesTreeNode = HDLmTree.locateTreeNode(newNodePath)
    # Report an error if the companies node could not be found 
    if companiesTreeNode == None:
      nodeString = str(newNodePath)
      HDLmError.buildError('Error', 'Locate', 9, nodeString)
      return None    
    # Adjust the host name (by adding a numeric suffix in parenthesis) 
    forceSuffixTrue = True
    removeTailsTrue = True
    uniqueHostName = HDLmMenus.adjustTreeNodeName(hostName,
                                                  companiesTreeNode, 
                                                  removeTailsTrue,
                                                  forceSuffixTrue)
    return uniqueHostName