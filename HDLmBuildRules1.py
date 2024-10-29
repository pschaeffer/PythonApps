# This program obtains a web site name from the user. A set of 
# rules are built for the web site and then added to the nule
# database.    

from   HDLmBuildRules  import *
from   HDLmTree        import *
from   HDLmWebSite     import *
from   http            import HTTPStatus 
from   selenium        import webdriver
from   selenium.webdriver.common import desired_capabilities
import json
import re
import time
import tkinter         as tk 

# Each instance of this class has all of the information about
# the current context. The context has a reference to the 
# configuration information, the web site we are building
# rules for, etc.
class Context(object):
  # The __init__ method creates an instance of the class
  def __init__(self):
    self.webSite = None 
  # Get the current web site and return it to the caller
  def getWebSite(self):
    return self.webSite  

# Check if a URL is valid or not. Note that is really a 
# domain name check. Real URLs typically start with http
# or (more likely) https. They also include a port number
# (in some cases) and a path (also in some cases).
def checkUrlStr(urlStr):
  # Use a regex to validate the URL (domain name)
  patStr = "^(([a-zA-Z])(\w)*(\.))+([a-zA-Z])(\w)*$"
  check = re.search(patStr, urlStr)
  # Handle a valid URL 
  if check:
    return True
  # Handle an invalid URL 
  else:
    return False

# This function enters a URL. The caller provides the complete 
# URL including protocol string. Note that this routine returns
# the results of the URL (the page source) to the caller. 
def enterUrl(browser, urlStr):
  browser.get(urlStr)
  output = browser.page_source
  return output

# Fix a web site dictionary. A new (hopefully improved) dictionary
# is returned to the caller.
def fixWebSiteDict(oldWebSiteDict):
  # Create a new empty web site dictionary
  newWebSiteDict = dict() 
  for oldKey in oldWebSiteDict:
    # Get the old value
    oldValue = oldWebSiteDict[oldKey]
    # Remove any URL percent encoded characters
    if oldKey.find('%') >= 0:
      newKey = urllib.parse.unquote(oldKey)
    else:
      newKey = oldKey
    # Use the new key value to build an HDLmUrl oject
    try:
      newHDLmUrlObj = HDLmUrl(newKey, prUrlOk=True, relativeUrl=True, semiSep=False)
    except Exception as e:
      print('In fixWebSiteDict using HDLmUrl')
      print(oldKey)
      print(newKey)
      print(str(e))
      continue
    # Get everything after the host name
    newAfterHost = newHDLmUrlObj.getEverythingAfterHost()
    # Check if we already have a new dictionary entry
    if newAfterHost not in newWebSiteDict:
      newWebSiteDict[newAfterHost] = oldValue
  return newWebSiteDict

# Get the name of the web site 
def getWebSiteName():
  # Create an instance of the main Tkinter frame or window
  TkRoot = tk.Tk()  
  # Set the TK window size
  TkRoot.geometry("650x100")  
  TkRoot.title("Get Web Site")
  # Declare a string variable for storing the web site name 
  TkNameVar=tk.StringVar()  
  name = '' 
  # Define an input validation function   
  def TkCallback(input):  
    # Check if the input area is empty
    if input == '':
      TkSetText(TkText1, 'Input area is empty') 
      return True 
    # Check the URL (really just a domain name) 
    check = checkUrlStr(input)
    # Handle valid input
    if check:
      TkSubmit1.config(state = 'normal') 
      TkSetText(TkText1, '')
    # Handle invalid input
    else:
      TkSetText(TkText1, 'Invalid input')
      return True 
    return True 
  # Define a function that will set the text area
  def TkSetText(widget, text):
    widget.config(state = 'normal') 
    widget.delete("1.0", "end")  
    widget.insert(tk.END, text)
    widget.config(state = 'disabled') 
  # Define a function that will handle the submit command
  def TkSubmit():  
    TkRoot.destroy()
  # Create an entry widget for the web site name 
  TkEntry1 = tk.Entry(TkRoot, textvariable = TkNameVar, font=('calibre',10,'normal'))  
  # Create a label for the web site name 
  TkLabel1 = tk.Label(TkRoot, text = 'Web Site', font=('calibre',10, 'bold'))
  # Create a submit button
  TkSubmit1 = tk.Button(TkRoot, text = 'Submit', command = TkSubmit, state='disabled')  
  # Create a text widget
  TkText1 = tk.Text(TkRoot, height = 1, width = 50)
  TkSetText(TkText1, 'Input area is empty')
  TkReg = TkRoot.register(TkCallback)
  TkEntry1.config(validate="key", validatecommand=(TkReg, '%P'))
  # placing the label and entry in
  # the required position using grid
  # method
  TkLabel1.grid(row=0,column=0)
  TkEntry1.grid(row=0,column=1) 
  TkText1.grid(row=0,column=2)
  TkSubmit1.grid(row=2,column=1)  
  # Run the main Tkinter loop 
  TkRoot.mainloop()  
  name=TkNameVar.get()  
  return name

