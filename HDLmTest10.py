# This file was created to test AWS Cognito and Python

from   datetime       import datetime
from   HDLmConfig     import *
from   HDLmConfigInfo import *
from   HDLmEmpty      import *
from   io             import BytesIO
from   io             import StringIO
import boto3
import datetime
import hashlib
import hmac
import jsons
import pycurl
import requests
import sys
import time
import urllib.parse
import urllib3
import uuid
import uuid6

glbAwsAccessKeyId = '' 
glbAwsSecretAccessKey = '' 
glbAwsCognitoHost = 'cognito-idp.us-east-2.amazonaws.com'
glbAwsRegionName = 'us-east-2'
glbNewPasswordSave = 'Pentium8023!'
glbNewPassword = 'Pdschaeffer123!'
glbOldPassword = 'Pdschaeffer123!'
glbUsername = 'pdschaeffer'
glbUserPoolClientAppId = '4aa1bqd057v64omjq84hc4pnvl'
glbUserPoolId = 'us-east-2_xTvIIRtgB'
glbUserPoolName = 'HeadlampUserPool1'
glbUserPoolRegion = 'us-east-2'
glbServiceName = "cognito-idp"
glbHttpMethod = "POST" 
glbCanonicalUri = "/"
glbQueryParameters = dict() 
glbAwsHeaders = dict() 
glbXAmzTargetGetUser = "AWSCognitoIdentityProviderService.AdminGetUser"
glbXAmzTargetSetUserPassword = "AWSCognitoIdentityProviderService.AdminSetUserPassword"
glbContentType = "application/x-amz-json-1.1" 
glbUserAgent = "Boto3/1.26.83 Python/3.9.13 Windows/10 Botocore/1.29.83"
glbCertifi = 'C:\\Users\\pscha\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\certifi\\cacert.pem'

