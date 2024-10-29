#----------------------------------------------------------------------#
#   Program dumpASN2.py                                                #
#                                                                      #
#   Notes                                                              #
#                                                                      #
#     1. Most output lines describe one ASN.1 entry. The               #
#        length of the entry is in brackets. The value of              #
#        the entry is in parenthesis. For example, a tag               #
#        with a length of 70 and a value of zero will be               #
#        displayed as Tag[70](0). The length value is                  #
#        optional and will not be displayed unless the                 #
#        length flag is set (except for bit strings).                  #
#                                                                      #
#     2. The length value for a bit string is always displayed         #
#        using brackets. This is done because bit strings have         #
#        two length values. First, the length of the bit string        #
#        in octets. Second, the number of trailing unused bits.        #
#        The length value over on the left will always be one          #
#        higher because it includes the prefix byte used to give       #
#        the number of trailing unused bits.                           #
#                                                                      #
#     3. At present we don't even try to extract any bit               #
#        or octet string less 20 bytes long. This is just              #
#        a heuristic. Any value could be used. This check              #
#        could be removed as well.                                     #
#                                                                      #
#     4. The current code uses exceptions to handle cases              #
#        where we do not have enough bytes available. This             #
#        should be done inline instead. Actually the current           #
#        approach is OK because the exceptions are caught with         #
#        a try/except blocks.                                          #
#                                                                      #
#     5. This program supports several input file types. The           #
#        file type suffix determines how the file is handled.          #
#        Files with a suffix of txt are assumed to contain             #
#        hexadecimal data. All blanks removed and the final            #
#        hexadecimal string is converted to binary.                    #
#                                                                      #
#        Files with a suffix of bs64 are assumed to contain            #
#        base 64 encoded data. All blanks are removed and the          #
#        final base 64 string is converted to binary.                  #
#                                                                      #
#        Files with a suffix of crt, csr, key, or pem are              #
#        assumed to be in PEM format. The first PEM structure          #
#        is found and extracted. All other certificates or             #
#        private keys are just ignored. Of course, it is               #
#        assumed that PEM data is base 64 encoded.                     #  
#                                                                      #
#        All other file types are assumed to contain binary            #
#        data. They are just read into memory and used.                #
#                                                                      #
#   Future changes                                                     #
#                                                                      #
#     1. Explicit and implicit tagging is not handled well.            #
#        See the 'Explicitly tagged types' section of the              #
#        below URL for more details. In some cases, other              #
#        ASN.1 formatters appear to treat explicit tags                #
#        as Sequences and Sets. It may be true that implicit           #
#        tags have a class of Context-Specific and also have           #
#        the constructed bit set.                                      #
#                                                                      #
#        http://luca.ntop.org/Teaching/Appunti/asn1.html               #
#                                                                      #
#     2. We check for two consecutive bytes of binary zero             #
#        (a tag of zero and a length of zero) to mark the              #
#        end of list (Set or Sequence) of components that              #
#        used the constructed, indefinite-length method.               #
#        This check should only be used if we know we are              #
#        handling a constructed, indefinite-length list.               #
#        In all other cases, it should be treated as an                #
#        error. See section 3.3 of the above URL for the               #
#        details.                                                      #
#                                                                      #
#     3. We need to make sure that all octets are used                 #
#        for Sets and Sequences with a known length                    #
#                                                                      #
#     4. A test suite should be included in this module                #
#        using standard Python conventions                             #
#                                                                      #
#     5. The formatting of UTCTime should be improved to               #
#        include the GMT offset and separate the year,                 #
#        month, day, etc.                                              #
#                                                                      #
#     6. Check for Sets and Sequences that do not have the             #
#        constructed type bit flag set. Report an error if             #
#        need be. This is a general point. Some types must             #
#        be constructed. Other types must be primitive. A              #
#        few types can be either. Check all of these cases.            #
#                                                                      #
#     7. The extract routines for several data type may need to        #
#        support the indefinite-length method                          #
#                                                                      #
#     8. The openssl asn1parse command produces a good report.         #
#        Each line has several values including the offset, length,    #
#        and other values. This could be a model for this routine.     #
#                                                                      #
#     9. We treat some octet strings and bit strings as encapsulated   #
#        data (assuming the encapsulated flag is set). In some cases,  #
#        a simple octet or bit string contains the encapsulated data.  #
#        However, in other cases (a constructed encoding) all of the   #
#        parts of the octet or bit string must be combined to create   #
#        the octet or bit string that can be processed as encapsulated #
#        data. A separate line should be written out to described      #
#        the combined octet or bit string if one is built.             #
#                                                                      #
#    10. Some print strings and OIDs are too long and should be        #
#        displayed on multiple lines. The OIDs aren't real OIDs.       #
#        They just appear to be OIDs because of tagging.               #
#                                                                      #
#    11. Some types (such as Boolean) have fixed lengths. These        #
#        lengths should be checked and verified.                       #
#                                                                      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
from   urllib.request import urlopen
import base64
import optparse
import pdb 
import sys
#----------------------------------------------------------------------#
#   Create a few values                                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
ConstructedType = 0x20
classes = { 0x00 : 'Universal',
            0x40 : 'Application',
            0x80 : 'Context-Specific',
            0xc0 : 'Private' }
tags = { 0x00 : '0',
         0x01 : 'Boolean',
         0x02 : 'Integer',
         0x03 : 'Bit String',
         0x04 : 'Octet String',
         0x05 : 'Null',
         0x06 : 'Object Identifier',
         0x07 : 'Object Descriptor',
         0x08 : 'External',
         0x09 : 'Real',
         0x0a : 'Enumerated',
         0x0b : 'Embedded-PDV',
         0x0c : 'UTF8String',
         0x0d : 'Relative Object Identifier',
         0x0e : 'Reserved-14',
         0x0f : 'Reserved-15',
         0x10 : 'Sequence',
         0x11 : 'Set',
         0x12 : 'NumericString',
         0x13 : 'PrintableString',
         0x14 : 'T61String',
         0x15 : 'VideotextString',
         0x16 : 'IA5String',
         0x17 : 'UTCTime',
         0x18 : 'GeneralizedTime',
         0x19 : 'GraphicString',
         0x1a : 'VisibleString',
         0x1b : 'GeneralString',
         0x1c : 'UniversalString',
         0x1d : 'CharacterString',
         0x1e : 'BMPString',
         0x1f : '31' }
#----------------------------------------------------------------------#
#   The character table can be used to convert all non-printable       #
#   characters to a period. Note that many characters from 0x80        #
#   to 0xff are actually printable.                                    #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
charTable = '................................' + \
            ' !"#$%&' + "'" +                    \
            '()*+,-./0123456789:;<=>?' +         \
            '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_' + \
            '`abcdefghijklmnopqrstuvwxyz{|}~.' + \
            '................................' + \
            '\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7' + \
            '\xa8\xa9\xaa\xab\xac\xad\xae\xaf' + \
            '\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7' + \
            '\xb8\xb9\xbb\xbb\xbc\xbd\xbe\xbf' + \
            '\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7' + \
            '\xc8\xc9\xcc\xcb\xcc\xcd\xce\xcf' + \
            '\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7' + \
            '\xd8\xd9\xdd\xdb\xdc\xdd\xde\xdf' + \
            '\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7' + \
            '\xe8\xe9\xee\xeb\xec\xed\xee\xef' + \
            '\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7' + \
            '\xf8\xf9\xff\xfb\xfc\xfd\xff\xff'
