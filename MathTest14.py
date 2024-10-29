# Get the xor value of all of the numbers starting from zero
def f(a):
  res = [a, 1, a+1, 0]
  return res[a % 4]

# Get the xor value of all numbers in a range
def getXor(a, b):
  return f(b) ^ f(a-1)

# Answer for Google
def answer(s, l):
  rv = 0
  totalLen = int(l * l)
  for pos in range(s, s+totalLen, l):
    rv = rv ^ getXor(pos, pos+l-1)
    l -= 1
  return rv
    
# Main program
def main():   
  rv = answer(17, 4)
  print(rv)

# Actual starting point
if __name__ == "__main__":
  main()   