class AWSSignatureV4Generator(object):
  # The __init__ method creates an instance of the class
  def __init__(self, builder): 
    self.accessKeyID = builder.accessKeyID 
    self.secretAccessKey = builder.secretAccessKey 
    self.regionName = builder.regionName 
    self.serviceName = builder.serviceName 
    self.httpMethod = builder.httpMethod 
    self.canonicalURI = builder.canonicalURI 
    self.queryParameters = builder.queryParameters 
    self.awsHeaders = builder.awsHeaders 
    self.payload = builder.payload 
    # Get current timestamp value (GTM)
    self.signedHeaderString = None
    self.xAmzDate = AWSSignatureV4Generator.getTimeStamp();
    self.currentDate = AWSSignatureV4Generator.getDate();
    self.xAmzTarget = builder.xAmzTarget
    self.contentType = builder.contentType
    self.hostName = builder.hostName
  # Prepare a canonical request
  def prepareCanonicalRequest(self): 
    canonicalURL = ""
    canonicalURL += self.httpMethod + "\n";
    self.canonicalURI = "/" if (self.canonicalURI == None or len(self.canonicalURI.strip()) == 0) else self.canonicalURI;
    canonicalURL += self.canonicalURI + "\n"
    canonicalURL = self.addCanonicalQueryString(canonicalURL) 
    signedHeaders = ""
    if (self.awsHeaders != None and len(self.awsHeaders) > 0): 
      for key in self.awsHeaders.keys(): 
        value = self.awsHeaders[key]
        signedHeaders += key + ";"
        canonicalURL += key + ":" + value + "\n"
      canonicalURL += "\n"
    else:
      canonicalURL += "\n"  
    self.signedHeaderString = signedHeaders[0:len(signedHeaders)-1]   
    canonicalURL += self.signedHeaderString + "\n"
    if (self.payload == None):
      self.payload = "" 
    payloadHash = AWSSignatureV4Generator.hash(self.payload)
    canonicalURL += payloadHash
    print("Canonical Request: " + canonicalURL);
    return canonicalURL 
  # Add the query parameters
  def addCanonicalQueryString(self, canonicalURL): 
    queryString = ""
    if (self.queryParameters != None and len(self.queryParameters) > 0): 
      for key in self.queryParameters.keys():
        value = self.awsHeaders[key]    
        queryString += key + "=" + AWSSignatureV4Generator.encodeParameter(value) + "&"
      queryString = queryString[0:queryString.rindex("&")]
      queryString += "\n"
    else:
      queryString += "\n"    
    canonicalURL += (queryString);
    return canonicalURL
  # Prepare to sign     
  def prepareStringToSign(self, canonicalURL): 
    stringToSign = "AWS4-HMAC-SHA256" + "\n"
    stringToSign += self.xAmzDate + "\n";
    stringToSign += self.currentDate + "/" + self.regionName + "/" + self.serviceName + "/" + "aws4_request" + "\n"
    stringToSign += AWSSignatureV4Generator.hash(canonicalURL)
    print("String to sign: " + stringToSign)
    return stringToSign;
  # Calculate signature
  def calculateSignature(self, stringToSign): 
    signatureKey = AWSSignatureV4Generator.getSignatureKey(self.secretAccessKey, \
                                                           self.currentDate,     \
                                                           self.regionName,      \
                                                           self.serviceName)
    signature = AWSSignatureV4Generator.hmacSHA256(signatureKey, stringToSign) 
    return AWSSignatureV4Generator.bytesToHex(signature) 
  # Get Headers      
  def getHeaders(self):
    self.awsHeaders["content-type"] = self.contentType
    self.awsHeaders["host"] = self.hostName
    self.awsHeaders["x-amz-date"] = self.xAmzDate
    self.awsHeaders["x-amz-target"] = self.xAmzTarget
    canonicalURL = self.prepareCanonicalRequest()
    stringToSign = self.prepareStringToSign(canonicalURL)
    signature = self.calculateSignature(stringToSign)
    header = dict() 
    header["x-amz-date"] = self.xAmzDate
    header["Authorization"] = self.buildAuthorizationString(signature);
    print("##Signature:\n" + signature)
    print("##Header:")
    for key in header.keys():
      value = header[key] 
      print(key  + " = " + value)
    print("================================");
    return header 
  # Build authorization string
  def buildAuthorizationString(self, strSignature):
    return "AWS4-HMAC-SHA256" + " "                              \
             + "Credential=" + self.accessKeyID + "/"            \
             + AWSSignatureV4Generator.getDate() + "/"           \
             + self.regionName + "/" + self.serviceName + "/"    \
             + "aws4_request" + ", "                             \
             + "SignedHeaders=" + self.signedHeaderString + ", " \
             + "Signature=" + strSignature;
  # Message digest returned as a hexadecimal string
  @staticmethod
  def hash(data):      
    messageDigest = hashlib.sha256()
    messageDigest.update(data.encode('utf-8')) 
    return messageDigest.hexdigest() 
  # HmacSHA256
  @staticmethod
  def hmacSHA256(key, data):   
    dataBytes = data.encode('utf-8')
    messageDigest = hmac.new(key, digestmod=hashlib.sha256)
    messageDigest.update(dataBytes)
    return messageDigest.digest() 
  # Get signature key
  @staticmethod
  def getSignatureKey(key, date, regionName, serviceName):
    kSecret = ("AWS4" + key).encode('utf-8') 
    kDate = AWSSignatureV4Generator.hmacSHA256(kSecret, date) 
    kRegion = AWSSignatureV4Generator.hmacSHA256(kDate, regionName) 
    kService = AWSSignatureV4Generator.hmacSHA256(kRegion, serviceName) 
    return AWSSignatureV4Generator.hmacSHA256(kService, "aws4_request")  
  # Bytes to hex
  @staticmethod
  def bytesToHex(bytes):
    hexArray = "0123456789abcdef" 
    hexChars = " " * (len(bytes) * 2);
    for j in range(0, len(bytes)): 
      v = ord(bytes[j:j+1])
      vFirst = v >> 4
      vSecond = v % 16
      hexChars = hexChars[:j * 2] + hexArray[vFirst] + hexChars[j * 2 + 1:]
      hexChars = hexChars[:j * 2 + 1] + hexArray[vSecond] + hexChars[j * 2 + 2:]
    return hexChars 
  # Get time stamp
  @staticmethod
  def getTimeStamp():
    dateTimeValue = datetime.utcnow()
    # dateTimeValue = "20230412T024911Z" 
    dateTimeValue = datetime(year = 2023, month = 10, day = 27, hour = 18, minute = 39, second = 35)
    dateTimeStr = dateTimeValue.strftime("%Y%m%dT%H%M%SZ") 
    return dateTimeStr
  # Get date
  @staticmethod
  def getDate():
    dateTimeValue = datetime.utcnow()
    # dateTimeValue = "20230412T024911Z"
    dateTimeValue = datetime(year = 2023, month = 10, day = 27, hour = 18, minute = 39, second = 35)
    dateStr = dateTimeValue.strftime("%Y%m%d") 
    return dateStr
  # Encode parameter
  @staticmethod
  def encodeParameter(param): 
    paramBytes = param.encode('utf-8')      
    return urllib.parse.quote(paramBytes)

