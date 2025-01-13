from   bs4         import BeautifulSoup
from   HDLmUtility import * 
from   HDLmWebSite import *
from   selenium    import webdriver
from   selenium.webdriver.common      import desired_capabilities
from   selenium.webdriver.common.by   import By
from   selenium.webdriver.common.keys import Keys
from   selenium.webdriver.common.action_chains import ActionChains
import HDLmAssert     
import HDLmError
import platform
import sys
import time
import urllib3

glbGoogleFileName    = 'HDLmLisg.js'
glbWikipediaFileName = 'HDLmLisi.js'
glbWindowsFileName   = 'HDLmLisw.js'
glbFilePath = 'C:\\Users\\pscha\\Documents\\Visual_Studio_Code\\Projects\\WebApplication5\\WebApplication5\\js'
glbGoogleFontList = 'https://fonts.google.com'
glbGoogleSavedFontList = 'C:\\Users\\pscha\\Desktop\\Browse Fonts - Google Fonts.mhtml'
glbWikipediaFontList = 'https://en.wikipedia.org/wiki/List_of_typefaces'
glbWindows11FontList = 'https://learn.microsoft.com/en-us/typography/fonts/windows_11_font_list'
# Set a few values for use below
glbFirstFontName = 'Adobe Jenson'
glbFirstFontFound = False    
glbLastFontName = 'Sans forgetica'
glbLastFontFound = False

# This function enters a URL. The caller provides the complete 
# URL including protocol string. Note that this routine returns
# the results of the URL (the page source) to the caller. 
def enterUrl(browser, urlStr):
  browser.get(urlStr)
  output = browser.page_source
  return output

# Get some output lines from the font list
def getFontLines(fontList, maxLength):
  # Start the list of output lines
  outLines = []
  curLine = ''
  # Get the number of fonts
  fontListLen = len(fontList)
  for font in fontList:
    fontInQuotes = "'" + font + "', "
    curLine += fontInQuotes
    if len(curLine) > maxLength:
      outLines.append(curLine)
      curLine = ''
  return outLines

# Get some Google font name for use later
def getFontNamesGoogle(fontList, curElement):
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the current element is set or not 
    if  curElement == None:
      break
    # Get the name of the current element, if possible
    curName = curElement.name
    if curName != None and curName == 'h1':  
      # Get the value of the current Table Data element
      curString = str(curElement.string)  
      # Get a font value in a few cases
      if curString != None and \
         curString != 'None':
        fontStr = curString 
        fontStr = fontStr.lstrip()
        if fontStr not in fontList:
          print(len(fontList), fontStr)
          fontList.append(fontStr)
    # Check if current element has any children
    if hasattr(curElement, 'children') == False:
      break;
    # Get the children of the current element 
    curElementChildren = curElement.children 
    # Process all of the children of the current element 
    for curElementChild in curElementChildren: 
      fontList = getFontNamesGoogle(fontList, curElementChild)    
    # Terminate the dummy loop 
    break 
  return fontList

# Get some Wikipedia font name for use later
def getFontNamesWikipedia(fontList, curElement):
  # Make a few varialbes global
  global glbFirstFontName 
  global glbFirstFontFound   
  global glbLastFontName  
  global glbLastFontFound  
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the current element is set or not 
    if  curElement == None:
      break
    # Get the name of the current element, if possible
    curName = curElement.name
    if curName != None and curName == 'a':
      # Get the value of the current Table Data element
      curString = str(curElement.string) 
      # Get a font value in a few cases
      if curString != None         and \
         curString != 'None':
        fontStr = curString 
        fontStr = fontStr.lstrip()
        # Check if this font name is already known
        if fontStr not in fontList: 
          # Check for the first font name we care about
          if glbFirstFontFound == False and \
             glbLastFontFound == False  and \
             fontStr == glbFirstFontName:
            glbFirstFontFound = True  
          # Add the current font to the font list
          if glbFirstFontFound == True and \
             glbLastFontFound == False:
            fontList.append(fontStr)
          # Check for the last font name we care about
          if glbFirstFontFound == True and \
             glbLastFontFound == False and \
             fontStr == glbLastFontName:
            glbLastFontFound = True 
    # Check if current element has any children
    if hasattr(curElement, 'children') == False:
      break;
    # Get the children of the current element 
    curElementChildren = curElement.children 
    # Process all of the children of the current element 
    for curElementChild in curElementChildren: 
      fontList = getFontNamesWikipedia(fontList, curElementChild)    
    # Terminate the dummy loop 
    break 
  return fontList

