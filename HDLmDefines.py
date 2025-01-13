# The HDLmDefines class doesn't actually do anything. However, 
# it does serve to hold all of the values defined with define. 
#
# The methods of this class return define values to the
# caller

from HDLmAssert import *
 
class HDLmDefines(object):
  # Create a set of values for use later
  #
  # The following data structure contains information about all 
  # of the standard defines. The standard defines are used in many
  # places in the code. Note that the Java code has another copy of
  # these values. The JavaScript code also has a copy of these values.
  HDLmDefinesConstants = { 
    "HDLMAPICHECKUSERNAMEPASSWORD":       "checkUsernamePassword",
    "HDLMAPICHECKLASTTIME":               "checkLastTime",
    "HDLMAPIGETUSER":                     "getUser",
    "HDLMAPISETPASSWORD":                 "setPassword",
    "HDLMAPIVERIFYCODE":                  "verifyCode",
    "HDLMBACKGROUNDCOLORHEX":             "00BFFF",
    "HDLMBACKGROUNDCOLORRGB":             "0, 191, 255",
    "HDLMBUILDJSNAME":                    "HDLmBuildJs",
    "HDLMBUILDSETTESTOFF":                "HDLmBuildSetTestOff",
    "HDLMBUILDSETTESTON":                 "HDLmBuildSetTestOn",
    "HDLMCOMPANIESNODENAME":              "Companies",
    "HDLMCOMPANIESTYPE":                  "companies",
    "HDLMCOMPANYTYPE":                    "company",
    "HDLMCONFIGS":                        "HDLmConfigs",
    "HDLMCURENV":                         "HDLm_Cur_Env",
    "HDLMDATANODENAME":                   "Data",
    "HDLMDATATYPE":                       "data",
    "HDLMDEBUGENABLED":                   "HDLmDebugEnabled",
    "HDLMDEFAULTMODNAME":                 "Modification",
    "HDLMDIVISIONNODENAME":               "example.com",
    "HDLMDIVISIONTYPE":                   "division",
    "HDLMDOMDOCUMENT":                    "DOMDocument",
    "HDLMDOMELEMENT":                     "DOMElement",
    "HDLMENTRYDESCRIPTIONS":              "#entryDescriptions",
    "HDLMENTRYVALUES":                    "#entryValues",
    "HDLMERRORTEXT":                      "HDLmErrorText",
    "HDLMEXPECTEDFILENAME":               "HDLmExpectedGetJsOutput.txt",
    "HDLMFANCYTREE":                      "#tree",
    "HDLMFIXEDFILENAME":                  "HDLmFixedJs.txt",
    "HDLMFONTSIZEMAX":                    300,
    "HDLMFONTSIZEMIN":                    1,
    "HDLMFORCEVALUE":                     "TCELESECROF",
    "HDLMFULLVALUENAME":                  "Value",
    "HDLMGEMPREFIX":                      "HDLmGemPrfx",
    "HDLMGETDATA":                        "HDLmGetData",
    "HDLMGETJSVALUE":                     "HDLmGetJS",
    "HDLMGXEPREFIX":                      "HDLmGxePrfx",
    "HDLMLEFTDEF":                        "leftDef",
    "HDLMHEIGHTMAX":                      2000,
    "HDLMHEIGHTMIN":                      1,
    "HDLMHOSTNAME":                       "HDLm_Host_Name",
	  "HDLMHOSTOS":                         "HDLm_Host_OS",	  
	  "HDLMHOSTUSERDIR":                    "HDLm_Host_UserDir",
    "HDLMHTMLFOOTER":                     "#footer",
    "HDLMHTMLHEADER":                     "#header",
    "HDLMIGNORELISTSNODENAME":            "Ignore Lists",
    "HDLMINLINELEFT":                     "#entryLeft",
    "HDLMINLINERIGHT":                    "#entryRight",
    "HDLMINVALIDNODENAME":                "Invalid",
    "HDLMINVOKEAPI":                      "HDLmInvokeApi",
    "HDLMLASTARRAYSIZE":                  100,
    "HDLMLEFTANDRIGHTPAGE":               "leftAndRightPage",
    "HDLMLOADMODNAME":                    "load",
    "HDLMLOADPAGEMODNAME":                "load page",
    "HDLMLOADPAGEMODNAMEOLD":             "load",
    "HDLMMAXCHANGES":                     100,
    "HDLMMAXIDENTEXTLEN":                 20,
    "HDLMMAXJSONERRORLEN":                50,
    "HDLMMAXMODNODEPATHLENGTH":           5,
    "HDLMMAXMODNODERPATHLENGTH":          7,
    "HDLMMAXPARAMETERCOUNT":              1000,
    "HDLMMODS":                           "HDLmMods",
    "HDLMNODEPATH":                       "HDLmNodePath",
    "HDLMOVERALLNODENAME":                "Overall",
    "HDLMPLUSSIGN":                       "HDLmPlusSign",
    "HDLMPOSTDATA":                       "HDLmPostData",
    "HDLMPREFIX":                         "HDLm",
    "HDLMREPORTNAMEPREFIX":               "Report",
	  "HDLMREPORTSNODENAME":                "Reports",
    "HDLMRIGHTDEF":                       "rightDef",
    "HDLMRULESNODENAME":                  "Rules",
    "HDLMRULESNODEPATHLENGTH":            7,
    "HDLMRULESTYPE":                      "rules",
    "HDLMSESSIONCLASSES":                 "HDLmSessionClasses",
    "HDLMSESSIONCOOKIE":                  "HDLmSessionCookie",
    "HDLMSESSIONDEBUGRULESENABLED":       "HDLmSessionDebugRulesEnabled",
    "HDLMSESSIONID":                      "HDLmSessionId",
    "HDLMSESSIONDEBUGNODEIDENENABLED":    "HDLmSessionDebugNodeIdenEnabled",
    "HDLMSESSIONPASSWORD":                "HDLmSessionPassword",
    "HDLMSESSIONPOSTRULETRACINGENABLED":  "HDLmSessionPostRuleTracingEnabled",
    "HDLMSESSIONRULEINFODIVISIONNAME":    "HDLmSessionRuleInfoDivisionName",
    "HDLMSESSIONRULEINFOHOSTNAME":        "HDLmSessionRuleInfoHostName",
    "HDLMSESSIONRULEINFOSITENAME":        "HDLmSessionRuleInfoSiteName",
    "HDLMSESSIONUSERNAME":                "HDLmSessionUserName",
    "HDLMSETLASTTIME":                    "setLastTime",
    "HDLMSHORTMODNAME":                   "Mod",
    "HDLMSITENODEPATHLENGTH":             6,
    "HDLMSITENODENAME":                   "example.com",
    "HDLMSITETYPE":                       "site",
    "HDLMSYSTEMPROD":                     "prod",
	  "HDLMSYSTEMTEST":                     "test",
	  "HDLMTIMINGSARRAYSIZE":               200,
    "HDLMTOPNODENAME":                    "Top",
    "HDLMTOPNODEPATHLENGTH":              1,
    "HDLMTOPNODETYPE":                    "top",
    "HDLMTREE":                           "HDLmTree",
    "HDLMTYPECOMPANIES":                  15,
	  "HDLMTYPECOMPANY":                    2,
	  "HDLMTYPECONFIG":                     6,
	  "HDLMTYPEDIVISION":                   3,
	  "HDLMTYPEIGNORE":                     9,
	  "HDLMTYPELINE":                       12,
	  "HDLMTYPELINES":                      13,
	  "HDLMTYPELIST":                       8,
	  "HDLMTYPELISTS":                      14,
	  "HDLMTYPEMOD":                        5,
	  "HDLMTYPEREPORT":                     11,
	  "HDLMTYPEREPORTS":                    10,
	  "HDLMTYPERULES":                      16,
	  "HDLMTYPESITE":                       4,
	  "HDLMTYPESTORE":                      7,
	  "HDLMTYPETOP":                        1,
    "HDLMUPDATED":                        "HDLmUpdated",
    "HDLMUSEARRAYSIZE":                   100,
    "HDLMVALIDNODENAME":                  "Valid",
    "HDLMVALUETYPE":                      "value",
    "HDLMWIDTHMAX":                       4000,
    "HDLMWIDTHMIN":                       1
                         }   
  # This method returns the numeric value of a define
  # if the define name is valid (exists) and if the define
  # value is actually a number (not a string)
  @classmethod 
  def getNumber(cls, defineName):
    # Make sure the value passed by the caller is a string  
    if type(defineName) is not str: 
      errorText = f'Define ({defineName}) name value passed to getNumber method is not a string'
      HDLmAssert(False, errorText)
		# Check if the define name passed by the caller is valid
		# or not. We need to raise an exception if the define name
		# passed by the caller is unknown. 
    if defineName not in HDLmDefines.HDLmDefinesConstants:
      errorText = f'Invalid define name ({defineName}) passed to getNumber'
      HDLmAssert(False, errorText)
		# Get the value from the object and check if the value is not a number. 
    # This method can only be used to obtain values that are actually numbers. 
    rv = HDLmDefines.HDLmDefinesConstants[defineName]
    rvType = str(type(rv))
    if rvType != "<class 'int'>"    and \
       rvType != "<class 'float'>"  and \
       rvType != "<class 'complex'>":
      errorText = f'Value of define name ({defineName}) is not a number'
      HDLmAssert(False, errorText) 
    return rv
  # This method returns the string value of a define
  # if the define name is valid (exists) and if the define
  # value is actually a string (not a number)
  @classmethod
  def getString(cls, defineName):
    # Make sure the value passed by the caller is a string 
    if type(defineName) is not str:
      errorText = f'Define ({defineName}) name value passed to getString method is not a string'
      HDLmAssert(False, errorText) 
		# Check if the define name passed by the caller is valid
		# or not. We need to raise an exception if the define name
		# passed by the caller is unknown. 
    if defineName not in HDLmDefines.HDLmDefinesConstants:
      errorText = f'Invalid Define Name ({defineName}) passed to getString'  
      HDLmAssert(False, errorText)
		# Get the value from the object and check if the value is not a string. 
    # This method can only be used to obtain values that are actually strings. 
    rv = HDLmDefines.HDLmDefinesConstants[defineName]
    rvType = str(type(rv))
    if rvType != "<class 'str'>":     
      errorText = f'Value of define name ({defineName}) is not a string' 
      HDLmAssert(False, errorText)
    return rv