class Builder(object):
  # The __init__ method creates an instance of the class
  def __init__(self, accessKeyID, secretAccessKey):  
    self.accessKeyID = accessKeyID
    self.secretAccessKey = secretAccessKey
    self.regionName = None
    self.serviceName = None
    self.httpMethod = None
    self.canonicalURI = None
    self.queryParameters = None
    self.awsHeaders = None
    self.payload = None
    self.xAmzTarget = None
    self.contentType = None
    self.hostName = None
  # Region name
  def funcRegionName(self, regionName):
    self.regionName = regionName 
    return self 
  # Service name
  def funcServiceName(self, serviceName):
    self.serviceName = serviceName 
    return self       
  # Http method  
  def funcHttpMethod(self, httpMethod):
    self.httpMethod = httpMethod 
    return self 
  # Canonical URI
  def funcCanonicalURI(self, canonicalURI):
    self.canonicalURI = canonicalURI 
    return self 
  # Query parameters
  def funcQueryParameters(self, queryParameters):
    self.queryParameters = queryParameters 
    return self 
  # AWS headers 
  def funcAwsHeaders(self, awsHeaders):
    self.awsHeaders = awsHeaders 
    return self
  # Payload
  def funcPayload(self, payload):
    self.payload = payload 
    return self
  # XAmzTarget
  def funcXAmzTarget(self, xAmzTarget):
    self.xAmzTarget = xAmzTarget 
    return self
  # Content type
  def funcContentType(self, contentType):
    self.contentType = contentType 
    return self
  # Host name
  def funcHostName(self, hostName):
    self.hostName = hostName 
    return self
  # Build an AWSSignatureV4Generator instance
  def build(self):
    return AWSSignatureV4Generator(self) 

# Try an admin_get_user call
def boto3AdminGetUser(client, userPoolId, userName):
  try:
    resp = client.admin_get_user(
             UserPoolId = userPoolId,
             Username = userName)
  except Exception as e:
    return None, str(e) 
  return resp, None

# Try an admin_set_user_password call
def boto3AdminSetUserPassword(client, userPoolId, userName, passwordStr):
  try:
    resp = client.admin_set_user_password(
             UserPoolId = userPoolId,
             Username = userName,
             Password = passwordStr,
             Permanent = True)
  except Exception as e:
    return None, str(e) 
  return resp, None

# Try an initiate_auth call
def boto3InitiateAuth(client, username, password):
  try:
    # UserPoolId = glbUserPoolId
    resp = client.initiate_auth(
             ClientId = glbUserPoolClientAppId,
             AuthFlow = 'USER_PASSWORD_AUTH',
             AuthParameters = { 
               'USERNAME': username, 
               'PASSWORD': password
             },
             ClientMetadata = {
               'username': username,
               'password': password })
  except client.exceptions.NotAuthorizedException:
    return None, "The username or password is incorrect"
  except client.exceptions.UserNotConfirmedException:
    return None, "User is not confirmed"
  except Exception as e:
    return None, str(e) 
  return resp, None

# Try a respond_to_auth_challenge call
def boto3RespondToAuthChallenge(client, username, password, session):
  try:
    # UserPoolId = glbUserPoolId
    resp = client.respond_to_auth_challenge(
             ClientId = glbUserPoolClientAppId,
             ChallengeName = 'NEW_PASSWORD_REQUIRED',
             Session = session,
             ChallengeResponses = { 
               'USERNAME': username, 
               'NEW_PASSWORD': password
             },
             ClientMetadata = {
               'username': username,
               'new_password': password })
  except client.exceptions.NotAuthorizedException:
    return None, "The username or password is incorrect"
  except client.exceptions.UserNotConfirmedException:
    return None, "User is not confirmed"
  except Exception as e:
    return None, str(e) 
  return resp, None

