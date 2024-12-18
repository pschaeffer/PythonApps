# The methods of this class return configuration information
# to the caller

from HDLmAwsUtility import * 

class HDLmConfig(object):
  # Create a map for use below
  configValues = dict()
  # A reference to the configuration values is stored
  # in the configuration object. Note that this is a class 
  # (static) variable. This means that the values are shared
  # by all instances of the class and only one copy of the
  # values exists.
  #
  # The entries in this dict/map are also in the Java and 
  # JavaScript code 
  configValues["awsAccessKeyId"]                  = ""   
  configValues["awsSecretAccessKey"]              = ""
  configValues["clustersMaxCount"]                = "10"
  configValues["clustersSampleSize"]              = "100"
  configValues["clustersThreshold"]               = "0.10"
  configValues["companyName"]                     = "example.com"
  configValues["currentEnvironment"]              = "prod"
  configValues["entriesBridgeApi"]                = "bucket"
  configValues["entriesBridgeCompanyPrefix"]      = ""
  configValues["entriesBridgeContentSuffix"]      = "java"
  configValues["entriesBridgeDeleteUrl"]          = "/io/bucket/delete/"
  configValues["entriesBridgeInsertUrl"]          = "/io/bucket/insert/"
  configValues["entriesBridgeInternetMethod"]     = "https"
  configValues["entriesBridgePartialPath"]        = "io/bucket"
  configValues["entriesBridgePassword"]           = ""
  configValues["entriesBridgeReadUrl"]            = "/io/bucket/search/"
  configValues["entriesBridgeTableSeparate"]      = "main_9"
  configValues["entriesBridgeUpdateUrl"]          = "/io/bucket/update/"
  configValues["entriesBridgeUseCache"]           = "false"
  configValues["entriesBridgeUserid"]             = ""
  configValues["entriesDatabaseCompanyPrefix"]    = ""
  configValues["entriesDatabaseContentSuffix"]    = "java"
  configValues["entriesDatabaseDatabaseNameProd"] = "main_9"
  configValues["entriesDatabaseDatabaseNameTest"] = "test_1"
  configValues["entriesDatabaseDomainNameProd"]   = ""
  configValues["entriesDatabaseDomainNameTest"]   = "test-1.cluster-c7czx6cxnjsz.us-east-2.rds.amazonaws.com"
  configValues["entriesDatabaseInternetMethod"]   = "https"
  configValues["entriesDatabasePassword"]         = ""	
  configValues["entriesDatabaseTableName"]        = "main_9"
  configValues["entriesDatabaseUseCache"]         = "false"
  configValues["entriesDatabaseUserid"]           = ""	
  configValues["fixWebSockets"]                   = "true"
  configValues["logFileName"]                     = "info.log"
  configValues["logRuleMatching"]                 = "false"
  configValues["openAIApiKey"]                    = ""	
  configValues["parametersAccessMethod"]          = "cgi-bin/get-set.py?get"
  configValues["parametersInternetMethod"]        = "http"
  configValues["parametersUpdateMethod"]          = "cgi-bin/get-set.py?set"
  configValues["parametersUrl"]                   = "headlamp-software.com"
  configValues["passThroughLimit"]                = "5.0"
  configValues["phashName"]                       = "HDLmPHash"
  # The port number below is hardcoded into the browser extension
  # that uses WebSockets to send node identifier values to the 
  # Electron JS application. Of course, this is Python code where
  # JavaScript and Electron JS will never be used. However, we do 
  # need to be complete. 
  configValues["portNumberWebSocket"]             = "8102"
  configValues["proxyName"]                       = "HDLmProxy.php"
  configValues["requestTypeName"]                 = "HDLmRequestType"
  configValues["serverName"]                      = "javaproxya.dnsalias.com"
  configValues["supportHTTP2"]                    = "true"		
  configValues["urlValueName"]                    = "HDLmUrlValue"
  # The code below does some of the work needed to set the configuration
  # values. This code gets some secrets from the AWS Secrets Manager and
  # stores them in the configuration values. 
  mainList = [
               # The order here is, where to put the configuration value, the AWS name of the value, and the JSON key,
               # if any. 
               ["awsAccessKeyId", "AwsAccessKeyId", ""], 	
               ["awsSecretAccessKey", "AwsSecretAccessKey", ""],
               ["openAIApiKey", "OpenApiAiKeySchaeffer", ""],
               ["entriesDatabaseUserid", "Main9Auroa", "username"],
               ["entriesDatabasePassword", "Main9Auroa", "password"],
               ["entriesDatabaseDomainNameProd", "Main9Auroa", "host"],
               # ["entriesDatabaseDatabaseNameProd", "Main9Auroa", "dbClusterIdentifier"]
               ["entriesBridgePassword", "EntriesBridgePassword", ""],
               ["entriesBridgeUserid", "EntriesBridgeUserid", ""]
             ]
  # Build a list of AWS secret names 
  secretsNames = []
  for secretInfo in mainList:
    secretName = secretInfo[1]
    if secretName not in secretsNames: 
      secretsNames.append(secretName);  		
  # Get the actual secrets from the AWS Secrets Manager
  client = HDLmAwsUtility.buildAwsSecretsManagerClient("us-east-2")
  secretsMap = HDLmAwsUtility.getAMapOfSecrets(client, secretsNames)
  # Store each of the secrets in the configuration values 
  for secretInfo in mainList:
    secretConfigName = secretInfo[0]
    secretAwsName = secretInfo[1]
    secretAwsJsonKey = secretInfo[2]
    # Get the secret value from the map 
    secretAwsValue = secretsMap[secretAwsName]
    # Check if we need to extract the actual secret from some JSON *
    if secretAwsJsonKey != "":
      # Convert the JSON string to an object
      secretJsonObject = json.loads(secretAwsValue) 
      actualSecretValue = secretJsonObject[secretAwsJsonKey]
      configValues[secretConfigName] = actualSecretValue
    else:
      configValues[secretConfigName] = secretAwsValue	  
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
    if valueStr not in self.configValues:
      errorText = f'Value ({valueStr}) is not in the configuration values'
      raise ValueError(errorText)
    return self.configValues[valueStr]
  # This routine sets one configuration value. If the value already
  # exists, it is replaced. If the value does not exist, it is added.
  # This routine is no longer used. Actually, it is used by a routine
  # that is no longer used.
  @classmethod
  def setConfigValueNotUsed(self, configName, configValue):
    # Check a few values passed by the caller
    if configName == None:
      errorText = 'The name of the configuration value is not set'
      raise ValueError(errorText)
    # Check the type of the configuration name
    if type(configName) != type(''):
      errorText = f'The name ({configName}) of the configuration value is not a string'
      raise ValueError(errorText)
    # Check the length of the configuration name
    if len(configName) <= 0:
      errorText = 'The length of the configuration name is invalid' 
      raise ValueError(errorText)
    # Check if the configuration value is set
    if configValue == None:
      errorText = 'The configuration value is not set'
      raise ValueError(errorText)
    # Check the type of the configuration Value
    if type(configValue) != type(''):
      errorText = f'The type of the configuration value ({configValue}) is not a string'
      raise ValueError(errorText)
    # Check the length of the configuration Value
    if len(configValue) <= 0:
      errorText = 'The length of the configuration Value is invalid' 
      raise ValueError(errorText)
    self.configValues[configName] = configValue
  # This routine does all of the work needed to set the configuration
  # values. Some secrets are stored in the configuration values. This 
  # routine gets the secrets from the AWS Secrets Manager and stores 
  # them in the configuration values. This routine is no longer used.
  @staticmethod
  def setConfigValuesNotUsed():
    mainList = []
		# The order here is, where to put the configuration value, the AWS name of the value, and the JSON key,
		# if any. 
    infoAwsAccessKeyId = ["awsAccessKeyId", "AwsAccessKeyId", ""] 	
    infoAwsSecretAccessKey =	["awsSecretAccessKey", "AwsSecretAccessKey", ""]
    infoOpenAiKey = ["openAIApiKey", "OpenApiAiKeySchaeffer", ""]
    infoAwsDatabaseUserid = ["entriesDatabaseUserid", "Main9Auroa", "username"]
    infoAwsDatabasePassword = ["entriesDatabasePassword", "Main9Auroa", "password"]
		# The value that was obtained below was not the actual database name. It is not clear what this
		# value really is/was.  
    if False:
      infoAwsDatabaseDatabaseNameProd = ["entriesDatabaseDatabaseNameProd", "Main9Auroa", "dbClusterIdentifier"]
    infoAwsDatabaseDomainNameProd = ["entriesDatabaseDomainNameProd", "Main9Auroa", "host"]
    infoAwsEntriesUserid = ["entriesBridgeUserid", "EntriesBridgeUserid", ""]
    infoAwsEntriesPassword = ["entriesBridgePassword", "EntriesBridgePassword", ""]
		# Add each set of information about an AWS secret to the main list
    mainList.append(infoAwsAccessKeyId)
    mainList.append(infoAwsSecretAccessKey)
    mainList.append(infoOpenAiKey)
    mainList.append(infoAwsDatabaseUserid)
    mainList.append(infoAwsDatabasePassword)
		# The value that was obtained below was not the actual database name. It is not clear what this
	  # value really is/was.  
    if False:
      mainList.append(infoAwsDatabaseDatabaseNameProd)
    mainList.append(infoAwsDatabaseDomainNameProd)
    mainList.append(infoAwsEntriesUserid)
    mainList.append(infoAwsEntriesPassword)
	  # Build a list of AWS secret names 
    secretsNames = []
    for secretInfo in mainList:
      secretName = secretInfo[1]
      if secretName not in secretsNames: 
        secretsNames.append(secretName);  		
		# Get the actual secrets from the AWS Secrets Manager
    client = HDLmAwsUtility.buildAwsSecretsManagerClient("us-east-2")
    secretsMap = HDLmAwsUtility.getAMapOfSecrets(client, secretsNames)
	  # Store each of the secrets in the configuration values 
    for secretInfo in mainList:
      secretConfigName = secretInfo[0]
      secretAwsName = secretInfo[1]
      secretAwsJsonKey = secretInfo[2]
			# Get the secret value from the map 
      secretAwsValue = secretsMap[secretAwsName]
	    # Check if we need to extract the actual secret from some JSON *
      if secretAwsJsonKey != "":
				# Convert the JSON string to an object
        secretJsonObject = json.loads(secretAwsValue) 
        actualSecretValue = secretJsonObject[secretAwsJsonKey]
        HDLmConfig.setConfigValueNotUsed(secretConfigName, actualSecretValue)
      else:
        HDLmConfig.setConfigValueNotUsed(secretConfigName, secretAwsValue)	