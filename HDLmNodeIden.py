# The HDLmNodeIden class is used to create objects in several places
# This class also contains code for creating and handling node
# identifiers. 

from   bs4          import BeautifulSoup 
from   HDLmAssert   import *
from   HDLmEmpty    import *
from   HDLmError    import *
from   HDLmDefines  import *
from   HDLmHtml     import *
from   HDLmString   import *
from   HDLmUrl      import *
from   HDLmUtility  import *
import jsons
import math
import re
import types

class HDLmNodeIden(object):
  # The __init__ method creates an instance of the class
  def __init__(self):
    # Each node identifier nas a set of fields
    self.attributes = None
    self.counts = None
    self.type = None
    self.parent = None
    self.grand = None 
  # This method build a set of node identifier values for a DOM element
  # node. This information can be used to find the DOM element node
  # later. The information is returned to the caller as a JSON string. 
  @staticmethod
  def buildNodeIdentifierObj(soup, currentElement):
    # print('In HDLmNodeIden.buildNodeIdentifer')
    # print(currentElement) 
    # Create an empty object that will contain all of the
    # count values for each type of search 
    counts = HDLmNodeIden.getCounts(soup, currentElement)
    # print('In HDLmNodeIden.buildNodeIdentifer')
    # print(counts) 
    # Find the key with the lowest count value 
    minKey = HDLmNodeIden.getLowestCount(counts)
    # print(minKey) 
    # Get all of the attributes of the current element 
    currentAttrsObj = HDLmNodeIden.getAttributes(currentElement)
    # print(currentAttrsObj) 
    currentAttrsObj = HDLmNodeIden.updateAttrsFields(currentAttrsObj)
    # print(currentAttrsObj)  
    # Try to get the HTML attributes of the parent HTML element. Of course,
    # we may not have a parent HTML element. 
    parentAttrsObj = types.SimpleNamespace()
    parentElement = currentElement.parent
    if parentElement != None:
      parentAttrsObj = HDLmNodeIden.getAttributes(parentElement)
      parentAttrsObj = HDLmNodeIden.updateAttrsFields(parentAttrsObj) 
    # Try to get the HTML attributes of the grant parent HTML element. Of course,
    # we may not have a grand parent HTML element. Indeed we may not even have a
    # parent element. 
    grandElement = None
    grandAttrsObj = types.SimpleNamespace()
    if parentElement != None:
      grandElement = parentElement.parent
      if grandElement != None:
        grandAttrsObj = HDLmNodeIden.getAttributes(grandElement)
        grandAttrsObj = HDLmNodeIden.updateAttrsFields(grandAttrsObj)
    # Add the tag as an attribute of the current element. The tag is not
    # really an attribute of the current element. Howver, we treat the tag
    # as an attribute anyway. 
    #
    # print(currentAttrsObj) 
    # print('tag') 
    # print(currentElement) 
    currentAttrsObj.tag = currentElement.name.lower()
    # Check if the current DOM element has any inner text. If it does,
    # save the inner text as an attribute. Of course, inner text is not
    # not really an attribute. However, treating inner text as an attribute
    # makes the rest of the code much simpler. Note that the inner text (if
    # any) is always converted to lower case. This is because the inner text
    # has a bad habit of changing case, as the browser window changes size.
    # To make the inner text more stable, we always convert it to lower case. 
    currentInnerText = HDLmNodeIden.getInnerText(currentElement) 
    if str(type(currentInnerText)) == "<class 'NoneType'>":
      currentInnerText = None
    if currentInnerText != None:
      currentIndexOf = currentInnerText.find('') # Vertical bar
      if currentIndexOf >= 0 and currentIndexOf < 0:
        currentInnerText = currentInnerText[0:currentIndexOf]
      currentIndexOf = currentInnerText.find('\n')
      if currentIndexOf >= 0:
        currentInnerText = currentInnerText[0:currentIndexOf]
      currentInnerText = currentInnerText.lower().strip()
      maxNodeIdenTextLength = HDLmDefines.getNumber('HDLMMAXIDENTEXTLEN')
      if len(currentInnerText) > maxNodeIdenTextLength:
        currentInnerText = currentInnerText[0:maxNodeIdenTextLength]
    if currentInnerText != None:
      currentAttrsObj.innertext = currentInnerText
    # Add the tag as an attribute of the parent element. The tag is not
    # really an attribute of the parent element. Howver, we treat the tag
    # as an attribute anyway. 
    if parentElement != None:
      parentAttrsObj.tag = parentElement.name.lower()
      # Check if the parent DOM element has any inner text. If it does,
      # save the inner text as an attribute. Of course, inner text is not
      # not really an attribute. However, treating inner text as an attribute
      # makes the rest of the code much simpler. Note that the inner text (if
		  # any) is always converted to lower case. This is because the inner text
		  # has a bad habit of changing case, as the browser window changes size.
      # To make the inner text more stable, we always convert it to lower case. 
      parentInnerText = HDLmNodeIden.getInnerText(parentElement) 
      if str(type(parentInnerText)) == "<class 'NoneType'>":
        parentInnerText = None
      if parentInnerText != None:
        parentIndexOf = parentInnerText.find('') # Vertical bar
        if parentIndexOf >= 0 and parentIndexOf < 0:
          parentInnerText = parentInnerText[0:parentIndexOf]
        parentIndexOf = parentInnerText.find('\n')
        if parentIndexOf >= 0:
          parentInnerText = parentInnerText[0:parentIndexOf]
        parentInnerText = parentInnerText.lower().strip()
        maxNodeIdenTextLength = HDLmDefines.getNumber('HDLMMAXIDENTEXTLEN')
        if len(parentInnerText) > maxNodeIdenTextLength:
          parentInnerText = parentInnerText[0:maxNodeIdenTextLength] 
      if parentInnerText != None:
        parentAttrsObj.innertext = parentInnerText 
    # Add the tag as an attribute of the grand parent element. The tag is not
    # really an attribute of the grand parent element. Howver, we treat the tag
    # as an attribute anyway. 
    if grandElement != None:
      grandAttrsObj.tag = grandElement.name.lower()
      # Check if the grand parent DOM element has any inner text. If it does,
      # save the inner text as an attribute. Of course, inner text is not
      # not really an attribute. However, treating inner text as an attribute
      # makes the rest of the code much simpler. Note that the inner text (if
		  # any) is always converted to lower case. This is because the inner text
		  # has a bad habit of changing case, as the browser window changes size.
      # To make the inner text more stable, we always convert it to lower case. 
      grandInnerText = HDLmNodeIden.getInnerText(grandElement) 
      if str(type(grandInnerText)) == "<class 'NoneType'>":
        grandInnerText = None
      if grandInnerText != None:
        grandIndexOf = grandInnerText.find('') # Vertical bar
        if grandIndexOf >= 0 and grandIndexOf < 0:
          grandInnerText = grandInnerText[0:grandIndexOf]
        grandIndexOf = grandInnerText.find('\n')
        if grandIndexOf >= 0:
          grandInnerText = grandInnerText[0:grandIndexOf]
        grandInnerText = grandInnerText.lower().strip()
        maxNodeIdenTextLength = HDLmDefines.getNumber('HDLMMAXIDENTEXTLEN')
        if len(grandInnerText) > maxNodeIdenTextLength:
          grandInnerText = grandInnerText[0:maxNodeIdenTextLength] 
      if grandInnerText != None:
        grandAttrsObj.innertext = grandInnerText 
    # Build the final node informaton object 
    nodeIdenObj = HDLmNodeIden()
    nodeIdenObj.type = minKey
    nodeIdenObj.attributes = currentAttrsObj
    nodeIdenObj.counts = counts
    if jsons.dumps(parentAttrsObj) != '{}':
      nodeIdenObj.parent = parentAttrsObj
    if jsons.dumps(grandAttrsObj) != '{}':
      nodeIdenObj.grand = grandAttrsObj
    return nodeIdenObj
  # This JavaScript function tries to find a set of HTML elements
  # (DOM elements) that match the node identifier passed by the
  # caller. The DOM is always searched using one of the built-in
  # Beautiful Soup functions.
  #
  # A copy of this code is use to find DOM elements that may need to
  # be changed in the inserted JavaScript program. The code in the
  # copy is a slightly modified version of this code. 
  @staticmethod
  def findNodeIden(soup, nodeIdenDict, nodeIdenTracing): 
    nodeElements = []
    nodeIdenLocalDict = nodeIdenDict
    nodeList = []
    nodeAttributesDict = nodeIdenLocalDict['attributes']
    nodeCountsDict = nodeIdenLocalDict['counts']
    nodeType = nodeIdenLocalDict['type']
    # nodeIdenTracing = HDLmNodeIdenTracing.all 
    #
    # We need to use a different function depending on the type
    # of the node identifier  
    #
    # We may be searching by tag name. This might work in some
    # cases. 
    if nodeType == 'tag':
      nodeTag = nodeAttributesDict['tag']
      nodeElements = soup.find_all(nodeTag)
    # We may be searching by id. This will only work if the id
    # values are permanent, rather than generated. Generated id
    # values change each time a web page is loaded. As a consequence,
    # they can not be used. 
    elif nodeType == 'id':  
      nodeId = nodeAttributesDict['id']
      nodeElement = soup.find_all(id=nodeId)
      if nodeElement != None:
        if str(type(nodeElement)) != "<class 'list'>":
          nodeElements = [nodeElement]
        else:
          nodeElements = nodeElement
      else:
        nodeElements = [] 
    # We may be searching by class name. Class names tend to be
    # relatively permanent and hence are a good thing to search
    # for. Of course, an HTML DOM node can have more than one
    # class name. The first class name is always used. 
    elif nodeType == 'class':
      nodeClassList = nodeAttributesDict['class']
      nodeClass = nodeClassList[0]
      nodeElements = soup.find_all(class_=nodeClass)
    # We may be searching by name. This will work in some cases. 
    elif nodeType == 'name':
      nodeName = nodeAttributesDict['name']
      nodeElements = soup.find_all(attrs={"name": nodeName})
    # The default case should never happen, but you never know
    else:
      errorText = 'Invalid node identifier type value - ' + nodeType
      HDLmError.buildError('Error', 'NodeIden', 40, errorText) 
      HDLmAssert(False, errorText)
    # Save the number of node elements found in a local variable. This variable
    # is used in several places below. 
    nodeElementsLength = len(nodeElements)
    # Check if node identifier tracing is active or not. Trace the
    # number of nodes, if need be. 
    if nodeIdenTracing == HDLmNodeIdenTracing.all:
      errorText = f'Node identifier - get for (${nodeType}) returned (${nodeElementsLength}) nodes'
      HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
    # Check for a very special case. If the original node identifier collection
    # found just one DOM HTML element for the current type and if current document
    # search also found just one DOM HTML element for the current type, then we
    # are done. We don't need to check any attributes. 
    if nodeCountsDict[nodeType] == 1 and nodeElementsLength == 1:
      return nodeElements
    # At this point we have a set of HTML node elements. Some of them
    # may really match the node identifier criteria. Others may not. 
    nodeList = HDLmNodeIden.findNodeIdenCheck(nodeElements,
                                              nodeIdenLocalDict,
                                              nodeIdenTracing)
    return nodeList
  # This routine takes a list of HTML node elements and checks each one.
  # If an HTML node matches the current attributes (well enough), it is
  # added to the output list of HTML nodes that is returned to the caller. 
  @staticmethod
  def findNodeIdenCheck(nodeElements, nodeIdenDict, nodeIdenTracing):
    nodeList = []
    for currentElement in nodeElements:
      # Get the node identifier attributes and convert them to
      # a dictionary
      nodeCurrentIdenAttributesDict = nodeIdenDict['attributes'] 
      currentMatchValue = HDLmNodeIden.findNodeIdenMatch(currentElement,
                                                         nodeCurrentIdenAttributesDict,
                                                         nodeIdenTracing)
      # Check if node identifier tracing is active or not. Trace the
      # match value, if need be. 
      if nodeIdenTracing == HDLmNodeIdenTracing.all:
        errorText = f'Node identifier - current match value (${currentMatchValue}) for element (${currentElement})'
        HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
      if currentMatchValue < 0.95:
        continue
      # We now need to check the attributes of the parent of the current
      # HTML DOM element, if possible 
      parentElement = currentElement.parent
      if parentElement != None:
        nodeParentAttributesDict = nodeIdenDict['parent']
        parentMatchValue = HDLmNodeIden.findNodeIdenMatch(parentElement,
                                                          nodeParentAttributesDict,
                                                          nodeIdenTracing)
        # Check if node identifier tracing is active or not. Trace the
        # match value, if need be. 
        if nodeIdenTracing == HDLmNodeIdenTracing.all:
          errorText = f'Node identifier - parent match value (${parentMatchValue}) for element (${parentElement})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
        if parentMatchValue < 0.95:
          continue 
      # We now need to check the attributes of the grand parent of the current
      # HTML DOM element, if possible 
      grandElement = None
      if parentElement != None:
        grandElement = parentElement.parent
      if grandElement != None:
        nodeGrandAttributesDict = nodeIdenDict['grand']
        grandMatchValue = HDLmNodeIden.findNodeIdenMatch(grandElement,
                                                         nodeGrandAttributesDict,
                                                         nodeIdenTracing)
        # Check if node identifier tracing is active or not. Trace the
        # match value, if need be. 
        if nodeIdenTracing == HDLmNodeIdenTracing.all:
          errorText = f'Node identifier - grand parent match value (${grandMatchValue}) for element (${grandElement})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
        if grandMatchValue < 0.95:
          continue 
      nodeList.append(currentElement) 
    return nodeList 
  # This routine takes one HTML node element and checks how well it matches
  # a set of attributes. The final match score is returned to the caller.
  # The final match score is a floating-point value in the range of 0.0
  # to 1.0. The HTML DOM element (node element) and the expected node
  # attributes are passed by the caller. 
  # 
  # Note that the node identifier attributes passed to this routine
  # will always be a dictionary, not an object. This statement is 
  # checked with an assertion below.
  @staticmethod
  def findNodeIdenMatch(nodeElement, nodeIdenAttributesDict, nodeIdenTracing):
    # Make sure that the attributes passed to this routine are a dictionary,
    # versus anything else
    if str(type(nodeIdenAttributesDict)) != "<class 'dict'>":
      errorText = 'Node identification attributes passed to this routine are not a dictionary'
      HDLmAssert(False, errorText)
    denominator = 0.0
    nodeIdenAttributeTagUpper = nodeIdenAttributesDict['tag'].upper()
    numerator = 0.0 
    # Check for a quick exit. If the tag name doesn't match, then
    # we are done. We insist that the tag name match immediately
    # and exactly. 
    if nodeElement.name.upper() != nodeIdenAttributeTagUpper:
      return 0.0
    # Check all of the attributes passed by the caller. Get the
    # set of keys for each of the attributes. The keys are used
    # to obtain the expected and actual value of each attribute. 
    nodeIdenAttributeKeys = nodeIdenAttributesDict.keys()
    for nodeIdenAttributeKey in nodeIdenAttributeKeys:
      numeratorIncrementValue = 0.0
      # Always bump the denominator. This is done for all
      # attributes including those that don't match. 
      denominator += 1
      # Get the current node attributes expected value from the node
      # attributes passed by the caller. Note that these are the
      # expected values. For most attributes this is a string. For
      # class attributes, this is an array of class names. 
      nodeIdenAttributeValue = nodeIdenAttributesDict[nodeIdenAttributeKey]
      # Check if the attribute we want is the tag. The tag is not really
      # an attribute. Special case code is needed to handle the tag.
      # A special call is needed to get the actual tag name of the
      # DOM element. This call will always return the tag name in
      # uppercase. As a consequence, the expected value must also be
      # changed to uppercase. 
      if nodeIdenAttributeKey == 'tag':
        nodeActualValue = nodeElement.name.upper()
        nodeIdenAttributeValue = nodeIdenAttributeValue.upper()
        # Check if node identifier tracing is active or not. Trace the
        # attribute values, if need be. 
        if nodeIdenTracing == HDLmNodeIdenTracing.all: 
          traceValue = 0.0
          if nodeActualValue != None and \
            nodeIdenAttributeValue == nodeActualValue:
            traceValue = 1.0
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) actual (${nodeActualValue}) expected (${nodeIdenAttributeValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText)
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) comparison value (${traceValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
        # If we don't have a value that we can compare, then we are done 
        if nodeActualValue == None:
          continue
        # Compare the expected value and the actual value. If they are the
        # same, then we can increment the numerator. 
        if nodeIdenAttributeValue == nodeActualValue:
          numeratorIncrementValue = 1.0 
      # Check if the attribute we want is the class. The class in the
      # DOM element is always just one string. However, the DOM class
      # string can have several class names in it. The code below
      # extracts the first actual (DOM) class name and the first
      # expected class name. 
      elif nodeIdenAttributeKey == 'class':
        nodeActualValueString = nodeElement['class']
        # print('In HDLmNodeIden.findNodeIdenMatch', nodeActualValueString) 
        if 1 == 2 and nodeActualValueString != None:
          nodeActualValueString = HDLmNodeIden.removeClassStrings(nodeActualValueString)   
          # print('In HDLmNodeIden.findNodeIdenMatch', nodeActualValueString) 
          if nodeActualValueString == '':
            nodeActualValueString = None 
        # print('In HDLmNodeIden.findNodeIdenMatch', nodeActualValueString) 
        if nodeActualValueString != None:
          nodeActualValueSplit = nodeActualValueString.split(' ')
          nodeActualValue = nodeActualValueSplit[0] 
        else:
          nodeActualValue = None
        # Check if node identifier tracing is active or not. Trace the
        # attribute values, if need be. 
        if nodeIdenTracing == HDLmNodeIdenTracing.all: 
          traceValue = 0.0
          if nodeActualValue != None and \
            nodeIdenAttributeValue.includes(nodeActualValue):
            traceValue = 1.0
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) actual (${nodeActualValue}) expected (${nodeIdenAttributeValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText)
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) comparison value (${traceValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
        # If we don't have a value that we can compare, then we are done 
        if nodeActualValue == None:
          continue
        # Check if the actual value (the first actual class value) is one of
        # the expected class values. If this is true, then we can increment
        # the numerator. 
        if nodeIdenAttributeValue.includes(nodeActualValue):
          numeratorIncrementValue = 1.0 
      # Check if the attribute we want is the inner text. The inner
      # text is not really an attribute. Special case code is needed
      # to handle the inner text. A special call is needed to get the
      # actual inner text (if any) for a DOM element. Note that the
      # inner text (if any) is always converted to lower case. This
      # is because the inner text has a bad habit of changing case,
      # as the browser window changes size. To make the inner text
      # more stable, we always convert it to lower case.
      elif nodeIdenAttributeKey == 'innertext': 
        nodeInnerText = HDLmNodeIden.getInnerText(nodeElement)
        if str(type(nodeInnerText)) == "<class 'NoneType'>":
          nodeInnerText = None
        if nodeInnerText != None:
          nodeIndexOf = nodeInnerText.find('') # Vertical bar
          if nodeIndexOf >= 0 and nodeIndexOf < 0:
            nodeInnerText = nodeInnerText[0:nodeIndexOf]
          nodeIndexOf = nodeInnerText.find('\n')
          if nodeIndexOf >= 0:
            nodeInnerText = nodeInnerText[0:nodeIndexOf]
          nodeInnerText = nodeInnerText.lower().strip()
          maxNodeIdenTextLength = HDLmDefines.getNumber('HDLMMAXIDENTEXTLEN')
          if len(nodeInnerText) > maxNodeIdenTextLength:
            nodeInnerText = nodeInnerText[0:maxNodeIdenTextLength] 
        nodeActualValue = nodeInnerText
        # Check if node identifier tracing is active or not. Trace the
        # attribute values, if need be. 
        if nodeIdenTracing == HDLmNodeIdenTracing.all:
          traceValue = 0.0
          if nodeActualValue != None and \
            HDLmString.compareCaseInsensitive(nodeIdenAttributeValue,
                                              nodeActualValue):
            traceValue = 1.0
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) actual (${nodeActualValue}) expected (${nodeIdenAttributeValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText)
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) comparison value (${traceValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
        # If we don't have a value that we can compare, then we are done 
        if nodeActualValue == None:
          continue
        # Compare the expected value and the actual value. If they are the
        # same, then we can increment the numerator. 
        if HDLmString.compareCaseInsensitive(nodeIdenAttributeValue,
                                             nodeActualValue):
          numeratorIncrementValue = 1.0 
      # For all other attributes, we can just extract the actual
      # attribute value from the DOM element 
      else:
        nodeActualValue = nodeElement[nodeIdenAttributeKey]
        # Check if the attribute we want is href. Special case code
        # is needed for handling href. Basically, we need to remove
        # the protocol and host before we do any matching on href.
        # This was done in building the node identifier. 
        if nodeIdenAttributeKey == 'href':
          if len(nodeActualValue) >= 7 and \
             nodeActualValue.startswith('mailto:'):
            nodeActualValue = nodeActualValue
          elif len(nodeActualValue) >= 4 and \
               nodeActualValue.startswith('tel:'):
            nodeActualValue = nodeActualValue
          else:
            nodeActualValue = HDLmUtility.removeHost(nodeActualValue) 
        # Check if node identifier tracing is active or not. Trace the
        # attribute values, if need be. 
        if nodeIdenTracing == HDLmNodeIdenTracing.all:
          traceValue = 0.0
          if nodeActualValue != None and \
            nodeIdenAttributeValue == nodeActualValue:
            traceValue = 1.0
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) actual (${nodeActualValue}) expected (${nodeIdenAttributeValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText)
          errorText = f'Node identifier - key (${nodeIdenAttributeKey}) comparison value (${traceValue})'
          HDLmError.buildError('Trace', 'NodeIden', 41, errorText) 
        # If we don't have a value that we can compare, then we are done 
        if nodeActualValue == None:
          continue
        # Compare the expected value and the actual value. If they are the
        # same, then we can increment the numerator. 
        if nodeIdenAttributeValue == nodeActualValue:
          numeratorIncrementValue = 1.0 
      # Possibly increment the numerator 
      numerator += numeratorIncrementValue 
    return numerator / denominator 
  # Get the attribute values for the DOM element passed by the caller.
  # This routine returns an object with a property for each DOM element
  # attribute. The property name is the attribute name. The property
  # value is the attribute value. 
  @staticmethod
  def getAttributes(element):
    attrsObj = HDLmEmpty()
    # The code below produces a dictionary with an entry for each 
    # node attribute. This is a feature of Beautiful Soup.
    elementAttrsDict = element.attrs
    elementAttrsLength = len(elementAttrsDict)
    keys = elementAttrsDict.keys()
    for key in keys:
      # Get the name and value of the current attribute 
      attrsDictName = key
      attrsDictValue = elementAttrsDict[key]
      # Check if the attribute name starts with a special string. These
      # attriutes are created by our code and we definitely don't want
      # to check them. These attributes must be bypassed and not treated
      # as normal attributes. 
      if attrsDictName.startswith('hdlmupdated'):
        continue
      # We need some very special case code for the class attribute. The
      # class attribute in actually a simple string. However, we don't
      # want to treat the class attribute as a simple string. We want
      # to create an array with each of the class values in it. 
      if attrsDictName == 'class':
        if str(type(attrsDictValue)) == "<class 'list'>" and \
           len(attrsDictValue) > 0:
          attrsDictValue = attrsDictValue[0]          
        attrsDictValueSplit = attrsDictValue.split(' ')
        attrsDictValueSplitLength = len(attrsDictValueSplit)
        attrsDictValueList = []
        for i in range(0, attrsDictValueSplitLength): 
          # Add the current class value to the class value array.
          # However, we don't want to add zero-length class values
          # to the class value array. Check the length of the current
          # class value and skip it, if it is a zero-length class
          # value. 
          attrsDictValueSplitValue = attrsDictValueSplit[i]
          # We need to check the current class value to see if it
          # ends with a newline character. If we find a newline
          # character at the end of the current class value, then
          # we need to remove it. 
          if attrsDictValueSplitValue.endswith('\n'):
            attrsDictValueSplitValueLen = len(attrsDictValueSplitValue)
            attrsDictValueSplitValue = attrsDictValueSplitValue[0:attrsDictValueSplitValueLen - 1]           
          # Check if the remaining length is greater than zero 
          if len(attrsDictValueSplitValue) > 0:
            attrsDictValueList.append(attrsDictValueSplitValue) 
        attrsDictValue = attrsDictValueList 
      # We need to use some special case code for href attributes. The
      # problem is that we always want to use relative names, not href
      # values that have a host name in them. 
      if attrsDictName == 'href':
        if len(attrsDictValue) >= 7 and \
            attrsDictValue.startswith('mailto:'):
          attrsDictValue = attrsDictValue
        elif len(attrsDictValue) >= 4 and \
                 attrsDictValue.startswith('tel:'):
          attrsDictValue = attrsDictValue
        else:
          attrsDictValue = HDLmUtility.removeHost(attrsDictValue)  
      # Generally we use all attributes. However, some attributes are just
      # too dangerous to use. For example, an id (note, lower case) attribute 
      # with a generated numeber value that was probably generated. It will 
      # change each time it is used. We should not use it as a consequence. 
      if attrsDictName == 'id':
        numCount = HDLmString.numericCount(attrsDictValue)
        if numCount > 0 or len(attrsDictValue) < 3:
          continue 
      setattr(attrsObj, attrsDictName, attrsDictValue) 
    return attrsObj  
  # Get the count values for the current element. This is the number of
  # times the tag, id, class, and name occur in the current DOM. Of course,
  # special case code is used to handle (ignore) generated id (note, lower 
  # case) values and only the first class is checked. 
  @staticmethod
  def getCounts(soup, element):
    # Create an empty object that will contain all of the
    # count values for each type of search 
    counts = types.SimpleNamespace()
    # Get the count of DOM elements with the current tag name 
    elementTag = element.name
    nodeList = soup.find_all(elementTag)
    nodeListCount = len(nodeList)
    counts.tag = nodeListCount
    elementAttrsDict = element.attrs
    # Get the count of DOM elements with the current element id (note, lower 
    # case) value. Of course, this number should always be one. Id values are 
    # supposed to be unique. In real life, they aren't always unique (because 
    # of bugs). This assumes that the current DOM element has an id value (not
    # always true) and that the id value can be used. If the id value
    # has any numeric characters, then we will not use it. 
    if 'id' in elementAttrsDict:
      elementId = element['id']
      if elementId != None:
        numCount = HDLmString.numericCount(elementId)
        if numCount == 0 and len(elementId) >= 3:
          counts.id = 1
    # Get the count of DOM elements with the current class value. In
    # real life, class values can actually contain multiple class
    # values. We only use the first class value for now. 
    if 'class' in elementAttrsDict: 
      elementClassStrings = element['class']
      elementClassString = None
      if str(type(elementClassStrings)) == "<class 'list'>" and \
         len(elementClassStrings) > 0:
        elementClassString = elementClassStrings[0]       
      # print('In HDLmNodeIden.getCounts') 
      # print(elemClassString)
      if elementClassString != None:
        elementClassString = HDLmNodeIden.removeClassStrings(elementClassString)
        # print('In HDLmNodeIden.getCounts', elementClassString) 
        if elementClassString == '':
          elementClassString = None 
      # print('In HDLmNodeIden.getCounts', elementClassString) 
      if elementClassString != None:
        elementClassSplit = elementClassString.split(' ')
        elementClassFirst = elementClassSplit[0]
        nodeList = soup.find_all(class_=elementClassFirst)
        nodeListCount = len(nodeList)
        setattr(counts, 'class', nodeListCount)  
    # Get the count of DOM elements with the current name value. In
    # real life, not all DOM elements have a name. 
    if 'name' in elementAttrsDict:
      elementName = element['name']
      if elementName != None:
        nodeList = soup.find_all(attrs={"name": elementName})
        nodeListCount = len(nodeList)
        counts.name = nodeListCount 
    return counts 
  # Get the inner text for a DOM element. Beautiful Soup does not
  # provide this functionality out-of-the-box. We provide a routine
  # that does this. The native DOM does have provide inner text, as 
  # need be. We provide something like inner text here.
  @staticmethod
  def getInnerText(element):
    # Build a list of output entries 
    outputList = []
    HDLmNodeIden.getInnerTextChild(element, outputList)
    # Try to get the final inner text
    outputListLen = len(outputList)
    if outputListLen == 0:
      return None
    finalInnerText = ''
    for output in outputList:
      # Newlines in the list are just ignored and not used
      if output == '\n':
        continue
      # Break elements are changed into newlines that are 
      # actually used
      if output == 'elementBrTag':
        finalInnerText += '\n'
        continue      
      finalInnerText += output  
    # Remove any extra whitespace from the final text
    while True:
      newFinalText = re.sub('\\n +', '\\n', finalInnerText)
      if newFinalText != finalInnerText:
        finalInnerText = newFinalText
      newFinalText = re.sub('  +', ' ', finalInnerText)
      if newFinalText == finalInnerText:
        break
      finalInnerText = newFinalText
    finalInnerText = finalInnerText.replace(' elementLiTag', '\n')
    finalInnerText = finalInnerText.strip() 
    return finalInnerText.strip()
  # The next routine recursively calls itself to get inner text 
  # and more tags in some cases
  @staticmethod
  def getInnerTextChild(element, outputList):
    # Get the name (really the tag) of the current element
    elementName = element.name 
    # Check for a 'style' (without the quotes) element. We 
    # need to skip all style elements and the children of   
    # any style elements.
    if elementName == 'style':
      return
    # Check if current element has any attributes and if we have
    # the hidden attribute
    if hasattr(element, 'attrs'):
      elementAttrs = element.attrs
      if 'hidden' in elementAttrs and \
         elementAttrs['hidden'] == '':
        return
    # Check for an HTML break. We add a break in this case.
    if elementName == 'br':
      outputList.append('elementBrTag')
      return
    # One tag is handled in a special way. This tag is returned
    # to the caller with a special name. 
    if elementName == 'li':
      outputList.append('elementLiTag') 
    # Check if we have a string that we can use
    if str(type(element)) == "<class 'bs4.element.NavigableString'>":
      elementText = element.string
      # Remove any extra whitespace from the current element text
      while True:
        newElementText = re.sub('\\s +', ' ', elementText)
        if newElementText == elementText:
          break
        elementText = newElementText
      if elementText == '':
        return
      # Check if the current element is really 'hidden text' (without 
      # the quotes). Skip all text that is hidden.       
      elementParent = element.parent
      if elementParent != None:
        elementParentAttrs = elementParent.attrs
        if 'style' in elementParentAttrs:
          elementParentStyle = elementParentAttrs['style']
          elementParentVisibility = HDLmHtml.checkVisibility(elementParentStyle)
          if elementParentVisibility == False:
            return
      # Add the current text to the output list. A list
      # is used here, because lists are mutable. In other
      # words, we add to the same list, each time.
      outputList.append(elementText)
      return
    elementChildren = element.children
    for child in elementChildren:
      HDLmNodeIden.getInnerTextChild(child, outputList)
  # The next routine finds the object property with the lowest value
  # and returns the property to the caller. In practice, this routine
  # finds the most specific type of search and returns it to the caller. 
  @staticmethod
  def getLowestCount(counts):
    keysDict = vars(counts)
    maxValue = math.inf 
    minKey = None
    for countKey, countValue in keysDict.items():
      # Check if the count value is less than one. We don't want to
      # use any count value that is less than one (for example zero). 
      if countValue < 1.0:
        continue
      if countValue < maxValue:
        minKey = countKey
        maxValue = countValue 
    return minKey 
  # This routine gets and checks the node identifier for a specific DOM element.
  # Note that if the node identifier is not unique (matches more then one DOM
  # element) or does not match any DOM elements, then this routine will return
  # a none value. 
  @staticmethod
  def getNodeIdentifierObj(soup, currentElement):
    # print('In HDLmNodeIden.getNodeIdentifier', currentElement) 
    # Get some JSON for the current element 
    nodeIdenObj = HDLmNodeIden.buildNodeIdentifierObj(soup, currentElement)
    jsonStr = jsons.dumps(nodeIdenObj)
    # print('In HDLmNodeIden.getNodeIdentifier', jsonStr) 
    #
    # Check if the new node identifier uniquely identifies just one
    # DOM element, or many DOM elements. Report an error if the node
    # identifier is not unambiguous. 
    matchCount = HDLmNodeIden.testNodeIdenInformation(soup, jsonStr)
    if matchCount != 1:
      jsonStr = None 
      nodeIdenObj = None
    # print('In HDLmNodeIden.getNodeIdentifier', jsonStr) 
    # print('In HDLmNodeIden.getNodeIdentifier', matchCount) 
    return nodeIdenObj
  # This method removes all traces of one string from another. One
  # leading or trailing blank is removed as need be. The return value
  # is the modified string. 
  @staticmethod
  def removePaddedString(haystack, needle):
    # print('In HDLmNodeIden.removeString', haystack, needle) 
    haystack = haystack.replace(' ' + needle, '')
    # print('In HDLmNodeIden.removeString', haystack) 
    haystack = haystack.replace(needle + ' ', '')
    # print('In HDLmNodeIden.removeString', haystack) 
    haystack = haystack.replace(needle, '')
    # print('In removeString', haystack) 
    return haystack 
  # This method removes a set of fixed class strings from a 
  # string passed to it 
  @staticmethod
  def removeClassStrings(haystack):
    haystack = HDLmNodeIden.removePaddedString(haystack,
                                               'HDLmClassPrimary')
    haystack = HDLmNodeIden.removePaddedString(haystack,
                                               'HDLmClassBackground')
    return haystack 
  # This method tests a set of node identifier values against the current DOM.
  # The number of matches is returned to the caller. If the match count is greater
  # than one, the current set of node identifier information is ambiguous. 
  @staticmethod
  def testNodeIdenInformation(soup, nodeIdenStr):
    # Convert the JSON node identifier string to a Python dictionary
    nodeIdenDict = jsons.loads(nodeIdenStr)
    # Get the list of matching nodes 
    nodeTracingFalse = False
    matchList = HDLmNodeIden.findNodeIden(soup, nodeIdenDict, nodeTracingFalse)
    return len(matchList) 
  # Update a set of fields in the current object. The goal is too 
  # update/remove fields that only have internal values. These 
  # values are not needed/cause problems later. 
  @staticmethod
  def updateAttrsFields(elementObjAttrs):
    # print('In HDLmNodeIden.updateAttrsFields') 
    # print(elementObjAttrs) 
    elementObjAttrs = HDLmNodeIden.updateClassField(elementObjAttrs)
    #print(elementObjAttrs) 
    elementObjAttrs = HDLmNodeIden.updateStyleField(elementObjAttrs)
    #print(elementObjAttrs) 
    elementObjAttrs = HDLmNodeIden.updateInternalAttrs(elementObjAttrs)
    #print(elementObjAttrs) 
    return elementObjAttrs 
  # Update the class field (probably a DOM element) by removing certain
  # internal classes. In some cases (many cases) there will be nothing 
  # left. The class field is deleted in this case. 
  @staticmethod
  def updateClassField(elementObjAttrs):
    # print('In HDLmNodeIden.updateClassField') 
    # print(elementObjAttrs) 
    # At this point, we may want to make some changes to JSON object.
    # If the JSON uses some class values, then they need to be removed. 
    if hasattr(elementObjAttrs, 'class'):
      classValue = getattr(elementObjAttrs, 'class')
      # print(classValue) 
      #
      # In some cases, for some unknown reason, the class value
      # may not be an array at this point. We need to fix this
      # and make sure we have an array to process below. 
      if str(type(classValue)) != "<class 'list'>":
        classValueArray = []
        classValueArray.append(classValue)
        classValue = classValueArray 
      # print(classValue) 
      # Try to remove the first internal class 
      if 'HDLmClassPrimary' in classValue:
        firstIndex = classValue.index('HDLmClassPrimary')
      else:
        firstIndex = -1;
      if firstIndex >= 0:
        del classValue[firstIndex]
      # Try to remove the second internal class 
      if 'HDLmClassBackground' in classValue:
        secondIndex = classValue.find('HDLmClassBackground')
      else:
        secondIndex = -1;
      if secondIndex >= 0:
        del classValue[secondIndex]
      # print(classValue) 
      # Remove the entire class field, if need be 
      classValueLen = len(classValue)
      if classValueLen == 0: 
        delattr(elementObjAttrs, 'class')
    return elementObjAttrs 
  # Remove any attributes that were added for internal use. We don't 
  # want to keep these attributes in some (many) cases. 
  @staticmethod
  def updateInternalAttrs(elementObjAttrs):
    # print('In HDLmNodeIden.removeInternalAttrs') 
    # print(elementObjAttrs) 
    # Check all of the attributes 
    hdlmPrefixLower = HDLmDefines.getString('HDLMPREFIX').lower()
    for curKey in vars(elementObjAttrs):
      # print(curKey) 
      curKeyLower = curKey.lower()
      # Skip any attributes that were not added by our code 
      if curKeyLower.startswith(hdlmPrefixLower) == False:
        continue
      del elementObjAttrs.curKey 
    # print(elementObjAttrs) 
    return elementObjAttrs 
  # Update the style field (probably a DOM element) by removing certain
  # internal styles. In some cases (many cases) there will be nothing
  # left. The style field is deleted in this case. 
  @staticmethod
  def updateStyleField(elementObjAttrs):
    # print('In HDLmNodeIden.updateStyleField', elementObjAttrs) 
    # At this point, we may want to make some changes to JSON object.
    # If the JSON uses some style values, then they need to be removed. 
    if hasattr(elementObjAttrs, 'style'):
      styleValue = elementObjAttrs.style
      # print(styleValue)  
      # Try to remove the first internal style   
      internalBackgroundStr = 'background-color: rgb('
      internalBackgroundStr += HDLmDefines.getString('HDLMBACKGROUNDCOLORRGB')
      internalBackgroundStr += ')'
      styleValue = styleValue.replace(internalBackgroundStr, '')
      # print(styleValue) 
      # Remove the entire style field, if need be 
      styleValueLen = len(styleValue)
      # print(styleValueLen) 
      if styleValueLen == 0:
        del elementObjAttrs.style 
    return elementObjAttrs 