# Build an accept encoding HTML header
def buildAcceptEncodingHeader(acceptEncodingStr):
  return buildHeader('Accept-Encoding', acceptEncodingStr)

# Build an Amazon authorization HTML header
def buildAmzAuthorizationHeader(accessKeyStr, secretAccessKeyStr, regionName, targetStr, jsonStr):
  # Create a Builder object for use later
  builderObj = createBuilderObject(targetStr, jsonStr)
  # Use the Builder object to get an AWS signature object
  sigObj = builderObj.build()
  # Get some headers for the AWS signature object
  headers = sigObj.getHeaders()
  valueStr = headers['Authorization']
  return buildHeader('Authorization', valueStr)

# Build an Amazon date type HTML header
def buildAmzDateHeader():
  dateTimeValue = datetime.utcnow()
  dateTimeValue = datetime(year = 2023, month = 10, day = 27, hour = 18, minute = 39, second = 35)
  dateStr = dateTimeValue.strftime("%Y-%m-%dT%H:%M:%SZ")
  dateStr = '20230408'
  dateStr = dateTimeValue.strftime("%Y%m%dT%H%M%SZ")
  return buildHeader('X-Amz-Date', dateStr)

# Build an Amazon SDK Invocation Id HTML header  
def buildAmzSdkInvocationIdHeader(sdkIdStr):
  return buildHeader('amz-sdk-invocation-id', sdkIdStr)

# Build an Amazon SDK Request HTML header  
def buildAmzSdkRequestHeader(attemptNumber):
  attemptStr = str(attemptNumber)
  requestStr = 'attempt' + '=' + attemptStr
  return buildHeader('amz-sdk-request', requestStr)

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

# Build an HTML header from the values passed the caller
def buildHeader(typeStr, valueStr):
  outStr = ''
  outStr += typeStr
  outStr += ':'
  outStr += ' '
  outStr += valueStr
  return outStr

# Build a HTML host header
def buildHostHeader(hostNameStr):
  return buildHeader('Host', hostNameStr)

# Build a user agent HTML header 
def buildUserAgentHeader(userAgentStr):
  return buildHeader('User-Agent', userAgentStr)

# Build an X-Amz-Target HTML header
def buildXAmzTargetHeader(targetStr):
  return buildHeader('X-Amz-Target', targetStr)

# Create a Builder object that is later used to build 
# another object
def createBuilderObject(targetStr, jsonStr):
	# Set a few values for use later  
  # Get a Builder object for use later
  builderObj = Builder(glbAwsAccessKeyId, glbAwsSecretAccessKey)
	# Set a few fields in the Builder object 
  builderObj.funcRegionName(glbUserPoolRegion)
  builderObj.funcServiceName(glbServiceName)
  builderObj.funcHttpMethod(glbHttpMethod)
  builderObj.funcCanonicalURI(glbCanonicalUri)
  builderObj.funcQueryParameters(glbQueryParameters)
  builderObj.funcAwsHeaders(glbAwsHeaders)
  builderObj.funcPayload(jsonStr)
  builderObj.funcXAmzTarget(targetStr)
  builderObj.funcContentType(glbContentType)
  builderObj.funcHostName(glbAwsCognitoHost)
  return builderObj

