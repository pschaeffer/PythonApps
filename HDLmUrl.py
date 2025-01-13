# Each instance of this class has all of the information about
# one URL. A URL is passed in when an instance of this class is
# created. The parts of the URL can be obtained using the methods
# provided by this class. 
# 
# The path string may be an empty string or it may be just a forward
# slash or it may be longer than one character. Note that the path 
# string will not contain the query string (if any) or the fragment
# (if any). The path string will not be a None value. 
# 
# The fragment is not converted to either upper or lower case. The
# fragment may be case sensitive in some cases.
#
# The host name string is always converted to lower case and is returned
# in lower case. The host type value is an enum value. The host parts is
# a list comprised of the parts of the host name. 
#
# The case of the original URL is not changed. The original URL may (or may
# not) be case sensitive. As a consequence, the case of the original URL is
# not altered. 
#
# The case of the path string is not changed. The path string may (or may
# not be case sensitive. As a consequence, the case of the path string is
# not altered. 
# 
# The port number (if any) is always returned as an integer
#
# The case of the query string is not changed. The query string may (or may
# not be case sensitive. As a consequence, the case of the query string is
# not altered. 
# 
# The scheme string is always converted to lower case and is returned
# in lower case
#
# The case of the user information string is not changed. The user information
# string may (or may not) be case sensitive. As a consequence, the case of the 
# user information string is not altered.
# 
# A few notes for later
#   1. The user information can be followed by a colon and (deprecated)
#      a password  
#   2. If prUrlOk is set to true, then a scheme is not required. However,
#      a scheme can still be specified. Note that if a scheme is specified,
#      then it must be valid. Only some scheme values are OK.
#   3. If relativeUrl is set to true, then a host name is not required. However,
#      a host name can still be specified. Note that if a host name is specified,
#      then it must be valid. Only some host name values are OK.
#   4. If relativeURL is set to true, then prUrlOk should proably be set to true
#      as well. If no host name is specified in a URL, it is rather likely that 
#      no scheme was provided as well. 

from   HDLmHtml   import *
from   HDLmString import *
import re
import urllib

