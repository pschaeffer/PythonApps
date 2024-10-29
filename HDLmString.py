# Start the string class. Note that no instances of this class
# are ever created.

from   HDLmAssert  import *
from   HDLmEnums   import *
from   HDLmError   import *
from   HDLmToken   import *
import re

HDLmStringImageTypes = ['ai',
                        'avif',
                        'bmp', 'dib',
                        'cdr',
                        'eps',
                        'exif',
                        'gif',
                        'heif', 'heic',
                        'ico', 'cur',
                        'ind', 'indd', 'indt', 'idml',
                        'jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi', 'pjpeg', 'pjp',
                        'jp2', 'j2k', 'jpf', 'jpm',
                        'jpg2', 'j2c', 'jpc', 'jpx',
                        'mj2',
                        'pdf',
                        'ppm', 'pgm', 'pbm', 'pnm',
                        'png', 'apng',
                        'psd',
                        'raw', 'arw', 'cr', 'crw', 'cr2', 'cr3', 'erf', 'k25',
                        'nef', 'nrw', 'orf', 'pef', 'rw2', 'srf', 'sr2', 'xdc',
                        'svg', 'svgz',
                        'tiff', 'tif',
                        'webp',
                        'xbm',
                        'xcf'];

class HDLmString(object):  
  # Capitalize a string. That means convert the first character
  # to uppercase and the rest of the string to lowercase.
  @staticmethod
  def capitalize(inStr):
    if len(inStr) == 0:
      return ''
    # Convert the entire string to lowercase
    lcStr = inStr.lower()
    # Convert the first character to uppercase
    return HDLmString.ucFirst(lcStr)
  # This function does a case insensitive string comparison. Of course,
  # this function can be changed as need be to better case insensitive
  # string comparisons. This routine will return true if the strings
  # are equal. This routine will return false if the strings are not
  # equal. 
  def compareCaseInsensitive(firstStr, secondStr):
    return firstStr.casefold() == secondStr.casefold()
  # Convert a list (vector) or tokens to a string. The string is returned
  # to the caller. The caller provides the list of tokens. Each token is 
  # added to the output string. 
  @staticmethod
  def convertTokens(tokenVec):
    # Build the initial output string
    outStr = ''
    # Process each of the tokens
    for token in tokenVec:
      # Check for a quoted string token
      if token.tokType == HDLmTokenTypes.quoted:
        outStr += token.originalValue
      # For all other token types, we can just copy the token value
      # to the output string
      else:
        outStr += token.value
    return outStr
  # Convert a list (vector) or tokens to a Java string. The string is
  # returned to the caller. The caller provides the list of tokens. 
  # Each token is added to the output string. Some tokens are modified
  # before they are added to the outout string.  
  @staticmethod
  def convertTokensJava(tokenVec):
    # Build the initial output string
    outStr = ''
    # Process each of the tokens
    for token in tokenVec:
      # Check for the end token
      if token.tokType == HDLmTokenTypes.quoted:
        outStr += token.originalValue
      # For all other token types, we can just copy the token value
      # to the output string
      else:
        line = token.value
        quoteChar = '"' 
        line = line.replace(quoteChar, '\\"')
        line = line.replace("'\\n'", "'\\\\n'")
        line = line.replace('\\s', '\\\s')
        line = line.replace('\\$', '\\\$')
        line = line.replace('\\.', '\\\.')
        line = line.replace('\\/', '\\\/')
        line = line.replace('\\(', '\\\(')
        line = line.replace('\\)', '\\\)')
        outStr += line
    return outStr
  # Find the offset (starting from zero, not one) of the first difference
  # between two strings. Note that if one string (either one) is longer than
  # the other string, and the strings match otherwise, the first extra 
  # character will be considered to be a mismatch. If the strings are 
  # the same length (which may be zero) and all of the characters match, 
  # a none value is returned.
  @staticmethod
  def findFirstDifference(firstStr, secondStr):
    # Get the lengths of each string
    firstStrLen = len(firstStr)
    secondStrLen = len(secondStr)
    minStrLen = min(firstStrLen, secondStrLen)
    # Check each character of both strings
    if firstStr != secondStr:
      index = -1
      for i in range(minStrLen):
        index += 1
        if firstStr[i] != secondStr[i]:
          return index
    # Check if the first string is longer than the second
    if firstStrLen > secondStrLen:
      return secondStrLen
    # Check if the second string is longer than the first
    if secondStrLen > firstStrLen:
      return firstStrLen
    # If the strings are the same length (which may be zero) and all
    # of the characters match, just return a none value
    return None  
  # Get the suffix, from what should be a file name. The 
  # suffix is everything after the last period. If no 
  # period is found a null value is returned to the 
  # caller. 
  @staticmethod
  def getFileNameSuffix(fileName):
    # Make sure the first argument passed by the caller is a string 
    if str(type(fileName)) != "<class 'str'>":
      errorText = f'File name (${fileName}) passed to getFileNameSuffix method is not a string'
      HDLmAssert(False, errorText)
    # Find the last occurrence (if any) of a period in the file name string 
    lastIndex = HDLmString.lastFindOf(fileName, '.')
    if lastIndex < 0:
      return None
    return fileName[lastIndex + 1:]  
  # Get the file type, from what should be the file name suffix.
  # The file name suffix is everything after the last period in
  # the file name. 
  def getFileNameType(fileNameSuffix):
    # Make sure the first argument passed by the caller is a string 
    if str(type(fileNameSuffix)) != "<class 'str'>":
      errorText = f'File name suffix (${fileNameSuffix}) passed to getFileNameType method is not a string'
      HDLmAssert(False, errorText) 
    # Check if the file name suffix is known 
    rv = None;
    if fileNameSuffix in HDLmStringImageTypes:
      rv = 'image';
    return rv
  # This function returns a vector of objects to the caller. The vector
  # of objects has one entry for each token in the string passed to this
  # routine, plus a sentinal entry to mark the end of the vector. The vector
  # of objects will contain just the sentinel entry if the string passed to
  # this routine is emtpy. This is not considered to be an error condition.
  #   
  # One object will be built for each token in the string passed by the 
  # caller. The object describes the token in some detail. The object
  # gives the token position (starting from 0, not 1), the token type,
  # and the token contents.
  #   
  # This is a low-level tokenization routine. No attempt is made in this
  # routine to build higher-level tokens. Other routines can do this or
  # use the tokens built by this routine to do so. This routine will return
  # integer tokens for sequences of numeric digits. It will not return 
  # number tokens. This means that a decimal point will end up in a separate
  # operator token. 
  #
  # Note that an identifier can contain numeric digits in it. This is part
  # of the definition of an identifier in JavaScript. 
  @staticmethod
  def getTokens(inStr, quoteChars = "'"):
    inLen = len(inStr) 
    rv = []
    pos = 0 
    # Process each character in the input string *
    while pos < inLen:
      # Get the current character 
      ch = inStr[pos]
      # Check for an alpha character of some kind. The first character 
      # of an identifier must be an alpha character. The other characters
      # can be alphanumeric. 
      if HDLmString.isAlpha(ch):
        obj = Token(HDLmTokenTypes.identifier, pos, ch) 
        pos += 1
        # Append all alphanumeric characters after the first one 
        while pos < inLen:
          # Get the next character 
          ch = inStr[pos]
          if HDLmString.isAlphaNumeric(ch) == False:
            break
          obj.addString(ch)
          pos += 1
        rv.append(obj)
        continue 
      # Check for a numeric character of some kind. Any number of numeric
      # characters are combined into one token. Note that the token type 
      # is integer, not number. This routine does not return number tokens. 
      # Instead, a decimal point after a series of digits will end up in a 
      # separate token. 
      if HDLmString.isDigit(ch):
        obj = Token(HDLmTokenTypes.integer, pos, ch) 
        pos += 1
        # Append all numeric characters after the first one 
        while pos < inLen:
          # Get the next character 
          ch = inStr[pos]
          if HDLmString.isDigit(ch) == False:
            break
          obj.addString(ch)
          pos += 1
        rv.append(obj)
        continue
      # Check for an Operator character of some kind. A separate token
      # is created for each operator.  
      if HDLmString.isOperator(ch):
        obj = Token(HDLmTokenTypes.operator, pos, ch) 
        pos += 1
        rv.append(obj)
        continue
      # Check for a quote character. The quote character does not become
      # part of the output token. Pairs of quotes are combined into one
      # quote character that does become part of the output token. The 
      # final quote terminates the quoted string. The first quote character
      # and the final quote character do not become part of the output token. 
      if ch in quoteChars:
        localQuoteChar = ch
        unmatchedQuotes = True
        quoteStringStartingPos = pos
        obj = Token(HDLmTokenTypes.quoted, pos, '') 
        obj.back = []
        obj.quote = localQuoteChar
        obj.originalValue = localQuoteChar
        pos += 1
        # Append the contents of the quoted string not including the 
        # leading and trailing quote characters 
        while pos < inLen:
          # Get the next character 
          ch = inStr[pos]
          obj.originalValue += ch
          # Check for an escape character. If we have an escape 
          # character, then the next character (if there is one) 
          # if always added to the output string.
          if ch == '\\':
            if (pos + 1) < inLen:
              # Keep track of where we found backslash characters
              # in the input string
              obj.back.append(pos-quoteStringStartingPos)
              ch = inStr[pos + 1]
              obj.addString(ch)
              obj.originalValue += ch
              pos += 2
              continue
            # Report an error if the quoted string has an escape at the end. 
            # Presently we handle this by raising an exception. The code for
            # building an error message is commented out. 
            else:
              # errorString = '(' + inStr + ')'
              # HDLmError.buildError('Error', 'Value missing after escape', 38, errorString)
              raise ValueError('Quoted string has an escape at the end')
          # Check for a quote character. Non-quote characters are just
          # added to the output token. 
          if ch != localQuoteChar:
            obj.addString(ch)
            pos += 1
            continue
          # At this point we need to check if the next character can
          # be obtained and if the next character is also a quote. If
          # both tests are true, then we have a pair of quotes that
          # can be combined into one quote character. 
          if (pos + 1 < inLen) and (inStr[pos + 1] == localQuoteChar):
            obj.addString(ch)
            pos += 2
            continue
          # At this point we have found the trailing quote character and
          # we can terminate the quoted string. Note that the trailing 
          # quote (like the leading quote) is not added to the token. 
          pos += 1
          unmatchedQuotes = False
          break
        # Report an error if the quoted string had unmatched quotes. Presently
        # we handle this by raising an exception. The code for building an 
        # error message is commented out. 
        if unmatchedQuotes:
          # errorString = '(' + inStr + ')'
          # HDLmError.buildError('Error', 'Unmatched Quotes', 15, errorString)
          raise ValueError('A quote string token is not complete')
        rv.append(obj)
        continue
      # Check for a white space character of some kind. Any number of white
      # space characters are combined into one token. Note that the function
      # used to check for white space characters only checks for traditional
      # white space characters at this time.  
      if HDLmString.isWhiteSpace(ch):
        obj = Token(HDLmTokenTypes.space, pos, ch) 
        pos += 1
        # Append all white space characters after the first one 
        while pos < inLen:
          # Get the next character 
          ch = inStr[pos]
          if HDLmString.isWhiteSpace(ch) == False:
            break
          obj.addString(ch)
          pos += 1
        rv.append(obj)
        continue
      # All other characters are treated as unknown characters. Because of the 
      # rules of JavaScript (not Python), Hash (pound) and curly braces are all 
      # treated as unknown characters. A separate token is created for each 
      # unknown character. 
      if True:
        obj = Token(HDLmTokenTypes.unknown, pos, ch) 
        pos += 1
        rv.append(obj)
        continue
    # Add the sentinel entry at the end of the token object array 
    obj = Token(HDLmTokenTypes.end, pos, '') 
    pos += 1
    rv.append(obj)
    return rv
  # This function returns a vector of objects to the caller. The vector
  # of objects has one entry for each non-white token in the string passed 
  # to this routine, plus a sentinal entry to mark the end of the vector.
  # The vector of objects will contain just the sentinel entry if the string 
  # passed to this routine is emtpy. This is not considered to be an error 
  # condition.
  # 
  # One object will be built for each token in the string passed by the 
  # caller. The object describes the token in some detail. The object
  # gives the token position (starting from 0, not 1), the token type,
  # and the token contents. 
  @staticmethod
  def getTokensNonWhite(inStr):
    rv = []
    tokenVec = HDLmString.getTokens(inStr)
    tokenLen = len(tokenVec)
    for i in range(tokenLen): 
      if tokenVec[i].tokType != HDLmTokenTypes.space:
        rv.append(tokenVec[i])
    return rv
  # The function below returns a boolean showing if a character
  # is a valid alpha character or not. The caller actually passes 
  # a string. However, the length of the string must be exactly
  # one. Note that in keeping with the rules of JavaScript,
  # underscore and dollar sign are considered to be alpha
  # characters.  The list of valid alpha characters is based
  # on JavaScript, not Python.
  @staticmethod
  def isAlpha(inChar):
    inLen = len(inChar) 
    # Make sure the input string length is one 
    if inLen != 1:
      errorText = 'Input string (' + inChar + ') length (' + str(inLen) + ') passed to isAlpha is not one'
      HDLmAssert(False, errorText)
    # Return the final True or False value. Note that this check
    # follows the rules of JavaScript, not Python.
    return (inChar >= 'a' and inChar <= 'z') or \
           (inChar >= 'A' and inChar <= 'Z') or \
           (inChar == '_' or inChar == '$')
  # The function below returns a boolean showing if a character
  # is a valid alphanumeric character or not. The caller actually
  # passes a string. However, the length of the string must be 
  # exactly one. Note that in keeping with the rules of JavaScript,
  # underscore and dollar sign are considered to be alphanumeric 
  # characters. The list of valid alphanumeric characters is based
  # on JavaScript, not Python.
  @staticmethod
  def isAlphaNumeric(inChar):
    inLen = len(inChar) 
    # Make sure the input string length is one 
    if inLen != 1:
      errorText = 'Input string (' + inChar + ') length (' + str(inLen) + ') passed to isAlphaNumeric is not one'
      HDLmAssert(False, errorText)
    # Return the final True or False value
    return (inChar >= '0' and inChar <= '9') or \
           (inChar == '_' or inChar == '$') or \
           (inChar >= 'a' and inChar <= 'z') or \
           (inChar >= 'A' and inChar <= 'Z')   
  # The function below returns a boolean showing if a character
  # is a valid numeric digit or not. The caller actually passes 
  # a string. However, the length of the string must be exactly
  # one. Note that the code below does not consider non-traditional
  # digit characters to be digits. This could be a problem in the
  # future. The list of valid digit characters is based on JavaScript, 
  # not Python.
  @staticmethod
  def isDigit(inChar):
    inLen = len(inChar) 
    # Make sure the input string length is one 
    if inLen != 1:
      errorText = 'Input string (' + inChar + ') length (' + str(inLen) + ') passed to isDigit is not one'
      HDLmAssert(False, errorText)
    # Return the final True or False value
    return inChar >= '0' and inChar <= '9'
  # The function below returns a boolean showing if a string consists
  # entirely of valid hexadecimal characters or not. Both upper and 
  # lower case hexadecimal are accepted. The string can be any length
  # including zero-length. A zero length string is considered to be a
  # valid hexadecimal string. The input string is not modified. 
  @staticmethod
  def isHex(inStr):
    regexStr = '^[0-9A-Fa-f]*$'
    regexCompiled = re.compile(regexStr)
    regexMatch = regexCompiled.match(inStr)
    return regexMatch != None 
  # The function below returns a boolean showing if a character
  # is a valid operator character or not. The caller actually
  # passes a string. However, the length of the string must be 
  # exactly one. Note that comma is included in the list of
  # operator characters below because comma is a valid JavaScript
  # operator. Period and brackets (left and right) are also 
  # included in the list of operator characters because they 
  # are used as accessors. Curly braces are not included because
  # curly braces are not valid JavaScript operators. For the same
  # reason the hash (pound) character is not included either. The
  # list of valid operator characters is based on JavaScript, not
  # Python.
  @staticmethod
  def isOperator(inChar):
    inLen = len(inChar) 
    # Make sure the input string length is one  
    if inLen != 1:
      errorText = 'Input string (' + inChar + ') length (' + str(inLen) + ') passed to isOperator is not one'
      HDLmAssert(False, errorText)
    haystack = '+-*/%=!><&|~^?:,().[]'
    return haystack.find(inChar) >= 0
  # The function below returns a boolean showing if a character
  # is a valid white space character or not. The caller actually
  # passes a string. However, the length of the string must be 
  # exactly one. The list below only includes the traditional 
  # white space characters. Many other (Unicode) non-traditional
  # white space characters exist. They may need to be added in 
  # the future. The list of valid white space characters is based
  # on JavaScript, not Python.
  @staticmethod
  def isWhiteSpace(inChar):
    inLen = len(inChar)
    # Make sure the input string length is one 
    if inLen != 1:
      errorText = 'Input string (' + inChar + ') length (' + str(inLen) + ') passed to isWhiteSpace is not one'
      HDLmAssert(False, errorText) 
    haystack = ' \f\n\r\t\v'
    return haystack.find(inChar) >= 0
  # Get the last index of a substring in a string. This
  # routine returns the last index, not the first index
  # which is what is generally wanted. Note that this 
  # routine returns a negative value, if the needle is 
  # not found in the haystack. An exception is not raised.
  @staticmethod
  def lastFindOf(haystack, needle):
    # Search for the first occurrence of the needle in the
    # haystack 
    lio = haystack.find(needle)
    if lio < 0:
      return lio
    # Keep looking for more occurrences of the needle in the 
    # haystack
    while True:
      nio = haystack[lio+1:].find(needle)
      if nio < 0:
        break;
      lio = lio + 1 + nio
    return lio
  # This method is passed a string. It counts the number of numeric 
  # characters (0-9) and returns the count to the caller.  
  @staticmethod
  def numericCount(inStr):
    rv = 0
    for i in range(0, len(inStr)): 
      cuChar = inStr[i]
      if cuChar >= '0' and cuChar <= '9':
        rv += 1
    return rv 
  # Pad a string on the left with zero or more padding characters
  @staticmethod
  def padLeft(inStr, desiredLength, padChar = ' '):
    return inStr.rjust(desiredLength, padChar)
  # Pad a string on the right with zero or more padding characters
  @staticmethod
  def padRight(inStr, desiredLength, padChar = ' '):
    return inStr.ljust(desiredLength, padChar)
  # The function below does a replace all on an input string. The 
  # input string is not modified. The new string is returned to the
  # caller. Note that regex is used below. The search string is escaped
  # as need be for regex use. 
  @staticmethod
  def replaceAll(inStr, search, replacement):
    return inStr.replace(search, replacement)
  # Remove a file number tail (if any) from a string. Some strings end
  # with a file number (of the form (nnn)) that must be removed for 
  # duplicate checking. This routine checks if the input string has 
  # a file number tail and removes it. In other words, 'Abcd' is 
  # returned as 'Abcd' and 'Abcd(3)' is also returned as 'Abcd'. 
  # Note that this routine does not change the case of any part of
  # the input or output strings. 
  @staticmethod
  def removeFileNumberTail(inStr):
    regexStr = r'\(\d+\)$'
    regexCompiled = re.compile(regexStr)
    regexSearch = regexCompiled.search(inStr)
    if regexSearch == None:
      return inStr
    else:
      regexIndex = regexSearch.start()
      return inStr[0:regexIndex]
  # Remove a prefix from a string if the prefix is found at the
  # start of the string. The original string is never changed.
  # The possibly modified string is returned to the caller. 
  @staticmethod
  def removePrefix(testStr, prefixStr):
    # Check for and remove the prefix string
    if testStr.startswith(prefixStr):
      prefixStrLen = len(prefixStr)
      testStr = testStr[prefixStrLen:]
    # Return the possibly modified test string to the caller
    return testStr
  # The remove suffix routine removes a suffix from an input
  # string if the string ends with the suffix
  @staticmethod
  def removeSuffix(inStr, suffix):
    if len(inStr) > 0:
      if inStr.endswith(suffix):
        inStr = inStr[:-len(suffix)]
    return inStr
  # Convert the first character of a string to uppercase and leave 
  # the rest of the string alone. Return the modified string to the
  # caller. The original string is not modified.  
  @staticmethod
  def ucFirst(value):
    if len(value) == 0:
      return value
    return value[0].upper() + value[1:]
  # Convert the first character all of words in a string to uppercase
  # and return the possibly modified sentence to the caller 
  def ucFirstSentence(inputValue):
    # Make sure the argument passed by the caller is a string 
    if str(type(inputValue)) != "<class 'str'>":
      errorText = f'Input value passed to ucFirstSentence is not a string'
      HDLmAssert(False, errorText);
    outputValue = '' 
    valueTokens = HDLmString.getTokens(inputValue)
    tokenCountMinusOne = len(valueTokens) - 1;
    for i in range(0, tokenCountMinusOne): 
      # Get some information from the current token 
      valueToken = valueTokens[i]
      valueString = valueToken.value
      # If the current token is an identifier, then we must
      # convert the first character to uppercase 
      if valueToken.tokType == HDLmTokenTypes.identifier:
        valueString = HDLmString.ucFirst(valueString)
      # Add the current (possibly modified) value to the output 
      # string 
      outputValue += valueString
    return outputValue