# Get a set of headers for an admin get user request
def getHeadersAdminGetUser(hostNameStr, contentLength):
  # Create an empty headers list
  headers = []
  # Build a host name header and add it to list
  hostHeader = buildHostHeader(hostNameStr)
  headers.append(hostHeader)
  # Build an accept encoding header and add it to the list
  acceptHeader = buildAcceptEncodingHeader('identity')
  headers.append(acceptHeader)
  # Build a X-Amz-Target header and add it to the list
  hostHeader = buildXAmzTargetHeader(glbXAmzTargetGetUser)
  headers.append(hostHeader) 
  # Build a content type header and add it to the list
  contentTypeHeader = buildContentTypeHeader(glbContentType)
  headers.append(contentTypeHeader) 
  # Build a user agent header and add it to the list
  hostHeader = buildUserAgentHeader(glbUserAgent)
  headers.append(hostHeader) 
  # Build an Amazon date header and add it to the list
  hostHeader = buildAmzDateHeader()
  headers.append(hostHeader) 
  # Build an Amazon authorization header and add it to the list
  targetStr = glbXAmzTargetGetUser
  userPoolId = glbUserPoolId
  userName = glbUsername
  jsonStr = getJsonAdminGetUser(userPoolId, userName)
  hostHeader = buildAmzAuthorizationHeader(glbAwsAccessKeyId, glbAwsSecretAccessKey, glbAwsRegionName, targetStr, jsonStr)
  headers.append(hostHeader) 
  # Build an Amazon SDK invocation Id header and add it to the list
  uuidStr = getUuidStr()
  hostHeader = buildAmzSdkInvocationIdHeader(uuidStr)
  headers.append(hostHeader) 
  # Build an Amazon SDK request header and add it to the list
  hostHeader = buildAmzSdkRequestHeader(1)
  headers.append(hostHeader) 
  # Build a content length header and add it to the list
  hostHeader = buildContentLengthHeader(contentLength)
  headers.append(hostHeader)
  # Return the headers to the caller
  return headers

# Get a set of headers for an admin set user password request
def getHeadersAdminSetUserPassword(hostNameStr, contentLength):
  # Create an empty headers list
  headers = []
  # Build a host name header and add it to list
  hostHeader = buildHostHeader(hostNameStr)
  headers.append(hostHeader)
  # Build an accept encoding header and add it to the list
  acceptHeader = buildAcceptEncodingHeader('identity')
  headers.append(acceptHeader)
  # Build a X-Amz-Target header and add it to the list
  hostHeader = buildXAmzTargetHeader(glbXAmzTargetSetUserPassword)
  headers.append(hostHeader) 
  # Build a content type header and add it to the list
  contentTypeHeader = buildContentTypeHeader(glbContentType)
  headers.append(contentTypeHeader) 
  # Build a user agent header and add it to the list
  hostHeader = buildUserAgentHeader(glbUserAgent)
  headers.append(hostHeader) 
  # Build an Amazon date header and add it to the list
  hostHeader = buildAmzDateHeader()
  headers.append(hostHeader) 
  # Build an Amazon authorization header and add it to the list
  targetStr = glbXAmzTargetSetUserPassword
  userPoolId = glbUserPoolId
  userName = glbUsername
  password = glbNewPassword
  jsonStr = getJsonAdminSetUserPassword(userPoolId, userName, password)
  hostHeader = buildAmzAuthorizationHeader(glbAwsAccessKeyId, glbAwsSecretAccessKey, glbAwsRegionName, targetStr, jsonStr)
  headers.append(hostHeader) 
  # Build an Amazon SDK invocation Id header and add it to the list
  uuidStr = getUuidStr()
  hostHeader = buildAmzSdkInvocationIdHeader(uuidStr)
  headers.append(hostHeader) 
  # Build an Amazon SDK request header and add it to the list
  hostHeader = buildAmzSdkRequestHeader(1)
  headers.append(hostHeader) 
  # Build a content length header and add it to the list
  hostHeader = buildContentLengthHeader(contentLength)
  headers.append(hostHeader)
  # Return the headers to the caller
  return headers

# Get a set of headers for an initiate authentication request
def getHeadersInitiateAuth(hostNameStr, contentLength):
  # Create an empty headers list
  headers = []
  # Build a host name header and add it to list
  hostHeader = buildHostHeader(hostNameStr)
  headers.append(hostHeader)
  # Build an accept encoding header and add it to the list
  hostHeader = buildAcceptEncodingHeader('identity')
  headers.append(hostHeader)
  # Build a X-Amz-Target header and add it to the list
  hostHeader = buildXAmzTargetHeader('AWSCognitoIdentityProviderService.InitiateAuth')
  headers.append(hostHeader) 
  # Build a content type header and add it to the list
  hostHeader = buildContentTypeHeader('application/x-amz-json-1.1')
  headers.append(hostHeader) 
  # Build a user agent header and add it to the list
  hostHeader = buildUserAgentHeader(glbUserAgent)
  headers.append(hostHeader) 
  # Build an Amazon SDK invocation Id header and add it to the list
  uuidStr = getUuidStr()
  hostHeader = buildAmzSdkInvocationIdHeader(uuidStr)
  headers.append(hostHeader) 
  # Build an Amazon SDK request header and add it to the list
  hostHeader = buildAmzSdkRequestHeader(1)
  headers.append(hostHeader) 
  # Build a content length header and add it to the list
  hostHeader = buildContentLengthHeader(contentLength)
  headers.append(hostHeader)
  # Return the headers to the caller
  return headers

