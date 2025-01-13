import argparse
import binascii
import enum
import os
import struct
import sys
import time

# The PST input file name is stored in the field below
glbInFileName = 'c:\\Users\\pscha\\Desktop\\Outlook.pst'
# The output file name is stored in the field below
glbOutFileName = 'c:\\Users\\pscha\\Desktop\\Outfile.txt'

# The standard PST page size is stored in the field below
glbPageSize = 512

# The table below is used for PST permutation
glbMpbbCrypt = [65,  54,  19,  98, 168,  33, 110, 187,
                244,  22, 204,   4, 127, 100, 232,  93,
                30, 242, 203,  42, 116, 197,  94,  53,
                210, 149,  71, 158, 150,  45, 154, 136,
                76, 125, 132,  63, 219, 172,  49, 182,
                72,  95, 246, 196, 216,  57, 139, 231,
                35,  59,  56, 142, 200, 193, 223,  37,
                177,  32, 165,  70,  96,  78, 156, 251,
                170, 211,  86,  81,  69, 124,  85,   0,
                7, 201,  43, 157, 133, 155,   9, 160,
                143, 173, 179,  15,  99, 171, 137,  75,
                215, 167,  21,  90, 113, 102,  66, 191,
                38,  74, 107, 152, 250, 234, 119,  83,
                178, 112,   5,  44, 253,  89,  58, 134,
                126, 206,   6, 235, 130, 120,  87, 199,
                141,  67, 175, 180,  28, 212,  91, 205,
                226, 233,  39,  79, 195,   8, 114, 128,
                207, 176, 239, 245,  40, 109, 190,  48,
                77,  52, 146, 213,  14,  60,  34,  50,
                229, 228, 249, 159, 194, 209,  10, 129,
                18, 225, 238, 145, 131, 118, 227, 151,
                230,  97, 138,  23, 121, 164, 183, 220,
                144, 122,  92, 140,   2, 166, 202, 105,
                222,  80,  26,  17, 147, 185,  82, 135,
                88, 252, 237,  29,  55,  73,  27, 106,
                224,  41,  51, 153, 189, 108, 217, 148,
                243,  64,  84, 111, 240,198, 115, 184,
                214,  62, 101,  24,  68,  31, 221, 103,
                16, 241,  12,  25, 236, 174,   3, 161,
                20, 123, 169,  11, 255, 248, 163, 192,
                162,   1, 247,  46, 188,  36, 104, 117,
                13, 254, 186,  47, 181, 208, 218,  61,
                20,  83,  15,  86, 179, 200, 122, 156,
                235, 101,  72,  23,  22,  21, 159,   2,
                204,  84, 124, 131,   0,  13,  12,  11,
                162,  98, 168, 118, 219, 217, 237, 199,
                197, 164, 220, 172, 133, 116, 214, 208,
                167, 155, 174, 154, 150, 113, 102, 195,
                99, 153, 184, 221, 115, 146, 142, 132,
                125, 165,  94, 209,  93, 147, 177,  87,
                81,  80, 128, 137,  82, 148,  79,  78,
                10, 107, 188, 141, 127, 110,  71,  70,
                65,  64,  68,   1,  17, 203,   3,  63,
                247, 244, 225, 169, 143,  60,  58, 249,
                251, 240,  25,  48, 130,   9,  46, 201,
                157, 160, 134,  73, 238, 111,  77, 109,
                196,  45, 129,  52,  37, 135,  27, 136,
                170, 252,   6, 161,  18,  56, 253,  76,
                66, 114, 100,  19,  55,  36, 106, 117,
                119,  67, 255, 230, 180,  75,  54,  92,
                228, 216,  53,  61,  69, 185,  44, 236,
                183,  49,  43,  41,   7, 104, 163,  14,
                105, 123,  24, 158,  33,  57, 190,  40,
                26,  91, 120, 245,  35, 202,  42, 176,
                175,  62, 254,   4, 140, 231, 229, 152,
                50, 149, 211, 246,  74, 232, 166, 234,
                233, 243, 213,  47, 112,  32, 242,  31,
                5, 103, 173,  85,  16, 206, 205, 227,
                39,  59, 218, 186, 215, 194,  38, 212,
                145,  29, 210,  28,  34,  51, 248, 250,
                241,  90, 239, 207, 144,182, 139, 181,
                189, 192, 191,   8, 151,  30, 108, 226,
                97, 224, 198, 193,  89, 171, 187,  88,
                222,  95, 223,  96, 121, 126, 178, 138,
                71, 241, 180, 230,  11, 106, 114,  72,
                133,  78, 158, 235, 226, 248, 148,  83,
                224, 187, 160,  2, 232,  90,   9, 171,
                219, 227, 186, 198, 124, 195,  16, 221,
                57,   5, 150,  48, 245,  55,  96, 130,
                140, 201,  19,  74, 107,  29, 243, 251,
                143,  38, 151, 202, 145,  23,   1, 196,
                50,  45, 110,  49, 149, 255, 217,  35,
                209,   0,  94, 121, 220,  68,  59,  26,
                40, 197,  97,  87,  32, 144,  61, 131,
                185,  67, 190, 103, 210,  70,  66, 118,
                192, 109,  91, 126, 178,  15,  22,  41,
                60, 169,   3,  84,  13, 218,  93, 223,
                246, 183, 199,  98, 205, 141,   6, 211,
                105,  92, 134, 214,  20, 247, 165, 102,
                117, 172, 177, 233,  69,  33, 112,  12,
                135, 159, 116, 164,  34,  76, 111, 191,
                31,  86, 170,  46, 179, 120,  51,  80,
                176, 163, 146, 188, 207,  25,  28, 167,
                99, 203,  30,  77,  62,  75,  27, 155,
                79, 231, 240, 238, 173,  58, 181,  89,
                4, 234,  64,  85,  37,  81, 229, 122,
                137,  56, 104,  82, 123, 252,  39, 174,
                215, 189, 250,   7, 244, 204, 142,  95,
                239,  53, 156, 132,  43,  21, 213, 119,
                52,  73, 182,  18,  10, 127, 113, 136,
                253, 157,  24,  65, 125, 147, 216,  88,
                44, 206, 254,  36, 175, 222, 184,  54,
                200, 161, 128, 166, 153, 152, 168,  47,
                14, 129, 101, 115, 228, 194, 162, 138,
                212, 225,  17, 208,   8, 139,  42, 242,
                237, 154, 100,  63, 193, 108, 249, 236]

