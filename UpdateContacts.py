import pywintypes 
import win32com.client

glbExcept = 'Except'
glbNone = 'None'
glbZeroLength = 'Zero-Length'

# Display the contents of a contact
def displayContact(contact, i):
  contactFirst = getContactValue(contact, 'FirstName')
  contactLast = getContactValue(contact, 'LastName')
  contactFull = getContactValue(contact, 'FullName') 
  contactFileAs = getContactValue(contact, 'FileAs')  
  print(i, contactFileAs, contactFull, contactFirst, contactLast)
  print('Full name', contactFull, 'File as', contactFileAs)
  print(len(contactFileAs), len(contactFull))

# Get a value from a contact
def getContactValue(contact, valueName):
  try:
    rv = eval('contact.' + valueName)
  except:
    rv = glbExcept
  if len(rv) == 0:
    rv = glbZeroLength
  return rv

# This is the main program
# Main program
def main():    
  o = win32com.client.Dispatch("Outlook.Application")
  ns = o.GetNamespace("MAPI")  
  mainPst = ns.Folders.Item('Outlook Data file') 
  contacts = mainPst.Folders.Item("Contacts")
  contactsItems = contacts.Items
  contactsLen = len(contactsItems)
  for i in range(1, contactsLen):   
    # Get the current contact
    contact = contacts.Items[i]   
    # Get some information about the current contact
    contactFull = getContactValue(contact, 'FullName') 
    contactFileAs = getContactValue(contact, 'FileAs') 
    # Skip the current contact in a few cases
    if contactFull == glbExcept or contactFull == glbNone: 
      displayContact(contact, i)
      continue
    if contactFileAs == glbExcept or contactFileAs == glbNone: 
      displayContact(contact, i)
      continue
    if len(contactFileAs) > len(contactFull):
      displayContact(contact, i)
      continue
    if contactFileAs.startswith('pschaeffer'):
      displayContact(contact, i)
      continue     
    # Reset the file as value
    print('Full name', contactFull, 'File as', contactFileAs)
    contact.FileAs = contactFull
    contact.Save()
  # Edit: I don't always do these last steps.
  ns = None 
  o = None

if __name__ == "__main__":
  main()