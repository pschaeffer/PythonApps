# Each instance of this class has all of the information about
# one node in the DOM

from   selenium import webdriver
from   selenium.webdriver.common.keys import Keys
import datetime
import mouseinfo
import sys
import time

glbNodeCount = None
glbSamples = None

class DomNode(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, nodePath):
    self.x = None
    self.y = None
    self.width = None
    self.height = None
    self.childCount = None
    self.objectClass = None
    # The node object is the Selenium node at this point.
    # However, that might change in the future. 
    self.nodeObject = None
    self.nodePath = nodePath
    self.nodeId = None
    self.nodeClass = None
    self.innerHtml = None
    self.innerText = None
    self.outerHtml = None
    self.outerText = None
    self.tagName = None
    self.text = None
    self.subNodes = []
  # Add a subnode to the current class instances
  def addSubNode(self, subNode):
    self.subNodes.append(subNode)
  # Add some Id and class information about an HTML node
  def setIdClass(self, nodeId, nodeClass):
     self.nodeId = nodeId
     self.nodeClass = nodeClass
  # Set all of the inner and outer values
  def setInnerOuter(self, innerHtml, innerText, outerHtml, outerText):
    self.innerHtml = innerHtml
    self.innerText = innerText
    self.outerHtml = outerHtml
    self.outerText = outerText
  # Add some location and size information about an HTML node
  def setLocationSize(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
  # Save the node name (really object class) and length (really
  # child node count)
  def setNameLength(self, className, childCount):
    self.childCount = childCount
    self.objectClass = className
  # Save a reference to the node itself
  def setNode(self, nodeObj):
    self.nodeObject = nodeObj
  # Save some additional information about an HTML node
  def setTagNameText(self, tagName, text):
    self.tagName = tagName
    self.text = text

# Each instance of this class has all of the information about
# one sample
class Sample(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, newDescription):
    self.descriptionText = newDescription
    self.cpuTime = time.process_time_ns() / (10**9)
    self.wallTime = time.time_ns() / (10**9)
  # Return the description text
  def getDescriptionText(self):
    return self.descriptionText
  # Return the length of the description text
  def getDescriptionLength(self):
    return len(self.descriptionText)
  # Return the CPU time and wall-clock time to the caller
  def getTimes(self):
    return [self.cpuTime, self.wallTime]

# Each instance of this class has all of the information about
# all of the samples
class Samples(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, newDescription):       
    self.descriptionText = newDescription
    # The maximum description length is the maximum for each of 
    # samples
    self.maxDescriptionLength = 0
    self.samplesList = []
  # Add a sample (provided by the caller) to the list of samples
  def addSample(self, newSample):
    self.samplesList.append(newSample)
    self.maxDescriptionLength = max(self.maxDescriptionLength, 
                                    newSample.getDescriptionLength())
  # Build and add a sample to the list of samples
  def buildAndAddSample(self, newDescription):
    newSample = Sample(newDescription)
    self.samplesList.append(newSample)
    self.maxDescriptionLength = max(self.maxDescriptionLength, 
                                    len(newDescription))
  # Get the maximum sample description length
  def getMaxDescriptionLength(self):
    return self.maxDescriptionLength
  # Print a simple report with all of the sample data
  def printSimpleReport(self, startCpuTime, startWallTime):
    # Get the sample count
    sampleCount = len(self.samplesList)
    maxDescriptionLength = self.maxDescriptionLength
    # Start the simple report
    newText = '{0} - Sample count ({1})'.format(self.descriptionText, sampleCount)
    print(newText)
    print()
    # Set the initial CPU time and wall-clock time values
    oldCpuTime = startCpuTime
    oldWallTime = startWallTime
    # Print out each line of the report
    for i in range(sampleCount):
       # Get the description text from the current sample
       newText = self.samplesList[i].getDescriptionText()
       # Get the times from the current sample  
       newCpuTime, newWallTime = self.samplesList[i].getTimes()
       # Build the format string with the correct width for the 
       # description
       formatStr = '{0:'
       formatStr += str(maxDescriptionLength)
       formatStr += '} {1:9.6f} {2:9.6f}'
       # Build a line of text from the current sample
       line = formatStr.format(newText, newCpuTime-oldCpuTime, newWallTime-oldWallTime)
       print(line)
       # Reset the old CPU time and wall-clock time vales
       oldCpuTime = newCpuTime
       oldWallTime = newWallTime

# Get the location of the mouse inside the browser Window
def getLocationInBrowser(browser):
  # Get the location of the browser
  browserX, browserY = getLocationBrowser(browser)
  # Get the screen location of the mouse
  screenX, screenY = getLocationMouse()
  # Get the location in the browser window
  mouseX = screenX - browserX
  mouseY = screenY - browserY
  return [mouseX, mouseY]

# Get the location of the browser window
def getLocationBrowser(browser):
  # Build a string to get all of the needed data
  script = 'return [' + 'window.screenX,window.screenY' + ']' 
  # Run the script to get all the needed data
  scriptRv = browser.execute_script(script)
  browserX, browserY = scriptRv
  return [browserX, browserY]

# Get the location of the mouse. This method returns
# the absolute location of the mouse. Not the mouse
# location relative to some window.
def getLocationMouse():
  screenX, screenY = mouseinfo.position()
  return [screenX, screenY]

# Get some information about an HTML node and all of the 
# subnodes of the current HTML node. This routine is highly
# recursive and will obtain a great number of nodes (typically).
def getNode(browser, nodePath):
  global glbNodeCount, glbSamples
  glbNodeCount += 1
  # Create the HTML node object
  domNode = DomNode(nodePath)
  # Build a string to get all of the needed node data
  glbSamples.buildAndAddSample('Before build script')
  script = 'return [' +  nodePath + ',' + \
                         nodePath + '.constructor.name,' + \
                         nodePath + '.children.length,' + \
                         nodePath + '.id,' + \
                         nodePath + '.className,' + \
                         nodePath + '.innerHTML,' + \
                         nodePath + '.innerText,' + \
                         nodePath + '.outerHTML,' + \
                         nodePath + '.outerText' + ']'   
  # Run the script to get all the needed node data
  glbSamples.buildAndAddSample('After build script')
  scriptRv = browser.execute_script(script)
  glbSamples.buildAndAddSample('After script execute')
  # Extract all of the needed values
  node, name, length, nodeId, nodeClass, \
    nodeInnerHtml, nodeInnerText, \
    nodeOuterHtml, nodeOuterText = scriptRv
  # Save a reference to the HTML node 
  domNode.setNode(node)
  # Set the node name (really object class) and length
  domNode.setNameLength(name, length)
  domNode.setIdClass(nodeId, nodeClass)
  domNode.setInnerOuter(nodeInnerHtml, nodeInnerText, nodeOuterHtml, nodeOuterText)
  # Get the location and size of the HTML node object
  nodeRect = node.rect
  domNode.setLocationSize(nodeRect['x'], nodeRect['y'], 
                          nodeRect['width'], nodeRect['height'])
  # Get some more information about the HTML node 
  nodeText = node.text
  nodeTagName = node.tag_name
  domNode.setTagNameText(nodeTagName, nodeText)
  # Process each of the subnodes of the current node
  for i in range(length):
    nodePathSub = nodePath + '.children.item('
    nodePathSub += str(i) + ')'
    nodeSub = getNode(browser, nodePathSub)
    domNode.addSubNode(nodeSub)
  return domNode

# Handle shutdown 
def shutdown(browser, cpuTimeStart, wallTimeStart):  
  global glbNodeCount, glbSamples
  browser.quit()
  print(glbNodeCount)
  glbSamples.printSimpleReport(cpuTimeStart, wallTimeStart)
  return

# Handle startup 
def startup():  
  global glbNodeCount, glbSamples
  glbNodeCount = 0
  glbSamples = Samples('Simple report')
  browser = webdriver.Firefox()
  browser.get('http://www.oneworldobservatory.com')
  return browser

# Main program
def main():   
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)
  # Start processing
  browser = startup() 
  getLocationInBrowser(browser)
  topNode = getNode(browser, 'document.documentElement')
  # End processing
  shutdown(browser, cpuTimeStart, wallTimeStart)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__":
  main()