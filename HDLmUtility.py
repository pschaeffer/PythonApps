# Class for providing utility functions. This is considered to be a low-level
# routine that can not import any higher-level routines. The ban on imports is
# required to avoid Python circular import errors.  This code uses PycURL for 
# the actual network I/O.
   
from   HDLmConfigInfo import *
from   HDLmDefines    import *
from   HDLmError      import *
from   HDLmGlobals    import *
from   HDLmStateInfo  import *
from   HDLmString     import *
from   io             import BytesIO
import json
import os
import pycurl
import sys
import urllib.parse

glbCertifi = 'C:\\Users\\pscha\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\certifi\\cacert.pem'
  
class HDLmUtility(object):
  # Build a bridge rest API query from values passed by
  # the caller. The returned value is the query string.
  @staticmethod
  def buildBridgeRestQuery(colName):
    # Make sure the first argument passed by the caller is a string
    if type(colName) is not str:
      errorText = f'Column name value ({colName}) passed to buildBridgeRestQuery is not a string'
      HDLmAssert(False, errorText) 
    queryStr = ''
    # Build the content string for use below. 
    valueModified = HDLmUtility.getContentString()
    # Actually build the suffix string 
    queryStr += 'q=[[['
    queryStr += "'"
    queryStr += colName
    queryStr += "'"
    queryStr += ",'eq',"
    queryStr += "'"
    queryStr += valueModified
    queryStr += "'"
    queryStr += ','
    queryStr += "'"
    queryStr += valueModified
    queryStr += "'"
    queryStr += ']]]'
    return queryStr 
  # The method below converts whatever is passed to it, to
  # JSON. A special routine is provided for things that can
  # not be directly converted to JSON. Note that objects and
  # enums can not be directly converted to JSON. Also note 
  # that testing has shown that this code works fine for enums.
  # Testing has also shown that this code fails for complex 
  # numbers.
  @staticmethod
  def convertToJson(value):
    # Convert the value passed by the caller to JSON
    valueJson = json.dumps(value, default=HDLmUtility.convertToJsonSerialize)
    return valueJson
  # The method below is used to handle things that can not be
  # easily converted to JSON. In effect, this is an exit routine
  # for the main JSON conversion routine.
  @staticmethod
  def convertToJsonSerialize(value):
    # Get the type of the value passed to this routine
    typeStr = str(type(value))
    typeStr = typeStr[1:]
    typeStrList = typeStr.split()
    typeStrFirst = typeStrList[0]
    # Check for a enum value
    if typeStrFirst == 'enum':
      return str(value)
    # All other values are converted to a dictionary (for now)
    return value.__dict__
  # Get the content string from the current configuation 
  @staticmethod
  def getContentString(): 
    # Get some values used to build the content string 
    companyPrefix = HDLmConfigInfo.getEntriesBridgeCompanyPrefix()
    contentType = HDLmGlobals.getActiveEditorType()
    contentTypeStr = HDLmUtility.getContentType(contentType)
    # In at least one important case, we need to change the editor
    # type here. The GUI editor or the GXE editor needs to share 
    # data with the main pass-through editor. This is accomplished
    # by changing the editor type here.
    #
    # Note that the GUI editor and/or the GXE editor is not used 
    # with Python. This code is provided for compatibility.
    if HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gem or \
       HDLmGlobals.getActiveEditorType() == HDLmEditorTypes.gxe:
      editorType = HDLmEditorTypes.passEnum
      contentTypeStr = HDLmUtility.getContentType(editorType)
    # In at least one important case, we need to change the editor
    # type here. The inline editors needs to share data with the main
    # pass-through editor. This is accomplished by changing the 
    # editor type here. 
    #
    # Note that the inline editors are not used with Python. 
    # This code is provided for compatibility.
    if HDLmGlobals.checkForInlineEditor():
      editorType = HDLmEditorTypes.passEnum
      contentTypeStr = HDLmUtility.getContentType(editorType)
    contentSuffix = HDLmConfigInfo.getEntriesBridgeContentSuffix()
    contentSuffixSystem = HDLmStateInfo.getSystemValue()
    contentSuffix += contentSuffixSystem
    # Add the prefix to the value. If the prefix is an empty string,
    # this step can be skipped. 
    valueModified = contentTypeStr
    if companyPrefix != '':
      valueModified = valueModified + '_' + companyPrefix
    # Add the suffix to the value. If the suffix is an empty string,
    # this step can be skipped. 
    if contentSuffix != '':
      valueModified = valueModified + '_' + contentSuffix
    # Return the content string 
    return valueModified
  # Get the current content type based on the current editor type. The 
  # returned value will always be a string. Note that this code goes to
  # some trouble to remove the 'Enum' (without the quotes) suffix if need
  # be.
  @staticmethod
  def getContentType(editorType):
    typeString = str(editorType)
    findIndx = typeString.find('.')
    if findIndx >= 0:
      typeString = typeString[findIndx+1:]
    if typeString.endswith('Enum'):
      typeLen = len(typeString)
      typeString = typeString[:typeLen-4]
    return typeString
  # The method below gets the files in a directory. The files
  # are returned to the caller in a list. The call must pass 
  # the path to the directory.  
  @staticmethod
  def getFileList(path):
    outList = []
    for root, dirs, files in os.walk(path):
      outList.extend(files)
    return outList
  # The method below gets the next number from a list of 
  # numbers. If the list is empty, this routine will return
  # one. If the list has a gap, this routine will return the
  # first number from the gap. For example, if the list has
  # [1, 2, 4, 5], this routine will return 3. If the list has
  # no gaps, then this routine will return a value that is one
  # higher than the highest number in the list. For example, if
  # the list has [1, 2, 3, 4], then this routine will return 5.
  # Note that if the list is missing one, then the value of one
  # will be returned. For example, if the list has [2, 3, 4],
  # then this routine will return one. 
  @staticmethod
  def getNextInteger(integerList):
    # Make sure the argument passed by the caller is an array 
    if str(type(integerList)) != "<class 'list'>": 
      errorText = 'Integer list value passed to getNextInteger method is not a list'
      HDLmAssert(False, errorText)
    integerListLen = len(integerList)
    # Check if the existing integer list is empty. Just return
    # one in this case. 
    if integerListLen == 0:
      return 1
    # Check if the number one is in the list. If the number one
    # is not in the list, return a one to the caller. 
    if 1 not in integerList:
      return 1
    # Check each entry in the list passed by the caller. We may
    # find a gap in the list. 
    for i in range(0, integerListLen): 
      # Get the current value and calculate the next 
      # value. See if the next value is missing from the
      # list. If the next value is missing, then we can
      # return the next value to the caller. 
      currentValue = integerList[i]
      nextValue = currentValue + 1
      if nextValue not in integerList:
        return nextValue 
    return integerListLen + 1 
  # The next method takes an input URL and extracts the path value
  # from it. The path value string is returned to the caller. The 
  # path value string does not include the protocol, the host name,
  # or the port number (if any). The path value string also excludes
  # the URL fragment (if any) and the URL search value (if any).
  # For example, the path value part of 
  # https://www.oneworldobservatory.com/en-US/buy-tickets?q=123
  # is 
  # /en-US/buy-tickets 
  @staticmethod
  def getPathString(urlStr):
    # Make sure the argument passed by the caller is a string 
    if str(type(urlStr)) != "<class 'str'>":
      errorText = f'URL value passed to getPathString is not a string'
      HDLmAssert(False, errorText)
    # Remove the protocol (if any), the host name (if any), and 
    # the port number (if any) from the URL string 
    urlStr = HDLmUtility.removeHost(urlStr)
    # Remove the fragment (if any) from the URL string 
    indexOf = HDLmString.lastFindOf(urlStr, '#')
    if indexOf >= 0:
      urlStr = urlStr[0:indexOf]
    # Remove the search value (if any) from the URL string 
    indexOf = HDLmString.lastFindOf(urlStr, '?')
    if indexOf >= 0:
      urlStr = urlStr.substr[0:indexOf]
    return urlStr
  # The method below get the perceptual hash value for an 
  # image. At least for now, the image is specified by a 
  # URL value. The caller provides the URL value and the 
  # rountine below returns a string that will eventually
  # be converted to a 64-bit (in hexadecimal) perceptual 
  # hash value.
  @staticmethod 
  def getPerceptualHash(urlStr):
    hdlmPlusSign = HDLmDefines.getString('HDLMPLUSSIGN')
    newStr = urlStr.replace('+', hdlmPlusSign)
    URL = HDLmConfigInfo.getEntriesBridgeInternetMethod() + "://" + \
      HDLmConfigInfo.getServerName() + "/"                        + \
      HDLmConfigInfo.getPHashName()
    userid = HDLmConfigInfo.getEntriesBridgeUserid()
    password = HDLmConfigInfo.getEntriesBridgePassword()
    requestAJAXAsyncTrue = True    
    newString = HDLmUtility.runAJAX('URL', requestAJAXAsyncTrue, URL, \
                                 userid, password, 'post', newStr)
    return newString 
  # The method below determines Electron JS is active or not.
  # Electron JS is never active under Python.
  @staticmethod
  def isElectron():
    # Electron is never active under Python
    return False
  # Return a boolean showing if we are running under Windows
  @staticmethod
  def isWindows():
    curPlatform = sys.platform
    return curPlatform.startswith('win')
  # Read an input file and return a list of lines
  @staticmethod
  def readInputFile(fileName, encodingStr = 'UTF-8'):
    rv = []
    try:
      with open(fileName, 'r', encoding = encodingStr) as file:
        for line in file:
          line = HDLmString.removeSuffix(line, '\n')
          rv.append(line)
    except IOError as e:
      print('File ({}) did not open'.format(fileName) + '\n  ' + str(e))
      raise
    except Exception as e:
      print('File ({}) caused exception'.format(fileName) + '\n  ' + str(e))
      raise
    return rv
  # The next routine takes an input URL and removes the protocol
  # and the host name from it (if they are present). The returned
  # value is the path string followed by the search string followed
  # by the fragment string. Note that the host name (which is removed)
  # includes the port number, if any. 
  @staticmethod
  def removeHost(urlStr):
    # print('in HDLmUtility.removeHost') 
    # print(urlStr) 
    # Make sure the argument is a string 
    if str(type(urlStr)) != "<class 'str'>":
      errorText = f'URL value passed to removeHost is not a string'
      HDLmAssert(False, errorText)
    # Check if the passed URL string has a colon in it. If it does
    # not have a colon or the colon is in the wrong place, then we
    # can just return the input string to the caller. 
    indexOfColon = urlStr.find(':')
    if indexOfColon < 0 or \
       indexOfColon > 6:
      return urlStr
    # Look for two forward slashes in the URL 
    doubleSlashPosition = urlStr.find('//')
    if doubleSlashPosition < 0:
      errorText = f'URL value passed to removeHost does not have two forward slashes'
      HDLmAssert(False, errorText)
    modifiedUrlStr = urlStr[doubleSlashPosition + 2]
    # print('In HDLmUtility.removeHost') 
    # print('(' + modifiedUrlStr + ')') 
    #
    # Look for one forward slash in the URL. This will not always work.
    # In some cases, we just have a domain name at this point, not 
    # followed by a slash character. 
    firstSlashIndex = modifiedUrlStr.find('/')
    firstQueryIndex = modifiedUrlStr.find('?')
    firstPoundIndex = modifiedUrlStr.find('#')
    lowestIndex = -1
    if firstSlashIndex >= 0 and \
       (lowestIndex == -1 or firstSlashIndex < lowestIndex):
      lowestIndex = firstSlashIndex 
    if firstQueryIndex >= 0 and \
       (lowestIndex == -1 or firstQueryIndex < lowestIndex):
      lowestIndex = firstQueryIndex 
    if firstPoundIndex >= 0 and \
       (lowestIndex == -1 or firstPoundIndex < lowestIndex):
      lowestIndex = firstPoundIndex 
    # Check if we found something to terminate the host name (and possible)
    # port number. If not, then nothing actually follows the host name (and
    # possible) port number.
    if lowestIndex < 0:
      # errorText = f'URL value passed to removeHost does not have anything to terminate the host name' 
      # HDLmAssert(False, errorText) 
      pathQueryFragStr = ''
    else:
      pathQueryFragS= modifiedUrlStr[lowestIndex:]
    # Get the part of the URL after the protocol, host name,
    # and port number 
    if lowestIndex >= 0:
      rv = urlStr[lowestIndex:]
      # print('(' + rv + ')') 
    # print('(' + pathQueryFragStr + ')') 
    return pathQueryFragStr
  # Build and send an AJAX request. We would really like to actually
  # run the AJAX request here (in some cases). However, we must invoke 
  # a proxy instead (in some cases). This is a SOP/CORS problem. The proxy
  # is always invoked using POST. However, a value is passed to the proxy
  # telling the proxy if it should use GET or POST. The type value (below)
  # is passed to the proxy to control the type of the final HTTP request.
  #
  # The proxy is a program that can use HTTP as need be. Because the
  # program runs on the server side, it is not subject to the SOP/CORS 
  # restrictions, that JavaScript in a browser is subject to.
  #     
  # The caller must pass an asynchronous value which is either True 
  # or False. This routine will always return an actual string value 
  # for the caller to use. In the Python environemnt (and elsewhere)
  # the asynchronous value is required and ignored.
  #
  # This routine returns a list (two) of values. The first
  # value is binary and must be decoded to get a string.
  #
  # This is not the real run AJAX routine. This is a copy from HDLmAJAX.
  # A copy is provided here to avoid circular Python import problems.
  @staticmethod
  def runAJAX(requestType, requestAsync,   
              URLStr = '',                 
              userid = '', password = '', 
              type = 'get',                
              extraInfo = ''):
    # print('In HDLMUtility.runAJAX')
    # print(requestType)
    # print(URLStr)
    # print(userid) 
    # print(password) 
    # print(type) 
    # print(extraInfo) 
    bypassProxy = False 
    # Get the name of the server used to handle some requests 
    serverName = HDLmConfigInfo.getServerName()
    # Check if we can bypass the proxy. This will be true in some
    # cases. We can bypass the proxy if the current request can be
    # handled by the server, without going through a proxy. 
    partialPath = HDLmConfigInfo.getEntriesBridgePartialPath()
    pHashPath = HDLmConfigInfo.getPHashName()
    # Check if the URL string matches one of the URLs that can 
    # be sent directly to the server. In other words, this type
    # of request can always bypass the proxy.
    matchingUrl = False 
    if URLStr.startswith('https://' + serverName + '/' + partialPath + '/') or \
       URLStr.startswith('https://' + serverName + '/' + pHashPath):
      matchingUrl = True 
    if requestType == 'URL' and \
       matchingUrl == True:
      bypassProxy = True 
    # We may be running in an Electron JS environment or the extension
    # window environment. In either of these environments, we don't need 
    # to use (can't use) a proxy to send HTTP(s) requests. They can be 
    # sent directly from this code. As a consequence, the actual HTTP(S) 
    # request must be built below. 
    # 
    # Note that if Python is active, we will never be in an extension
    # window and Electron JS will never be active. However, we may 
    # still want to send the request directly to a server.
    #
    # The underlying idea is that in a few environments, we can send
    # the request directly. However, in other environments, we must
    # send the request to a proxy server which will forward the
    # request as need be. This is actually a SOP/CORS problem. 
    # print('s1') 
    # print(isElectron()) 
    # print(HDLmGlobals.checkActiveExtensionWindow()) 
    if bypassProxy == True             or \
       HDLmUtility.isElectron()        or \
       HDLmGlobals.checkActiveExtensionWindow(): 
      # print('s2') 
      buffer = BytesIO()
      c = pycurl.Curl()
      c.setopt(c.URL, URLStr)
      c.setopt(c.WRITEDATA, buffer)
      # Specify a set of certificates for Windows
      if HDLmUtility.isWindows(): 
        c.setopt(c.CAINFO, glbCertifi)
      # Check if we are handling a 'post' (without the quotes) request.
      # Some special code is needed for posts.
      if type == 'post':
        c.setopt(pycurl.HTTPHEADER, ['Accept:application/json',
                                     'Content-Type:application/json'])
        c.setopt(pycurl.POST, 1)
        # extraInfo = urllib.parse.quote(extraInfo, safe='')
        c.setopt(pycurl.POSTFIELDS, extraInfo)
      # Set the userid and password, if need be
      if userid   != None and \
         userid   != ''   and \
         password != None and \
         password != '':
        userPass = userid + ':' + password
        c.setopt(c.USERPWD, userPass)
      # Actually send the URL 
      c.perform()
      responseCode = c.getinfo(c.RESPONSE_CODE)
      c.close()
      body = buffer.getvalue()
      return [body, responseCode]  
  # The method below sets the error text field in the footer. The error
  # text value passed by the caller may, or may not, be empty. The error 
  # text field can be cleared by having the caller pass an empty string
  # to this routine. 
  #
  # The footer does not exist in the Python environment
  @staticmethod
  def setErrorText(errorStr):
    # Make sure the argument is a string 
    if type(errorStr) is not str:
      errorText = f'Error value passed to setErrorText is not a string'
      HDLmAssert(False, errorText)
    # We don't have a footer in the Python environment
    # $("#footer").text(errorStr) 
  # This method tries to update a JSON string with a new value. The caller
  # passes the old JSON string and the update values. This routine converts
  # the JSON string to an object and then updates the object. The object is
  # then converted back to a JSON string.  
  @staticmethod
  def updateJsonStr(jsonStr, keyStr, valueStr):
    # print('In HDLmUtility.updateJsonStr')
    # print(jsonStr, keyStr, valueStr)
    # Check the JSON string passed the caller  
    if jsonStr == None:
      jsonStr = '{}'
    # Convert the JSON string back to an object so we can add the key
    # and the value for the key  
    jsonObj = json.loads(jsonStr)
    jsonObj[keyStr] = valueStr
    # print(jsonObj)
    jsonStr = json.dumps(jsonObj)
    # print(jsonStr, keyStr, valueStr)
    return jsonStr           
  # Write an output file from a list of lines
  @staticmethod
  def writeOutputFile(data, name):
    # Just create the file  
    with open(name, 'w', encoding='utf-8') as f:
      count = 0
      for line in data:
        if count > 0:
          line = '\n' + line
        f.write(line)
        count += 1
  # Write all of the files in the list passed by the caller
  @staticmethod
  def writeOutputFiles(fileList):
    # Handle each output file
    for fileEntry in fileList:
      fileName = fileEntry.getFileName()
      data = fileEntry.getLines()
      HDLmUtility.writeOutputFile(data, fileName)
    return  