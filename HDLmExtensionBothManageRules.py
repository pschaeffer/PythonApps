# Class for providing a set of functions. No instances of this
# class are ever created.

class HDLmExtensionBothManageRules(object):
  contentEventTarget = dict()
  # Set the current value of the rules updated flag 
  @classmethod
  def rulesUpdatedSet(cls, newValue):
    HDLmExtensionBothManageRules.contentEventTarget['rulesUpdated'] = newValue;