# This program reads an input SMS XML file and finds all 
# of the unique phone numbers

from   HDLmAwsUtility import *
from   twilio.rest    import Client
import csv
import xml.etree.ElementTree as ET
import time

# The input CSV file is specified below. This file has all of 
# the contacts
glbConCsv = "C:\\Users\\pscha\\Documents\\Personal\\Contacts\\Gmail Contacts 2023-01-21 Outlook Format.csv"
# The input XML file is specified below. This file was obtained using SMS Backup & Restore.
glbSmsXml = "C:\\Users\\pscha\\Documents\\Personal\\Messages\\sms-20230121112702.xml"
# A few Twilio values are specified below
glbTwilioSID = ""
glbTwilioAuthToken = ""
glbTwilioPhoneNumber = ""

# Each instance of this class has all of the information about one contact
class Contact(object):
  # The __init__ method creates an instance of the class      
  def __init__(self, fullNameVal, firstNameVal, middleNameVal, lastNameVal, \
               eMailAddressVal, eMailAddr1Val, eMailAddr2Val, eMailAddr3Val, \
               phoneNumberVal, primaryPhoneVal, homePhone1Val, homePhone2Val, mobilePhoneVal):
    self.fullName = fullNameVal
    self.firstName = firstNameVal 
    self.middleName = middleNameVal
    self.lastName = lastNameVal  
    self.eMailAddress = eMailAddressVal 
    self.eMailAddr1 = eMailAddr1Val 
    self.eMailAddr2 = eMailAddr2Val 
    self.eMailAddr3 = eMailAddr3Val 
    self.phoneNumber = phoneNumberVal 
    self.primaryPhone = primaryPhoneVal 
    self.homePhone1 = homePhone1Val 
    self.homePhone2 = homePhone2Val 
    self.mobilePhone = mobilePhoneVal 
  # Get the phone number from an instance of this class
  def getPhoneNumber(self):
    return self.phoneNumber

# Add a phone number to the phone number map. The phone
# number is not added in some cases.
def addPhoneNumber(phoneMap, phoneNumber):
  # Assume we are going to add the phone naume
  addOk = True
  # Check if the phone number is numeric
  if phoneNumber.isnumeric() == False:
    addOk = False
  phoneLen = len(phoneNumber) 
  # If the phone number is too short, then it can not
  # be added
  if phoneLen <= 6:
    addOk = False
  # If the phone number starts with an invalid prefix,
  # then it can not be added
  if phoneNumber.startswith('90007'):
    addOk = False
  elif phoneNumber.startswith('90008'):
    addOk = False
  # Add the phone number, if need be
  if addOk == True:
    phoneLen = len(phoneNumber) 
    if phoneNumber not in phoneMap:
      phoneMap[phoneNumber] = ''
      if phoneLen != 10:
        print(phoneNumber)

# Build a full name and return it to the caller
def buildFullName(firstName, middleName, lastName):
  # Check if all of the passed values are None
  if firstName == None and middleName == None and lastName == None:
    return None
  # Fix the values passed by the caller
  if firstName == None:
    firstName = ''
  if middleName == None:
    middleName = ''
  if lastName == None:
    lastName = ''
  # If we don't have a last name, then we can't build a full name
  if lastName == '':
    return None
  # Start building the full name
  fullName = ''
  if firstName != '':
    fullName += firstName
  # We really only want to use the middle name, if we have a first name
  if middleName != '':
    if firstName != '':
      fullName += ' ' + middleName
  # Add the last name 
  if fullName != '':
    fullName += ' ' + lastName 
  else:
    fullName += lastName
  return fullName

# Build an Email address and return it to the caller
def buildEmailAddress(eMailAddr1, eMailAddr2, eMailAddr3):
  # Check if all of the passed values are None
  if eMailAddr1 == None and eMailAddr2 == None and eMailAddr3 == None:
    return None
  # Fix the values passed by the caller
  if eMailAddr1 == None:
    eMailAddr1 = ''
  if eMailAddr2 == None:
    eMailAddr2 = ''
  if eMailAddr3 == None:
    eMailAddr3 = ''
  # Start building the final Email address
  eMailAddress = None
  if eMailAddr1 != '':
    eMailAddress = ''
    eMailAddress += eMailAddr1
    return eMailAddress
  if eMailAddr2 != '':
    eMailAddress = ''
    eMailAddress += eMailAddr2
    return eMailAddress
  if eMailAddr3 != '':
    eMailAddress = ''
    eMailAddress += eMailAddr3
    return eMailAddress
  return eMailAddress  

