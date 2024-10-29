# Each instance of this class has all of the information about
# one web site. This method is used to crawl the web site and
# find all of the pages of the web site. 
#
# The page dictionary and page list will contain relative
# URLs and/or full URLs. In other words, they may contain 
# path values (typically starting with a forward slash). 
# The associated host name is provided when an object of 
# this class is created. 
# 
# If a relative URL is used, then the associated host name
# will be used with it, along with a scheme of https. This 
# is the most likely case.
#
# However, in some cases a full URL is needed. For example,
# if the scheme is not https, then a full URL is required.
# This is probably a web site error, https should be use 
# in all cases, even for images.
#
# The phrase path values is used somewhat inaccurately above.
# Each path value may (or many not) contain query values and
# may (or may not) contain a fragment value. In this context
# a path value is defined as everything after the host name 
# (and possibly the port number) in a URL. The path value 
# might be an empty string or it might be a single forward
# slash.
#
# The page list contains one entry for every page that has
# been found so far, for the current web site. New pages
# are always added to the end of the list (never in the 
# middle or at the beginning). Note that some of the pages
# in the page list may have already been scanned (crawled).
# The crawl count gives the number of pages that have
# already been scanned.
#
# The page dictionary has all of the pages keyed by the
# relative URL (the path value, plus possibly the query
# values and the fragment) and/or the full URL. The value
# associated with each keyword will consist of a boolean 
# showing if this page has already been processed, and the 
# URL that was used to find the current page. The boolean 
# will be false, if the page has not already been scanned, 
# and true if the page has already been scanned. 

from HDLmUrl import *

