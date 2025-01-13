from   HDLmConfig     import *
from   HDLmConfigInfo import *
from   io             import BytesIO
import argparse
import json
import pycurl
import time

glbApiKey = ''
glbHtmlTagInstruction = 'Emphasize key words with HTML tags'
glbRephraseInstruction = 'Rewrite the phrase in a different way but keep the meaning'

# Build an accept encoding HTML header
def buildAcceptEncodingHeader(acceptEncodingStr):
  return buildHeader('Accept-Encoding', acceptEncodingStr)

# Build an accept application JSON content type header
def buildAcceptJsonContentTypeHeader():
  outStr = ''
  outStr += buildAcceptEncodingHeader('application/json')
  return outStr

# Build an Open AI authorization HTML header 
def buildAuthorizationHeader(apiKeyStr):
  authValueStr = 'Bearer' + ' ' + apiKeyStr
  return buildHeader('Authorization', authValueStr)

# Build a content length HTML header
def buildContentLengthHeader(contentLength):
  return buildHeader('Content-Length', str(contentLength))

# Build a content type HTML header 
def buildContentTypeHeader(contentTypeStr):  
  return buildHeader('Content-Type', contentTypeStr)

# Build a dictionary for a AI edit text request
def buildEditTextDictionary(model='text-davinci-edit-001', inputStr='Buy Now', n=10,
                            instruction=glbRephraseInstruction, temperature=0.7):
  textDict = dict()
  textDict['model'] = model
  textDict['input'] = inputStr
  textDict['n'] = n
  textDict['instruction'] = instruction
  textDict['temperature'] = temperature
  return textDict

# Build an HTML header from the values passed the caller
def buildHeader(typeStr, valueStr):
  outStr = ''
  outStr += typeStr
  outStr += ':'
  outStr += ' '
  outStr += valueStr
  return outStr

# Build an application JSON content type header
def buildJsonContentTypeHeader():
  outStr = ''
  outStr += buildContentTypeHeader('application/json')
  return outStr

# Generate some text choices
def generate(inputStr, apiKey, instruction, htmlFlag=False, compoundFlag=False, temperature=0.7):
  """
  Generate samples from Open AI per the provided instructional parameters

  Keyword arguments:
      inputStr -- The input string to act on
      apiKey -- API key when calling OpenAI
      instruction -- The instructions to send, telling OpenAI what to do with the input text
      htmlFlag -- Whether to generate HTML-formatted output
      compoundFlag -- Whether input text on subsequent looped calls to OpenAI include the selected suggestions
      temperature -- Value from 0.0 to 1.0 where a greater value means less predictable generated text
  """
  originalInputStr = inputStr
  outputStrList = []
  while True:
    print(f'Input string: {inputStr}')
    textList = getTextChoices(inputStr, apiKey, instruction, htmlFlag=htmlFlag, temperature=temperature)
    for i, textListElem in enumerate(textList):
      print(f'{i + 1}. {textListElem}')
    print('')
    userInput = input('Select the best outputs, separated by commas (q to quit, r to restart): ')
    print('')
    if userInput.lower() == 'q':
      break
    if userInput.lower() == 'r':
      input_str = originalInputStr
      print('None of the suggestions were good; clearing the input string and trying again...')
      continue
    elif userInput == '':
      print('None of the suggestions were good; trying again...')
      continue
    userInputList = [x.strip() for x in userInput.split(',')]
    if not compoundFlag:
      inputStr = originalInputStr
    for userInputArrElem in userInputList:
      outputStrList.append(textList[int(userInputArrElem) - 1])
      inputStr += textList[int(userInputArrElem) - 1]
  print('=== FINAL OUTPUT ===')
  print('\n'.join(outputStrList))
  return outputStrList

# Get some JSON from the entity passed by the caller
def getSomeJson(data):
  # Check the data passed by the caller. Convert the data
  # to JSON if need be.
  if data is not None:
    data_type_str = str(type(data))
    # Check if the data is already a string. In this case
    # we assume the string to be a JSON string.
    if data_type_str == "<class 'str'>":
        pass
    # Convert a Python dictionary into a string
    elif data_type_str == "<class 'dict'>":
        data = json.dumps(data)
    # Convert a Python object into a string. First, the Python
    # object is converted into a dictionary and then it is
    # converted to a JSON string.
    else:
      data = json.dumps(data.__dict__)
  return data

