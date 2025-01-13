import os
import sys
import time

glbEventInterval = 0

# Run the main event loop
def mainEventLoop():
  for i in range(10000):
    updateInterval(800)
    print(glbEventInterval)  
    updateInterval(200)
    print(glbEventInterval) 

# Update the event interval using a new value
def updateInterval(newInterval):
  global glbEventInterval
  glbEventInterval = (glbEventInterval * 0.999) + (newInterval * 0.001) 

# Main program
def main(): 
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Run the main event interval update loop
  mainEventLoop()
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()