# Build a phone number and return it to the caller
def buildPhoneNumber(primaryPhone, homePhone1, homePhone2, mobilePhone):
  # Check if all of the passed values are None
  if primaryPhone == None and homePhone1 == None and homePhone2 == None and mobilePhone == None:
    return None
  # Fix the values passed by the caller
  if primaryPhone == None:
    primaryPhone = ''
  if homePhone1 == None:
    homePhone1 = ''
  if homePhone2 == None:
    homePhone2 = ''
  if mobilePhone == None:
    mobilePhone = ''
  # Start building the final Email address
  phoneNumber = None
  if mobilePhone != '':
    phoneNumber = ''
    phoneNumber += mobilePhone
    return phoneNumber
  if primaryPhone != '':
    phoneNumber = ''
    phoneNumber += primaryPhone
    return phoneNumber
  if homePhone1 != '':
    phoneNumber = ''
    phoneNumber += homePhone1
    return phoneNumber
  if homePhone2 != '':
    phoneNumber = ''
    phoneNumber += homePhone2
    return phoneNumber
  return phoneNumber 

# Create a Twilio client and return the client to the caller
def createTwilioClient(sidStr, authTokenStr):
  cl = Client(sidStr, authTokenStr)
  return cl

# Fix a contact Email address
def fixEmailAddressContact(emailAddress):
  # Check if the Email address is blank
  if emailAddress == '':
    emailAddress = None
    return emailAddress
  # Break the Email address into parts
  finalEmailAddress = None
  splitEmailAddress = emailAddress.split()
  for part in splitEmailAddress:
    atIndex = part.find('@')
    if atIndex >= 0:
      finalEmailAddress = part
      break 
  return finalEmailAddress

# Fix an Android phone number by removing unneed characters from it
def fixPhoneNumberAndroid(phoneNumber):
  # The phone numbers listed below have a one prefixed in front of 
  # them. The one character is removed below.
  onePrefixList = ['16174294718', '17818882893', '19703765609', \
                   '15736390293', '19498741332', '17608597370']
  # The phone numbers listed below are actually international numbers
  # and should have a special prefix in front of them
  intPrefixList = ['385919594904', '41791597173', '447973214553', \
                   '447462762920', '447742738081']
  # Get some information about the phone number and try
  # to fix it
  phoneLen = len(phoneNumber)
  if phoneNumber.startswith('+1'):
    phoneNumber = phoneNumber[2:]
  elif phoneNumber in onePrefixList:
    phoneNumber = phoneNumber[1:]
  elif phoneNumber in intPrefixList:
    phoneNumber = '011' + phoneNumber
  return phoneNumber  