# Get some data
def getSomeOpenAiData(pathStr, apiKey, headerList=None, formData=None, postData=None):
  bytesBuffer = BytesIO()
  protocol = 'https'
  hostName = 'api.openai.com'
  pathValue = pathStr
  urlString = protocol + '://' + hostName + '/' + pathValue
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.SSL_VERIFYPEER, 0)
  c.setopt(pycurl.SSL_VERIFYHOST, 0)
  # Check if the caller passed any headers
  if headerList is None:
    headerList = []
  # Add the authorization header to the header list
  authHeader = buildAuthorizationHeader(apiKey)
  headerList.append(authHeader)
  c.setopt(pycurl.HTTPHEADER, headerList)
  # Check if the caller passed any form data to be posted)
  if formData is not None:
    c.setopt(c.HTTPPOST, formData)
  # Check if the caller passed any data to be posted
  if postData is not None:
    c.setopt(c.POSTFIELDS, postData)
  # Issue the Curl request and get some data back
  c.setopt(c.WRITEDATA, bytesBuffer)
  c.perform()
  c.close()
  bytesBody = bytesBuffer.getvalue()
  stringBody = bytesBody.decode('UTF-8')
  return stringBody

# Get some text choices using the Open AI API
def getTextChoices(inputStr, apiKey, instruction, htmlFlag=False, temperature=0.7):
  # We pass JSON to the Open AI API
  headerList = []
  contentTypeHeader = buildJsonContentTypeHeader()
  headerList.append(contentTypeHeader)
  # Get the phrase instruction value
  if instruction is not None and len(instruction) > 0:
    phraseInstruction = instruction
  else:
    if htmlFlag == True:
      phraseInstruction = glbHtmlTagInstruction
    else:
      phraseInstruction = glbRephraseInstruction 
  textDict = buildEditTextDictionary(inputStr=inputStr, instruction=phraseInstruction, temperature=temperature)
  # Get some JSON from the text dictionary
  textDict = getSomeJson(textDict)
  # Try to get some text choices
  print('About to get some Open AI data')
  wallTimeStart = time.time()
  outputJson = getSomeOpenAiData('v1/edits', apiKey, headerList, postData=textDict)
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
    choiceText = sanitizeText(suggestedText=choiceText, originalInput=inputStr,
                              instruction=phraseInstruction)
    if len(choiceText) > 0:
      choiceList.append(choiceText)
  return choiceList

# Parse the arguments used to run this program
def parseArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--html', action='store_true')
  parser.add_argument('--compound', action='store_true')
  parser.add_argument(
      '--key',
      action='store',
      type=str,
      default=glbApiKey,
        help='OpenAI API key'
    )
  parser.add_argument(
      '--instruction',
      action='store',
      type=str,
      default=None,
      help='Instruction for what to generate from the text'
  )
  parser.add_argument(
      '--temperature',
      action='store',
      type=float,
      default=0.7,
      help='Value from 0.0 to 1.0 where a greater value means less predictable generated text'
  )
  parser.add_argument(
      '--text',
      action='store',
      type=str,
      default='Buy Now',
      help='The text to regenerate')
  args = parser.parse_args()
  return parser 

# Return the first line that isn't similar to the original input or instruction text
def sanitizeText(suggestedText, originalInput, instruction):
  sanitizedText = ''
  for line in suggestedText.split('\n'):
    line = line.strip()
    if line.lower() == originalInput.lower() or \
       line.lower() == instruction.lower() or   \
       any(line.lower() == x.strip().lower() for x in originalInput.split('\n')):
      continue
    sanitizedText = line
    break
  return sanitizedText

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()   
  # Parse the arguments
  parser = parseArguments()
  # Get the Open AI key
  global glbApiKey
  glbApiKey = HDLmConfigInfo.getOpenAIApiKey()

  # Generate some choices
  args = parser.parse_args()
  args.html = True
  generate(args.text, args.key, args.instruction, htmlFlag=args.html, compoundFlag=args.compound, 
           temperature=args.temperature)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()