# Handle shutdown 
def shutdown(browser):  
  if browser != None:
    browser.quit()
  return
 
# Handle startup 
def startup():   
  pass

# Handle starting a specific driver. Return the driver to the
# caller. This function takes a standard application name.
def startDriver(browserName):
  # Get the driver name from the application (browser) name
  driverName = HDLmWebSite.getApplicationDriverName(browserName)
  # Check the driver name. We only support a few driver
  # names. 
  if driverName == 'Chrome':
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('--screen-size=1920X1080')
    browser = webdriver.Chrome(options=driver_options)
  elif driverName == 'Edge':
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('--screen-size=1920X1080')
    browser = webdriver.Edge("msedgedriver.exe")
  elif driverName == 'Firefox':
    browser = webdriver.Firefox()
  elif driverName == 'Opera':
    operaCaps = desired_capabilities.DesiredCapabilities.OPERA.copy()
    operaCaps = {}
    operaOpts = webdriver.ChromeOptions()
    operaOpts.add_argument('--no-sandbox')
    operaOpts.add_argument('--screen-size=1920X1080')
    browser = webdriver.Opera(desired_capabilities=operaCaps, options=operaOpts)
  else:
    raise SystemError("Unknown browser driver name - " + browserName)
  return browser

# Main program
def main(): 
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()  
  # The code below was used to test the HDLmWebSockets.getModifications
  # function
  # def messageRoutine(wsMessage):
  #   print(wsMessage)   
  # HDLmWebSockets.getModifications(messageRoutine)
  # Start the current program  
  startup()
  # Loop until we get a valid web site name
  while True:    
    newWebSite = 'www.oneworldobservatory.com'
    newWebSite = 'www.themarvelouslandofoz.com'
    if 1 == 1:
      break
    newWebSite = getWebSiteName()
    if checkUrlStr(newWebSite):
      break
  # Create the context object for use below
  context = Context()  
  # Get a few values from the context 
  # Try to set the initial system value 
  HDLmStateInfo.setEntriesSystemValue('a')  
  # HDLmUtility.getPerceptualHash('a')
  browserName = 'Firefox'
  browser = startDriver(browserName)
  # Build the web site object for use below
  if 1 == 2:
    webSite = HDLmWebSite(newWebSite)
    semiSep = False
    webSiteDict = webSite.getWebSiteDict(browser, newWebSite, semiSep)
    fixWebSiteDict(webSiteDict)
  # Get the rows from the database
  [responseBytes, responseCode] = HDLmTree.buildModificationTree()
  if responseCode != HTTPStatus.OK:
    errorText = f'Invalid response code ({responseCode}) received' 
    HDLmAssert(False, errorText)
  # Add the rows to the node tree
  responseJsonStr = responseBytes.decode('UTF-8')
  HDLmTree.addToTree(responseJsonStr) 
  # This is the URL string that we are going to pass to the rule
  # construction routine
  urlStr = 'https://' + newWebSite
  output = enterUrl(browser, urlStr)
  newRules = HDLmBuildRules.buildRules(urlStr, newWebSite, output)
  # Add all of the new rules to the rule tree
  for newRule in newRules:
    HDLmWebSockets.sendAddTreeNodeRequest(newRule)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took  
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart) 
  # End processing
  shutdown(browser)

# Actual starting point
if __name__ == "__main__":
  main()