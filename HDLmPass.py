# The HDLmPass class doesn't actually do anything. However, 
# it does provide a set of routines that are needed elsewhere.

from   HDLmDefines import * 
from   HDLmMod     import *
import datetime

# The following array has all of the field names. These are the
# field names in an ignore details instance or a line details 
# instance. The field names are in standard format. The first 
# character is lowercase. If these field names are going to be 
# used as headings, then the first character of each field name
HDLmPassFieldNames = ["createdFromVerificationCheck",
                      "scriptId",
                      "testCase",
                      "stepNumber",
                      "description",
                      "language",
                      "ticketPackage",
                      "testResults",
                      "detailsOne",
                      "detailsTwo",
                      "detailsThree"      
                     ]
# The following array has all of the field types. These are the
# field types in a line details instance.  
HDLmPassFieldTypes = ["date",
                      "number",
                      "number",
                      "number",
                      "text",
                      "text",
                      "text",
                      "text",
                      "text",
                      "text",
                      "text"
                     ]

class HDLmPass(object):
  # This routine adds any missing fields to a pass-through object. 
  # The possibly missing fields depend on the object type. The 
  # possibly missing fields are highly dependent on the object
  # type.  
  @staticmethod
  def addMissingPassObject(newPass):
    # Add any missing fields to the pass-through object  
    # (actually a modification object) passed by the caller 
    if hasattr(newPass, 'type') == False:
      return
    # Check for a companies level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'companies':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = []  
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod()
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'companies' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue  
      if hasattr(newPass.details, 'countCompanies') == False:
        newPass.details.countCompanies = 0 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field        
      if hasattr(newPass, 'children') == True and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countCompanies = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now()  
    # Check for a company level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'company':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'company' 
      # print(newPass) 
      if hasattr(newPass.details, 'name') == False:
        # print(newPass) 
        newPassNodePathLength = len(newPass.nodePath)
        # print(newPass) 
        if newPassNodePathLength > 0:
          # print(newPass) 
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          # print(newPass) 
          newPass.details.name = lastNodePathValue
          # print(newPass)  
        # print(newPass)  
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now() 
      # If the pass-through property does not already exist,
      # create the pass-through property 
      if hasattr(newPass.details, 'passThru') == False:
        newPass.details.passThru = False 
      if hasattr(newPass.details, 'updated') == False:
        newPass.details.updated = False  
    # Check for a data (zero, one, or more divisions) level object. 
    # Add any needed fields as need be. 
    if newPass.type == HDLmDefines.getString('HDLMDATATYPE') == False:
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = HDLmDefines.getString('HDLMDATATYPE') 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'countDivisions') == False:
        newPass.details.countDivisions = 0 
      if hasattr(newPass.details, 'updated') == False:
        newPass.details.updated = False 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') == True and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countDivisions = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.now() 
    # Check for an ignore-list entry object. Add any needed 
    # fields as need be. 
    if newPass.type == 'ignore':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'ignore' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now() 
      if hasattr(newPass.details, 'comments') == False:
        newPass.details.comments = '' 
      # We need to make sure all of the fields are defined as
      # properties 
      fieldNames = HDLmPass.getPassFieldNames()
      for fieldName in fieldNames:
        if hasattr(newPass.details, fieldName) == False:
          setattr(newPass.details, fieldName, '') 
    # Check for a line (just one line) level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'line':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = []  
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'line' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      # We need to make sure all of the fields are defined as
      # properties 
      fieldNames = HDLmPass.getPassFieldNames()
      fieldCounter = -1
      for fieldName in fieldNames:
        fieldCounter += 1
        # Fix each type of field 
        fieldType = HDLmPassFieldTypes[fieldCounter]
        # Check for, and handle a date field 
        if fieldType == 'date':
          if hasattr(newPass.details, fieldName) == False or \
             getattr(newPass.details, fieldName) == '':
            setattr(newPass.details, fieldName, datetime.datetime.now()) 
        # Check for, and handle a numeric field 
        if fieldType == 'number':
          if hasattr(newPass.details, fieldName) == False :
            setattr(newPass.details, fieldName, 0)  
        # Check for, and handle a text field 
        if fieldType == 'text':
          if hasattr(newPass.details, fieldName) == False: 
            setattr(newPass.details, fieldName, '')
    # Check for a lines (zero, one, or more lines) level object. 
    # Add any needed fields as need be. 
    if newPass.type == 'lines':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'lines' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'countLines') == False:
        newPass.details.countLines = 0 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') != False and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countLines = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
          newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'dummyTable') == False or \
         newPass.details.dummyTable == '':
        newPass.details.dummyTable = 'dummyTable'  
    # Check for an ignore-list (list) level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'list':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = []
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'list' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'countIgnores') == False:
        newPass.details.countIgnores = 0 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') != False and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countIgnores = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
          newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
          newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now() 
      if hasattr(newPass.details, 'comments') == False:
        newPass.details.comments = '' 
    # Check for an ignore-lists (lists) level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'lists':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'lists' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'countLists') == False:
        newPass.details.countLists = 0 
      if hasattr(newPass.details, 'updated') == False:
        newPass.details.updated = False 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') != False and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countLists = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
          newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now() 
    # Check for a report (just one report) level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'report':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'report' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'countLines') == False:
        newPass.details.countLines = 0 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') != False and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countLines = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
          newPass.details.created == '':
        newPass.details.created = datetime.datetime.now()
      # If the pass-through property does not already exist,
      # create the pass-through property 
      if hasattr(newPass.details, 'passThru') == False:
        newPass.details.passThru = False 
      if hasattr(newPass.details, 'dummyTable') == False or \
         newPass.details.dummyTable == '':
        newPass.details.dummyTable = 'dummyTable' 
    # Check for a reports (zero, one, or more reports) level object. 
    # Add any needed fields as need be. 
    if newPass.type == 'reports':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'reports' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'countReports') == False:
        newPass.details.countReports = 0 
      if hasattr(newPass.details, 'updated') == False:
        newPass.details.updated = False 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') != False and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countReports = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
          newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now() 
    # Check for a rules (zero, one, or more divisions) level object. 
    # Add any needed fields as need be. 
    if newPass.type == HDLmDefines.getString('HDLMRULESTYPE') == False:
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = []
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod()
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = HDLmDefines.getString('HDLMRULESTYPE')
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue
      if hasattr(newPass.details, 'countDivisions') == False:
        newPass.details.countDivisions = 0 
      if hasattr(newPass.details, 'updated') == False:
        newPass.details.updated = False 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the count field 
      if hasattr(newPass, 'children') != False and \
         str(type(newPass.children)) == "<class 'list'>":
        newPass.details.countDivisions = len(newPass.children)
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now()  
    # Check for a top-level object. Add any needed 
    # fields as need be. 
    if newPass.type == 'top':
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = 'top' 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      # If the pass-through property does not already exist,
      # create the pass-through property 
      if hasattr(newPass.details, 'passThru') == False:
        newPass.details.passThru = False 
    # Check for a value (a data value) level object. 
    # Add any needed fields as need be. 
    if newPass.type == HDLmDefines.getString('HDLMVALUETYPE') == False:
      # Create the node path field, if need be. The node path 
      # field is only created if it does not exist. 
      if hasattr(newPass, 'nodePath') == False:
        newPass.nodePath = [] 
      # Create the details field, if need be. The details
      # field is only created if it does not exist. 
      if hasattr(newPass, 'details') == False or \
         newPass.details == None:
        newPass.details = HDLmMod.makeEmptyMod() 
      if hasattr(newPass.details, 'type') == False:
        newPass.details.type = HDLmDefines.getString('HDLMVALUETYPE') 
      if hasattr(newPass.details, 'name') == False:
        newPassNodePathLength = len(newPass.nodePath)
        if newPassNodePathLength > 0:
          lastNodePathValue = newPass.nodePath[newPassNodePathLength - 1]
          newPass.details.name = lastNodePathValue 
      if hasattr(newPass.details, 'extra') == False:
        newPass.details.extra = '' 
      if hasattr(newPass.details, 'enabled') == False:
        newPass.details.enabled = True 
      if hasattr(newPass.details, 'comments') == False:
        newPass.details.comments = '' 
      if hasattr(newPass.details, 'value') == False:
        newPass.details.value = '' 
      if hasattr(newPass.details, 'updated') == False:
        newPass.details.updated = False 
      # Create the children array if need be 
      if hasattr(newPass, 'children') == False:
        newPass.children = []
      # Set or reset the created and last modified fields 
      if hasattr(newPass.details, 'created') == False or \
         newPass.details.created == '':
        newPass.details.created = datetime.datetime.now() 
      if hasattr(newPass.details, 'lastModified') == False or \
         newPass.details.lastModified == '':
        newPass.details.lastModified = datetime.datetime.now() 
  # Get the list of field names in the details of a line (report 
  # line) or in the details of an ignore (ignore-list entry). The
  # field names are the same in each case. 
  @staticmethod
  def getPassFieldNames():
    return HDLmPassFieldNames