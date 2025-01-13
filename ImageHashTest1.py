# The links below may be helpful
#
#   https://www.phash.org/
#   https://pypi.org/project/ImageHash/
#   https://github.com/JohannesBuchner/imagehash/blob/master/imagehash.py#L263
#   https://github.com/aetilius/pHash
#   http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
#   https://tech.okcupid.com/evaluating-perceptual-image-hashes-okcupid/
#   https://arxiv.org/abs/1306.4079
#   https://content-blockchain.org/research/testing-different-image-hash-functions/
#   http://phash.org/docs/howto.html
#   http://phash.org/docs/design.html
#   http://phash.org/docs/pubs/thesis_zauner.pdf

from   PIL import Image
import imagehash
import time

glbImagePrefix = 'c:\\Users\\pscha\\HeadlampJetty\\TestImages\\'
glbFileNamet = ['sunset0768.jpg', 'sunset1170.jpg', 'EarthRise31.jpg', 'inkeffectocean.jpg', 'sunset1550.jpg', 'sunset3840.jpg']
glbFileNames = ['sunset0768.jpg', 'sunset1170.jpg', 'sunset1550.jpg', 'sunset3840.jpg']

# Add a prefix value to a set of file Names
def addPrefixValue(prefixValue, fileNames):
  outputNames = []
  for name in fileNames:
    fileName = prefixValue + name
    outputNames.append(fileName)
  return outputNames

# Build a list of image hash values. The caller provides
# the list of file names and specifies the image hashing
# function.
def buildHashList(imageNames, hashFunction):
  outputList = []
  for name in imageNames:
    evalStr = 'imagehash.' + hashFunction + '(Image.open(name))' 
    hashValue = eval(evalStr)
    outputList.append(hashValue)  
  return outputList

# Open an image and return the image to the caller
def openImage(imageName):   
  imageObj = Image.open(imageName)
  return imageObj

# Run and time a hash algorithm 
def runHash(imageNames, hashFunction):
  print('Algorithm name   ', hashFunction)
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9) 
  # Run the hash algorithm specified by the caller
  outputList = buildHashList(imageNames, hashFunction)
  for value in outputList:
    print(value)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('Algorithm CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Algorithm Elapsed', wallTimeEnd - wallTimeStart) 
  print()

# This is the main program
def main():   
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time_ns() / (10**9)
  wallTimeStart = time.time_ns() / (10**9)  
  # Build a python list of finished file names
  fileNames = addPrefixValue(glbImagePrefix, glbFileNames) 
  runHash(fileNames, "average_hash")
  runHash(fileNames, "phash")
  runHash(fileNames, "phash_simple")
  runHash(fileNames, "dhash")
  runHash(fileNames, "dhash_vertical")
  runHash(fileNames, "whash")
  runHash(fileNames, "colorhash")
  # Collect some ending time values 
  cpuTimeEnd = time.process_time_ns() / (10**9)
  wallTimeEnd = time.time_ns() / (10**9)
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

if __name__ == "__main__":
  main()