import os
import random 

glbDebug = True

# Look for how long it took for all seeds to bloom
def bloomTime():
  count = 6
  seeds = ['F' for x in range(count)]
  days = 0
  # Process days until we have no seeds left
  while True:
    days += 1    
    flipSeeds(seeds)
    treeCount = countTrees(seeds)
    if days == 3:
      return treeCount

# Count the number of seeds that have bloomed into trees
def countTrees(seeds):
  count = 0
  for seed in seeds:
    if seed == 'T':
      count += 1
  return count  

# Simulate flipping a coin. Return a single F for
# false and a T for true.
def flipCoin():
  rv = random.randrange(0, 2)
  return 'FT'[rv:rv+1]

# Flip half of the remaining seeds to trees
def flipSeeds(seeds):
  for i, seed in enumerate(seeds):
    if seed == 'T':
      continue
    newSeed = flipCoin()
    if newSeed == 'F':
      continue
    seeds[i] = newSeed

# Run a few tests
def runTests(test, count):
  total = 0.0 
  for i in range(0, count): 
    tv = test()
    total += tv
  return total / count

# Handle startup
def startup():
  return
    
# Main program
def main():   
  for i in range(0, 5000, 33):
    print(i % 15)
   

  #startup() 
  #result = runTests(bloomTime, 10000)
  #print(result)

# Actual starting point
if __name__ == "__main__":
  main()
   