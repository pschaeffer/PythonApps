import copy
import datetime
import math
import time

# Build a deck of cards  
def buildDeckCards():
  suits = ['D', 'C', 'H', 'S']
  ranks = ['1','2','3','4','5','6','7','8','9','J','Q','K','A']
  outDeck = []
  for i in range(len(suits)):
    for j in range(len(ranks)):
      newCard = suits[i] + ranks[j]
      outDeck.append(newCard)
  return outDeck

# Build the initial vector of values 
def buildVectorValues(countsList, countsValues):
  outVec = []
  for i in range(len(countsList)):
    for j in range(countsList[i]):
      outVec.append(countsValues[i])
  return outVec

# This match function always returns true
def checkAlwaysTrue(inList):
  return True

# This match function check for the Ace of Spades 
def checkAceSpades(inList):
  newSum = sum(1 for item in inList if item == 'SA') 
  if newSum > 0:
    return True
  return False

# Generate all of the combination of values
def genCombosValues(inList):  
  matchCount = 0
  totalCount = 0
  for i in range(len(inList)):
    tempListA = inList.copy()
    itemA = tempListA[i]
    del tempListA[i]
    for j in range(len(tempListA)):
      tempListB = tempListA.copy()
      itemB = tempListB[j]
      del tempListB[j]
      for k in range(len(tempListB)):
        tempListC = tempListB.copy()
        itemC = tempListC[k]
        del tempListC[k] 
        newList = [itemA, itemB, itemC]
        newSum = sum(1 for item in newList if item == '75') 
        if (itemA != itemB and itemA != itemC and itemB != itemC): 
          print(i,itemA, j,itemB, k,itemC)
          matchCount += 1
        totalCount += 1
  return (matchCount, totalCount)

# Generate all of the permutations
def genPermutations(inList, selectCount, matchCheck):
  inListCount = len(inList)
  inLimit = []
  inIndex = []
  matchCount = 0
  totalCount = 0
  # Build the limit and index lists
  for i in range(selectCount):
    inLimit.append(inListCount-i)
    inIndex.append(0)
  # Generate all of the permutations
  while True:
    # Make a copy of the original list and extract each
    # of the samples
    tempList = inList.copy()
    matchList = []
    for i in range(selectCount):
      curIndex = inIndex[i]
      # Select a value from the remaining list and add it to
      # the current list
      matchList.append(tempList[curIndex])
      # Remove the value from the remaining list
      del tempList[curIndex]
    # Run the matching function against the current permutation. 
    # If a match is found, increment the match count. Always bump
    # the total count.
    checkValue = matchCheck(matchList)
    if checkValue:
      matchCount += 1
    totalCount += 1
    # Increment the left-most index value and carry right
    # as need be
    curIndex = 0
    while True:  
      curValue = inIndex[curIndex]
      curValue += 1
      curLimit = inLimit[curIndex]
      # Check if we have reached the limit for this index or not
      if curValue < curLimit:
        inIndex[curIndex] = curValue
        break
      # We must reset the current index and carry one to the right
      inIndex[curIndex] = 0
      curIndex += 1
      # Check to see if we are completely done. When the current
      # index goes past the number of indexes we are completely 
      # done.
      if curIndex >= selectCount:
        break
    # We are now done with the incrementing process. Of course, we 
    # may be completely done.
    if curIndex >= selectCount:
       break
  return (matchCount, totalCount)

# Main program 
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  printTimeStart = datetime.datetime.now()
  # Test code
  deckOfCards = buildDeckCards()
  (match, total) = genPermutations(deckOfCards, 4, checkAceSpades)
  print(match, total)
  if 1 == 2:
    countsList = [4,5,6] 
    countsValues = ['40','60','75']
    outVec = buildVectorValues(countsList, countsValues)
    (match, total) = genCombosValues(outVec)
    print(match, total)
  # Collect some ending time values  
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  printTimeEnd = datetime.datetime.now()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart) 
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()