# The PST encoding types folow
class NDBType(enum.Enum):
  NDBCryptNone       = 0x00
  NDBCryptPermute    = 0x01
  NDBCryptCyclic     = 0x02
  NDBCryptEdpcrypted = 0x10

# The known node ID types follow
class NIDType(enum.Enum):
  NIDTypeHid                   = 0x00
  NIDTypeInternal              = 0x01
  NIDTypeNormalFolder          = 0x02
  NIDTypeSearchFolder          = 0x03
  NIDTypeNormalMessage         = 0x04
  NIDTypeAttachment            = 0x05
  NIDTypeSearchUpdateQueue     = 0x06
  NIDTypeSearchCriteriaObject  = 0x07
  NIDTypeAssocMessage          = 0x08
  NIDTypeContentsTableIndex    = 0x0a   
  NIDTypeRecieveFolderTable    = 0x0b
  NIDTypeOutgoingQueueTable    = 0x0c
  NIDTypeHierarchyTable        = 0x0d
  NIDTypeContentsTable         = 0x0e
  NIDTypeAssocContentsTable    = 0x0f
  NIDTypeSearchContentsTable   = 0x10
  NIDTypeAtttachmentTable      = 0x11
  NIDTypeRecipientTable        = 0x12
  NIDTypeSearchTableIndex      = 0x13
  NIDTypeLtp                   = 0x1f
  NIDMessageStore              = 0x0021
  NIDNameToIdMap               = 0x0061

