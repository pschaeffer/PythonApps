# The HDLmIgnore class doesn't actually do anything. However, 
# it does provide a set of routines that are needed elsewhere.

class HDLmIgnore(object):
  # This routine adds any missing fields to a ignore (ignore-list 
  # entry value) object. A ignore-list entry object in this case 
  # means a modification object being used to build an ignore-list 
  # entry value 
  @staticmethod
  def addMissingIgnoreObject(newIgnore):
    # Add any missing fields to the ignore-list entry object
    # (actually a modification object) passed by the caller 
    if hasattr(newIgnore, 'type') == True and \
       newIgnore.type == 'ignore':
      if hasattr(newIgnore, 'comments') == False: 
        newIgnore.comments = '' 
      if hasattr(newIgnore, 'createdFromVerificationCheck') == False:
        newIgnore.createdFromVerificationCheck = '' 
      if hasattr(newIgnore, 'scriptId') == False:  
        newIgnore.scriptId = '' 
      if hasattr(newIgnore, 'testCase') == False: 
        newIgnore.testCase = '' 
      if hasattr(newIgnore, 'stepNumber') == False: 
        newIgnore.stepNumber = '' 
      if hasattr(newIgnore, 'description') == False:  
        newIgnore.description = '' 
      if hasattr(newIgnore, 'language') == False: 
        newIgnore.language = '' 
      if hasattr(newIgnore, 'ticketPackage') == False:  
        newIgnore.ticketPackage = '' 
      if hasattr(newIgnore, 'testResults') == False:  
        newIgnore.testResults = '' 
      if hasattr(newIgnore, 'detailsOne') == False:  
        newIgnore.detailsOne = '' 
      if hasattr(newIgnore, 'detailsTwo') == False:  
        newIgnore.detailsTwo = '' 
      if hasattr(newIgnore, 'detailsThree') == False:  
        newIgnore.detailsThree = '' 