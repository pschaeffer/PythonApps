import datetime
import time

glbDebug = True

# Sum a set of numbers 
def sumNumbers(): 
  # Initialize a few variables
  sumTotal = 0.0;
  sumIndex = 1.0
  # Create a set of nested loops to add up a set of numbers
  for i in range(1, 911111):
    sumTotal += 1/sumIndex;  
    sumIndex += 1.0;
  print(sumTotal);
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
    sumNumbers()  
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