# Get some Windows font name for use later
def getFontNamesWindows(fontList, curElement):
  # The dummy loop below is used to allow break to work 
  while True:
    # Check if the current element is set or not 
    if  curElement == None:
      break
    # Get the name of the current element, if possible
    curName = curElement.name
    if curName != None and curName == 'td':
      # Get the value of the current Table Data element
      curString = str(curElement.string) 
      # Check if the current string is a valid floating-point number
      validFloat = True
      try:
        # The floating-point number created below isn't really used.
        # However, we do check for the exception raised if the current
        # string isn't a valid floating-point number.
        curFloat = float(curString)
      except:
        validFloat = False
      # Get a font value in a few cases
      if curString != None         and \
         curString != 'None'       and \
         curString.find('.tt') < 0 and \
         validFloat == False:
        fontStr = curString 
        fontStr = fontStr.lstrip()
        if fontStr not in fontList:
          fontList.append(fontStr)
    # Check if current element has any children
    if hasattr(curElement, 'children') == False:
      break;
    # Get the children of the current element 
    curElementChildren = curElement.children 
    # Process all of the children of the current element 
    for curElementChild in curElementChildren: 
      fontList = getFontNamesWindows(fontList, curElementChild)    
    # Terminate the dummy loop 
    break 
  return fontList

# Get all of the Google font name. Google builds this web page
# in parts. We need to get and check each part of the web page
def getGoogleFontsWebPage(browser, urlStr, fontList):
  # Set some initial variables
  count = 0
  while True:
    count += 1
    # The first time this loop is executed, we need to actually
    # enter the URL
    if count == 1:
      contents = enterUrl(browser, urlStr)    
      soup = getSoup(contents) 
      fontList = getFontNamesGoogle(fontList, soup)
    # After the first time, we just page down to get some more
    # font names
    else:
      # htmlElements = browser.find_elements(By.TAG_NAME, 'body')
      # htmlElement = htmlElements[0]
      # htmlElement.click()
      # htmlElement.send_keys(Keys.PAGE_DOWN)
      ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
      # browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
      time.sleep(3)
      contents = browser.page_source   
      soup = getSoup(contents) 
      fontList = getFontNamesGoogle(fontList, soup)    
    # Check if this loop should be terminated
    if count > 250:
      break
  return fontList

# Get the name of current operating system
def getOperatingSystemName():
  osName = platform.system() 
  if osName == 'Darwin':
    osName = 'Macintosh'
  return osName

# Get some beautiful soup from some HTML  
def getSoup(html):
  soup = BeautifulSoup(html, 'html.parser')
  return soup

# Read a file with some Google font information. Some 
# further steps are required to get the original HTML
# from the file.
def readInputFile(inputFile):
  # Get the saved font file
  rawInputLines = HDLmUtility.readInputFile(inputFile)
  inputLines = []
  firstLineFound = False
  lastLineFound = False
  for line in rawInputLines:
    # Check for the first line we can use
    if line.find('<!DOCTYPE html>') >= 0:
      firstLineFound = True 
    # Check for a line after the last line that we can actually use
    if firstLineFound == True and \
       line.find('MultipartBoundary') >= 0:
      lastLineFound = True 
    # Check if we can use the current line
    if firstLineFound == True and \
       lastLineFound  == False:
      inputLines.append(line)
  # The input lines may end with an equals sign. This character
  # must be removed.
  finalLine = ''
  for line in inputLines:
    line = HDLmString.removeSuffix(line, '=')
    finalLine += line
  return finalLine

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


# Try to get the contents of a web page
def urllib3GetContents(fontUrl):
  urlString = fontUrl
  # Run the current request
  http = urllib3.PoolManager()
  resp = http.request('GET', urlString)
  respWebBinary = resp.data
  respWebString = respWebBinary.decode('UTF-8')
  return respWebString

# Write the final output lines
def writeOutputLines(outputLines, pathStr, fileStr):
  # Get the final file name
  fileNameStr = pathStr + '\\' + fileStr
  HDLmUtility.writeOutputFile(outputLines, fileNameStr)
  return

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()   
  # The next two lines are only needed to get fonts from Google
  # browserName = 'Firefox'
  # browser = startDriver(browserName)
  # Start with an empty list of font name
  fontList = []
  contents = urllib3GetContents(glbWikipediaFontList)
  soup = getSoup(contents)
  fontList = getFontNamesWikipedia(fontList, soup)
  # The line below was only used to get Google fonts
  # fontList = getGoogleFontsWebPage(browser, glbGoogleFontList, fontList)
  outLines = getFontLines(fontList, 70)
  # writeOutputLines(outLines, glbFilePath, glbGoogleFileName)
  writeOutputLines(outLines, glbFilePath, glbWikipediaFileName)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()