#----------------------------------------------------------------------#
#   Class charArray                                                    #
#                                                                      #
#   The charArray class is used to manage arrays of characters         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
class charArray(object):
#----------------------------------------------------------------------#
#   The __init__ method creates an instance of the class               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def __init__(self, chars):
    self.array = chars
    self.arLen = len(chars)
    self.off = 0
#----------------------------------------------------------------------#
#   The anyLeft method returns a boolean that indiates if              #
#   any data is left to be processed                                   #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def anyLeft(self):
    if self.off < self.arLen:
      return True
    else:
      return False
#----------------------------------------------------------------------#
#   The getChar method returns one character (if possible)             #
#   and updates the current offset. The character is consumed          #
#   and can not be returned again (without resetting the offset).      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def getChar(self):
    if self.off >= self.arLen:
      raise IndexError('No characters left for getChar call')
    charVal = self.array[self.off]
    self.off += 1
    return charVal
#----------------------------------------------------------------------#
#   The getChars method returns several characters (if possible)       #
#   and updates the current offset. The characters are consumed        #
#   and can not be returned again (without resetting the offset).      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def getChars(self, getLen):
    if self.off + getLen > self.arLen:
      raise IndexError('Not enough characters for getChars call')
    returnVal = self.array[self.off : self.off + getLen]
    self.off += getLen
    return returnVal
#----------------------------------------------------------------------#
#   The getCharsLeft method returns the remaining characters.          #
#   Note that this method does not consume any characters from         #
#   the character array. The current offset is not changed.            #
#   The number of returned characters may be zero.                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def getCharsLeft(self):
    if self.off >= self.arLen:
      return ''
    lengthLeft = self.arLen - self.off
    return self.array[self.off : self.off + lengthLeft]
#----------------------------------------------------------------------#
#   The getOffset method returns the current offset. No values         #
#   are changed and no characters are consumed.                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def getOffset(self):
    return self.off
#----------------------------------------------------------------------#
#   Class Int                                                          #
#                                                                      #
#   The Int class provides a mutable integer                           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
class Int(object):
#----------------------------------------------------------------------#
#   The __init__ method creates an instance of the class               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def __init__(self, value):
    self.value = value
#----------------------------------------------------------------------#
#   The __add__ method adds to the integer                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def __add__(self, other):
    return self.value + other
#----------------------------------------------------------------------#
#   The __mul__ method multiplies times an integer                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def __mul__(self, other):
    return self.value * other
#----------------------------------------------------------------------#
#   The __rmul__ method multiplies times an integer                    #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def __rmul__(self, other):
    return self.value * other
#----------------------------------------------------------------------#
#   The __str__ method returns the string form of an integer           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  def __str__(self):
    return str(self.value)
#----------------------------------------------------------------------#
#   Function bitsToString                                              #
#                                                                      #
#   Convert a bit string to a string                                   #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def bitsToString(b):
  ln = len(b)
  pad= ln % 8
  if pad > 0:
    b += '00000000'[pad:]
  out = ''
  for i in range(0, ln, 8):
    ch = 0
    for j in range(8):
      ch <<= 1
      ch += int(b[i + j : i + j + 1])
    out += chr(ch)
  return out
#----------------------------------------------------------------------#
#   Function bytesToString                                             #
#                                                                      #
#   This function converts a string of bytes to a character            #
#   string. Each binary byte is converted to exactly one               #
#   character. Note, that this routine returns a character             # 
#   string, not a binary string.                                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def bytesToString(bytes):
  outString = ''
  for byte in bytes: 
    intValue = int(byte)
    if intValue > 255:
      raise IndexError('Maximum simple character value(255) exceeded')
    outString += chr(intValue)
  return outString
#----------------------------------------------------------------------#
#   Function extractAny                                                #
#                                                                      #
#   Extract anything                                                   #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractAny(ca, nestLvl, baseOffset, printOff):
  while ca.anyLeft():
    curOffset = baseOffset + ca.getOffset()
#----------------------------------------------------------------------#
#   Extract the next tag from the input stream                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    tagList =  extractTag(ca)
    tagStr = tagList[0]
    classVal = tagList[1]
    ctVal = tagList[2]
    tagVal = tagList[3]
    charList = tagList[4]
    tagHexStr = stringToHex(charList)
#----------------------------------------------------------------------#
#   Extract the next length from the input stream. Note that           #
#   the length is undefined if constructed type flag is set            #
#   and if the indefinite-length method was used.                      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    lnList = extractPdfl(ca)
    lnVal = lnList[0]
    lnHexStr = stringToHex(lnList[2])
    lnOutStr = 'Undf' if (lnHexStr == '80' and ctVal) else str(lnVal)
    lnOutStrSquare = '[' + lnOutStr + ']' if glbLengthFlag else ''
#----------------------------------------------------------------------#
#   Display the contents of the current tag in some detail             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if glbDebugFlag:
      print('Debug top of extractAny loop', \
            'off=' + str(curOffset),  \
            tagStr + "/x'" + tagHexStr + "'", \
            ctVal, tagVal, \
            'len='+ str(lnVal) + "/x'" + lnHexStr + "'")
#----------------------------------------------------------------------#
#   Check for a zero tag value. If the length is also zero             #
#   and no class bits are set and the constructed type bit             #
#   is not set, then we have the end of a constructed type,            #
#   indefinite-length set of BER/DER encoded values. This              #
#   is actually two bytes of binary zeros.                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagHexStr == '00' and lnHexStr == '00':
      tagStr = 'EOC'
      tagFmt = tagStr + lnOutStrSquare
      printEntry(curOffset, nestLvl, tagFmt, lnVal, tagHexStr, printOff)
      if glbDebugFlag:
        print('Debug returning from extractAny')
      return
#----------------------------------------------------------------------#
#   Check for a class of Context-Specific with the constructed         #
#   type flag set. This appears to be how tags (probably explicit      #
#   tags) are encoded. This combination is displayed as a tag,         #
#   than as a combination of Context-Specific and the constructed      #
#   type flag. Note that the type is always displayed as a number,     #
#   rather than the type the number implies. For tags the type         #
#   implied by the number may not be correct.                          #
#                                                                      #
#   Note that the actual length is not passed to the print entry       #
#   function. The value passed may actually be 'Undf' which is         #
#   correct for an indefinite-length encoding of a constructed         #
#   value.                                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if classVal == 'Context-Specific' and ctVal:
      tagNumber = ord(hexToString(tagHexStr)) & 0x1f
      tagFmt = 'Tag' + lnOutStrSquare
      tagFmt += '(' + str(tagNumber) + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnOutStr, tagHexStr, printOff)
#----------------------------------------------------------------------#
#     Check for an indefinite-length encoding. Create a new            #
#     nesting level to handle it. We can not create a new              #
#     character array in this case, because we don't know              #
#     how long the type will actually be.                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
      if lnHexStr == '80':
        curOffset = baseOffset
        extractAny(ca, nestLvl + 1, curOffset, printOff)