# Fix a contact phone number by removing unneed characters from it
def fixPhoneNumberContact(phoneNumber):
  # Get some information about the phone number and try
  # to fix it
  phoneLen = len(phoneNumber)
  originalPhoneNumber = phoneNumber
  # Check for, and fix, phone numbers that start with plus one
  if phoneNumber.startswith('+1'):
    phoneNumber = phoneNumber[2:]
    phoneLen = len(phoneNumber)
    lParenIndex = phoneNumber.find('(')
    if lParenIndex >= 0:
      rParenIndex = phoneNumber.find(')')
      firstDashIndex = phoneNumber.find('-')
      phoneNumber = phoneNumber[lParenIndex+1:lParenIndex+4] + \
                    phoneNumber[lParenIndex+6:lParenIndex+9] + \
                    phoneNumber[lParenIndex+10:lParenIndex+14]
  # Check for, and fix, phone numbers that start with one
  if phoneNumber.startswith('1 '):
    phoneNumber = phoneNumber[2:]
    phoneNumber = phoneNumber.replace('-', '')
    phoneLen = len(phoneNumber)
  # Check for a blank phone number
  if phoneNumber == '':
    phoneNumber = None
    return phoneNumber
  # Check for some invalid characters in the phone number
  lParenIndex = phoneNumber.find('(')
  rParenIndex = phoneNumber.find(')')
  firstDashIndex = phoneNumber.find('-')
  firstBlankIndex = phoneNumber.find(' ')
  phoneNumber = phoneNumber.replace('(', '')
  phoneNumber = phoneNumber.replace(')', '')
  phoneNumber = phoneNumber.replace(' ', '')
  phoneNumber = phoneNumber.replace('-', '')
  # phoneNumber = phoneNumber.replace('[', '')
  # phoneNumber = phoneNumber.replace(']', '')
  phoneNumber = phoneNumber.replace('Dad', '')
  phoneNumber = phoneNumber.replace('Mom', '')
  phoneNumber = phoneNumber.replace('Arterra', '')
  phoneNumber = phoneNumber.replace('+49', '01149')
  phoneNumber = phoneNumber.replace('+61', '01161')
  phoneNumber = phoneNumber.replace('i4687563025', '0114687563025')
  phoneNumber = phoneNumber.replace('61[0]438452637', '011610438452637')
  phoneNumber = phoneNumber.replace('460703347217', '011460703347217')
  phoneNumber = phoneNumber.replace('41799168237', '01141799168237')
  phoneLen = len(phoneNumber)
  # Check for some invalid phone numbers
  numberIsValid = True
  if phoneNumber.isnumeric() == False:
    numberIsValid = False
    print('i', originalPhoneNumber, phoneNumber)
  if phoneLen <= 6:  
    numberIsValid = False
    print('6', originalPhoneNumber, phoneNumber)
  if phoneLen != 10:   
    print('10', originalPhoneNumber, phoneNumber)
  # Check if the phone number is invalid for any reason
  if numberIsValid == False:
    phoneNumber = None
  return phoneNumber 

# Get all of the elements from the root
def getElements(root):
  elements = []
  for child in root:
    elements.append(child)
  return elements

# Merge the messages map and the contact map. Use the contact
# map (if possible) to update the messages map
def mergeMaps(phoneMap, contactMap):
  phoneKeys = phoneMap.keys()
  for phoneKey in phoneKeys:
    if phoneKey != None and \
       phoneKey in contactMap:
      phoneMap[phoneKey] = contactMap[phoneKey]
  return

# Process one contact. If possible, the contact is added
# to the phone number / contact map
def processContact(eachContact, contactMap):
  phoneNumber = eachContact.getPhoneNumber()
  if phoneNumber == None:
    return
  contactMap[phoneNumber] = eachContact

# Process all of the contacts passed to this routine. Each
# list entry is a contact.
def processContacts(contactList):
  contactMap = dict()
  for eachContact in contactList:
    processContact(eachContact, contactMap)
  return contactMap

# Process an MMS element 
def processElementMms(smsElement, phoneMap): 
  parts = smsElement[0]
  addrs = smsElement[1]
  for smsAddr in addrs:
    attribs = smsAddr.attrib
    phoneNumber = attribs['address'] 
    phoneNumber = fixPhoneNumberAndroid(phoneNumber)
    # Add the phone number, if it is not known
    if phoneNumber not in phoneMap:
      addPhoneNumber(phoneMap, phoneNumber)
  return 

# Process an SMS element 
def processElementSms(smsElement, phoneMap): 
  attribs = smsElement.attrib
  phoneNumber = attribs['address']
  phoneNumber = fixPhoneNumberAndroid(phoneNumber)
  # Add the phone number, if it is not known
  if phoneNumber not in phoneMap:
    addPhoneNumber(phoneMap, phoneNumber)
  return 

# Process just one element. Each element is an SMS message.
def processElement(smsElement, phoneMap):
  elementTag = smsElement.tag
  if elementTag == 'sms':
    processElementSms(smsElement, phoneMap)
  elif elementTag == 'mms':
    processElementMms(smsElement, phoneMap)
  else:
    raise ValueError('Invalid tag found - (' + elementTag + ')') 
  return 

# Process all of the elements passed to this routine. Each
# element is an SMS message.
def processElements(elements, phoneMap):
  for smsElement in elements:
    processElement(smsElement, phoneMap)

