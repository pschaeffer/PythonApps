import datetime
import math
import time

# Get each of the values
def getTotal(min, max):  
  remainingPie = 100.0
  for i in range(min, max+1):
    amount = i/100 * remainingPie
    remainingPie -= amount
    print(i, amount, remainingPie)
    
# Main program 
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  printTimeStart = datetime.datetime.now()
  # Test code
  getTotal(1, 20)
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