# The known page types follow
class PType(enum.Enum):
  PTypeNone       = 0x00
  PTypeBBt        = 0x80
  PTypeNbt        = 0x81
  PTypeFMap       = 0x82
  PTypePMap       = 0x83
  PTypeAMap       = 0x84
  PTypeFPMap      = 0x85
  PTypeDL         = 0x86

# Each instance of this class has all of the information from one
# PST allocation map page
class AMapPage(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.rgbAMapBits = pageBytes[0:496]
    trailerBytes = pageBytes[496:512]
    self.pageTrailer = PageTrailer(trailerBytes)

# Each instance of this class has all of the information about
# one leaf BBT entry
class BBTPageEntry(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.BREF = PSTBref(pageBytes[0:16])
    self.cb = getShort(pageBytes[16:18], 0)
    self.cRef = getShort(pageBytes[18:20], 0)
    self.dwPadding = pageBytes[20:24]

# Each instance of this class has all of the information from one
# PST block trailer structure
class BlockTrailer(object):
  # The __init__ method creates an instance of the class
  def __init__(self, blockBytes):
    self.cb = getShort(blockBytes[0:2], 0)
    self.wSig = blockBytes[2:4]
    self.dwCRC = blockBytes[4:8]
    self.bid = PSTBid(blockBytes[8:16])

# Each instance of this class has all of the information about
# one B-Tree page
class BTPage(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.btkey = pageBytes[0:8]
    self.BREF = PSTBref(pageBytes[8:24])

# Each instance of this class has all of the information about
# one B-Tree page entry
class BTPageEntry(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.rgentries = pageBytes[0:488]
    self.cEnt = getByte(pageBytes[488:489], 0)
    self.cEntMax = getByte(pageBytes[489:490], 0)
    self.cbEnt = getByte(pageBytes[490:491], 0)
    self.cLevel = getByte(pageBytes[491:492], 0)
    self.dwPadding = pageBytes[492:496]
    trailerBytes = pageBytes[496:512]
    self.pageTrailer = PageTrailer(trailerBytes)

# Each instance of this class has all of the information about the
# one and only DList page
class DListPage(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.bFlags = pageBytes[0:1]
    self.cEntDList = getByte(pageBytes[1:2], 0)
    self.wPadding = pageBytes[2:4]
    self.usCurrentPage = getInt(pageBytes[4:8], 0)
    # Build all of the DList page entries
    self.rgDlistPageEnt = []
    offset = 8 - 4
    for i in range(119):
      offset += 4
      ba = pageBytes[offset:offset+4]    
      dListPageEntry = DListPageEntry(ba)
      self.rgDlistPageEnt.append(dListPageEntry)
    self.rgPadding = pageBytes[484:496]
    trailerBytes = pageBytes[496:512] 
    self.pageTrailer = PageTrailer(trailerBytes)

# Each instance of this class has all of the information about one
# DList page entry
class DListPageEntry(object):
  # The __init__ method creates an instance of the class
  def __init__(self, entryBytes):
    dValue = getUInt(entryBytes, 0)
    self.dwPageNum = dValue % 1048576
    self.dwFreeSlots = dValue >> 20

# Each instance of this class has all of the information from one
# PST free map page
class FMapPage(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.rgbFMapBits = pageBytes[0:496]
    trailerBytes = pageBytes[496:512]
    self.pageTrailer = PageTrailer(trailerBytes)

# Each instance of this class has all of the information from one
# PST free page map page
class FPMapPage(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.rgbFPMapBits = pageBytes[0:496]
    trailerBytes = pageBytes[496:512]
    self.pageTrailer = PageTrailer(trailerBytes)

# Each instance of this class has all of the information about
# one NBT entry (leaf NBT Entry)
class NBTEntry(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.nid = pageBytes[0:8]
    self.bidData = PSTBid(pageBytes[8:16])
    self.bidSub = PSTBid(pageBytes[16:24])
    self.nidParent = pageBytes[24:28]
    self.dwPadding = pageBytes[28:32]

# Each instance of this class has all of the information from one
# PST page trailer structure
class PageTrailer(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    pValue = getUByte(pageBytes[0:1], 0) 
    if pValue < 128 or pValue > 134:
      self.ptype = PType.PTypeNone
    else:
      self.ptype = PType(pValue)
    self.ptypeRepeat = getUByte(pageBytes[1:2], 0)
    self.wSig = pageBytes[2:4]
    self.dwCRC = pageBytes[4:8]
    self.bid = PSTBid(pageBytes[8:16])

# Each instance of this class has all of the information from one
# PST page map page
class PMapPage(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pageBytes):
    self.rgbPMapBits = pageBytes[0:496]
    trailerBytes = pageBytes[496:512]
    self.pageTrailer = PageTrailer(trailerBytes)

# Each instance of this class has all of the information from one
# PST BID (Block ID)
class PSTBid(object):
  # The __init__ method creates an instance of the class
  def __init__(self, bidBytes):
    biValue = getLong(bidBytes, 0)
    self.A = ((biValue % 2) > 0)
    self.B = ((biValue % 4) >= 2)
    biValue = biValue >> 2
    self.bidIndex = biValue

# Each instance of this class has all of the information from one
# PST BREF
class PSTBref(object):
  # The __init__ method creates an instance of the class
  def __init__(self, brefBytes):
    self.bid = PSTBid(brefBytes[0:8])
    self.ib = getLong(brefBytes[8:16], 0)

# Each instance of this class has all of the information from one
# PST header
class PSTHeader(object):
  # The __init__ method creates an instance of the class
  def __init__(self, pstBytes):
    self.dwMagic = pstBytes[0:4]
    self.dwCRCPartial = pstBytes[4:8]
    self.dwMagicClient = pstBytes[8:10]
    self.wVer = getShort(pstBytes[10:12], 0)
    self.wVerClient = getShort(pstBytes[12:14], 0)
    self.bPlatformCreate = getByte(pstBytes[14:15], 0)
    self.bPlatformAccess = getByte(pstBytes[15:16], 0)
    self.dwReserved1 = pstBytes[16:20]
    self.dwReserved2 = pstBytes[20:24]
    self.bidUnused = pstBytes[24:32]
    self.bidNextP = PSTBid(pstBytes[32:40])
    self.dwUnique = pstBytes[40:44]
    self.rgnid = pstBytes[44:172]
    self.qwUnused = pstBytes[172:180]
    rootBytes = pstBytes[180:252]
    self.root = PSTRoot(rootBytes)
    self.dwAlign = pstBytes[252:256]
    self.rgbFM = pstBytes[256:384]
    self.rgbFP = pstBytes[384:512]
    self.bSentinel = getByte(pstBytes[512:513], 0)
    byteValue = getByte(pstBytes[513:514], 0)
    self.bCryptMethod = NDBType(byteValue)
    self.rgbReserved = pstBytes[514:516]
    self.bidNextB = PSTBid(pstBytes[516:524])
    self.dwCRCFull = pstBytes[524:528]
    self.rgbReserved2 = pstBytes[528:531]
    self.bReserved2 = pstBytes[531:532]
    self.rgbReserved3 = pstBytes[532:564]
  # Get the root structure from an instance of this class 
  def getRoot(self):
    return self.root

# Each instance of this class has all of the information from one
# PST root structure
class PSTRoot(object):
  # The __init__ method creates an instance of the class
  def __init__(self, rootBytes):
    self.dwReserved = rootBytes[0:4]
    self.ibFileEof = getLong(rootBytes[4:12], 0)
    self.ibAMapLast = rootBytes[12:20]
    self.cbAMapFree = rootBytes[20:28]
    self.cbPMapFree = rootBytes[28:36]
    self.BREFNBT = PSTBref(rootBytes[36:52])
    self.BREFBBT = PSTBref(rootBytes[52:68])
    self.fAMapValid = getByte(rootBytes[68:69], 0)
    self.bReserved = rootBytes[69:70]

# Check an AMap page
def checkAMapPage(inFile, outFile, aMapPage, aMapNumber):
  # Make sure we were really passed an AMap page
  aMapPType = aMapPage.pageTrailer.ptype
  assert aMapPType == PType.PTypeAMap
  assert aMapNumber >= 0
  aMapBytes = aMapPage.rgbAMapBits
  aMapPageOffset = getAMapPageOffset(aMapNumber)
  offset = aMapPageOffset
  aMapLen = len(aMapBytes) 
  for i in range(aMapLen):
    offset += 512
    aMapByte = aMapBytes[i]
    if aMapByte == 255:
      continue
    page = readPageByOffset(inFile, offset)
    page = cryptPermute(page, False)
    pageStr = convertUtf16Le(page)
    outFile.write(pageStr)    
  return

# Check a specific FMap
def checkFMap(inFile, outFile, startCounter, byteArrayFMap, fileSize):
  byteArrayLen = len(byteArrayFMap)
  startCounter -= 1
  for i in range(byteArrayLen):
    startCounter += 1
    fMapByte = byteArrayFMap[i]
    aMapPageOffset = getAMapPageOffset(startCounter)
    if (aMapPageOffset+glbPageSize) > fileSize:
      break
    aMapPage = getAMapPage(inFile, startCounter)
    aMapPType = aMapPage.pageTrailer.ptype
    assert aMapPType == PType.PTypeAMap
    checkAMapPage(inFile, outFile, aMapPage, startCounter)  
  return

# Check the free space identified using FMaps
def checkFMaps(inFile, outFile, header, fileSize):
  # Handle the initial FMap. The initial FMap is in the 
  # PST file header. The initial FMap only has 128 entries.
  aMapCounter = 0
  initialFMap = header.rgbFM
  initialLen = len(initialFMap) 
  assert initialLen == 128
  # Handle the initial FMap
  checkFMap(inFile, outFile, aMapCounter, initialFMap, fileSize)
  aMapCounter += len(initialFMap)  
  # Handle all of the other FMaps 
  for i  in range(1, 151):
    print(i, aMapCounter)
    # Get an FMap page
    fMapPage = getFMapPage(inFile, i)
    fMapPType = fMapPage.pageTrailer.ptype
    assert fMapPType == PType.PTypeFMap
    fMapLen = len(fMapPage.rgbFMapBits) 
    assert fMapLen == 496
    checkFMap(inFile, outFile, aMapCounter, fMapPage.rgbFMapBits, fileSize)
    aMapCounter += len(fMapPage.rgbFMapBits)  
  return

# Check a specific FPMap 
def checkFPMap(inFile, outFile, startCounter, byteArrayFPMap, fileSize):
  byteArrayLen = len(byteArrayFPMap)
  startCounter -= 1
  for i in range(byteArrayLen):
    print('checkFPMap', i, startCounter)
    fPMapByte = byteArrayFPMap[i]
    # At this point we need to check every bit in the FP Map byte
    for j in range(0, 8):
      startCounter += 1
      fPMapBitFlag = ((fPMapByte >> j) % 2) != 0
      if fPMapBitFlag == False:
        continue
      pMapPageOffset = getPMapPageOffset(startCounter)
      if (pMapPageOffset+glbPageSize) > fileSize:
        break
      pMapPage = getPMapPage(inFile, startCounter)
      pMapPType = pMapPage.pageTrailer.ptype
      assert pMapPType == PType.PTypePMap
      checkPMapPage(inFile, outFile, pMapPage, startCounter)  
  return

# Check the free space identified using FPMaps
def checkFPMaps(inFile, outFile, header, fileSize):
  # Handle the initial FPMap. The initial FPMap is in the 
  # PST file header. The initial FPMap only has 128 entries.
  pMapCounter = 0
  initialFPMap = header.rgbFP
  initialLen = len(initialFPMap) 
  assert initialLen == 128
  # Handle the initial FPMap from the PST header
  checkFPMap(inFile, outFile, pMapCounter, initialFPMap, fileSize)
  pMapCounter += (8 * initialLen)  
  # Handle all of the other FPMaps 
  for i  in range(1, 4):
    print('checkFPMaps', i, pMapCounter)
    # Get an FPMap page
    fPMapPage = getFPMapPage(inFile, i)
    fPMapPType = fPMapPage.pageTrailer.ptype
    assert fPMapPType == PType.PTypeFPMap
    fPMapBytes = fPMapPage.rgbFPMapBits
    fPMapLen = len(fPMapBytes)
    assert fPMapLen == 496
    checkFPMap(inFile, outFile, pMapCounter, fPMapBytes, fileSize)
    pMapCounter += (8 * fPMapLen)  
  return

# Check a PMap page
def checkPMapPage(inFile, outFile, pMapPage, pMapNumber):
  assert pMapNumber >= 0
  # Make sure we were really passed an PMap page
  pMapPType = pMapPage.pageTrailer.ptype
  assert pMapPType == PType.PTypePMap
  # Get the array of bytes from the PMap
  pMapBytes = pMapPage.rgbPMapBits
  # Get the offset of the current PMap page
  pMapPageOffset = getPMapPageOffset(pMapNumber)
  offset = pMapPageOffset
  pMapLen = len(pMapBytes) 
  for i in range(pMapLen):
    pMapByte = pMapBytes[i]
    # At this point we need to check every bit in the FP Map byte
    for j in range(0, 8):
      offset += 512
      pMapBitFlag = ((pMapByte >> j) % 2) != 0
      if pMapBitFlag == False:
        continue 
      page = readPageByOffset(inFile, offset)
      page = cryptPermute(page, False)
      pageStr = convertUtf16Le(page)
      outFile.write(pageStr)    
  return

# Convert a UTF-16-LE byte array to a string
def convertUtf16Le(byteArray):
  outStr = byteArray.decode('utf-16-le', 'replace')
  return outStr

# This method handles encoding and decoding of data
def cryptPermute(inByteArray, fEncrypt):
  inByteArraySize = len(inByteArray)
  # Get a few sections of the encoding/decoding table
  mpbbR = glbMpbbCrypt
  mpbbS = glbMpbbCrypt[256:]
  mpbbI = glbMpbbCrypt[512:]
  # Get a few values for use later
  outByteArray = bytearray()
  pbTable = mpbbR if (fEncrypt) else mpbbI
  # Process all of the bytes in the input byte array
  for inByte in inByteArray:
    outByteArray.append(pbTable[inByte])
  return outByteArray

# Display a set of bytes in hexadecimal 
def displayHex(byteArray):
  print(binascii.hexlify(byteArray))

# Get an AMap (Allocation Map) page by AMap page number
def getAMapPage(file, pageNumber):
  assert pageNumber >= 0
  offset = getAMapPageOffset(pageNumber)
  page = readPageByOffset(file, offset)
  aMapPage = AMapPage(page)
  aMapPType = aMapPage.pageTrailer.ptype
  assert aMapPType == PType.PTypeAMap
  return aMapPage

# Get the offset of an AMap (Allocation Map) page by AMap page number
def getAMapPageOffset(pageNumber):
  assert pageNumber >= 0
  offset = 0x4400
  offset += pageNumber * 253952
  return offset

# Get a byte value (one signed byte) from a buffer
def getByte(byteArray, offset):
  assert offset >= 0
  byteInt = struct.unpack_from('<b', byteArray, offset)
  byteInt = byteInt[0]
  return byteInt

# Get the Density List (DList) for the current PST
def getDList(file):
  offset = 0x4200
  page = readPageByOffset(file, offset)
  dListPage = DListPage(page)
  dListPType = dListPage.pageTrailer.ptype
  assert dListPType == PType.PTypeDL
  return dListPage

# Get the size of a file from the operating system
def getFileSize(fileName):
  fileSize = os.path.getsize(fileName)
  return fileSize

# Get an FMap (Free Map) page by FMap page number
def getFMapPage(file, pageNumber):
  assert pageNumber >= 1
  offset = getFMapPageOffset(pageNumber) 
  page = readPageByOffset(file, offset)
  fMapPage = FMapPage(page)
  fMapPType = fMapPage.pageTrailer.ptype
  assert fMapPType == PType.PTypeFMap
  return fMapPage

# Get the offset of an FMap (Free Map) page by FMap page number
def getFMapPageOffset(pageNumber):
  assert pageNumber >= 1
  # Check the Free Map page number passed by the caller
  if pageNumber == 1:
    pageNumber = 128
  else:
    pageNumber = 128 + (496 * (pageNumber-1))
  offset = 0x4400
  offset += pageNumber * 253952
  offset += 1024
  return offset

# Get an FPMap (Free Page Map) page by FPMap page number
def getFPMapPage(file, pageNumber):
  assert pageNumber >= 1
  offset = getFPMapPageOffset(pageNumber) 
  page = readPageByOffset(file, offset)
  fPMapPage = FPMapPage(page)
  fPMapPType = fPMapPage.pageTrailer.ptype
  assert fPMapPType == PType.PTypeFPMap
  return fPMapPage

# Get the offset of an FPMap (Free Page Map) page by FPMap page number
def getFPMapPageOffset(pageNumber):
  assert pageNumber >= 1
  # Check the Free Page Map page number passed by the caller
  if pageNumber == 1:
    pageNumber = 128*8 
  else:
    pageNumber = 128*8 + 8*(496 * (pageNumber-1))
  offset = 0x4600
  offset += pageNumber * 2031616
  offset += 512
  return offset

# Get the header for the current PST
def getHeader(file):
  fBytes = readFileAtOffset(file, 0, 768)
  pstHeader = PSTHeader(fBytes) 
  return pstHeader

# Get an integer value (four signed bytes) from a buffer
def getInt(byteArray, offset):
  assert offset >= 0
  standardInt = struct.unpack_from('<i', byteArray, offset)
  standardInt = standardInt[0]
  return standardInt

# Get a long value (eight signed bytes) from a buffer
def getLong(byteArray, offset):
  assert offset >= 0
  longInt = struct.unpack_from('<q', byteArray, offset)
  longInt = longInt[0]
  return longInt

# Get an PMap (Page Map) page by PMap page number
def getPMapPage(file, pageNumber):
  offset = getPMapPageOffset(pageNumber)
  page = readPageByOffset(file, offset)
  pMapPage = PMapPage(page)
  pMapPType = pMapPage.pageTrailer.ptype
  assert pMapPType == PType.PTypePMap
  return pMapPage

# Get the offset of an PMap (Page Map) page by PMap page number
def getPMapPageOffset(pageNumber):
  assert pageNumber >= 0
  offset = 0x4600
  offset += pageNumber * 2031616
  return offset

# Get a short value (two signed bytes) from a buffer
def getShort(byteArray, offset):
  assert offset >= 0
  shortInt = struct.unpack_from('<h', byteArray, offset)
  shortInt = shortInt[0]
  return shortInt

# Get an unsigned byte value (one usigned byte) from a buffer
def getUByte(byteArray, offset):
  assert offset >= 0
  byteInt = struct.unpack_from('<B', byteArray, offset)
  byteInt = byteInt[0]
  return byteInt

# Get an unsigned integer value (four unsigned bytes) from a buffer
def getUInt(byteArray, offset):
  assert offset >= 0
  standardInt = struct.unpack_from('<I', byteArray, offset)
  standardInt = standardInt[0]
  return standardInt

# Open a file for binary processing 
def openFile(fileName, fileMode='rb'):
  f = open(fileName, fileMode)
  return f

# Process all of the pages in the input PST file
def processAllPages(inFile, outFile, fileSize):
  offset = 0
  offset -= glbPageSize
  while offset < fileSize:
    offset += glbPageSize
    if (offset % 1048576) == 0:
      print('processAllPages', offset)
    page = readPageByOffset(inFile, offset)
    page = cryptPermute(page, False)
    pageStr = convertUtf16Le(page)
    outFile.write(pageStr)
  return

# Read a set of bytes at a specific offset
def readFileAtOffset(file, offset, length): 
  assert offset >= 0
  assert length >= 0
  file.seek(offset, 0)
  bytes = file.read(length) 
  return bytes

# Read a specific page by BREF
def readPageByBref(file, bref):
  length = glbPageSize
  offset = bref.ib
  assert offset >= 0
  file.seek(offset, 0)
  bytes = file.read(length) 
  return bytes

# Read a specific page by number
def readPageByNumber(file, pageNumber):
  assert pageNumber >= 0
  length = glbPageSize
  offset = pageNumber << 9
  file.seek(offset, 0)
  bytes = file.read(length) 
  return bytes

# Read a specific page by offset from the start of the file
def readPageByOffset(file, offset):
  assert offset >= 0
  assert (offset % 512) == 0
  length = glbPageSize
  file.seek(offset, 0)
  bytes = file.read(length) 
  return bytes

# Read a PMap page by offset
def readPMapOffset(file, pageOffset):
  assert pageOffset >= 0
  assert (pageOffset % 512) == 0
  length = glbPageSize
  file.seek(pageOffset, 0)
  page = file.read(length)   
  pMapPage = PMapPage(page)
  pMapPType = pMapPage.pageTrailer.ptype
  assert pMapPType == PType.PTypePMap
  return pMapPage

# Read a PMap page by page number
def readPMapPage(file, pageNumber):
  assert pageNumber >= 0
  length = glbPageSize
  offset = pageNumber << 9
  file.seek(offset, 0)
  page = file.read(length)   
  pMapPage = PMapPage(page)
  pMapPType = pMapPage.pageTrailer.ptype
  assert pMapPType == PType.PTypePMap
  return pMapPage

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)  
  # Open the input PST file
  pstInFile = openFile(glbInFileName)
  # Open the output file
  outFile = open(glbOutFileName, 'w', encoding='utf-8')
  dList = getDList(pstInFile)
  pstHeader = getHeader(pstInFile)
  fileSize = getFileSize(glbInFileName)
  # checkFMaps(pstInFile, outFile, pstHeader, fileSize)
  # checkFPMaps(pstInFile, outFile, pstHeader, fileSize)
  processAllPages(pstInFile, outFile, fileSize)
  brefNbt = pstHeader.root.BREFNBT
  brefBbt = pstHeader.root.BREFBBT
  nbtPage = readPageByBref(pstInFile, brefNbt)
  bbtPage = readPageByBref(pstInFile, brefBbt) 
  # Read a few pages
  for i in range(1, 4):
    break
    fPMapPage = getFPMapPage(pstInFile, i)
    pTypeValue = fPMapPage.pageTrailer.ptype
    if pTypeValue != PType.PTypeFPMap:
      continue
    print(i, pTypeValue)
  # Read a few pages
  for i in range(1, 140):
    break
    fMapPage = getFMapPage(pstInFile, i)
    pTypeValue = fMapPage.pageTrailer.ptype
    if pTypeValue != PType.PTypeFMap:
      continue
    print(i, pTypeValue)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__":
  main()