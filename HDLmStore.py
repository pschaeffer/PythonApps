# The HDLmStore class doesn't actually do anything. However, 
# it does provide a set of routines that are needed elsewhere.
# it does provide a set of routines that are needed elsewhere.

class HDLmStore(object):
  # This routine adds any missing fields to a store (stored value) object.
  # A store object in this case means a modification object being used to 
  # build a stored value. 
  @staticmethod
  def addMissingStoreObject(newStore):
    # Add any missing fields to the store (stored value) object
    # (actually a modification object) passed by the caller */
    if hasattr(newStore, 'comments') == False:
      newStore.comments = '' 
    if hasattr(newStore, 'value') == False:
      newStore.value = '' 