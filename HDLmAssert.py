# The HDLmAssert function (which is not a class) is used to provide a 
# simple assert mechanism  
#
def HDLmAssert(test, errorText):
  if test:
    return
  raise SystemError(errorText)