# Get some JSON for an admin get user request
def getJsonAdminGetUser(userPoolId, userName):
  # Build the initially empty admin get user object
  adminObj = HDLmEmpty()
  # Add some fields to the admin get user object
  adminObj.UserPoolId = userPoolId
  adminObj.Username = userName   
  # Convert the admin get user object to JSON and return 
  # the JSON to the caller
  outJson = jsons.dumps(adminObj)
  return outJson

# Get some JSON for an admin set user password request
def getJsonAdminSetUserPassword(userPoolId, userName, password):
  # Build the initially empty admin get user object
  adminObj = HDLmEmpty()
  # Add some fields to the admin set user password object
  adminObj.UserPoolId = userPoolId
  adminObj.Username = userName 
  adminObj.Password = password  
  adminObj.Permanent = True
  # Convert the admin set user password object to JSON  
  # and return the JSON to the caller
  outJson = jsons.dumps(adminObj)
  outBase = '{}"UserPoolId": "{}", "Username": "{}", "Password": "{}", "Permanent": true{}'
  outJson = outBase.format('{', userPoolId, userName, password, '}')
  return outJson
 
# Get some JSON for an initiate authentication request
def getJsonInitiateAuth(clientId, userName, passwordStr):
  # Build the initially empty authentication object
  authObj = HDLmEmpty()
  # Build the initially empty parameters object
  parmObj = HDLmEmpty()
  # Set a few values in the parameters object
  setattr(parmObj, 'USERNAME', userName)
  setattr(parmObj, 'PASSWORD', passwordStr)
  # Build the initially empty client metadata object
  clientObj = HDLmEmpty()
  # Set a few values in the client metadata object
  setattr(clientObj, 'username', userName)
  setattr(clientObj, 'password', passwordStr)
  # Set a few values in the authentication object
  setattr(authObj, 'ClientId', clientId)
  setattr(authObj, 'AuthFlow', 'USER_PASSWORD_AUTH')
  setattr(authObj, 'AuthParameters', parmObj)
  setattr(authObj, 'ClientMetadata', clientObj)
  # Convert the authentication object to JSON and return 
  # the JSON to the caller
  outJson = jsons.dumps(authObj)
  return outJson

# The fake secret key is provided by the referenced docs
def getSignatureKey():
  kDate = signKeyMessage(("AWS4" + "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY").encode('utf-8'), "20120525".encode('utf-8'))
  kRegion = signKeyMessage(kDate, "us-east-1".encode('utf-8'))
  kService = signKeyMessage(kRegion, "glacier".encode('utf-8'))
  kSigning = signKeyMessage(kService, "aws4_request".encode('utf-8'))
  return kSigning

# Get a UUID string and return it to the caller
def getUuidStr():
  uuidStr = str(uuid6.uuid6())
  return uuidStr  

# Convert a string (array) of bytes to hexadecimal
def printBytesHex(byteArray):
  hexDigits = '0123456789abcdef'
  hexStr = ''
  # Get each of the bytes using a loop
  for intByte in byteArray:
    # Get the first and second digit of each byte
    firstDigit = intByte >> 4
    secondDigit = intByte % 16
    # Get the hexadecimal value of each byte
    firstChar = hexDigits[firstDigit:firstDigit+1]
    secondChar = hexDigits[secondDigit:secondDigit+1]
    # Add the hexadecimal characters to the output string
    hexStr += firstChar + secondChar
  return hexStr

# Try an admin_get_user call
def pyCurlAdminGetUser(clientId, userPoolId, userName):
  # Get some JSON for the current request
  curJson = getJsonAdminGetUser(userPoolId, userName)
  curJsonLen = len(curJson)
  # Get some headers for the current request
  curHeaders = getHeadersAdminGetUser(glbAwsCognitoHost, curJsonLen)
  bytesBuffer = BytesIO()
  stringBuffer = StringIO()
  protocol = 'https' 
  urlString = protocol + '://' + glbAwsCognitoHost
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(pycurl.HTTPHEADER, curHeaders)
  c.setopt(pycurl.POST, 1)
  c.setopt(c.POSTFIELDS, curJson)
  c.setopt(c.WRITEDATA, bytesBuffer) 
  c.perform()
  c.close()   
  bytesBody = bytesBuffer.getvalue()
  stringBody = bytesBody.decode('UTF-8')
  resp = ''
  resp = stringBody
  return resp, None 

