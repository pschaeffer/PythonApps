# The methods of this class return configuration information
# to the caller

from HDLmConfig import *

class HDLmConfigInfo(object):
  # print('In class HDLmConfigInfo')
  # Build a configuration object. This object 
  # is used to get the configuration values.
  # The configuration values are stored in a  
  # dictionary that is a class variable.
  configObj = HDLmConfig()
  # Create a set of False values for use later
  falseValues = {
    'f', 'F',
    'n', 'N', 'no', 'No', 'NO',
    'false', 'False', 'FALSE',
    'off', 'Off', 'OFF',
    '0', 0, 0.0,
    False
  }
  # Create a set of None values for use later
  noneValues = {'null', 'Null', 'NULL', '', None}
  # Create a set of True values for use later
  trueValues = {
    't', 'T',
    'y', 'Y', 'yes', 'Yes', 'YES',
    'true', 'True', 'TRUE',
    'on', 'On', 'ON',
    '1', 1,
    True
  }
  # Get the AWS access key Id and return it to the caller. The    
  # AWS access key Id is stored in the configuration values and
  # is returned to the caller as a string. 
  @classmethod
  def getAwsAccessKeyId(cls):
    return HDLmConfigInfo.configObj.getValue('awsAccessKeyId') 
  # Get the AWS secret access key and return it to the caller.     
  # The AWS secret access key Id is stored in the configuration
  # values and is returned to the caller as a string. 
  @classmethod
  def getAwsSecretAccessKey(cls):
    return HDLmConfigInfo.configObj.getValue('awsSecretAccessKey') 
  # Get the standard maximum number of clusters and return
  # it to the caller. The maximum number of clusters is
  # always returned to the caller as a proper number, not
  # a string.
  @classmethod
  def getClustersMaxCount(cls):
    return int(HDLmConfigInfo.configObj.getValue('clustersMaxCount'))  
  # Get the standard clusters sample size and return it to 
  # the caller. The clusters sample size is always returned 
  # to the caller as a proper number, not a string.
  @classmethod
  def getClustersSampleSize(self):
    return int(HDLmConfigInfo.configObj.getValue('clustersSampleSize')) 
  # Get the clusters threshold and return it to the caller. The 
  # clusters threshold is the maximum similarity value for all 
  # members of a cluster. The actual algorithm only checks the
  # first member of a cluster against other possible entries. 
  # So it is possible, the entries in a cluster might differ
  # by more than the threshold value. The clusters threshold
  # value is always returned to the caller as a proper number
  # (a double-precision floating-point number), not a string.
  @classmethod
  def getClustersThreshold(cls):
    return float(HDLmConfigInfo.configObj.getValue('clustersThreshold')) 
  # Get the current environment. The current environment will 
	# be set to values such as  "prod" or "production" or "test" 
	# (without the quotes). Other values may be added later.  
  @classmethod
  def getCurrentEnvironment(cls):
    return HDLmConfigInfo.configObj.getValue('currentEnvironment')
  # Get the API type that is used to obtain the modifications
  # using the bridge. The most basic API just accesses the bucket.
  # Other APIs are more sophisticated. 
  @classmethod
  def getEntriesBridgeApi(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgeApi')
  # Get the company prefix value that may (or may not) come 
  # before the content value. If the company prefix value 
  # is set, it will always be followed by an underscore that
  # separates the company prefix value from the content value
  # (something like 'mod' or 'proxy'). The company prefix value 
  # should not start or end with an underscore. Other code will 
  # supply the underscore.
  @classmethod
  def getEntriesBridgeCompanyPrefix(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgeCompanyPrefix')   
  # Get the suffix value that follows the content value. Note
  # that an underscore always separates the content value
  # (something like 'mod' or 'proxy') from the suffix value,
  # if the suffix value is non-blank. The suffix value should
  # not start with an underscore. Other code will supply the
  # underscore.
  @classmethod
  def getEntriesBridgeContentSuffix(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgeContentSuffix')   
  # Get the URL that is used to delete from the  
  # table that contains the modifications
  @classmethod
  def getEntriesBridgeDeleteUrl(cls):
    return HDLmConfigInfo.getServerName() + HDLmConfigInfo.configObj.getValue('entriesBridgeDeleteUrl') 
  # Get the URL that is used to insert into the table that
  # contains the modifications
  @classmethod
  def getEntriesBridgeInsertUrl(cls):
    return HDLmConfigInfo.getServerName() + HDLmConfigInfo.configObj.getValue('entriesBridgeInsertUrl')
  # Get the method that is used to access the table that contains
  # the modifications
  @classmethod
  def getEntriesBridgeInternetMethod(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgeInternetMethod') 
  # Get part of the path that is used to access the table that contains
  # the modifications
  @classmethod
  def getEntriesBridgePartialPath(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgePartialPath') 
  # Return the configuration password
  @classmethod
  def getEntriesBridgePassword(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgePassword') 
  # Get the URL that is used to access the table that contains
  # the modifications
  @classmethod
  def getEntriesBridgeReadUrl(cls):
    return HDLmConfigInfo.getServerName() + HDLmConfigInfo.configObj.getValue('entriesBridgeReadUrl') 
  # Get the table name that contains the modifications. This is the
  # table that has all of the rules as separate rows.
  @classmethod
  def getEntriesBridgeTableSeparate(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgeTableSeparate') 
  @classmethod
  # Get the URL that is used to update the table that contains
  # the modifications
  @classmethod
  def getEntriesBridgeUpdateUrl(cls):
    return HDLmConfigInfo.getServerName() + HDLmConfigInfo.configObj.getValue('entriesBridgeUpdateUrl') 
  # Return the bridge use cache value
  @classmethod
  def getEntriesBridgeUseCache(cls):
    curVal = HDLmConfigInfo.configObj.getValue('entriesBridgeUseCache')
    if curVal in HDLmConfigInfo.falseValues:
      return False
    if curVal in HDLmConfigInfo.trueValues:
      return True
    return None
  # Return the configuration userid
  @classmethod
  def getEntriesBridgeUserid(cls):
    return HDLmConfigInfo.configObj.getValue('entriesBridgeUserid')  
  # Get the company prefix value that may (or may not) come 
  # before the content value. If the company prefix value 
  # is set, it will always be followed by an underscore that
  # separates the company prefix value from the content value
  # (something like 'mod' or 'proxy'). The company prefix value 
  # should not start or end with an underscore. Other code will 
  # supply the underscore.
  @classmethod
  def getEntriesDatabaseCompanyPrefix(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseCompanyPrefix')
  # Get the suffix value that follows the content value. Note
  # that an underscore always separates the content value
  # (something like 'mod' or 'proxy') from the suffix value,
  # if the suffix value is non-blank. The suffix value should
  # not start with an underscore. Other code will supply the
  # underscore.
  @classmethod
  def getEntriesDatabaseContentSuffix(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseContentSuffix') 
  # Get the database name that is used to access the table that contains
  # the production modifications. The database name is returned to the 
  # caller as a string. The database name is stored in the configuration
  # values. 
  @classmethod
  def getEntriesDatabaseDatabaseNameProd(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseDatabaseNameProd')  
  # Get the database name that is used to access the table that contains
  # the test modifications. The database name is returned to the caller
  # as a string. The database name is stored in the configuration
  # values. 
  @classmethod
  def getEntriesDatabaseDatabaseNameTest(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseDatabaseNameTest')
  # Get the host name that is used to access the table that contains
  # the production modifications. The host name is returned to the 
  # caller as a string. The host name is stored in the configuration
  # values. The host name is actually a secret value. The host name 
  # is stored in the AWS Secrets Manager as part of the database 
  # secret values.
  @classmethod
  def getEntriesDatabaseDomainNameProd(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseDomainNameProd')
  # Get the host name that is used to access the table that contains
  # the test modifications. The host name is returned to the caller
  # as a string. The host name is stored in the configuration
  # values. 
  @classmethod
  def getEntriesDatabaseDomainNameTest(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseDomainNameTest')
  # Get the domain name that is used to insert into the table that
  # contains the modifications
  @classmethod
  def getEntriesDatabaseInsertDomainName(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseInsertDomainName') 
  # Get the method that is used to access the table that contains
  # the modifications
  @classmethod
  def getEntriesDatabaseInternetMethod(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseInternetMethod')
  # Get the password that is used to access the table that contains
  # the modifications. This value is returned to the caller as a string.
  # The password is stored in the configuration values. The password is
  # actually a secret value that should not be shared with others and 
  # is stored in the AWS Secrets Manager.
  @classmethod
  def getEntriesDatabasePassword(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabasePassword')
  # Get the table name that contains the modifications. This is the
  # table that has all of the rules as one very large JSON object.
  # This approach (using one very large JSON object) is no longer
  # in use. Instead, we create one row for each rule and some other
  # types of nodes as well. 
  @classmethod
  def getEntriesDatabaseTableName(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseTableName') 
  # Return the database use cache value
  @classmethod
  def getEntriesDatabaseUseCache(cls):
    curVal = HDLmConfigInfo.configObj.getValue('entriesDatabaseUseCache') 
    if curVal in HDLmConfigInfo.falseValues:
      return False
    if curVal in HDLmConfigInfo.trueValues:
      return True
    return None
  # Get the userid that is used to access the table that contains
  # the modifications. This value is returned to the caller as a string.
  # The userid is stored in the configuration values. The userid is
  # actually a secret value that should not be shared with others and
  # is stored in the AWS Secrets Manager.
  @classmethod
  def getEntriesDatabaseUserid(cls):
    return HDLmConfigInfo.configObj.getValue('entriesDatabaseUserid')
  # Get the Open AI API key value. The Open AI API key value is
  # returned to the caller as a string. The Open AI API key value
  # is used to access the Open AI API. The Open AI API key value
  # is stored in the configuration values.
  @classmethod
  def getOpenAIApiKey(cls):
    return HDLmConfigInfo.configObj.getValue('openAIApiKey')
  # Get the pass-through limit value abd return it to the caller. The
  # pass-through limit value determines the fraction of events that are
  # treated as null events (nothing is changed). The value is treated as
  # a percentage and can be a non-integer value (such as 5.5). If this
  # value is set to zero, no events will be treated as null events. If
  # this value is set to 10.0, then 10% of events will be treated as null
  # events. If this value is set to 100.0, then all events will be treated
  # as null events.
  @classmethod
  def getPassThroughLimit(cls):
    return float(HDLmConfigInfo.configObj.getValue('passThroughLimit')) 
	# Get the name of of the perceptual hash program. The name of pHash
	# program is returned to the caller.
  @classmethod
  def getPHashName(cls):
    return HDLmConfigInfo.configObj.getValue('phashName') 
  # Get the standard WebSocket server (listener) port number and
  # return it to the caller. The port number is always returned 
  # to the caller as a proper number, not a string.
  @classmethod
  def getPortNumberWebSocket(cls):
    return int(HDLmConfigInfo.configObj.getValue('portNumberWebSocket')) 
	# Get the name of of the proxy program (originally written in a different
	# language) that must be simulated by this code
  @classmethod
  def getProxyName(cls):
    return HDLmConfigInfo.configObj.getValue('proxyName') 
  # Get the name of of the field that contains the current request type 
  @classmethod
  def getRequestTypeName(cls):
    return HDLmConfigInfo.configObj.getValue('requestTypeName') 
  # Get the current server name used to handle POST requests
  # and perhaps other things. Return the server name to the 
  # caller as a string.  
  @classmethod
  def getServerName(cls):
    return HDLmConfigInfo.configObj.getValue('serverName') 
  # Get the name of of the field that contains the current URL value
  @classmethod
  def getUrlValueName(cls):
    return HDLmConfigInfo.configObj.getValue('urlValueName') 