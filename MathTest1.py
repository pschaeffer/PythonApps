import math
import os
import random 

glbDebug = True

# Run a few tests
def runTests():
  for x in range(0,50):
    for y in range(0,50):
      z = math.sqrt(18*x + 18*y + 1)
      zint = int(z)
      if zint == z:
        z1 = 17*x + y - x**2 
        z2 = x + 17*y - y**2
        print('trial', x, y, z, zint, z1, z2)
  return  

# Handle startup
def startup():
  return
    
# Main program
def main():   
  startup() 
  x = 16.94427
  y = -0.94427
  res = math.sqrt(x**2 + y**2 + 1)
  print(res)
  print(x**2 - 17*x)
  # result = runTests()

# Actual starting point
if __name__ == "__main__":
  main()
   