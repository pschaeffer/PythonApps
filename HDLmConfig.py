# The methods of this class return configuration information
# to the caller

class HDLmConfig(object):
  # The __init__ method creates an instance of the class
  def __init__(self):
    # Create a map for use below
    configDict = dict()
    # The entries in this map are also in the Java and JavaScript code 
    configDict["clustersMaxCount"]                = "10"
    configDict["clustersSampleSize"]              = "100"
    configDict["clustersThreshold"]               = "0.10"
    configDict["companyName"]                     = "example.com"
    configDict["currentEnvironment"]              = "prod"
    configDict["entriesBridgeApi"]                = "bucket"
    configDict["entriesBridgeCompanyPrefix"]      = ""
    configDict["entriesBridgeContentSuffix"]      = "java"
    configDict["entriesBridgeDeleteUrl"]          = "/io/bucket/delete/"
    configDict["entriesBridgeInsertUrl"]          = "/io/bucket/insert/"
    configDict["entriesBridgeInternetMethod"]     = "https"
    configDict["entriesBridgePartialPath"]        = "io/bucket"
    configDict["entriesBridgePassword"]           = "headlamp"
    configDict["entriesBridgeReadUrl"]            = "/io/bucket/search/"
    configDict["entriesBridgeTableSeparate"]      = "main_9"
    configDict["entriesBridgeUpdateUrl"]          = "/io/bucket/update/"
    configDict["entriesBridgeUseCache"]           = "false"
    configDict["entriesBridgeUserid"]             = "admin"
    configDict["entriesDatabaseCompanyPrefix"]    = ""
    configDict["entriesDatabaseContentSuffix"]    = "java"
    configDict["entriesDatabaseInternetMethod"]   = "https"
    configDict["entriesDatabaseTableName"]        = "main_9"
    configDict["entriesDatabaseUseCache"]         = "false"
    configDict["fixWebSockets"]                   = "true"
    configDict["logFileName"]                     = "info.log"
    configDict["logRuleMatching"]                 = "false"
    configDict["parametersAccessMethod"]          = "cgi-bin/get-set.py?get"
    configDict["parametersInternetMethod"]        = "http"
    configDict["parametersUpdateMethod"]          = "cgi-bin/get-set.py?set"
    configDict["parametersUrl"]                   = "headlamp-software.com"
    configDict["passThroughLimit"]                = "5.0"
    configDict["phashName"]                       = "HDLmPHash"
    # The port number below is hardcoded into the browser extension
    # that uses WebSockets to send node identifier values to the 
    # Electron JS application. Of course, this is Python code where
    # JavaScript and Electron JS will never be used. However, we do 
    # need to be complete. 
    configDict["portNumberWebSocket"]             = "8102"
    configDict["proxyName"]                       = "HDLmProxy.php"
    configDict["requestTypeName"]                 = "HDLmRequestType"
    configDict["serverName"]                      = "javaproxya.dnsalias.com"
    configDict["supportHTTP2"]                    = "true"		
    configDict["urlValueName"]                    = "HDLmUrlValue"
    # Store a reference to the configuration map in the 
    # configuration  object
    self.map = configDict 
  # This routine adds any missing fields to a configuration object.
  # A configuration object in this case means a modification object
  # being used to build a configuration. 
  @staticmethod
  def addMissingConfigObject(newConfig):
    # Add any missing fields to the configuration object (actually
    # a modification object) passed by the caller 
    typeInfo = HDLmConfig.HDLmConfigInfo
    configInfo = typeInfo['config']
    configInfoArray = configInfo['fields']
    configArrayLength = len(configInfoArray) 
    # Process each of the entries in the array. Check if the field
    # already exists or not. 
    for i in range(0, configArrayLength):
      fieldSource = configInfoArray[i].source
      fieldType = configInfoArray[i].fieldtype
      # Add a default (empty or false) value, if need be 
      if hasattr(newConfig, fieldSource) == False:
        if fieldType == 'checkbox':
          newConfig[fieldSource] = False
        else:
          newConfig[fieldSource] = '' 
      # Since the field already has a value, check the value
      # in some cases 
      else:
        if fieldType == 'checkbox' and \
           newConfig[fieldSource] == '':
          newConfig[fieldSource] = False
  # Get a configuration value
  def getValue(self, valueStr):
    # Check if the value is in the configuration map
    if valueStr not in self.map:
      errorText = f'Value ({valueStr}) is not in the configuration map'
      raise ValueError(errorText)
    return self.map[valueStr]