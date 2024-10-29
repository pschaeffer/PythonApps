from   gmpy2 import mpz,mpq,mpfr,mpc
import datetime
import gmpy2
import math
import time

# Integer Square Root 
def iSqrt(n):
  assert n >= 0
  if n == 0:
    return 0
  # i = floor((1 + floor(log_2(n))) / 2)
  i = n.bit_length() >> 1    
  # m = 2^i
  m = 1 << i    
  #
  # Fact: (2^(i + 1))^2 > n, so m has at least as many bits
  # as the floor of the square root of n.
  #
  # Proof: (2^(i+1))^2 = 2^(2i + 2) >= 2^(floor(log_2(n)) + 2)
  # >= 2^(ceil(log_2(n) + 1) >= 2^(log_2(n) + 1) > 2^(log_2(n)) = n. QED.
  #
  # (m << i) = m*(2^i) = m*m
  while (m << i) > n: 
    m >>= 1
    i -= 1
  d = n - (m << i) # d = n-m^2
  for k in range(i-1, -1, -1):
    j = 1 << k
    new_diff = d - (((m << 1) | j) << k) # n-(m+2^k)^2 = n-m^2-2*m*2^k-2^(2k)
    if new_diff >= 0:
      d = new_diff
      m |= j
  return m

# Get the total for two numbers
def getTwoTotal(min, max):
  twoPower = 1
  for power in range(min, max+1):
    if (power % 1000) == 0:
      print(power)
    twoPower = twoPower + twoPower
    twoPowerM615 = twoPower - 615
    if twoPowerM615 <= 0:
      continue 
    xVal = int(gmpy2.isqrt(twoPowerM615))
    if xVal * xVal == twoPowerM615:     
      print(power, twoPower, xVal)      
    
# Main program 
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  printTimeStart = datetime.datetime.now()
  # Test code
  if 1 == 2:
    rv = getTwoTotal(1, 4000000)
  gmpy2.get_context().precision=200
  a = mpz(6383088000457968550863626020707964592827)
  b = mpz(86901761472912010754925122912564100123)
  c = mpz(2743260400516683056616306684496286550899825)
  a = mpz(154476802108746166441951315019919837485664325669565431700026634898253202035277999)
  a = a + mpz(0)
  b = mpz(36875131794129999827197811565225474825492979968971970996283137471637224634055579)
  c = mpz(4373612677928697257861252602371390152816537558161613618621437993378423467772036)
  d = mpq(a, (b+c))
  e = mpq(b, (a+c))
  f = mpq(c, (a+b))
  print(d)
  print(e)
  print(f)
  print(d + e + f)
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