#----------------------------------------------------------------------#
#     Check for a length greater than zero for a definite              #
#     length encoding. We don't need to create a new nesting           #
#     level if the length is zero.                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
      elif lnVal > 0:
        curOffset = baseOffset + ca.getOffset()
        caTag = charArray(ca.getChars(lnVal))
        extractAny(caTag, nestLvl + 1, curOffset, printOff)
      continue
#----------------------------------------------------------------------#
#   Check if the encapsulated data flag is set and we have an          #
#   octet string or a bit string. If we do, try to obtain a copy       #
#   of the octet or bit string on a trial basis. This does not         #
#   actually consume the data from the current character array.        #
#   If the first byte of the octet or bit string shows that we         #
#   have a Set or Sequence, extact the Set or Sequence and             #
#   remove the bytes from the current character array.                 #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if glbEncapFlag and \
       (tagVal == 'Octet String' or tagVal == 'Bit String'):
#----------------------------------------------------------------------#
#     Create a new character array from all of the remaining bytes     #
#     in the current character array. This does not change the offset  #
#     in the current character array. This allows encapsulation to     #
#     be tested and skipped if need be.                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
      caLeft = charArray(ca.getCharsLeft())
      if tagVal == 'Octet String':
        charsArray, usedLen, firstUsed = \
          extractOctetStr(caLeft, lnVal, ctVal, lnHexStr)
      else:
        bitStr, outStr, trailPads, usedLen, firstUsed = \
          extractBitStr(caLeft, lnVal, ctVal, lnHexStr)
        charsArray = bitsToString(bitStr)
#----------------------------------------------------------------------#
#     Get the first byte in hexadecimal so that we can check for       #
#     a Set or a Sequence                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
      if len(charsArray) > 0:
        firstChar = stringToHex(charsArray[0])
      else:
        firstChar = '00'
#----------------------------------------------------------------------#
#     The code below extracts any Set or Sequence. A temporary         #
#     character array is used to handle the extract processing.        #
#     After the extract step is complete, the bytes are finally        #
#     removed from the current character array.                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
      if usedLen >= 0 and \
         (firstChar == '30' or firstChar == '31'):
#----------------------------------------------------------------------#
#       Try to extract the current bit or octet string. This           #
#       may cause an exception. If it does, just skip the              #
#       current bit or octet string. Note that the no print            #
#       flag is set to true below so that the extract won't            #
#       generate any output.                                           #
#                                                                      #
#       A flag of true is passed to the extract routine below.         #
#       This prevents any output from test extract processing.         #
#       Normally, this flag is set to false.                           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
        try:
          curOffsetTry = baseOffset + ca.getOffset() + firstUsed
          caData = charArray(charsArray)
          extractAny(caData, nestLvl + 1, curOffsetTry, True)
          extractOK = True
        except IndexError:
          extractOK = False
#----------------------------------------------------------------------#
#       If the trial extract did't raise an error, do the              #
#       actual extract. The trial extract didn't change                #
#       the current offset. The extract below will change              #
#       the current offset after the extract is complete.              #
#                                                                      #
#       The offset adjustment factor is only needed for Bit            #
#       Strings. Bit Strings have an extra byte used to note           #
#       the number of unused trailing bits. This byte is not           #
#       part of the embedded Sequence or Set.                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
        offAdj = 0
        if extractOK:
          if tagVal == 'Octet String':
            tagFmt = tagStr + lnOutStrSquare
          else:
            lnOutBitStr = str((len(bitStr) + 7) >> 3) + ', ' + \
                          str(trailPads)
            tagFmt = tagStr + '[' + lnOutBitStr + ']'
            offAdj = 1
          printEntry(curOffset, nestLvl, tagFmt, \
                     lnOutStr, tagHexStr, printOff)
          curOffset = baseOffset + ca.getOffset() + firstUsed + offAdj
          caData = charArray(charsArray)
          extractAny(caData, nestLvl + 1, curOffset, printOff)
          charsArray = ca.getChars(usedLen)
          continue
#----------------------------------------------------------------------#
#   Check if we have any class value with a constructed type           #
#   tag with a constructed indefinite-length value. This               #
#   type of tag must be handled at the next nesting level.             #
#   Note that the test below applies to any type of tag value          #
#   and any class value.                                               #
#                                                                      #
#   Note that the actual length is not passed to the print entry       #
#   function. The value passed may actually be 'Undf' which is         #
#   correct for an indefinite-length encoding of a constructed         #
#   value.                                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if ctVal and lnHexStr == '80':
      tagFmt = tagStr + lnOutStrSquare
      printEntry(curOffset, nestLvl, tagFmt, lnOutStr, tagHexStr, printOff)
      curOffset = baseOffset
      extractAny(ca, nestLvl + 1, curOffset, printOff)
      continue
#----------------------------------------------------------------------#
#   Check if we have any class value with a constructed type           #
#   tag with a constructed definite-length value that is not           #
#   zero. This type of tag must be handled at the next nesting         #
#   level. Note that the test below applies to any type of tag         #
#   value and any class value.                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if ctVal and lnVal > 0:
      tagFmt = tagStr + lnOutStrSquare
      printEntry(curOffset, nestLvl, tagFmt, lnVal, tagHexStr, printOff)
      curOffset = baseOffset + ca.getOffset()
      caObj = charArray(ca.getChars(lnVal))
      extractAny(caObj, nestLvl + 1, curOffset, printOff)
      continue