class HDLmWebSite(object):
  # The __init__ method creates an instance of the class
  def __init__(self, newHostName):
    # Set all of the initial values for the web site object.
    self.crawlCount = 0
    self.pageDict = dict()
    self.pageList = []
    # We need to store the host name value. However, we need 
    # to remove the www. prefix from the host name (if it has
    # a www. prefix).
    if len(newHostName) >= 4 and \
       newHostName[0:4] == 'www.':
      newHostName = newHostName[4:]
    self.hostName = newHostName
  # The method below is used to add a new page to the page
  # list. Currently, we only allow relative URLs to added
  # with this method.
  def addPage(self, newPage):
    # Make sure the new page is a relative URL. In other words
    # the new page string has no scheme or host name. 
    pageObj = HDLmUrl(newPage, prUrlOk=True, relativeUrl=True)
    # Make sure no scheme value is specified
    pageScheme = pageObj.getScheme()
    if pageScheme != None:
      raise ValueError('New page has disallowed scheme value for add method')
    # Make sure no host name value is specified
    pageHost = pageObj.getHost()
    if pageHost != None:
      raise ValueError('New page has disallowed host name value for add method')
    # Make sure the new page string is actually new
    if newPage in self.pageDict:
      raise ValueError('New page has already been added or found')
    # We assume that the new page was added by the home page of the
    # current web site. This is not really true. The new page was
    # added by a call to this routine.
    newPageUrl = 'https://' + self.hostName + '/'
    # Add the new page to the list and the dictionary
    self.pageDict[newPage] = [False, newPageUrl]
    self.pageList.append(newPage)
  # This function takes a standard application name and converts it to an
  # Selenium driver application name. The Selenium driver application name
  # is the name that can actually be started and/or stopped. The caller
  # should pass a common application name. Note that Microsoft Edge is 
  # listed as Microsoft Edge and just Edge.
  @staticmethod
  def getApplicationDriverName(applicationName):
    # Build the application dictionary
    applicationDict = {'Brave Browser': None, 'Chrome': 'Chrome', 'Dolphin Browser': None, 
                       'Edge': 'Edge', 'Firefox': 'Firefox', 'Internet Explorer': None,
                       'Microsoft Edge': 'Edge', 'Opera': 'Opera', 'Safari': None,
                       'UC Browser': None, 'Yandex': None}
    # Check if the application name is invalid
    if applicationName not in applicationDict:
      raise ValueError('Invalid application name - ' + applicationName)
    # Get the Selenium driver application name
    appName = applicationDict[applicationName]
    if appName == None:
      raise SystemError("No Selenium drver name for - " + applicationName)
    return appName
  # Get a set of attribute values from the current web page
  @staticmethod
  def getAttributes(browser, attribute):
    # Build the CSS selector
    selector = '[' + attribute + ']'
    # Build the main script string
    scriptStr = "let values = [];" + \
                "let elements = document.querySelectorAll('" + selector + "');" + \
                "for (element of elements) {" + \
                "  let valueText = element.getAttribute('" + attribute + "');" + \
                "  values.push(valueText);" + \
                "}" + \
                "return values;"   
    # Execute the script string
    values = browser.execute_script(scriptStr)
    return values
  # Scan a web site and get all of the links from the
  # web site. Return the dictionary of links to the caller. 
  def getWebSiteDict(self, browser, webSiteHost, semiSep=True):
    # Add the home page to the web site object
    self.addPage('/')
    # Define a local function that gets a web page. Note that 
    # this function does not return anything. 
    def getPageFunc(urlStr):
      # Assume that we actually want to process the current URL
      enterTheUrl = True
      # Check if the current URL should be bypassed. Testing has
      # shown that some URLs cause problems with Firefox. Why is
      # not known.
      if len(urlStr) >= 6:
        if urlStr.endswith('.woff2'):
          enterTheUrl = False
      # If indicated, process the current URL
      if enterTheUrl:
        browser.get(urlStr)
    # Define a local function that gets the links from
    # a web page
    def getPageHrefs():
      hrefsFromAttributes = HDLmWebSite.getAttributes(browser, 'href')
      hrefs = []
      for href in hrefsFromAttributes:
        if href == '#'               or \
           href.startswith('mailto') or \
           href.startswith('javascript'):
          continue
        hrefs.append(href)
      return hrefs
    # Try to get all of the links for the current web site
    # print('In getWebSiteDict ' + str(semiSep))
    self.update(getPageFunc, getPageHrefs, semiSep)
    # Return all of the links to caller as a dictionary
    return self.getDict()
  # The method below is used to update the web site instance. 
  # What this means is that all unscanned pages will be crawled
  # as need be. The get page function is a routine passed to 
  # this method. The get page function will obtain whatever 
  # page (URL) is passed to it.
  def update(self, getPageFunc, getPageHrefs, semiSep=True):
    # print('In update 1 ' + str(semiSep))
    # Crawl all of the uncrawled pages
    while self.crawlCount < len(self.pageList):
      # Try to get and scan a new page
      pageUrlBase = self.pageList[self.crawlCount]
      pageUrlCurrent = pageUrlBase
      # At this point we want to mark the current page as
      # processed in the dictionary
      if pageUrlBase in self.pageDict:  
        pageUrlValue = self.pageDict[pageUrlBase]
        pageUrlValue[0] = True
        self.pageDict[pageUrlBase] = pageUrlValue
      else:
        raise ValueError('URL not found in dictionary during update')
      # Check if the current URL is really an Email address. We 
      # don't want to treat Email addresses as URLs. 
      if pageUrlBase.find("mailto:") >= 0:
        self.crawlCount += 1
        continue
      # Check if the page has a host name and a scheme. The call
      # below (actually object creation) may fail with an exception
      # of some sort. We need to trap the exception and handle it.
      try:
        # print('In update 2 ' + str(semiSep))
        pageObj = HDLmUrl(pageUrlBase, prUrlOk=True, relativeUrl=True, semiSep=semiSep)
      except Exception as e:
        print('In HDLmWebSite.update using HDLmUrl')
        print(pageUrlBase)
        print(str(e))
        self.crawlCount += 1
        continue
      # Given that an exception did not occur, we need to obtain 
      # some information about the current URL.
      pageScheme = pageObj.getScheme()
      pageHost = pageObj.getHost()
      # If we actually have a page host name and the host name
      # is outside of our web site, then we don't want to scan
      # it
      if pageHost != None and pageHost.find(self.hostName) < 0:
        self.crawlCount += 1
        continue
      # The host name and the scheme are about to be added to the 
      # current URL. We need to make sure that the current URL 
      # starts with a forward slash. This code was added so that
      # paths such as '01.htm' (without the quotes) would actually
      # work. Note that '01.htm' (without the quotes) is actually
      # a valid path (apparently).
      if len(pageUrlCurrent) > 0 and \
         pageHost == None        and \
         pageScheme == None      and \
         pageUrlCurrent.startswith('/') == False:
        pageUrlCurrent = '/' + pageUrlCurrent
      # Add the host name and scheme as need be
      if pageHost == None:
        pageUrlCurrent = '//' + self.hostName + pageUrlCurrent
      if pageScheme == None:
        pageUrlCurrent = 'https' + ':' + pageUrlCurrent
      # Get the page using the passed function. Note that the call
      # below does not actually get the contents of the page. The
      # page contents are not actually fetched from the web site.
      try:
        pageContents = getPageFunc(pageUrlCurrent)
      except Exception as e:
        print('In HDLmWebSite.update invoking getPageFunc')
        print(pageUrlCurrent)
        print(str(e))
        self.crawlCount += 1
        continue
      # Get the hrefs from the page
      pageHrefs = getPageHrefs()
      # Check all of the hrefs from the page
      for href in pageHrefs: 
        # Check if we have seen this href before
        if href in self.pageDict:
          continue
        self.pageDict[href] = [False, pageUrlBase]
        self.pageList.append(href)
      self.crawlCount += 1
  # Get the dictionary of links that we have found so far
  # return it to the caller
  def getDict(self):
    return self.pageDict
  # Get the host name string and return it to the caller
  def getHost(self):
    return self.hostName
  # Get the list of links that we have found so far and
  # return it to the caller
  def getList(self):
    return self.pageList