from   gmpy2 import mpz,mpq,mpfr,mpc
import datetime
import gmpy2
import math
import time    
    
# Main program 
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  printTimeStart = datetime.datetime.now()
  # Test code
  a = math.sqrt(2.0) 
  b = 1.0 / math.sqrt(2.0)
  c = 1.0 - b 
  print(a, b, c)
  x = (b**2+a*c+c**2) / (2*b)
  y = a/2.0
  print(x, y)
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