#----------------------------------------------------------------------#
#   Check if we have any class value with a constructed type           #
#   tag with a constructed definite-length value that is zero.         #
#   This type of tag must be handled here and no new nesting           #
#   level can or should be created. Note that the test below           #
#   applies to any type of tag value and any class value.              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if ctVal and lnVal == 0:
      tagFmt = tagStr + lnOutStrSquare
      printEntry(curOffset, nestLvl, tagFmt, lnVal, tagHexStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a zero tag value. Testing has shown that some            #
#   zero tag values have a non-zero length. These tag values           #
#   do not have the constructed type flag set. As a consequence        #
#   we handle them here. Since the actual content of the data          #
#   is unknown, it is formatted in hexadecimal.                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == '0':
      tagFmt = tagStr + lnOutStrSquare
      printEntry(curOffset, nestLvl, tagFmt, lnVal, tagHexStr, printOff)
      if lnVal > 0:
        charsArray = ca.getChars(lnVal)
        printHex(nestLvl + 1, charsArray, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a Bit String. The first byte of a bit string             #
#   contains the number of trailing pad bits at the end of             #
#   the bit string. As a consequence, the length string has            #
#   two parts. First the actual number of bytes. Second, the           #
#   number of trailing pad bits.                                       #
#                                                                      #
#   Note that in a constructed encoding of a bit string each           #
#   part of the constructed encoding will have a length and            #
#   a byte indicating the number of trailing pad bits. We              #
#   combine each of the bit strings of a constructed encoding          #
#   to form the bit string (at least in some cases).                   #
#                                                                      #
#   In practice the call below will never handle a constructed         #
#   encoding of a bit string. Constructed encodings of bit             #
#   strings are handled earlier.                                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Bit String':
      bitStr, outStr, trailPads, usedLen, firstUsed = \
        extractBitStr(ca, lnVal, ctVal, lnHexStr)
      lnOutBitStr = str((len(bitStr) + 7) >> 3) + ', ' + \
                    str(trailPads)
      tagFmt = tagStr + '[' + lnOutBitStr + ']'
      printEntry(curOffset, nestLvl, tagFmt, \
                 lnVal, tagHexStr, printOff)
      printBitStr(nestLvl + 1, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a BMPString                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'BMPString':
      outStr = extractPrintStr(ca, lnVal, ctVal)
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a Boolean                                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Boolean':
      outStr = extractBoolean(ca, lnVal, ctVal)
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a IA5String                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'IA5String':
      outStr = extractPrintStr(ca, lnVal, ctVal)
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for an Integer                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Integer':
      intVal = extractInt(ca, lnVal)
      intStr = str(intVal)
      if len(intStr) <= 50:
        tagFmt = tagStr + '(' + intStr + ')'
        printEntry(curOffset, nestLvl, tagFmt, lnVal, intStr, printOff)
      else:
        tagFmt = tagStr + lnOutStrSquare
        printEntry(curOffset, nestLvl, tagFmt, lnVal, intStr, printOff)
        printInt(nestLvl + 1, intStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a Null                                                   #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Null':
      printEntry(curOffset, nestLvl, tagStr, lnVal, tagHexStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for an Object Identifier                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Object Identifier':
      oidStr = extractOid(ca, lnVal, printOff)
      tagFmt = tagStr + '(' + oidStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, oidStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for an Octet String                                          #
#                                                                      #
#   Note that in a constructed encoding of an octet string each        #
#   part of the constructed encoding will have a separate length.      #
#   We combine each of the octet strings of a constructed encoding     #
#   to form the octet string (at least in some cases).                 #
#                                                                      #
#   In practice the call below will never handle a constructed         #
#   encoding of an octet string. Constructed encodings of octet        #
#   strings are handled earlier.                                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Octet String':
      charsArray, usedLen, firstUsed = \
        extractOctetStr(ca, lnVal, ctVal, lnHexStr)
      tagFmt = tagStr + lnOutStrSquare
      printEntry(curOffset, nestLvl, tagFmt, lnVal, tagHexStr, printOff)
      printHex(nestLvl + 1, charsArray, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a PrintableString                                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'PrintableString':
      outStr = extractPrintStr(ca, lnVal, ctVal)
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a Relative Object Identifier                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'Relative Object Identifier':
      oidStr = extractRoid(ca, lnVal, printOff)
      tagFmt = tagStr + '(' + oidStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, oidStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a UTF8String. The decode operation below does not        #
#   appear to work, but really does. However, when the data is         #
#   finally printed it is encoded as UTF-8 making it appear that       #
#   the docode never happened. Note that the decode will convert       #
#   multiple bytes to one byte which can be tested by checking         #
#   the length of the string returned by decode.                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'UTF8String':
      outStr = extractPrintStr(ca, lnVal, ctVal)
      outBytes = stringToBytes(outStr)
      outStr = outBytes.decode('utf-8')
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a UTCTime                                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'UTCTime':
      outStr = extractPrintStr(ca, lnVal, ctVal)
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Check for a VisibleString                                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if tagVal == 'VisibleString':
      outStr = extractPrintStr(ca, lnVal, ctVal)
      tagFmt = tagStr + '(' + outStr + ')'
      printEntry(curOffset, nestLvl, tagFmt, lnVal, outStr, printOff)
      continue
#----------------------------------------------------------------------#
#   Handle all other cases                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    outStr = extractPrintStr(ca, lnVal, ctVal)
    tagFmt = tagStr + lnOutStrSquare
    printEntry(curOffset, nestLvl, tagFmt, lnVal, tagHexStr, printOff)
    printHex(nestLvl + 1, outStr, printOff)
  return
#----------------------------------------------------------------------#
#   Function extractBase128                                            #
#                                                                      #
#   Extract one length. A length is stored as one or more bytes.       #
#   This routine returns the length and the number of bytes used.      #
#   The BER/DER encoding uses base 128. The last byte does not have    #
#   the 0x80 bit set.                                                  #
#                                                                      #
#   This routine returns a list of values. The values are:             #
#                                                                      #
#     The extracted length value                                       #
#     The number of bytes consumed                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractBase128(ca):
  outLen = 0
  outCnt = 0
  moreChars = True
  while moreChars:
    nextChar = ca.getChar()
    outCnt += 1
    nextInt = ord(nextChar)
    if (nextInt & 0x80) == 0:
      moreChars = False
    else:
      moreChars = True
    outLen = outLen << 7
    outLen += nextInt & 0x7f
  return [outLen, outCnt]
#----------------------------------------------------------------------#
#   Function extractBitStr                                             #
#                                                                      #
#   Extract one bit string. We really have two very different          #
#   cases to handle here. First, we must be able to extract a          #
#   primitive bit string. Second, we must be able to extract           #
#   a constructed encoding of a bit string. In the second case,        #
#   each part of the constructed encoding must be combined to          #
#   build the final bit string. Note that the constructed              #
#   encoding might use the definite-length method or the               #
#   indefinite-length method.                                          #
#                                                                      #
#   This routine returns a tuple of values. The values are:            #
#                                                                      #
#     The bit string as a sequence of zeros and ones with no padding   #
#     The bit string in hexadecimal                                    #
#     The number of trailing pads                                      #
#     The number of character array bytes used                         #
#     The offset of the first byte of actual bit data                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractBitStr(ca, btLen, ctVal, lnHexStr):
  hexStr = ''
  if not ctVal:
    trailPads = ord(ca.getChar())
    charsArray = ca.getChars(btLen - 1)
    bitStr = stringToBits(charsArray)
    if trailPads > 0:
      bitStr = bitStr[ : ((btLen - 1) << 3) - trailPads]
#----------------------------------------------------------------------#
#   Convert the bit string to hexadecimal                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    for ch in charsArray:
      if hexStr != '':
        hexStr += ' '
      hexStr += stringToHex(ch)
    return (bitStr, hexStr, trailPads, btLen, 0)
#----------------------------------------------------------------------#
#   Get each part of the constructed encoding                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  outBitStr = ''
  usedLen = 0
  firstUsed = 0
  while True:
#----------------------------------------------------------------------#
#   Get the next tag and length and check if we have found             #
#   the end of an indefinite-length encoding                           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    tagList = extractTag(ca)
    usedLen += len(tagList[4])
    lnList = extractPdfl(ca)
    usedLen += lnList[1]
#----------------------------------------------------------------------#
#   Set the first used value to the offset of the first actual         #
#   octet string data byte                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if firstUsed == 0:
      firstUsed = usedLen
#----------------------------------------------------------------------#
#   Check for the end of an indefinite-length encoding                 #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if lnHexStr == '80' and \
       stringToHex(tagList[4]) == '00' and \
       stringToHex(lnList[2]) == '00':
      break
#----------------------------------------------------------------------#
#   Get the next (possibly only) part of the bit string                #
#   and then check if we have retrieved the last part of               #
#   a definite-length encoding                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    lnVal = lnList[0]
    trailPads = ord(ca.getChar())
    usedLen += 1
    charsArray = ca.getChars(lnVal - 1)
    usedLen += lnVal - 1
    bitStr = stringToBits(charsArray)
    if trailPads > 0:
      bitStr = bitStr[:((lnVal - 1) << 3) - trailPads]
    outBitStr += bitStr
    if lnHexStr != '80' and usedLen >= btLen:
      break
#----------------------------------------------------------------------#
#   Get the number of trailing pads                                    #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  md = len(outBitStr) % 8
  trailPads = 0 if md == 0 else 8 - md
  charsArray = bitsToString(outBitStr)
#----------------------------------------------------------------------#
#   Convert the bit string to hexadecimal                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  for ch in charsArray:
    if hexStr != '':
      hexStr += ' '
    hexStr += stringToHex(ch)
  return (outBitStr, hexStr, trailPads, usedLen, firstUsed)
#----------------------------------------------------------------------#
#   Function extractBoolean                                            #
#                                                                      #
#   Extract one Boolean                                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractBoolean(ca, boolLen, ctVal):
  boolVal = ca.getChars(boolLen)
  outStr = 'False' if ord(boolVal) == 0 else 'True'
  return outStr
#----------------------------------------------------------------------#
#   Function extractInt                                                #
#                                                                      #
#   Extract one integer. The integer is assumed to be encoded          #
#   using BER/DER rules.                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractInt(ca, intLen):
#----------------------------------------------------------------------#
#   Check for a zero length interger. Zero length integers are         #
#   treated as zero values.                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if intLen == 0:
    return 0
#----------------------------------------------------------------------#
#   Get the integer value                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  chars = ca.getChars(intLen)
  firstChar = chars[0]
  firstInt = ord(firstChar)
  hexStr = stringToHex(chars)
  intVal = int(hexStr, 16)
#----------------------------------------------------------------------#
#   If the original two's complement value was positive, we are done   #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if firstInt & 0x80 == 0:
    return intVal
#----------------------------------------------------------------------#
#   Since the value was negative, we must get the two's complement     #
#   value                                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  binStr = bin(intVal)
  binStr = binStr[2:]
  binStr = ''.join('1' if ch =='0' else '0' for ch in binStr)
  intVal = int(binStr, 2) + 1
  return -intVal
#----------------------------------------------------------------------#
#   Function extractOctetStr                                           #
#                                                                      #
#   Extract one octet string. We really have two very different        #
#   cases to handle here. First, we must be able to extract a          #
#   primitive octet string. Second, we must be able to extract         #
#   a constructed encoding of an octet string. In the second case,     #
#   each part of the constructed encoding must be combined to          #
#   build the final octet string. Note that the constructed            #
#   encoding might use the definite-length method or the               #
#   indefinite-length method.                                          #
#                                                                      #
#   This routine returns a tuple of values. The values are:            #
#                                                                      #
#     The octet string                                                 #
#     The number of character array bytes used                         #
#     The offset of the first data byte of the octet string            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractOctetStr(ca, ocLen, ctVal, lnHexStr):
  if not ctVal:
    outStr = ca.getChars(ocLen)
    return (outStr, ocLen, 0)
#----------------------------------------------------------------------#
#   Get each part of the constructed encoding                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  outStr = ''
  usedLen = 0
  firstUsed = 0
  while True:
#----------------------------------------------------------------------#
#   Get the next tag and length and check if we have found             #
#   the end of an indefinite-length encoding                           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    tagList =  extractTag(ca)
    usedLen += len(tagList[4])
    lnList = extractPdfl(ca)
    usedLen += lnList[1]
#----------------------------------------------------------------------#
#   Set the first used value to the offset of the first actual         #
#   octet string data byte                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if firstUsed == 0:
      firstUsed = usedLen
#----------------------------------------------------------------------#
#   Check for the end of an indefinite-length encoding                 #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    if lnHexStr == '80' and \
       stringToHex(tagList[4]) == '00' and \
       stringToHex(lnList[2]) == '00':
      break
#----------------------------------------------------------------------#
#   Get the next (possibly only) part of the octet string              #
#   and then check if we have retrieved the last part of               #
#   a definite-length encoding                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
    ctStr = ca.getChars(lnList[0])
    usedLen += lnList[0]
    outStr += ctStr
    if lnHexStr != '80' and usedLen >= ocLen:
      break
  return (outStr, usedLen, firstUsed)
#----------------------------------------------------------------------#
#   Function extractOid                                                #
#                                                                      #
#   Extract one OID. The length is passed by the caller.               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractOid(ca, oidLen, printOff):
  out = ''
#----------------------------------------------------------------------#
#   Process the first byte which has two values in it                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  nextChar = ca.getChar()
  nextInt = ord(nextChar)
  out = str(nextInt // 40) + '.' + str(nextInt % 40)
  oidLen -= 1
  while oidLen > 0:
    nextLen = extractBase128(ca)
    out += '.' + str(nextLen[0])
    oidLen -= nextLen[1]
#----------------------------------------------------------------------#
#   Try to get the text for an OID                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  oidText = getOidText(out, printOff)
  if oidText != '':
    out = oidText
  return out
#----------------------------------------------------------------------#
#   Function extractPdfl                                               #
#                                                                      #
#   Extract one length. A length is stored as one or more bytes.       #
#   This routine handles the Primitive Definite-Length method.         #
#   This routine returns a list of values. The values are:             #
#                                                                      #
#     The final extracted length value                                 #
#     The number of bytes used                                         #
#     The used bytes themselves                                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractPdfl(ca):
  outLen = 0
  charList = ''
  char = ca.getChar()
  ordValue = ord(char)
  charsUsed = 1
  charList += char
  if (ordValue & 0x80) == 0:
    outLen = ordValue
    return [outLen, charsUsed, charList]
#----------------------------------------------------------------------#
#   The length is stored in multiple bytes                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  charCount = ordValue & 0x7f
  while charCount > 0:
    charCount -= 1
    char = ca.getChar()
    ordValue = ord(char)
    charsUsed += 1
    charList += char
    outLen = outLen << 8
    outLen += ordValue
  return [outLen, charsUsed, charList]
#----------------------------------------------------------------------#
#   Function extractPrintStr                                           #
#                                                                      #
#   Extract one PrintableString                                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractPrintStr(ca, psLen, ctVal):
  if not ctVal:
    outStr = ca.getChars(psLen)
    return outStr
#----------------------------------------------------------------------#
#   Get each part of the constructed encoding                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  outStr = ''
  usedLen = 0
  while True:
    tag =  extractTag(ca)
    usedLen += len(tag[4])
    lnVals = extractPdfl(ca)
    usedLen += lnVals[1]
    ctStr = ca.getChars(lnVals[0])
    usedLen += lnVals[0]
    outStr += ctStr
    if usedLen >= psLen:
      break
  return outStr
#----------------------------------------------------------------------#
#   Function extractRoid                                               #
#                                                                      #
#   Extract one relative object identifier. The length is passed       #
#   by the caller. See ITU X.690 standard for details. Note that       #
#   we create a local character array object here to prevent any       #
#   extra bytes from being removed from the character array passed     #
#   by the caller.                                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractRoid(ca, oidLen, printOff):
  out = ''
  caRoid = charArray(ca.getChars(oidLen))
#----------------------------------------------------------------------#
#   Extract each subidentifier and combine them into an OID string     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  while oidLen > 0:
    nextLen = extractBase128(caRoid)
    if out != '':
      out += '.'
    out += str(nextLen[0])
    oidLen -= nextLen[1]
    if oidLen < 0:
      raise IndexError('Negative length processing a Relative ' +
                       'Object Identifier')
#----------------------------------------------------------------------#
#   Try to get the text for an OID                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  oidText = getOidText(out, printOff)
  if oidText != '':
    out = oidText
  return out
#----------------------------------------------------------------------#
#   Function extractTag                                                #
#                                                                      #
#   Extract one tag. A tag is stored as one or more bytes.             #
#   This function returns a list of values. The values are:            #
#                                                                      #
#     The tag as a formatted string, suitable for display              #
#     The class value as a string                                      #
#     A boolean indicating if the tag was constructed                  #
#     Just the tag value as a string                                   #
#     All of the bytes in the tag                                      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def extractTag(ca):
  out = ''
  charList = ''
  char = ca.getChar()
  charList += char
  charInt = ord(char)
#----------------------------------------------------------------------#
#   Check if the constructed type bit flag is set                      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  ctvlBit = charInt & ConstructedType
  ctvlBool = True if ctvlBit != 0 else False
#----------------------------------------------------------------------#
#   Get the tag class value                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  clvlBit = charInt & 0xc0
  clvlStr = classes[clvlBit]
#----------------------------------------------------------------------#
#   Check if the tag value requires several bytes                      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  tgvl = charInt & 0x1f
  if tgvl > 30:
    tgvl = 0
    moreChars = True
    while moreChars:
      nextChar = ca.getChar()
      charList += nextChar
      nextInt = ord(nextChar)
      nextTag = nextInt & 0x7f
      tgvl = tgvl << 7
      tgvl += nextTag
      if (nextInt & 0x80) == 0:
        moreChars = False
      else:
        moreChars = True
#----------------------------------------------------------------------#
#   Convert the tag value to a string                                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if tgvl <= 31:
    tgvlStr = tags[tgvl]
  else:
    tgvlStr = str(tgvl)
#----------------------------------------------------------------------#
#   Get the class value. Since Universal is the standard, there        #
#   is no need to display it                                           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if clvlStr == 'Universal':
    clvlMod = ''
  else:
    clvlMod = clvlStr + ':'
#----------------------------------------------------------------------#
#   Format the constructed type value. For Sequences and Sets          #
#   we can just ignore the constructed type value.                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  ctvlMod = ctvlBool
  if ctvlMod:
    if tgvlStr == 'Sequence':
      ctvlMod = False
    elif tgvlStr == 'Set':
      ctvlMod = False
  ctvlStr = 'CType:' if ctvlMod else ''
#----------------------------------------------------------------------#
#   Build the output value. The first value of the tuple               #
#   is the tag in a printable form. The other values of                #
#   the tuple are the components of the tag.                           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  out = clvlMod + ctvlStr + tgvlStr
  return (out, clvlStr, ctvlBool, tgvlStr, charList)
#----------------------------------------------------------------------#
#   Function getOidText                                                #
#                                                                      #
#   Get the text explanation of an OID string                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def getOidText(oid, noPrint):
#----------------------------------------------------------------------#
#   Check if OID URL processing has been disabled                      #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if glbNoOIDFlag == True:
    return oid
#----------------------------------------------------------------------#
#   Check output printing has been disabled. There is                  #
#   no point in trying to obtain the explanation text                  #
#   printing if off.                                                   #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if noPrint == True:
    return oid
#----------------------------------------------------------------------#
#   Try to use a URL to get an OID string                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  oidText = ''
  url = 'http://oid-info.com/get/'     
  url += oid
#----------------------------------------------------------------------#       
#   Get the OID explanation page                                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  try:
    page = urlopen(url)
  except Exception:
    return ''
#----------------------------------------------------------------------#
#   Find the OID text                                                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  for lineBytes in page:
    lineString = bytesToString(lineBytes)
    if lineString.find('textarea') < 0:
      continue
    lils = lineString.split('{')
    if len(lils) < 2:
       continue
    lineString = lils[1]
    lils = lineString.split('}')
    oidText = lils[0]
    break
  return oidText
#----------------------------------------------------------------------#
#   Function hexToString                                               #
#                                                                      #
#   Take a string containing hexadecimal data and return the           #
#   string built from each pair of hexadecimal digits. Note,           #
#   that this routine returns a character string, not a binary         #
#   string.                                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def hexToString(hexString):
  outString = ''
  hexStringLen = len(hexString)
  for i in range(0, hexStringLen, 2):
    hexSubString = hexString[i:i+2]
    intValue = int(hexSubString, 16)
    charValue = chr(intValue)
    outString += charValue
  return outString
#----------------------------------------------------------------------#
#   Function loadFile                                                  #
#                                                                      #
#   Load a file into memory and return the file as a character         #
#   array                                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def loadFile(fileName):
#----------------------------------------------------------------------#
#   Parse the file name into a main name and a suffix                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  fileNameArray = fileName.split('.')
  suffix = ''
  ln = len(fileNameArray)
  if ln >= 2:
    suffix = fileNameArray[ln - 1]
#----------------------------------------------------------------------#
#   Handle each type of suffix                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if suffix == 'bs64':
    outChars = loadFileBs64(fileName)
  elif suffix == 'crt':
    outChars = loadFilePem(fileName)
  elif suffix == 'csr':
    outChars = loadFilePem(fileName)
  elif suffix == 'key':
    outChars = loadFilePem(fileName)
  elif suffix == 'pem':
    outChars = loadFilePem(fileName)
  elif suffix == 'txt':
    outChars = loadFileTxt(fileName)
  else:
    outChars = loadFileBinary(fileName)
  return outChars
#----------------------------------------------------------------------#
#   Function loadFileBinary                                            #
#                                                                      #
#   Load a binary file into memory and return the file                 #
#   as a character array                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def loadFileBinary(fileName):
  f = open(fileName, 'r')
  outChars = f.read()
  f.close()
  return outChars
#----------------------------------------------------------------------#
#   Function loadFileBs64                                              #
#                                                                      #
#   Load a base 64 encoded file into memory and return the file        #
#   as a character array                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def loadFileBs64(fileName):
  f = open(fileName, 'r')
  bs64 = ''
  for line in f:
    line = line.strip()
    bs64 += line
  f.close()
  outBytes = base64.b64decode(bs64)
  outChars = bytesToString(outBytes)
  return outChars
#----------------------------------------------------------------------#
#   Function loadFilePem                                               #
#                                                                      #
#   Load a PEM file into memory and return the file as a               #
#   character array. Note that only the first certificate              #
#   or private key is processed. All others are just ignored.          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def loadFilePem(fileName):
  f = open(fileName, 'r')
  lineList = f.readlines()
  lineCount = len(lineList)
#----------------------------------------------------------------------#
#   Skip all lines prior to the first line marking the start           #
#   of a certificate or private key                                    #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  i = 0
  while i < lineCount:
    line = lineList[i].strip()
    if line.startswith('-----'):
      i += 1
      break
    i += 1
#----------------------------------------------------------------------#
#   Collect lines until we reach the end of the first                  #
#   certificate or private key                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  bs64 = ''
  while i < lineCount:
    line = lineList[i].strip()
    if line.startswith('-----'):
      break
    bs64 += line
    i += 1
  f.close()
  outBytes = base64.b64decode(bs64)
  outChars = bytesToString(outBytes)
  return outChars
#----------------------------------------------------------------------#
#   Function loadFileTxt                                               #
#                                                                      #
#   Load a text file into memory and return the file                   #
#   as a character array                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def loadFileTxt(fileName):
  f = open(fileName, 'r')
  hexString = ''
  for line in f:
    line = line.strip()
    hexString = hexString + line
  f.close()
  outChars = hexToString(hexString)
  return outChars
#----------------------------------------------------------------------#
#   Function printBitStr                                               #
#                                                                      #
#   Print one bit string                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def printBitStr(nestLvl, bitStr, printOff):
  if printOff == True:
    return
  indentStr = ' ' * nestLvl * 2
  indentStr += ' ' * 14
  while bitStr != '':
    curLen = 48 if len(bitStr) >= 48 else len(bitStr)
    curStr = bitStr[0 : curLen]
    hexStr = curStr.replace(' ', '')
    hexStr = hexToString(hexStr)
    hexStr = ''.join(charTable[ord(c)] for c in hexStr)
    spaces = (1 + 48 - curLen) * ' '
    print(indentStr + curStr + spaces + hexStr)
    bitStr = bitStr[curLen :]
  return
#----------------------------------------------------------------------#
#   Function printEntry                                                #
#                                                                      #
#   Print one ASN.1 entry                                              #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def printEntry(curOffset, nestLvl, tagStr, prLen, value, printOff):
  if printOff == True:
    return
  indentStr = ' ' * nestLvl * 2
  indentStr = right(str(curOffset), 5) + \
              right(str(prLen), 5) + \
              right(str(nestLvl), 3) + \
              ' ' + indentStr
  print(indentStr + tagStr)
  return
#----------------------------------------------------------------------#
#   Function printHex                                                  #
#                                                                      #
#   Print some data in hexadecimal                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def printHex(nestLvl, chars, printOff):
  if printOff == True:
    return
  indentStr = ' ' * nestLvl * 2
  indentStr += ' ' * 14
  charLen = len(chars)
  off = 0
  while charLen > 0:
    curLen = 32 if charLen >= 32 else charLen
    curChars = chars[off : off + curLen]
    charLen -= curLen
    off += curLen
    spaces = (2 + 64 - 2 * curLen) * ' '
    print(indentStr + stringToHex(curChars) + spaces + \
          ''.join(charTable[ord(c)] for c in curChars))
  return
#----------------------------------------------------------------------#
#   Function printInt                                                  #
#                                                                      #
#   Print an Integer on as many lines as need be                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def printInt(nestLvl, chars, printOff):
  if printOff == True:
    return
  indentStr = ' ' * nestLvl * 2
  indentStr += ' ' * 14
  charLen = len(chars)
  off = 0
  while charLen > 0:
    curLen = 50 if charLen >= 50 else charLen
    curChars = chars[off : off + curLen]
    charLen -= curLen
    off += curLen
    print(indentStr + curChars)
  return
#----------------------------------------------------------------------#
#   Function right                                                     #
#                                                                      #
#   Get the right end of a string padding with blanks or truncating    #
#   as need be. This function is modeled after the REXX function with  #
#   the same name.                                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def right(inputStr, n):
  inputLen = len(inputStr)
  if inputLen >= n:
    skip = inputLen - n
    return inputStr[skip : inputLen + 1]
  else:
    pad = n - inputLen
    return ' ' * pad + inputStr
#----------------------------------------------------------------------#
#   runMain                                                            #
#                                                                      #
#   Run the main code                                                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def runMain():
#----------------------------------------------------------------------#
#   Check the input file name and load the file into memory            #
#   as a character array                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if glbInFile == None:
    print('Input file name missing')
    exit()
  charsArray = loadFile(glbInFile)
#----------------------------------------------------------------------#
#   Check if an output file name was specified. If any output          #
#   file name was specified, write the character array to the          #
#   output file. This mechanism allows other file types to be          #
#   converted to binary.                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  if glbOutFile != None:
    f = open(glbOutFile, 'w')
    f.write(charsArray)
    f.close()
#----------------------------------------------------------------------#
#   Add some characters to the character array                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  charsArray += chr(0) * 00
  ca = charArray(charsArray)
#----------------------------------------------------------------------#
#   Decode the charArray object                                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  nestLvl = 0
  baseOffset = 0
  extractAny(ca, nestLvl, baseOffset, False)
  return
#----------------------------------------------------------------------#
#   runTest                                                            #
#                                                                      #
#   Run one test                                                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def runTest(z):
#----------------------------------------------------------------------#
#   Convert the hexadecimal bytes to a character array                 #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z = z.replace(' ', '')
  z = hexToString(z)
#----------------------------------------------------------------------#
#   Run the actual test                                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  ca = charArray(z)
  nestLvl = 0
  baseOffset = 0
  extractAny(ca, nestLvl, baseOffset, False)
  return
#----------------------------------------------------------------------#
#   runTests                                                           #
#                                                                      #
#   Run the test code                                                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def runTests():
#----------------------------------------------------------------------#
#   Some Sequence test code                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 1c 02 01 05 16 0e 41 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  z += '0d 04 c2 7b 03 02'
  z += '02 01 12'
  runTest(z)
#----------------------------------------------------------------------#
#   Some RDNSequence test code                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 42'
  z += '31 0b'
  z += '30 09'
  z += '06 03 55 04 06'
  z += '13 02 55 53'
  z += '31 1d'
  z += '30 1b'
  z += '06 03 55 04 0a'
  z += '13 14'
  z += '45 78 61 6d 70 6c 65 20 4f 72'
  z += '67 61 6e 69 7a 61 74 69 6f 6e'
  z += '31 14'
  z += '30 12'
  z += '06 03 55 04 03'
  z += '13 0b'
  z += '54 65 73 74 20 55 73 65 72 20 31'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Bit String test code                                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '03 04 06 6e 5d c0'
  runTest(z)
  z =  '03 04 06 6e 5d e0'
  runTest(z)
  z =  '03 81 04 06 6e 5d c0'
  runTest(z)
  z =  '23 09'
  z += '03 03 00 6e 5d'
  z += '03 02 06 c0'
  runTest(z)
  z =  '23 09'
  z += '03 03 01 6e 5d'
  z += '03 02 06 c0'
  runTest(z)
  z =  '23 09'
  z += '03 03 02 6e 5d'
  z += '03 02 06 c0'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Boolean test code                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '01 01 00'
  runTest(z)
  z =  '01 01 01'
  runTest(z)
  z =  '01 01 ff'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Integer test code                                             #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '02 02 ff 7f'
  runTest(z)
  z =  '02 01 80'
  runTest(z)
  z =  '02 01 81'
  runTest(z)
  z =  '02 01 ff'
  runTest(z)
  z =  '02 00'
  runTest(z)
  z =  '02 01 00'
  runTest(z)
  z =  '02 01 01'
  runTest(z)
  z =  '02 01 7f'
  runTest(z)
  z =  '02 02 00 80'
  runTest(z)
  z =  '02 02 00 81'
  runTest(z)
  z =  '02 02 01 00'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Null test code                                                #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '05 00'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Octet String test code                                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '04 08 01 23 45 67 89 ab cd ef'
  runTest(z)
  z =  '04 81 08 01 23 45 67 89 ab cd ef'
  runTest(z)
  z =  '24 0c'
  z += '04 04 01 23 45 67'
  z += '04 04 89 ab cd ef'
  runTest(z)
#----------------------------------------------------------------------#
#   Some OID test code                                                 #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '06 05 2b 06 01 04 01'
  runTest(z)
#----------------------------------------------------------------------#
#   Some RDNSequence test code                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 42'
  z += '31 0b'
  z += '30 09'
  z += '06 03 55 04 06'
  z += '13 02 55 53'
  z += '31 1d'
  z += '30 1b'
  z += '06 03 55 04 0a'
  z += '13 14'
  z += '45 78 61 6d 70 6c 65 20 4f 72'
  z += '67 61 6e 69 7a 61 74 69 6f 6e'
  z += '31 14'
  z += '30 12'
  z += '06 03 55 04 03'
  z += '13 0b'
  z += '54 65 73 74 20 55 73 65 72 20 31'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Sequence test code                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 13 02 01 05 16 0e 41 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Sequence test code                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 1c 02 01 05 16 0e 41 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  z += '0d 04 c2 7b 03 02'
  z += '02 01 12'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Sequence test code                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 0a 1a 04 6a 61 6e 65 02 02 00 80'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Sequence test code using Bit Strings                          #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 14 03 12 00'
  z += '30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  runTest(z)
  z =  '30 80 03 12 00'
  z += '30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  z += '00 00'
  runTest(z)
  z =  '30 80 23 14'
  z += '03 12 00'
  z += '30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  z += '00 00'
  runTest(z)
  z =  '30 80 23 17'
  z += '03 0f 00'
  z += '30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65'
  z += '03 04 00'
  z += '72 65 3f'
  z += '00 00'
  runTest(z)
  z =  '30 80 23 80'
  z += '03 0f 00'
  z += '30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65'
  z += '03 04 00'
  z += '72 65 3f'
  z += '00 00'
  z += '00 00'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Sequence test code using Octet Strings                        #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '30 13 04 11 30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  runTest(z)
  z =  '30 80 04 11 30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  z += '00 00'
  runTest(z)
  z =  '30 80 24 80'
  z += '04 11 30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65 72 65 3f'
  z += '00 00 00 00'
  runTest(z)
  z =  '30 80 24 80'
  z += '04 0e 30 0f 02 0d 6e 79 62 6f 64 79 20 74 68 65'
  z += '04 03 72 65 3f'
  z += '00 00 00 00'
  runTest(z)
#----------------------------------------------------------------------#
#   Some Set test code                                                 #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '31 0e 16 06 77 65 71 71 73 69 02 01 04 01 01 ff'
  runTest(z)
  z =  '31 0e 02 01 04 01 01 FF 16 06 4d 41 47 47 49 45'
  runTest(z)
#----------------------------------------------------------------------#
#   Some UTF8String test code using definite-length encoding           #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  '2c 13'
  z += '0c 05 74 65 73 74 31'
  z += '0c 01 40'
  z += '0c 07 72 73 61 23 63 c2 a2'
  runTest(z)
#----------------------------------------------------------------------#
#   Some UTF8String test code using indefinite-length encoding         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
  z =  'ac 80'
  z += '0c 05 74 65 73 74 31'
  z += '0c 01 40'
  z += '0c 07 72 73 61 23 63 c2 a2'
  z += '00 00'
  runTest(z)
#----------------------------------------------------------------------#
#   Function stringToBits                                              #
#                                                                      #
#   Convert a string to bit string                                     #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def stringToBits(s):
  ords = (ord(c) for c in s)
  shifts = (7, 6, 5, 4, 3, 2, 1, 0)
  return ''.join(str((o >> shift) & 1) \
                 for o in ords for shift in shifts)
#----------------------------------------------------------------------#
#   Function stringToBytes                                             #
#                                                                      #
#   This function converts a string of characters to a byte            #
#   string. Each character is converted to exactly one byte.           #
#   Note, that this routine returns a binary string, not a             # 
#   character.                                                         #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def stringToBytes(inStr):
  outBytes = b''
  for c in inStr: 
    intValue = ord(c)
    if intValue > 255:
      raise IndexError('Maximum simple character value(255) exceeded')
    outBytes += bytes([intValue])
  return outBytes
#----------------------------------------------------------------------#
#   Function stringtoHex                                               #
#                                                                      #                         
#   Take an input string and convert each character to hexadecimal.    #    
#   It is assumed that each character is in the range from 0 to 255.   #
#   Note, that this routine returns a character string, not a binary   # 
#   string.                                                            #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
def stringToHex(inStr):
  hexStr = "".join([hex(ord(c))[2:].zfill(2) for c in inStr])
  return hexStr
#----------------------------------------------------------------------#
#   Parse the command line input                                       #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
p = optparse.OptionParser(description='ASN.1 parser')
p.add_option('-d', action='store_true', dest='glbDebugFlag')
p.add_option('--debug', action='store_true', dest='glbDebugFlag')
p.add_option('-e', action='store_true', dest='glbEncapFlag')
p.add_option('--encapsulated', action='store_true', dest='glbEncapFlag')
p.add_option('-l', action='store_true', dest='glbLengthFlag')
p.add_option('--length', action='store_true', dest='glbLengthFlag')
p.add_option('-n', action='store_true', dest='glbNoOIDFlag')
p.add_option('--nooid', action='store_true', dest='glbNoOIDFlag')
p.add_option('-t', action='store_true', dest='glbTestFlag')
p.add_option('--test', action='store_true', dest='glbTestFlag')
p.add_option('-f', action='store', type='string', dest='glbInFile')
p.add_option('-o', action='store', type='string', dest='glbOutFile')
p.set_defaults(glbDebugFlag=False)
p.set_defaults(glbEncapFlag=False)
p.set_defaults(glbLengthFlag=False)
p.set_defaults(glbNoOIDFlag=False)
p.set_defaults(glbTestFlag=False)
(opts, args) = p.parse_args()
glbDebugFlag  = opts.glbDebugFlag
glbEncapFlag  = opts.glbEncapFlag
glbLengthFlag = opts.glbLengthFlag
glbNoOIDFlag  = opts.glbNoOIDFlag
glbTestFlag   = opts.glbTestFlag
glbInFile     = opts.glbInFile
glbOutFile    = opts.glbOutFile
#----------------------------------------------------------------------#
#   Run the main code or the test cod                                  #
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7-#
if glbTestFlag:
  runTests()
else:
  runMain()
