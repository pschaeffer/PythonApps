# Each instance of this class has all of the information about
# one token. Tokens are created when a string is tokenized. Each
# token object represents one (and only one) token. 
class Token(object):
  # The __init__ method creates an instance of the class
  def __init__(self, tokenType, tokenPos, tokenValue):
    # The token type is actually an enum value with only 
    # a small number of values
    self.tokType = tokenType
    # The token position is really an index and starts from
    # zero, not one
    self.pos = tokenPos
    self.value = tokenValue
  # Add a string passed by the caller to the token value. Return
  # the updated token value (always a string).
  def addString(self, addStr):
    self.value += addStr
    return self.value
  # Get the token position (really an index) and return it to the caller
  def getPos(self):
    return self.pos
  # Get the token type (really an enum) and return it to the caller
  def getType(self):
    return self.tokType
  # Get the token value (really a string) and return it to the caller
  def getValue(self):
    return self.value