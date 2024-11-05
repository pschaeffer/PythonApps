from   HDLmConfig     import *
from   HDLmConfigInfo import *
from   io             import BytesIO
from   io             import StringIO
from   PIL            import Image
from   urllib.parse   import urlencode
import json
import os
import pycurl
import requests   
import time

glbApiKey = ''
glbCertifi = 'C:\\Users\\pscha\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\certifi\\cacert.pem'

# This class creates an empty object with no fields. Fields
# can be added later if need be.
class EmptyObject(object):
  pass

# Build an accept header 
def buildAcceptHeader(contentTypeStr):
  outStr = ''
  outStr += 'Accept'
  outStr += ':'
  outStr += ' ' 
  outStr += contentTypeStr
  return outStr

# Build an accept application JSON content type header 
def buildAcceptJsonContentTypeHeader():
  outStr = ''
  outStr += buildAcceptHeader('application/json')
  return outStr

# Build an Open AI authorization header 
def buildAuthorizationHeader(apiKeyStr):
  outStr = ''
  outStr += 'Authorization'
  outStr += ':'
  outStr += ' ' 
  outStr += 'Bearer'
  outStr += ' '
  outStr += apiKeyStr
  return outStr

# Build a content type header 
def buildContentTypeHeader(contentTypeStr):
  outStr = ''
  outStr += 'Content-Type'
  outStr += ':'
  outStr += ' ' 
  outStr += contentTypeStr
  return outStr

# Build a dictionary for a AI edit text request
def buildEditTextDictionary(model='text-davinci-edit-001', input='Buy Now', n=15, instruction='Create text variants'):
  # Create an empty dictionary
  textDict = dict()
  # Add a few fields to the dictionary
  textDict['model'] = model 
  textDict['input'] = input
  textDict['n'] = n 
  textDict['instruction'] = instruction
  # Return the dictionary to the caller
  return textDict

# Get some image choices using the Open AI API
def getImageChoices():
  # Build some headers for use below
  headerList = []
  acceptContentTypeHeader = buildAcceptJsonContentTypeHeader()
  headerList.append(acceptContentTypeHeader)
  # Build some form data for use below 
  path = 'c:/Users/pscha/Documents/Visual_Studio_Code/Projects/PythonApps/PythonApps/corgi.png'
  send = [("n", "5"), ("size", "1024x1024"),
          ('image', (pycurl.FORM_FILE, path)),]
  # Try to get some image choices
  outputJson = getSomeOpenAiData('v1/images/variations', headerList, formData=send)
  outputDict = json.loads(outputJson)
  outputData = outputDict['data']
  # Handle each of the images
  imageList = []
  for imageDict in outputData:
    if 'error' in imageDict:
      continue
    genImage = imageDict['url']
    imageList.append(genImage) 
  return imageList

# Build an application JSON content type header 
def buildJsonContentTypeHeader():
  outStr = ''
  outStr += buildContentTypeHeader('application/json')
  return outStr

# Get some JSON from the entity passed by the caller
def getSomeJson(data):
  # Check the data passed by the caller. Convert the data
  # to JSON if need be.
  if data != None:
    dataTypeStr = str(type(data))
    # Check if the data is already a string. In this case
    # we assume the string to be a JSON string.
    if dataTypeStr == "<class 'str'>":
      pass
    # Convert a Python dictionary into a string
    elif dataTypeStr == "<class 'dict'>":
      data = json.dumps(data)
    # Convert a Python object into a string. First, the Python
    # object is converted into a dictionary and then it is 
    # converted to a JSON string. 
    else:
      data = json.dumps(data.__dict__)
  return data

# Get some data
def getSomeOpenAiData(pathStr, headerList=None, formData=None, postData=None):
  bytesBuffer = BytesIO()
  protocol = 'https'
  hostName = 'api.openai.com'
  pathValue = pathStr
  urlString = protocol + '://' + hostName + '/' + pathValue 
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.CAINFO, glbCertifi)
  # Check if the caller passed any headers
  if headerList == None:
    headerList = []
  # Add the authorization header to the header list
  authHeader = buildAuthorizationHeader(glbApiKey)
  headerList.append(authHeader)
  c.setopt(pycurl.HTTPHEADER, headerList)
  # Check if the caller passed any form data to be posted)
  if formData != None: 
    c.setopt(c.HTTPPOST, formData)
  # Check if the caller passed any data to be posted
  if postData != None: 
    c.setopt(c.POSTFIELDS, postData)
  # Issue the Curl request and get some data back
  c.setopt(c.WRITEDATA, bytesBuffer)
  c.perform()
  c.close()   
  bytesBody = bytesBuffer.getvalue()
  stringBody = bytesBody.decode('UTF-8')
  return stringBody

# Get some text choices using the Open AI API
def getTextChoices(inputStr):
  # We pass JSON to the Open AI API
  headerList = []
  contentTypeHeader = buildJsonContentTypeHeader()
  headerList.append(contentTypeHeader)
  textDict = buildEditTextDictionary(input=inputStr)
  # Get some JSON from the text dictionary
  textDict = getSomeJson(textDict)
  # Try to get some text choices
  print('About to get some Open AI data')
  wallTimeStart = time.time()
  outputJson = getSomeOpenAiData('v1/edits', headerList, postData=textDict)
  print('Got some Open AI data')
  wallTimeEnd = time.time()
  print('Elapsed', wallTimeEnd - wallTimeStart)
  outputDict = json.loads(outputJson)
  outputChoices = outputDict['choices']
  # Handle each of the choices
  choiceList = []
  for choiceDict in outputChoices:
    if 'error' in choiceDict:
      continue
    choiceText = choiceDict['text']
    choiceList.append(choiceText) 
  return choiceList
    
# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Get the Open AI key
  global glbApiKey
  glbApiKey = HDLmConfigInfo.getOpenAIApiKey()
  # Start processing
  # imageList = getImageChoices()
  # firstImage = imageList[0]
  # img = Image.open(requests.get(firstImage, stream=True).raw)
  # img.show()
  textList = getTextChoices('Buy Now')
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()