# Read all of the contacts from an input file
def readContacts(contactsFileName):
  # Build a list that will contain all of the new contacts
  newContactList = []
  # Process the contacts file
  with open(contactsFileName, 'r') as csvFile:
    csvReader = csv.reader(csvFile)
    rowCount = 0
    for row in csvReader:
      rowCount += 1
      # Get a number of fields from the CSV row
      firstName = row[0]
      middleName = row[1]
      lastName = row[2]
      fullName = buildFullName(firstName, middleName, lastName)
      # Get some Email address information
      eMailAddr1 = row[14]
      eMailAddr1 = fixEmailAddressContact(eMailAddr1)
      eMailAddr2 = row[15]
      eMailAddr2 = fixEmailAddressContact(eMailAddr2)
      eMailAddr3 = row[16]
      eMailAddr3 = fixEmailAddressContact(eMailAddr3)
      eMailAddress = buildEmailAddress(eMailAddr1, eMailAddr2, eMailAddr3)
      # Get some phone number information
      primaryPhone = row[17]
      primaryPhone = fixPhoneNumberContact(primaryPhone)
      homePhone1 = row[18]
      homePhone1 = fixPhoneNumberContact(homePhone1)
      homePhone2 = row[19]
      homePhone2 = fixPhoneNumberContact(homePhone2)
      mobilePhone = row[20]
      mobilePhone = fixPhoneNumberContact(mobilePhone)
      phoneNumber = buildPhoneNumber(primaryPhone, homePhone1, homePhone2, mobilePhone)
      # Use all of the contact information to build a contact instance (class instance)
      newContact = Contact(fullName, firstName, middleName, lastName, \
                           eMailAddress, eMailAddr1, eMailAddr2, eMailAddr3, \
                           phoneNumber, primaryPhone, homePhone1, homePhone2, mobilePhone)
      # The following code was used to get the column numbers
      # fieldCount = -1
      # for field in row:
      #   fieldCount += 1
      #   print(fieldCount, row[fieldCount])
      # print()
      # Add the new contact to the list of contacts
      newContactList.append(newContact)
  return newContactList

# Read an XML file and return the XML tree to the caller
def readXml(xmlFileName):
  tree = ET.parse(glbSmsXml)
  root = tree.getroot()  
  return root

# Send a message to a phone
def sendMessage(client, msgTxt, fromPhone, toPhone):
  # Send a message
  client.messages.create(body=msgTxt,from_=fromPhone, to=toPhone)
  return

# Send a message to all of the phone numbers we have 
def sendMessages(client, msgTxt, fromPhone, phoneMap):
  # Process each entry in the phone map
  phoneKeys = phoneMap.keys()
  for phoneKey in phoneKeys:
    if phoneKey == None:
      continue
    # The code below only allows messages to be sent to my cell
    # phone number. This is appropriate for testing. The possible
    # sensitive number include both sisters, Lois's kids, Daniel, 
    # etc. 
    if phoneKey != '2817990319':
      continue
    # Send the message
    sendMessage(client, msgTxt, fromPhone, phoneKey)
  return

# This routine sets a bunch of Twilio access global values
def setTwilioAccessGlobals():
  # Get the Twilio access globals. The Twilio access values
  # are stored in AWS Secrets Manager.
  twilioSidStr, twilioAuthStr, twilioPhoneStr = HDLmAwsUtility.getTwilioAccessValues()
  # Set some of the Twilio access global values 
  glbTwilioSID = twilioSidStr
  glbTwilioAuthToken = twilioAuthStr
  glbTwilioPhoneNumber = twilioPhoneStr
  return

# Handle startup 
def startup():   
  pass

# Main program
def main():   
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Set some Twilio access global values
  setTwilioAccessGlobals()
  print('Starting')
  # Start the current program  
  startup() 
  # Create the Twilio client
  twilioClient = createTwilioClient(glbTwilioSID, glbTwilioAuthToken)
  # Read all of the contacts
  contactList = readContacts(glbConCsv)
  # Process all of the contacts
  contactMap = processContacts(contactList)
  # Read the input XML
  root = readXml(glbSmsXml) 
  # Get the messages
  elements = getElements(root)
  # Process each of the elements
  phoneMap = dict()
  processElements(elements, phoneMap)
  # Merge the messages map and the contact map
  mergeMaps(phoneMap, contactMap)
  # Send a message to all of the phone numbers
  sendMessages(twilioClient, 'Hk', glbTwilioPhoneNumber, phoneMap)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took  
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__":
  main()