# Try an admin_set_user_password call
def pyCurlAdminSetUserPassword(clientId, userPoolId, userName, password):
  # Get some JSON for the current request
  curJson = getJsonAdminSetUserPassword(userPoolId, userName, password)
  curJsonLen = len(curJson)
  # Get some headers for the current request
  curHeaders = getHeadersAdminSetUserPassword(glbAwsCognitoHost, curJsonLen)
  bytesBuffer = BytesIO()
  stringBuffer = StringIO()
  protocol = 'https' 
  urlString = protocol + '://' + glbAwsCognitoHost
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(pycurl.HTTPHEADER, curHeaders)
  c.setopt(pycurl.POST, 1)
  c.setopt(c.POSTFIELDS, curJson)
  c.setopt(c.WRITEDATA, bytesBuffer) 
  c.perform()
  c.close()   
  bytesBody = bytesBuffer.getvalue()
  stringBody = bytesBody.decode('UTF-8')
  resp = ''
  resp = stringBody
  return resp, None 

# Try an initiate_auth call
def pyCurlInitiateAuth(clientId, userName, passwordStr):
  # Get some JSON for the current request
  curJson = getJsonInitiateAuth(clientId, userName, passwordStr)
  curJsonLen = len(curJson)
  # Get some headers for the current request
  curHeaders = getHeadersInitiateAuth(glbAwsCognitoHost, curJsonLen)
  bytesBuffer = BytesIO()
  stringBuffer = StringIO()
  protocol = 'https' 
  urlString = protocol + '://' + glbAwsCognitoHost
  c = pycurl.Curl()
  c.setopt(c.URL, urlString)
  c.setopt(pycurl.CAINFO, glbCertifi)
  c.setopt(pycurl.HTTPHEADER, curHeaders)
  c.setopt(pycurl.POST, 1)
  c.setopt(c.POSTFIELDS, curJson)
  c.setopt(c.WRITEDATA, bytesBuffer) 
  c.perform()
  c.close()   
  bytesBody = bytesBuffer.getvalue()
  stringBody = bytesBody.decode('UTF-8')
  resp = ''
  resp = stringBody
  return resp, None 

# Try an admin_get_user call
def requestsAdminGetUser(clientId, userPoolId, userName):
  # Get some JSON for the current request
  curJson = getJsonAdminGetUser(userPoolId, userName)
  curJsonLen = len(curJson)
  # Convert the JSON string to a Python dictionary
  jsonDict = jsons.loads(curJson)
  # Get some headers for the current request
  curHeaders = getHeadersAdminGetUser(glbAwsCognitoHost, curJsonLen)
  # Convert the list of headers to a dictionary
  curDict = dict()
  for header in curHeaders:
    curIndex = header.find(":")
    key = header[:curIndex]
    value = header[curIndex+2:]
    curDict[key] = value
  # Run the current request
  protocol = 'https' 
  urlString = protocol + '://' + glbAwsCognitoHost
  resp = requests.post(urlString, headers = curDict, json = jsonDict)  
  resp = ''
  return resp, None 

# This routine sets a bunch of AWS access global values
def setAwsAccessGlobals():
  # Set some of the AWS access global values. The AWS 
  # access values are stored in AWS Secrets Manager.
  global glbAwsAccessKeyId
  glbAwsAccessKeyId = HDLmConfigInfo.getAwsAccessKeyId()
  global glbAwsSecretAccessKey
  glbAwsSecretAccessKey = HDLmConfigInfo.getAwsSecretAccessKey()
  return

# This function appear to require a binary key and a binary message and 
# returns a string that is binary
def signKeyMessage(binaryKey, binaryMesg):
  return hmac.new(binaryKey, binaryMesg, hashlib.sha256).digest()

