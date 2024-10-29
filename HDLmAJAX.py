# Class for providing a set of AJAX functions. No instances of this
# class are ever created. This code is not really used in the Python
# environment. 

from   HDLmAssert     import *
from   HDLmConfigInfo import *
from   HDLmEnums      import *
from   HDLmGlobals    import * 
from   HDLmUtility    import * 

class HDLmAJAX(object):
  @staticmethod
  def runNothing():
    pass