class HDLmUrl(object):
  # The __init__ method creates an instance of the class
  def __init__(self, urlStr, prUrlOk=False, relativeUrl=False, semiSep=True):
    # Set all of the initial values for the URL object. These values
    # may be reset later as the URL string is parsed.
    self.fragment = None
    self.hostParts = None
    self.hostString = None
    self.hostType = None
    self.originalUrl = urlStr
    # The path string may be an empty string or it may be just a forward
    # slash or it may be longer than one character. Note that the path 
    # string will not contain the query string (if any) or the fragment
    # (if any). The path string will not be a None value.
    self.pathParts = None
    self.pathString = None
    self.portNumber = None
    self.queryParts = None
    self.queryString = None
    self.scheme = None
    self.userInfo = None
    # Break the URL up into tokens
    tokens = HDLmString.getTokens(urlStr)
    tokenCount = len(tokens)
    tokenIndex = 0
    curToken = tokens[tokenIndex]
    # Check if a URL scheme is present
    if tokenCount >= 3:
      nextToken = tokens[tokenIndex+1]
      if nextToken.getValue() == ':':
        schemeStr = curToken.getValue()
        schemeStr = schemeStr.lower()
        # Check if the URL scheme is valid. Report an error if
        # the URL scheme is invalid
        schemeValid = HDLmHtml.checkScheme(schemeStr)
        if not schemeValid:
          raise ValueError('Scheme value from the URL is not valid')
        self.scheme = schemeStr       
        tokenIndex += 2
      # If we didn't find a colon in the expected location, then we
      # probably don't have a valid scheme. This is generally an error.
      # However, in some cases, not having a scheme is OK.
      else:
        if prUrlOk == False:
          raise ValueError('Colon after URL scheme missing')
    # If we don't have at least three tokens, then we clearly don't
    # have a valid scheme. This is generally an error. However, in
    # some cases, not having a scheme is OK.
    else:
      if prUrlOk == False:
        raise ValueError('URL does not appear to contain a valid scheme')
    # Get the number of remaining tokens
    remainingTokens = tokenCount - tokenIndex
    hostNamePresent = False
    # Check if we have (apparently) a host name and if the host 
    # name is optional or not 
    if relativeUrl == False:
      # If we have enough remaining tokens for the two slashes (plus one
      # for the hypothetical sentinel) then we assume we have a host name.
      # What this really means is that the code below will do the checking
      # needed to verify that we have a valid host name. 
      if remainingTokens >= 3:
        hostNamePresent = True 
      else:
        raise ValueError('URL does not appear to contain a valid host name')    
    # We are allowing for the possibility of not having a valid host name.
    # We will assume that a host name is truly present, if the next two
    # tokens are forward slashes. This isn't a perfect check. The path 
    # could start with two forward slashes.
    else:
      # If we have enough remaining tokens for the two slashes (plus one
      # for the hypothetical sentinel) then we might have a host name. We
      # must check if the two forward slashes are present.
      if remainingTokens >= 3:
        curToken = tokens[tokenIndex]
        nextToken = tokens[tokenIndex+1]
        if curToken.getValue() == '/' and \
           nextToken.getValue() == '/':
          hostNamePresent = True 
    # At this point we should know if we need to handle a host name
    # or not
    if hostNamePresent:
      # Check for the first forward slash in the URL
      curToken = tokens[tokenIndex]
      if curToken.getValue() == '/':
        tokenIndex += 1
      else:
        raise ValueError('First forward slash missing from the URL')
      # Check for the second forward slash in the URL
      curToken = tokens[tokenIndex]
      if curToken.getValue() == '/':
        tokenIndex += 1
      else:
        raise ValueError('Second forward slash missing from the URL')
      # Check if we have user information present
      curToken = tokens[tokenIndex]
      remainingTokens = tokenCount - tokenIndex
      if remainingTokens >= 3:
        nextToken = tokens[tokenIndex+1]
        if nextToken.getValue() == '@':
          self.userInfo = curToken.getValue()
          tokenIndex += 2
      # At this point we need to build a temporary host string that
      # we can use to decide what type of host name we are dealing
      # with. The temporary host string may have the port number in
      # it. That means that it can not be used as the real host name
      # string. 
      tempHostStr = ''
      tempTokenIndex = tokenIndex
      while True:
        tempToken = tokens[tempTokenIndex]
        tempTokenType = tempToken.getType()
        tempTokenValue = tempToken.getValue()
        # Check for something that will terminate the temporary host
        # string. There are many possibilities.
        if tempTokenType == HDLmTokenTypes.end or \
           tempTokenValue == '/' or \
           tempTokenValue == '?' or \
           tempTokenValue == '#':
          break
        # Add the current token to the temporary host string
        tempHostStr += tempTokenValue
        tempTokenIndex += 1
      # Use the temporary host string to get the host string type
      tempHostType = HDLmUrl.checkHostType(tempHostStr)
      # Try to get the host name from the URL. The host name may be
      # a traditional host name (such as google.com) or it may be an
      # IPv4 address or it may be an IPv6 address.
      curToken = tokens[tokenIndex]
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # Check for the sentinel token. If we have reached the sentinel
      # token, then the URL does not have a host name string at all.
      if curTokenType == HDLmTokenTypes.end:
        raise ValueError('Host name is missing from the URL')
      # Set the beginning host name string to an empty string
      hostStr = ''
      # Check for a traditional (standard) domain name
      if tempHostType == HDLmHostTypes.standard:
        # Loop over tokens looking for the end of the host name string
        while True:
          curToken = tokens[tokenIndex]
          curTokenType = curToken.getType()
          curTokenValue = curToken.getValue()
          # We are done building the host name as soon as we reach the
          # sentinel token
          if curTokenType == HDLmTokenTypes.end:
            break
          # Check for an operator token
          if curTokenType == HDLmTokenTypes.operator:
            # Several operator tokens terminate the host name
            if curTokenValue == ':' or curTokenValue == '/':
              break
          # Check for a few terminating tokens
          if curTokenValue == '?' or curTokenValue == '#':
            break
          # We can now use the current token to extend the host name
          # string
          hostStr += curTokenValue
          tokenIndex += 1
        # We now have the final host name string. Check the host name
        # string and make sure that it is a valid domain name. 
        hostStr = hostStr.lower()
        hostTypeValue = HDLmHostTypes.standard
        rv = HDLmUrl.checkHost(hostStr, hostTypeValue)
        if rv[0] == False:
          raise ValueError('Standard host name is not valid')
        # Save the final host name string and host name type
        self.hostString = hostStr
        self.hostType = hostTypeValue
        self.hostParts = rv[1]
      # Check for an IPv4 host name string (such as 192.0.0.0)
      elif tempHostType == HDLmHostTypes.ipv4:
        # Loop over tokens looking for the end of the host name string
        while True:
          curToken = tokens[tokenIndex]
          curTokenType = curToken.getType()
          curTokenValue = curToken.getValue()
          # We are done building the host name as soon as we reach the
          # sentinel token
          if curTokenType == HDLmTokenTypes.end:
            break
          # Check for an operator token
          if curTokenType == HDLmTokenTypes.operator:
            # Several operator tokens terminate the host name
            if curTokenValue == ':' or curTokenValue == '/':
              break
          # Check for a few terminating tokens
          if curTokenValue == '?' or curTokenValue == '#':
            break
          # We can now use the current token to extend the host name
          # string
          hostStr += curTokenValue
          tokenIndex += 1
        # We now have the fina-l IPv4 host name string
        hostStr = hostStr.lower()
        hostTypeValue = HDLmHostTypes.ipv4
        rv = HDLmUrl.checkHost(hostStr, hostTypeValue)
        if rv[0] == False:
          raise ValueError('IPv4 host name is not valid')
        # Save the final host name string and host name type
        self.hostString = hostStr
        self.hostType = hostTypeValue
        self.hostParts = rv[1]
      # Check for an IPv6 host name string (such as ::192.9.5.5 or
      # [::192.9.5.5])
      elif tempHostType == HDLmHostTypes.ipv6:
        # Skip past the leading left square bracket token, if need be. 
        # IPv6 host names can optionally be placed in (leading and 
        # trailing) square brackets. Square brackets are required 
        # if a port numbr is specified. 
        bracketsUsed = False
        if curTokenValue == '[':
          bracketsUsed = True
          tokenIndex += 1
        # Loop over tokens looking for the end of the IPv6 host name string
        while True:
          curToken = tokens[tokenIndex]
          curTokenType = curToken.getType()
          curTokenValue = curToken.getValue()
          # We are done building the host name as soon as we reach the
          # sentinel token. This is might be an error. We should have 
          # found the closing square bracket first, if square brackets
          # are in use. 
          if curTokenType == HDLmTokenTypes.end:
            if bracketsUsed:
              raise ValueError('Right square bracket not found the URL')
            break
          # Check if we have found the trailing right square bracket.
          # Of course, this check is only done if square brackets are
          # in use.
          if curTokenType == HDLmTokenTypes.operator:
            # Check if square brackets are in use. This may or may not
            # be true.
            if bracketsUsed:
              if curTokenValue == ']':
                tokenIndex += 1
                break
            # It appears that square brackets are not in use
            else:
              # Several operator tokens terminate the host name. We
              # check for a colon here, even though we can't really 
              # allow a colon to terminate an IPv6 host address (that
              # is not in brackets).
              if curTokenValue == ':' or curTokenValue == '/':
                if curTokenValue == '/':
                  break
          # Check for a few terminating tokens, if square brackets
          # are not in use.
          if not bracketsUsed:
            if curTokenValue == '?' or curTokenValue == '#':
              break
          # We can now use the current token to extend the host name
          # string
          hostStr += curTokenValue
          tokenIndex += 1
        # We now have the final ipv6 host name string
        hostStr = hostStr.lower()
        hostTypeValue = HDLmHostTypes.ipv6
        rv = HDLmUrl.checkHost(hostStr, hostTypeValue)
        if rv[0] == False:
          raise ValueError('IPv6 host name is not valid')
        # Save the final host name string and host name type
        self.hostString = hostStr
        self.hostType = hostTypeValue
        self.hostParts = rv[1]
      # All other cases are errors
      else:
        raise ValueError('URL has an invalid host name value')
      # Try to get the port number from the URL. The port number may or may
      # not be present.     
      curToken = tokens[tokenIndex]
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      remainingTokens = tokenCount - tokenIndex
      if remainingTokens >= 3 and \
         curTokenType == HDLmTokenTypes.operator and \
         curTokenValue == ':':
        # We must have a valid port number at this point 
        tokenIndex += 1
        curToken = tokens[tokenIndex]
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # The port number should always be an integer
        if curTokenType != HDLmTokenTypes.integer:
          raise ValueError('URL port number is invalid or missing')
        # Get and check the actual port number 
        curTokenValueInteger = int(curTokenValue)
        if curTokenValueInteger < 0:
          raise ValueError('URL port number is too low')
        if curTokenValueInteger > 65535:
          raise ValueError('URL port number is too high')
        # Save the URL port number value
        self.portNumber = curTokenValueInteger
        tokenIndex += 1
    # At this point we may have the (optional) path string. The path 
    # string may be an empty string or it may be just a forward slash
    # or it may be longer than one character. Note that the path string
    # will not contain the query string (if ahy) or the fragment (if any).
    # The path string will not be a none value.
    pathStr = ''
    # Loop over tokens looking for the end of the path string
    while True:
      curToken = tokens[tokenIndex]
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # We are done building the path string as soon as we reach the
      # sentinel token. This is not an error. . 
      if curTokenType == HDLmTokenTypes.end:
        break
      # Check if we have found a question mark. This is not an error case. 
      if curTokenType == HDLmTokenTypes.operator and \
         curTokenValue == '?':
        break
      # Check if we have found a pound sign. This is not an error case. 
      if curTokenValue == '#':
        break
      # We can now use the current token to extend the path string
      pathStr += curTokenValue
      tokenIndex += 1
    # We now have the final path string
    rv = HDLmUrl.checkPath(pathStr)
    if rv[0] == False:
      raise ValueError('URL path string is invalid')
    self.pathString = pathStr
    self.pathParts = rv[1]
    # At this point we may have the (optional) query string. The query 
    # string starts with a question mark that is not used as part of the
    # query string. The query string is optional. If we don't find a query
    # string, a none value will be used. Check for a question mark
    curToken = tokens[tokenIndex]
    curTokenType = curToken.getType()
    curTokenValue = curToken.getValue()
    remainingTokens = tokenCount - tokenIndex
    # Check for the question mark operator
    if remainingTokens >= 2 and \
       curTokenType == HDLmTokenTypes.operator and \
       curTokenValue == '?':
      queryStr = ''
      tokenIndex += 1
      # Loop over tokens looking for the end of the query string
      while True:
        curToken = tokens[tokenIndex]
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # We are done building the query string as soon as we reach the
        # sentinel token. This is not an error. . 
        if curTokenType == HDLmTokenTypes.end:
          break
        # Check if we have found a pound sign. This is not an error case. 
        if curTokenValue == '#':
          break
        # We can now use the current token to extend the query string
        queryStr += curTokenValue
        tokenIndex += 1
      # We now have the final query string
      rv = HDLmUrl.checkQuery(queryStr, semiSep)
      if rv[0] == False:
        # print('In HDLmUrl constructor 2 ' + str(semiSep))
        raise ValueError('URL query string is invalid')
      self.queryString = queryStr
      self.queryParts = rv[1]
    # At this point we may have the (optional) fragment string. The 
    # fragment string starts with a pound sign that is not used as 
    # part of the fragment string. The fragment string is optional.
    # If we don't find a fragment string, a none value will be used.
    # Check for a pound sign.
    curToken = tokens[tokenIndex]
    curTokenType = curToken.getType()
    curTokenValue = curToken.getValue()
    remainingTokens = tokenCount - tokenIndex
    # Check for the question mark operator
    if remainingTokens >= 2 and \
       curTokenValue == '#':
      fragmentStr = ''
      tokenIndex += 1
      # Loop over tokens looking for the end of the fragment string
      while True:
        curToken = tokens[tokenIndex]
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # We are done building the fragment string as soon as we reach the
        # sentinel token. This is not an error. . 
        if curTokenType == HDLmTokenTypes.end:
          break
        # We can now use the current token to extend the fragment string
        fragmentStr += curTokenValue
        tokenIndex += 1
      # We now have the final fragment string
      self.fragment = fragmentStr    
  # Check a host name string. Host names can only take certain
  # forms. Of course, the correct form of a host name depends
  # on whether we are handling a standard host name, an IPv4
  # host name, or an IPv6 host name. Note that IPv6 host names
  # are assumed not to be in square brackets. 
  #
  # If the host name is valid, this code returns a list with two
  # entries. The first entry is a boolean true value. The second
  # entry is a list containing all of the parts of  the host name.
  # However, if an error is found, then the list will start with 
  # the false boolean value, followed by an error string. 
  @staticmethod
  def checkHost(hostStr, hostType):
    # Get the length of the host name string
    hostLen = len(hostStr)
    # Check the length of the host name string
    if hostLen == 0:
      return [False, 'Host name string is empty']
    if hostLen > 253:
      return [False, 'Host name string is too long']     
    # Check for a standard host name (for example, google.com)
    if hostType == HDLmHostTypes.standard:
      rv = HDLmUrl.checkHostStandard(hostStr, hostLen)
      return rv
    # Check for an IPv4 host name (for example, 192.168.1.0)
    elif hostType == HDLmHostTypes.ipv4:
      rv = HDLmUrl.checkHostIpv4(hostStr, hostLen)
      return rv
    # Check for an IPv6 host name (for example, 1080::8:800:200C:417A)
    elif hostType == HDLmHostTypes.ipv6:
      rv = HDLmUrl.checkHostIpv6(hostStr, hostLen)
      return rv
    # Report an error if we don't recognize the host name type
    else:
      return [False, 'The host name type is invalid']
  # Check an IP version 4 host name. An IPv4 host name is a set
  # of integers separated by periods. The number of integers will
  # always be exactly four. This requirement is enforced below.
  #
  # If the host name is valid, this code returns a list with two
  # entries. The first entry is a boolean true value. The second
  # entry is a list containing all of the integers. However, if
  # an error is found, then the list will start with the false
  # boolean value, followed by an error string. 
  @staticmethod
  def checkHostIpv4(hostStr, hostLen):
    integerList = []
    # Break the host name up into tokens
    tokens = HDLmString.getTokens(hostStr)
    tokenIndex = 0
    # Get all of the integer values. The first (and only the first)
    # integer value will not have a period in front of it. 
    while True:
      curToken = tokens[tokenIndex]   
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # Check for the sentinel token (which will terminate the current
      # domain name)
      if curTokenType == HDLmTokenTypes.end:
        break
      # At this point, the only valid token is a period unless we are
      # processing the first integer. The first integer has no leading
      # period.
      if integerList != []:
        if curTokenValue != '.':
          return [False, 'Host name is missing a required period']
        tokenIndex += 1
      # The period must be followed by a valid integer
      curToken = tokens[tokenIndex]   
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # At this point we must have a valid integer token
      if curTokenType != HDLmTokenTypes.integer:
        return [False, 'Host name token is not an integer where an integer is required']
      # Get and check the integer value of the current token
      curTokenValueInteger = int(curTokenValue)
      if curTokenValueInteger < 0:
        return [False, 'Part of host name is too low']
      if curTokenValueInteger > 255:
        return [False, 'Part of host name is too high']  
      # Use the current integer value 
      integerList.append(curTokenValueInteger)
      tokenIndex += 1
    # The correct number of integers for an IPv4 host name is 
    # always four (4). This rule is enforced below.
    if len(integerList) != 4:
      return [False, 'IPv4 host name does not have four parts']  
    # The domain name appears to be OK
    return [True, integerList]
  # Check an IP version 6 host name. An IPv6 host name is a set
  # of hexadecimal values (or in some cases decimal values) separated
  # by colons or periods. Each of the hexadecimal values or decimal
  # values is called a group. The number of groups will be highly 
  # variable, but can not exceed 8. 
  #
  # The number of groups can only be 8 if the number of empty groups
  # is exactly zero. If the number of empty groups is one, then the
  # number of groups must be less than 8. The number of empty groups
  # can not be greater than one. 
  #
  # It is possible to have a missing group in an IPv6 address. This
  # is indicated by two consecutive colons. This is not an error
  # condition. The output hexadecimal or decimal group list will 
  # have an empty entry (a none value) for each pair of colons. 
  # A valid IPv6 address can have only one empty entry.
  #
  # It is assumed, that the IPv6 host name passed to this routine
  # does not have leading or trailing square brackets and does not
  # have an associated port number.
  # 
  # All of the group values (except for empty entries) will be 
  # converted to decimal values before they are added to the 
  # output group list. This step is required to handle IPv4 
  # addresses in IPv6 format. 
  # 
  # If the host name is valid, this code returns a list with two
  # entries. The first entry is a boolean true value. The second
  # entry is a list containing all of the hexadecimal or decimal 
  # groups. Note that all of the hexadecimal or decimal values are
  # converted to integers before they are added to the list. However,
  # if an error is found, then the list will start with the false 
  # boolean value, followed by an error string. 
  @staticmethod
  def checkHostIpv6(hostStr, hostLen):
    emptyCount = 0
    groupList = []
    groupsNotDone = True
    # Break the host name up into tokens
    tokens = HDLmString.getTokens(hostStr)
    tokenLen = len(tokens)
    tokenIndex = 0
    # We need to check for a very special case here. The IPv6 address
    # may start with two consecutive colons. This is not an error case.
    # We need to detect this case and put an empty entry into the 
    # hexadecimal or decimal group list and skip past the first colon 
    # token. This means that we really start processing with the second
    # colon. The second colon is (mostly) treated as a leading colon
    # before an actual hexadecimal or decimal value. 
    if tokenLen >= 3:
      # Get the first and second token values
      firstToken = tokens[0]   
      firstTokenValue = firstToken.getValue()
      secondToken = tokens[1]   
      secondTokenValue = secondToken.getValue()
      # Check if the first and second tokens are colons
      if firstTokenValue == ':' and \
         secondTokenValue == ':':
        groupList.append(None)
        emptyCount += 1
        tokenIndex += 1
        # At this point we may actually be done. If the IPv6 address
        # starts and ends with two colons, then we are done. Check for,
        # and handle this (not an error) case.
        if (tokenIndex+1) < tokenLen:
          # Get the next token
          nextToken = tokens[tokenIndex+1]   
          nextTokenType = nextToken.getType()
          if nextTokenType == HDLmTokenTypes.end:
            groupsNotDone = False
    # Get all of the hexadecimal or decimal values. The first (and only
    # the first) hexadecimal or decimal value will not have a colon or 
    # period in front of it. Note that if the first hexadecimal or decimal
    # value has two colons in front of it (not an error case), then the
    # first hexadecimal or decimal value will have a colon in front of it. 
    while groupsNotDone:
      curToken = tokens[tokenIndex]   
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # Check for the sentinel token (which will terminate the current
      # domain name)
      if curTokenType == HDLmTokenTypes.end:
        break
      # At this point, the only valid tokens are a colon or a period 
      # unless we are processing the first hexadecimal or decimal value.
      # The first hexadecimal or decimal value has no leading colon or 
      # period. Note that if the first hexadecimal or decimal value has 
      # two colons in front of it (not an error case), then the first 
      # hexadecimal or decimal value will have a colon in front of it. 
      delimiterStr = ''
      if groupList != []:
        if curTokenValue != '.' and \
           curTokenValue != ':':
          return [False, 'Host name is missing a required colon/period']
        delimiterStr = curTokenValue
        tokenIndex += 1
      # The colon or period must (in most cases) be followed by a valid
      # hexadecimal or decimal value. The hexadecimal or decimal value 
      # may be one token or it may be two tokens. For example, '23FF' 
      # will be treated as two tokens, but is really just one value. 
      curToken = tokens[tokenIndex]   
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # We may actually have a colon at this point. That indicates a 
      # missing hexadecimal value (not an error condition). 
      if delimiterStr == ':' and \
         curTokenValue == ':':
        groupList.append(None)
        emptyCount += 1
        # At this point we may actually be done. If the IPv6 address
        # ends with two colons, then we are done. Check for, and handle
        # this (not an error) case.
        if (tokenIndex+1) < tokenLen:
          # Get the next token
          nextToken = tokens[tokenIndex+1]   
          nextTokenType = nextToken.getType()
          if nextTokenType == HDLmTokenTypes.end:
            break
        # At this point we need to continue processing. The second 
        # colon will now be the colon preceeding a hexadecimal or
        # decimal value.
        continue
      # We need to check for an integer token at this point followed
      # by an identifier token. The two values must be combined for
      # use below. 
      if curTokenType == HDLmTokenTypes.integer and \
         (tokenIndex+1) < tokenLen:
        # Get the next token
        nextToken = tokens[tokenIndex+1]   
        nextTokenType = nextToken.getType()
        nextTokenValue = nextToken.getValue()
        # Check if we can combine the next token with the current
        # token
        if nextTokenType == HDLmTokenTypes.identifier:
          curTokenValue += nextTokenValue
          tokenIndex += 1
      # At this point we must have a valid integer token or a valid
      # identifier token
      if curTokenType != HDLmTokenTypes.integer and \
         curTokenType != HDLmTokenTypes.identifier:
        return [False, 'Host name token is not a valid hexadecimal or decimal string']
      # Check the length of the hexadecimal or decimal host name token
      if len(curTokenValue) > 4:
        return [False, 'Host name hexadecimal or decimal string is too long']
      # Check if the hexadecimal or decimal string is valid
      if not HDLmString.isHex(curTokenValue):
        return [False, 'Host name hexadecimal or decimal string is invalid']
      # Use the current hexadecimal or decimal value. We need to decide if
      # we are handling a hexadecimal value or a decimal value. Of course,
      # we need convert hexadecimal values to decimal values. 
      hexValue = True
      # Check if the token prior to the current token is a period. If this 
      # is true, then we are handling a decimal value, not a hexadecimal value.
      if tokenIndex > 0:
        # Get the prior token
        priorToken = tokens[tokenIndex-1]   
        priorTokenValue = priorToken.getValue()
        if priorTokenValue == '.':
          hexValue = False
      # Check if the token after the current token is a period. If this
      # is true, then we are handling a decimal value, not a hexadecimal
      # value.
      if (tokenIndex+1) < tokenLen:
        # Get the next token
        nextToken = tokens[tokenIndex+1]   
        nextTokenValue = nextToken.getValue()
        if nextTokenValue == '.':
          hexValue = False
      # Convert the current value to decimal
      if hexValue:
        curTokenValueInt = int(curTokenValue, 16)
      else:
        curTokenValueInt = int(curTokenValue, 10)
      groupList.append(curTokenValueInt)
      tokenIndex += 1
    # Check the number of groups in the group list
    if len(groupList) == 0:
      return [False, 'IPv6 host name does not contain any groups']
    if len(groupList) > 8:
      return [False, 'IPv6 host name contains too many groups']
    if (len(groupList) - emptyCount) == 8 and emptyCount == 1:
      return [False, 'IPv6 host name contains eight groups and an empty group']
    # Check the number of empty groups in the group list
    if emptyCount > 1:
      return [False, 'IPv6 host name contains too many empty groups']
    # The domain name appears to be OK
    return [True, groupList]
  # Check a standard host name. A standard host name is a set
  # of labels separated by periods. The number of labels will
  # always be one or greater. 
  #
  # If the host name is valid, this code returns a list with two
  # entries. The first entry is a boolean true value. The second
  # entry is a list containing all of the labels. However, if an 
  # error is found, then the list will start with the false
  # boolean value, followed by an error string. 
  @staticmethod
  def checkHostStandard(hostStr, hostLen):
    labelList = []
    # Break the host name up into tokens
    tokens = HDLmString.getTokens(hostStr)
    tokenIndex = 0    
    # The domain name is a sequence of periods followed by
    # label strings. The first (and only the first) label
    # will not have a period in front of it. 
    while True:
      curToken = tokens[tokenIndex]  
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # Check for the sentinel token (which will terminate the current
      # domain name)
      if curTokenType == HDLmTokenTypes.end:
        break
      # At this point, the only valid token is a period unless we are
      # processing the first label. The first label has no leading
      # period.
      if labelList != []:
        if curTokenValue != '.':
          return [False, 'Host name is missing a required period']
        tokenIndex += 1
      # The period must be followed by a valid label
      curLabel = ''
      while True:
        curToken = tokens[tokenIndex]   
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # Check for the sentinel token (which will terminate the current
        # label)
        if curTokenType == HDLmTokenTypes.end:
          break
        # Check for a period that will terminate the current label
        if curTokenValue == '.':
          break
        # Check for something that can be part of a label
        if curTokenType == HDLmTokenTypes.identifier or \
           curTokenType == HDLmTokenTypes.integer or \
           curTokenType == HDLmTokenTypes.unknown or \
           curTokenValue == '-':
          curLabel += curTokenValue
          tokenIndex += 1
          continue
        # Report than an invalid token was found
        return [False, 'Later part of the domain name had an invalid token']
      # The label after a period must be an actual string
      if curLabel == '':
        return [False, 'Label after period in the domain name is missing']
      # Check the current label and make sure it is valid
      rv = HDLmUrl.checkLabel(curLabel)
      if rv[0] == False:
        return [*rv]  
      labelList.append(curLabel)
    # Check the number of labels in the label list
    if len(labelList) == 0:
      return [False, 'Standard host name does not contain any labels']
    if len(labelList) > 127:
      return [False, 'Standard host name has too many labels']
    # The domain name appears to be OK
    return [True, labelList]
  # Check (really) get the host type of a host name. Host names
  # can be standard host names, IPv4 host names, or IPv6 host
  # names. This routine uses a number techniques to decide 
  # what type of host name was passed to it. 
  # 
  # The host string passed to this routine is not really the 
  # final host string and should not be used as the final host
  # string. For example, the port number (and the colon before
  # the port number) may be part of the string passed to this
  # routine. 
  # 
  # This routine is a classifier that tries to classify host
  # addresses using a number of techniques. Of course, it could
  # fail and make the wrong decision. This routine will need to 
  # be changed from time to time. 
  @staticmethod
  def checkHostType(hostStr):
    # Set a default value for the final type
    badTokenFound = False
    finalType = HDLmHostTypes.none
    # Set a few initial values
    adjustedColonCount = 0 
    adjustedGroupCount = 0
    adjustedIdentifierCount = 0
    adjustedIntegerCount = 0
    adjustedIpv4Count = 0
    colonCount = 0
    dotCount = 0
    groupCount = 0
    identifierCount = 0
    integerCount = 0
    ipv4Count = 0
    trailingPortFlag = False
    trailingPortNumber = None
    trailingPortNumberIpv4 = False
    trailingPortNumberGroup = False
    # Break the host name up into tokens
    tokens = HDLmString.getTokens(hostStr)
    tokens = HDLmUrl.combineTokens(tokens)
    tokenCount = len(tokens)
    tokenIndex = 0
    # Check if the token list ends with what looks like a port
    # number
    if tokenCount >= 3 and \
       tokens[-2].getType() == HDLmTokenTypes.integer and \
       tokens[-3].getValue() == ':':
      trailingPortFlag = True
      trailingPortStr = tokens[-2].getValue()
      trailingPortNumber = int(trailingPortStr)
      trailingPortNumberIpv4 = (trailingPortNumber >= 0 and trailingPortNumber <= 255)
      trailingPortNumberGroup = (len(trailingPortStr) >= 1 and len(trailingPortStr) <= 4)
    # Check if the token list is empty or just contains
    # the colon and port number
    if tokenCount == 1:
      return finalType
    if tokenCount == 3 and \
       trailingPortFlag == True:
      return finalType
    # Process all of the tokens
    for curToken in tokens:
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # We need to skip the sentinel token
      if curTokenType == HDLmTokenTypes.end:
        break
      # Check for a bad token. Some tokens are so bad that
      # we can quit processing immediately. 
      if curTokenType == HDLmTokenTypes.operator:
        if curTokenValue != ':' and \
           curTokenValue != '.' and \
           curTokenValue != '-' and \
           curTokenValue != '[' and \
           curTokenValue != ']':
          badTokenFound = True
      # Check for a colon
      if curTokenValue == ':':
        colonCount += 1
        continue
      # Check for a dot
      elif curTokenValue == '.':
        dotCount += 1
        continue
      # Check for a valid IPv6 group
      if len(curTokenValue) <= 4 and \
         HDLmString.isHex(curTokenValue):
        groupCount += 1
      # Check for a valid identifier. Note that a token
      # can be both a valid IPv6 group and a valid identifier
      if curTokenType == HDLmTokenTypes.identifier:
        identifierCount += 1
      # Check for a valid integer. Note that a token can
      # be both a valid IPv6 group and a valid integer.
      if curTokenType == HDLmTokenTypes.integer:
        integerCount += 1
        # Check if the integer value is in range for an IPv4
        # address component
        curTokenValueInteger = int(curTokenValue)
        if curTokenValueInteger >= 0 and \
           curTokenValueInteger <= 255:
          ipv4Count += 1
    # Get the adjusted colon count
    if colonCount > 0:
      adjustedColonCount = colonCount - (1 if trailingPortFlag else 0)
    else:
      adjustedColonCount = 0
    # Get the adjusted group count. The trailing port number only 
    # needs to be considered, if it in the range of 0 to 9999. 
    if groupCount > 0:
      adjustedGroupCount = groupCount - (1 if trailingPortNumberGroup else 0)
    else:
      adjustedGroupCount = 0
    # Get the adjusted identifier count
    if identifierCount > 0:
      adjustedIdentifierCount = identifierCount 
    else:
      adjustedIdentifierCount = 0
    # Get the adjusted integer count
    if integerCount > 0:
      adjustedIntegerCount = integerCount - (1 if trailingPortFlag else 0)
    else:
      adjustedIntegerCount = 0
    # Get the adjusted IPv4 component count
    if ipv4Count > 0:
      adjustedIpv4Count = ipv4Count - (1 if trailingPortNumberIpv4 else 0)
    else:
      adjustedIpv4Count = 0
    # Check if the first token is a left square bracket. This 
    # means that we have an IPv6 host string.
    if tokenCount > 0 and \
      tokens[0].getValue() == '[':
      return HDLmHostTypes.ipv6
    # Check if a bad token was found. if a bad token was found,
    # return a default host string type value. Note that this
    # check follows the left square bracket IPv6 check.
    if badTokenFound:
      return finalType
    # Check if the adjusted colon count is greater than zero.
    # This means that we must have an IPv6 host string.
    if adjustedColonCount >= 1:
      return HDLmHostTypes.ipv6
    # If the adjusted colon count is zero, then we may have 
    # a standard host string or an IPv4 host string. First we
    # check if the identifier count is greater than or equal
    # to the group count. Consider a host string such as 'a:25'.
    if adjustedIdentifierCount > 0 and \
       adjustedIdentifierCount >= adjustedGroupCount:
      return HDLmHostTypes.standard
    # Check if the integer count is greater than zero and if
    # the integer count is greater than or equal to the adjusted
    # group count. Consider a host string such as '0:25'.
    if adjustedIntegerCount > 0 and \
       adjustedIntegerCount >= adjustedGroupCount and \
       adjustedIpv4Count == 4:
      return HDLmHostTypes.ipv4
    # Check if combined identifier and integer count is greater then
    # zero and if the combined count is greater than or equal to
    # adjusted group count. Consider a host string such as '192.168.a.1'.
    adjustedCombinedCount = adjustedIdentifierCount + adjustedIntegerCount
    if adjustedCombinedCount > 0 and \
       adjustedCombinedCount >= adjustedGroupCount:
      # Check if we really have an IPv4 address. If we do, return
      # the correct type value to the caller.
      if adjustedIdentifierCount == 0 and \
         adjustedIpv4Count == 4:
        return HDLmHostTypes.ipv4
      else:
        return HDLmHostTypes.standard
    # In all other cases, just return a default value
    return finalType
  # Check a label string. A label is one part of a host name. 
  # Various rules apply to labels. This code hopefully enforces
  # all of the rules. If the label is valid, this code returns
  # a list with just one entry (the boolean true value). However,
  # if an error is found, then the list will start with the false
  # boolean value, followed by an error string. 
  @staticmethod
  def checkLabel(labelStr):
    # Get the length of the label string
    labelLen = len(labelStr)
    # Check the length of the label string
    if labelLen == 0:
      return [False, 'Label string is empty']
    if labelLen > 63:
      return [False, 'Label string is too long']
    # Check the first character of the label. The first character can
    # not be a minus sign.
    firstChar = labelStr[0]
    if firstChar == '-':
      return [False, 'Label string starts with a minus sign']
    # Check the last character of the label. The last character can
    # not be a minus sign.
    lastChar = labelStr[-1]
    if lastChar == '-':
      return [False, 'Label string ends with a minus sign']
    # Check if the label is valid. Labels can only contain certain
    # limited characer values. 
    patternStr = '^(-|[a-zA-Z0-9])*$'
    matches = re.search(patternStr, labelStr)
    if matches == None:
      return [False, 'Label string is not valid']
    return [True]
  # Check a standard path string. A standard path string is a set
  # of segments separated by slashes. The number of segments will
  # be zero or greater. 
  #
  # If the path string is valid, this code returns a list with two
  # entries. The first entry is a boolean true value. The second
  # entry is a list containing all of the segments of the path. 
  # However, if an error is found, then the list will start with
  # the false boolean value, followed by an error string. 
  # 
  # If the path string is empty or consists of just one forward
  # slash character, then the list of path segments will be empty.
  # Note, that if the path string contain a pair of consecutive 
  # forward slashes, then the path segment between them will be 
  # an empty string. 
  #
  # The path string and each of the path segments is treated as
  # case-sensitive. No conversion to lower or uppercase is done.
  @staticmethod
  def checkPath(pathStr):
    pathList = []
    pathLen = len(pathStr)
    # Check for a few very simple cases
    if pathLen == 0 or \
       pathStr == '/':
      return [True, pathList]
    # Break the path string up into tokens
    tokens = HDLmString.getTokens(pathStr)
    tokenIndex = 0
    # The path string is a sequence of forward slash characters
    # followed by segment strings. The segment string may be made
    # up of several tokens. Note that the first segment might not
    # have a slash in front of it. This is not an error. For example,
    # '01.htm' (without the quotes) is actually a valid path (if no
    # host name is present) and is used in some cases.
    segmentCount = 0 
    while True:
      curToken = tokens[tokenIndex]  
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      segmentCount += 1
      # Check for the sentinel token (which will terminate the current
      # path string)
      if curTokenType == HDLmTokenTypes.end:
        break
      # At this point, the only valid token is a forward slash for all
      # segments after the first. The first segment does not have to
      # have a leading forward slash.
      if curTokenValue != '/' and \
         segmentCount > 1:
        return [False, 'Path string is missing a required forward slash']
      # We only want to skip the current token if it is a forward slash.
      # In other cases, we really don't want to skip the current token.
      if curTokenValue == '/':
        tokenIndex += 1
      # The forward slash must be followed by a valid segment
      curSegment = ''
      curSegmentValid = False
      while True:
        curToken = tokens[tokenIndex]   
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # Check for the sentinel token (which will terminate the current
        # segment). Note that if nothing comes before the sentinel token,
        # then the current segment will not be treated as valid.
        if curTokenType == HDLmTokenTypes.end:
          break
        # Check for a forward slash or several other characters that will
        # terminate the current segment
        if curTokenValue == '/'or \
           curTokenValue == '?' or \
           curTokenValue == '#':
          curSegmentValid = True
          break
        # Check for something that can be part of a segment
        if curTokenType == HDLmTokenTypes.identifier or \
           curTokenType == HDLmTokenTypes.operator or \
           curTokenType == HDLmTokenTypes.quoted or \
           curTokenType == HDLmTokenTypes.integer or \
           curTokenType == HDLmTokenTypes.space or \
           curTokenType == HDLmTokenTypes.unknown:
          curSegment += curTokenValue
          curSegmentValid = True
          tokenIndex += 1
          continue
        # Report than an invalid token was found
        return [False, 'Path string segment had an invalid token']
      # The current segment may contain one or more percent-encoded
      # characters. We need to convert them to standard characters. 
      curSegmentCount = curSegment.count('%')
      if curSegmentCount > 0:
        curSegment = urllib.request.unquote(curSegment)
      # Add the current segment to the segment list 
      if curSegmentValid:
        pathList.append(curSegment)
    # The path string appears to be OK
    return [True, pathList]
  # Check a standard query string. A standard query string is a set
  # of keyword/value pairs separated by ampersands or semicolons. 
  # The number of keyword/value pairs will be one or greater. 
  #
  # If the query string is valid, this code returns a list with two
  # entries. The first entry is a boolean true value. The second
  # entry is a dictionary containing all of the keyword/value pairs 
  # in the query. However, if an error is found, then the list will 
  # start with the false boolean value, followed by an error string. 
  # 
  # In the original URL, the query string (if any) starts with a 
  # leading question mark The query string passed to this routine
  # will not start with a leading question mark. The query string
  # ends either at the end of the URL or when a pound sign (start
  # of the fragment) is found. Note that the pound sign (if any)
  # is not part of the query string and will not be passed to this
  # routine. 
  # 
  # Each keyword/value pair will be preceeded by an ampersand or
  # a semicolon. However, the first keyword/value pair will not
  # be preceeded by an ampersand or a semicolon.
  #
  # The query string and each of the query keyword/value pairs is 
  # treated as case-sensitive. No conversion to lower or uppercase 
  # is done.
  # 
  # It turns out that using (supporting) semicolons as separator 
  # characters seems to be an idea that has come and gone. The 
  # current W3 standard does not appear to allow semicolons to 
  # be used to separate query parameters. Note that the default
  # is to handle semicolons as separator characters. This was 
  # done to maintain compatibility with old code.  
  @staticmethod
  def checkQuery(queryStr, semiSep=True):
    queryDict = dict()
    queryLen = len(queryStr)
    # Break the query string up into tokens
    tokens = HDLmString.getTokens(queryStr)
    tokenIndex = 0
    # The query string is a sequence of separator (ampersands or semicolons) 
    # characters followed by keyword/value pairs. The keyword and the value
    # may be made up of several tokens.
    while True:
      curToken = tokens[tokenIndex]  
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      # Check for the sentinel token (which will terminate the current
      # query string)
      if curTokenType == HDLmTokenTypes.end:
        break
      # At this point, the only valid tokens are an ampersand or a semicolon
      if len(queryDict) > 0:
        # Assume that the current token is not invalid 
        curTokenValueInvalid = False
        # Check if a semicolon can be used as a query parameters separator
        if semiSep:
          if curTokenValue != '&' and \
             curTokenValue != ';':
            curTokenValueInvalid = True
        # It appears that a semicolon can not be used as a query parameters 
        # separator
        else:
          if curTokenValue != '&':
            curTokenValueInvalid = True
        if curTokenValueInvalid: 
          return [False, 'Query string is missing a required ampersand or semicolon']
        tokenIndex += 1
      # The separator character (an ampersand or a semicolon) must be followed
      # by a valid keyword
      curKeyword = ''
      while True:
        curToken = tokens[tokenIndex]   
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # Check for the sentinel token (which will terminate the current
        # keyword). We should never reach the sentinel token processing
        # the keyword. This  is an error condition.
        if curTokenType == HDLmTokenTypes.end:
          return [False, 'Sentinel token reached trying to build the keyword']
        # Check for a separator character (an ampersand or semicolon). We should
        # never reach a separator character processing the keyword. This is an
        # error condition.
        if curTokenValue == '&' or \
           (curTokenValue == ';' and semiSep):     
          return [False, 'Separator character reached trying to build the keyword']
        # Check for an equals sign. A complete keyword should preceed the 
        # equals sign.
        if curTokenValue == '=':
          break
        # Check for something that can be part of a keyword value
        if curTokenType == HDLmTokenTypes.identifier or \
           curTokenType == HDLmTokenTypes.operator or \
           curTokenType == HDLmTokenTypes.quoted or \
           curTokenType == HDLmTokenTypes.integer or \
           curTokenType == HDLmTokenTypes.space or \
           curTokenType == HDLmTokenTypes.unknown:
          curKeyword += curTokenValue
          tokenIndex += 1
          continue
        # Report than an invalid token was found
        return [False, 'Query string keyword had an invalid token']
      # Make sure we have a valid keyword. An empty string is not a 
      # valid keyword.  
      if curKeyword == '':
        return [False, 'Query string keyword is an empty string']
      # At this point we must have an equals sign. Nothing else is
      # allowed at this point. 
      curToken = tokens[tokenIndex] 
      curTokenValue = curToken.getValue()
      if curTokenValue != '=':
        return [False, 'Query string missing equals sign after keyword']
      tokenIndex += 1
      # The equals sign character must be followed by a valid value
      curValue = ''
      while True:
        curToken = tokens[tokenIndex]   
        curTokenType = curToken.getType()
        curTokenValue = curToken.getValue()
        # Check for the sentinel token (which will terminate the current
        # value). We might reach the sentinel token processing the value.
        # This is not an error condition.
        if curTokenType == HDLmTokenTypes.end:
          break
        # Check for a separator character (an ampersand or semicolon). We 
        # might reach a separator character processing the value. This is
        # not an error condition.
        if curTokenValue == '&' or \
           (curTokenValue == ';' and semiSep):     
          break
        # Check for an equals sign. An equals sign should never be found 
        # processing a value.   
        if curTokenValue == '=':
          return [False, 'Query value contains an equals sign']
        # Check for something that can be part of a keyword value
        if curTokenType == HDLmTokenTypes.identifier or \
           curTokenType == HDLmTokenTypes.operator or \
           curTokenType == HDLmTokenTypes.quoted or \
           curTokenType == HDLmTokenTypes.integer or \
           curTokenType == HDLmTokenTypes.space or \
           curTokenType == HDLmTokenTypes.unknown:
          curValue += curTokenValue
          tokenIndex += 1
          continue
        # Report than an invalid token was found
        return [False, 'Query string value had an invalid token']
      # Make sure we have a valid value. An empty string is not a 
      # valid value. It appears that an empty string is a valid 
      # value in a query string. The check below will never be true.
      if curValue == '' and curValue != '':
        return [False, 'Query string value is an empty string']
      # Check if the query dictionary already has the current keyword
      if curKeyword in queryDict:
        return [False, 'Query string has a duplicate keyword value']
      # Add the keyword/value pair to the dictionary  
      queryDict[curKeyword] = curValue
    # Make sure we found at least one keyword/value pair
    if len(queryDict) == 0:
      return [False, 'Query string does not contain any keyword/value pairs']
    # The query string appears to be OK
    return [True, queryDict]
  # This routine does something quite simple. This routine combines
  # tokens in some cases. The combination case is where an identifier
  # or an integer or a hyphen (minus sign) is directly followed
  # by some number of identifiers, integers, or hyphens. All of 
  # these tokens are combined into one (identifier) token. 
  #
  # This is done because combinations of identifier, integers, and
  # hypens are really just one token host string purposes. The 
  # combined token might be part of standard host name or it
  # might be part of an IPv6 host name.
  # 
  # Note that the original token list is not modified by this
  # routine. A new token list is returned to the caller. 
  @staticmethod
  def combineTokens(tokens):
    # Set a few initial values
    outputTokens = []
    tokenCount = len(tokens)
    tokenIndex = 0
    # Check each of the tokens
    while tokenIndex < tokenCount:
      # Get the contents of the current token
      curToken = tokens[tokenIndex]   
      curTokenPos = curToken.getPos()
      curTokenType = curToken.getType()
      curTokenValue = curToken.getValue()
      finalTokenType = curTokenType
      # Check if the current token is something that can be combined
      # with other tokens  
      if curTokenType == HDLmTokenTypes.identifier or \
         curTokenType == HDLmTokenTypes.integer or \
         curTokenValue == '-':
        # Skip past the current token
        tokenIndex += 1
        # Add as many tokens to th current token as possible
        while tokenIndex < tokenCount:
          # Get the contents of the next token
          nextToken = tokens[tokenIndex]   
          nextTokenPos = nextToken.getPos()
          nextTokenType = nextToken.getType()
          nextTokenValue = nextToken.getValue()
          # Check if the next token is an identifier or an integer 
          # or a minus sign. Check if the next token immediately 
          # follows the current token.
          if nextTokenType == HDLmTokenTypes.identifier or \
             nextTokenType == HDLmTokenTypes.integer or \
             nextTokenValue == '-': 
            # Check if the next token position immediately 
            # follows the current token. Note that if we can
            # combine tokens, the token type is always set to
            # that of an identifier.
            if (curTokenPos + len(curTokenValue)) == nextTokenPos:
              tokenIndex += 1
              curTokenValue += nextTokenValue
              finalTokenType = HDLmTokenTypes.identifier
            else:
              break
          else:
            break
        # Build a new token and add it to the output token list
        outputToken = Token(finalTokenType, curTokenPos, curTokenValue)
        outputTokens.append(outputToken)
        continue
      # Just add the current token to the output token list
      tokenIndex += 1
      outputTokens.append(curToken)
    # Return the final token list to the caller
    return outputTokens
  # Get everything after the host name and return these items
  # to the caller. The host name is follow by the optional path,
  # the optional query string, and the optional fragment. 
  def getEverythingAfterHost(self):
    # Get the path string, if any
    pathSTr = ''
    if self.pathString != None:
      pathStr = self.pathString
    # Get the query string, if any
    queryStr = ''
    if self.queryString != None:
      queryStr = self.queryString
    # Get the fragment string, if any
    fragmentStr = ''
    if self.fragment != None:
      fragmentStr = self.fragment
    # Return the combined values to the caller
    return pathStr + queryStr + fragmentStr
  # Get the URL fragment (if any) and return it to the caller
  def getFragment(self):
    return self.fragment
  # Get the URL host string (if any) and return it to the caller.
  # The host string may be a domain name or it may be an IPv4 
  # address or it may be an IPv6 address.
  #
  # The path string may be an empty string or it may be just a forward
  # slash or it may be longer than one character. Note that the path 
  # string will not contain the query string (if ahy) or the fragment
  # (if any). The path string will not be a none value.
  def getHost(self):
    return self.hostString
  # Return the parts of the host name string (if any) to the caller
  def getHostParts(self):
    return self.hostParts
  # Get the URL host type (if any) and return it to the caller.
  # The host type (if any) value will be an enum value. 
  def getHostType(self):
    return self.hostType
  # Get the original URL and return it to the caller
  def getOriginalUrl(self):
    return self.originalUrl
  # Get the URL path string (if any) and return it to the caller
  def getPath(self):
    return self.pathString
  # Get the parts of the URL path string (if any) and return them
  # to the caller
  def getPathParts(self):
    return self.pathParts
  # Get the URL port number (if any) and return it to the caller. 
  # The port number (if one is specified), will be an integer.
  def getPort(self):
    return self.portNumber
  # Get the URL query string (if any) and return it to the caller
  def getQuery(self):
    return self.queryString
  # Get the parts of the URL query string (if any) and return them
  # to the caller
  def getQueryParts(self):
    return self.queryParts
  # Get the URL scheme (if any) and return it to the caller
  def getScheme(self):
    return self.scheme
  # Get the URL user information (if any) and return it to the caller
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
    while (True):
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
    while (True):
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
      # value. At least for now we can not handle data values.
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
  def getUser(self):
    return self.userInfo