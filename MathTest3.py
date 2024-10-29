import datetime
import time

glbDebug = True

# Find a number we are looking for 
def findNumber(): 
  # Create a set of nested loops to find the number
  for a in range(1, 10):
    for b in range(1, 10):
      for c in range(1, 10):
        for d in range(1, 10):
          for e in range(1, 10): 
            inVar = a*10000 + b*1000 + c*100 + d*10 + e
            outVar = inVar * a
            testVar = e*100000 + e*10000 + e*1000 + e*100 + e*10 + e
            if outVar == testVar:
              print(inVar, outVar, testVar)
  return

# Handle startup
def startup():
  return
    
# Main program
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Handle startup
  startup()
  # Test code
  if 1 == 1:
    findNumber()  
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
   