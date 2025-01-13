# The HDLmError class is not used to create any objects. However,
# it does contain the static methods used for error logging. See 
# the Java version of this routine for the standard error numbers. 

from   HDLmEmpty import * 
import jsons
import sys

class HDLmError(object):
  # This is the standard error function. The caller provides the severity,
  # type, number, and error message text. 
  @staticmethod
  def buildError(severity, type, number, text):
    errorStr = ''
    errorStr += 'HDLm' + ' '
    errorStr += severity + ' '
    errorStr += type + ' '
    errorStr += str(number) + ' '
    errorStr += text
    HDLmError.errorLog(errorStr)
    return errorStr
  # This is the lowest level error logging method. This method does the
  # actual logging of errors. 
  @staticmethod
  def errorLog(errorStr):
    print(errorStr, file=sys.stderr)
  # Build a (JSON) string from an error object. The error object may
  # be an actual error object or just a string containing an error
  # message. The code below handles both cases and returns a JSON
  # string to the caller. 
  #
  # This routine was originally in the HDLmUtility file. However, it 
  # was moved here to avoid Python circular import problems.
  @staticmethod
  def errorToString(errorObj):
    newObj = HDLmEmpty() 
    if str(type(errorObj)) == "<class 'str'>":
      newObj.name = ''
      newObj.message = errorObj
      newObj.reason = 'exception' 
    else:
      newObj.name = ''
      newObj.message = errorObj.args[0]
      newObj.reason = 'exception'
    return jsons.dumps(newObj) 
  # This routine is used to report an error. The caller provides the
  # the error information. This routine does the error reporting
  # using the information passed by the caller.  
  @staticmethod
  def reportError(errorObj, nameStr):
    errorStr = HDLmError.errorToString(errorObj)
    builtStr = nameStr + ' Error (' + errorStr + ')'
    HDLmError.errorLog(builtStr)
    return builtStr 