# Try an admin_get_user call
def urllib3AdminGetUser(clientId, userPoolId, userName):
  # Get some JSON for the current request
  curJson = getJsonAdminGetUser(userPoolId, userName)
  curJsonLen = len(curJson)
  # Convert the JSON string to a Python dictionary
  jsonDict = jsons.loads(curJson)
  # Get some headers for the current request
  curHeaders = getHeadersAdminGetUser(glbAwsCognitoHost, curJsonLen)
  # Convert the list of headers to a dictionary
  curDict = dict()
  for header in curHeaders:
    curIndex = header.find(":")
    key = header[:curIndex]
    value = header[curIndex+2:]
    curDict[key] = value
  # Build the URL string
  protocol = 'https' 
  urlString = protocol + '://' + glbAwsCognitoHost
  # Run the current request
  http = urllib3.PoolManager()
  resp = http.request('POST', urlString, body = curJson, headers = curDict)
  resp = ''
  return resp, None 

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Set a few AWS access values for use later
  setAwsAccessGlobals()
  # Run some checks. Note that in the actual tests the string was
  # moved all they way to the left.
  # sts = """AWS4-HMAC-SHA256
  # 20120525T002453Z
  # 20120525/us-east-1/glacier/aws4_request
  # 5f1da1a2d0feb614dd03d71e87928b8e449ac87614479332aced3a701f916743"""
  # signature = signKeyMessage(getSignatureKey(), sts.encode('utf-8'))
  # print(printBytesHex(signature))
  # Start
  # aws_access_key_id = glbAwsAccessKeyId
  # aws_secret_access_key = glbAwsSecretAccessKey
  # boto3.set_stream_logger(name='botocore')
  client = boto3.client('cognito-idp', 
                        aws_access_key_id = glbAwsAccessKeyId,  
                        aws_secret_access_key = glbAwsSecretAccessKey,
                        region_name = glbUserPoolRegion)
  # Initiate admin_get_user
  # adminGetUserResp, errMsg = boto3AdminGetUser(client, glbUserPoolId, glbUsername) 
  # errMsg = errMsg
  # print(errMsg)
  # print(adminGetUserResp)
  initiateAuthRespStr, errMsg = pyCurlInitiateAuth(glbUserPoolClientAppId,
                                                   glbUsername,
                                                   glbOldPassword)  
  # Convert the JSON string to a Python dictionary
  initiateAuthRespDict = jsons.loads(initiateAuthRespStr)
  challenge = initiateAuthRespDict['ChallengeName']
  # Check if authentication worked
  if challenge != None:
  # Extract a few values from the response
    challengeParameters = initiateAuthRespDict['ChallengeParameters'] 
    userNameForSrp = challengeParameters['USER_ID_FOR_SRP'] 
    requiredAttributes = challengeParameters['requiredAttributes']
    session = initiateAuthRespDict['Session']
  # Check if a new password is required
  if challenge == 'NEW_PASSWORD_REQUIRED':
    # setPasswordResp, errMsg = boto3AdminSetUserPassword(client, 
    #                                                     glbUserPoolId,
    #                                                     glbUsername, 
    #                                                     glbNewPassword) 
    # print(errMsg)
    # print(setPasswordResp)
    setUserPasswordRespStr, errMsg = pyCurlAdminSetUserPassword(glbUserPoolClientAppId,
                                                                glbUserPoolId,
                                                                glbUsername,
                                                                glbNewPassword)  
    print(errMsg)
    print(setUserPasswordRespStr)
  # Respond to the challenge
  #    respondToChallengeResp, errMsg = boto3RespondToAuthChallenge(client, glbUsername, 
  #                                                                 glbNewPassword, session)
  # Initiate authentication
  # initiateAuthResp, errMsg = pyCurlInitiateAuth(glbUserPoolClientAppId,
  #                                               glbUsername,
  #                                               glbOldPassword)  
  # adminGetUserResp, errMsg = urllib3AdminGetUser(glbUserPoolClientAppId,
  #                                                glbUserPoolId,
  #                                                glbUsername) 
  # adminGetUserResp, errMsg = pyCurlAdminGetUser(glbUserPoolClientAppId,
  #                                               glbUserPoolId,
  #                                               glbUsername) 
  # initiateAuthResp, errMsg = boto3InitiateAuth(client, glbUsername, glbOldPassword) 
  # print(errMsg)
  # print(initiateAuthResp)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()