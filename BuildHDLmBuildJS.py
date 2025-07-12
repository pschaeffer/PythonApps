# This Python program builds a Java program, that in turns builds a JavaScript 
# program when it is run. The Java program becomes part of the Java server and
# is called to build a JavaScript program for each client.

# A few things are not successfully compressed by this code. The text 'new Object()' 
# should be handled some other way. Braces are not treated as operators (but should
# be). The phrase '{ sensitivity:'accent' }' should be more compressed than it is.
# The phrase 'background-color: yellow' should be more compressed than it is. The 
# phrase 'filter: grayscale(100%)' should be more compressed than it it. 
 
from   HDLmString  import *
from   HDLmUtility import *
import jsons
import os
import pycurl
import sys 
import time 

glbDebug = True
glbInfile = HDLmDefines.getString('HDLMBUILDJSNAME') + '.txt'
glbJavaFilePath = '../../../../../HeadlampJetty/workspace-4.33.0/ProxyServerA/src/com/headlamp/' 
glbOutFile = HDLmDefines.getString('HDLMBUILDJSNAME') 
glbNoMatchFile = 'HDLmNoMatch.txt'
glbPythonWorkPath = '../../PythonApps/PythonApps/'       
glbVarList = [
             'actualText',             
             'actualTextLower',
             'arrayLength',
             'arrayType',
             'attrObj',
             'attrObjName',
             'attributeName', 
             'attributeRequest',
             'attributeValue',
             'attrs',
             'attrsLength',
             # 'back',
             'backLast',
             'backStr',
             'backType',
             'builtStr',
             # 'changes',
             'changesMatch',
             'changesObj',
             'changesType',
             'changesValue',
             # 'child',
             # 'children',
             # 'childrenLength',
             # 'computed',
             'computedStyle',
             'countHigh',
             'curArray',
             'curChild',
             'curChildren',
             'curChildrenLength',
             'currentMatchValue',
             'curMod',
             'curModExtra',
             'curModExtraArray',
             'curModExtraLower',
             'curModLen',
             'curModSplit',
             'curModSplitLength',
             'curNode',
             'currentCount',
             'currentElement',
             'curStr',
             'curStyle',
             'curType',
             'curValue',
             'dataStr',
             'denominator',
             # 'Disabled',
             'disabledStatus',
             # 'distance',
             'distanceCount',
             'distanceFinal',
             'distanceValue',
             # 'divisionName',
             'divisionNameStr',
             'divisionNameValue',
             'domElement',
             'domNode',
             'domObj',
             'domSubNode',
             'domSubNodes',
             'domSubNodesLength',
             'domSubNodeNode',
             'domText',
             # 'Double',
             'elementClasses',
             'elementNodeReference',
             'elementLoop',
             'errNumber',
             'errorObj',
             'errorStr',
             'errorText',
             'errSeverity',
             'errText', 
             'eventJson',
             'eventName',
             # 'extra',
             'extraStr',
             # 'finalDistance', 
             'finalUrl', 
             # 'find', 
             'findEntry', 
             'findFirst',
             # 'finds', 
             'findsArray' ,
             'findsArrayLength', 
             # 'first', 
             'firstElement', 
             'firstInt', 
             'firstStr', 
             'firstSub', 
             'firstVal',
             'fontNames', 
             'forceBreak',
             'forceReadyState',
             'forceSelectFound',
             'forceSelectString',
             'forceSelectStringValue',
             'grandParentElement',
             'grandParentMatchValue',
             'HDLmApplyMod',
             'HDLmApplyMods',
             'HDLmArrayJoin',
             'HDLmBuildError',
             'HDLmBuildErrorRule',
             'HDLmBuildNodeFromObject',
             'HDLmBuildOrder',
             'HDLmBuildSuffix',
             'HDLmChangeAttributes',
             'HDLmChangeNodes',
             'HDLmCheckTextMatches',
             'HDLmCheckVariable',
             'HDLmClassAddClass',
             'HDLmClassAddCss',
             'HDLmClassAddEntry',
             'HDLmClassAddSpecialClass',
             'HDLmCompareCaseInsensitive',
             'HDLmErrorToString',
             'HDLmFind',
             'HDLmFindNodeIden',
             'HDLmFindNodeIdenCheck',
             'HDLmFindNodeIdenMatch',
             'HDLmFindOneLevel',
             'HDLmFindPHash',
             'HDLmGetAllPropertyNames',
             'HDLmGetAttributesString',
             'HDLmGetBackground',
             'HDLmGetJsonForEventObject',
             'HDLmGetJsonForLink',
             'HDLmGetLookupIndex',
             'HDLmGetLookupValue',
             'HDLmGetObjectName',
             'HDLmGetParametersArray',
             'HDLmGetPHash',
             'HDLmGetUpdateCount',
             'HDLmHammingDistance',
             'HDLmHammingDistanceAdjusted',
             'HDLmHammingDistanceLong',
             'HDLmHandleVisitRequest',
             'HDLmIncrementUpdateCount',
             'HDLmIndexValue',
             'HDLmModifySearch',
             'HDLmNodeIdenTracing',
             'HDLmObsCallback',
             'HDLmObsConfig',
             'HDLmObsObserver',
             'HDLmObsTargetNode',
             'HDLmObtainValue',
             'HDLmPHashObject',
             'HDLmRemoveHost',
             'HDLmRemoveProtocol',
             'HDLmReplaceInString',
             'HDLmResetStyleSheetEnablement',
             'HDLmSaveChange',
             'HDLmSaveData',
             'HDLmSavedExtracts',
             'HDLmSavedNotifies',
             'HDLmSavedUpdates',
             'HDLmSendData',
             'HDLmSendUpdates',
             'HDLmStyleFixValues',
             'HDLmStyleSplitString',
             'HDLmToggleStyleSheetEnablement',
             'HDLmUpdateJsonStr',
             # 'hostName',
             'hostNameStr',
             'hostNameValue',
             'httpReq',
             # 'indexUsed',
             # 'indexValue',
             'indexValueUsed',
             'inStr',
             'inputSplit',
             'inputString',
             'inputStyles',
             'ix',
             # 'JavaScript',
             'joinChar',
             # 'JS', 
             # 'JSON',
             # 'JSONArray',
             # 'JSONElement',
             # 'JSONObject',
             'jsonObj',
             # 'JSONParser',
             'jsonStr',
             'jsonText',
             'keyStr',
             'keyValue',
             'lengthValue',
             'linkStr',
             'localMod',
             'localNode',
             'localNodeList',
             'localNodeListLen',
             'localReason',
             'localUpdates',
             'logRuleMatching',
             'logRuleMatchingString',
             'lookupData',
             'lookupIndex',
             'lookupValue',
             # 'match',
             'matchError',
             'matchFound',
             'matchModifiedName',
             'matchRe',
             'matchRes',
             'matchUpdateCount',
             # 'modification',
             # 'Modification',
             # 'Modifications',
             'modificationName',
             'modificationType',
             'modName',
             'modPathValue',
             'modsArray',
             'modsArrayLength',
             'modType',
             'mutationsList',
             'nameStr',
             'newClass',
             'newCount',
             'newData',
             'newData',
             'newIntArray', 
             'newIntArrayMin', 
             'newIntLength', 
             'newName',
             'newNode', 
             'newNodeList',
             'newNodeListLen',
             'newNodeListLength',
             'newNodeObj',
             'newNodesList',
             'newNodesListLen',
             'newNodesListLength',
             'newObj', 
             'newOrder', 
             'newText',
             'newTextArray',
             'newTexts',
             'newTextSplit',
             'newValue',
             # 'node',
             'nodeActualIndex',
             'nodeActualPHash',
             'nodeActualUrl',
             'nodeActualValue',
             'nodeActualValueString',
             'nodeActualValueSplit',
             'nodeActualValueSplitArray',
             'nodeActualValueSplitArrayLen',
             'nodeActualValueSplitValue',
             'nodeActualValueSplitValueLen',
             'nodeAttributeCheck',
             'nodeAttributeChecks',
             'nodeAttributeKey',
             'nodeAttributeKeys',
             'nodeAttributeKeysLength',
             'nodeAttributeTagUpper',
             'nodeAttributeValue',
             'nodeAttributes',
             'nodeAttributesPHashSimilarity',
             'nodeAttributesPHashValue',
             'nodeChildrenLength',
             'nodeClass',
             'nodeClassList',
             'nodeCounter',
             'nodeCounts',
             'nodeCurrentAttributes',
             'nodeElement',
             'nodeElements',
             'nodeElementsLength',
             'nodeGrandParentAttributes',
             'nodeId',
             'nodeIden',
             'nodeIdenCheckType',
             'nodeIdenTracing',
             'nodeIndexOf',
             'nodeInnerText',
             'nodeIter',
             'nodeList',
             'nodeListLen',
             'nodeListLength',
             'nodeName',
             'nodeParentAttributes',
             'nodePHashCheck',
             'nodeSend',
             'nodeSrc',
             'nodeTag',
             'nodeText',
             'nodeType',
             'nodeValue',
             'nodeURL', 
             'number', 
             'numerator', 
             'numeratorIncrementValue', 
             'obj',
             'objName',
             'objProps',
             'objValue',
             'objValueFirst',
             'objValueLast',
             'oldRvLength',
             'oldText',
             'oldTextLower',
             'oldValue',
             # 'out',
             'outArray',
             'outIntArray',
             # 'output',
             'outputStr',
             'parameterIndex', 
             'parameterNumber',
             'parameterValue',
             'parametersArray',
             'parentElement', 
             'parentMatchValue', 
             'parentNode', 
             'parmNumber',
             'parmValue',
             'passedName',
             'passedRules',
             'pathNameStr',
             'pathValue',
             'pathValueStr',
             'postName',
             'postRuleTracing',
             'postTrace',
             'postTraceName',
             'protocolStringGetPHash',
             'protocolStringLower',
             'proxyDomain',
             'proxySecureDomain',
             'quotes',
             'readyState',
             'reasonStr',
             'replacementImageName',
             'requiredText',
             'requiredTextLower',
             'result',
             'resultStr',
             'ruleName',
             'savedUpdates',
             'searchAttrs',
             'searchIndex',
             'searchInner',
             'searchObj',
             'searchText',
             'searchValue',
             # 'second',
             'secondInt',
             'secondStr',
             'secondSub',
             'secondVal',
             'secureHostName',
             'sendUpdates',
             'sessionIdJava',
             'sessionIdJS',
             'sessionIdValue',
             'sessionIndexStr',
             # 'severity',
             # 'siteName',
             'siteNameStr',
             'siteNameValue',
             'splitOn',
             # 'String',
             # 'style',
             'styleSheet',
             'styleSheetList',
             'styleTitle',
             'styleValue',
             'styleVar',
             # 'suffix',
             'suffixStr',
             'tempInt',
             'tempIntArray',
             'tempLookupIndex',
             'testFlag',
             # 'text',
             'textMatch',
             'textNode',
             'textValue',
             'thisNode',
             'titleValue',
             'totalLength',
             'traceValue',
             # 'type',
             'typeValue',
             # 'update',
             'updateName',
             'updateObj',
             'updateStr',
             # 'URL',
             'urlIndex',
             'urlObj',
             'urlStr',
             'urlStrIndexOfColon',
             'urlStrMod',
             'urlVal',
             # 'value',
             'valueStr',
             'visitText',
             'weightStr',
             'xHttpReq',
             'xorValue'
             ]

# This is the first set of Java code 
docJavaFirst = \
'''
package com.headlamp; 
import com.google.common.cache.*;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonPrimitive;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
/**
 * Class for building a set of JavaScript. This is a generated program.
 * A Python program (BuildHDLmBuildJS.py) actually creates this Java 
 * program. This program should never be edited by hand in any way.
 *
 * @version 1.0
 * @author Peter
 */
 /* This is a purely static class and no instances of this class
    can ever be created */
class HDLmBuildJs {
	/* The next statement initializes logging to some degree. Note that having the
     slf4j jars and the log4j jars in the classpath also plays some role in
     logging initialization.	 */
  private static final Logger LOG = LoggerFactory.getLogger(HDLmBuildJs.class);
	/* This class can never be instantiated */
	private HDLmBuildJs() {}
  /* Build a set of JavaScript and return it to the caller */
  @SuppressWarnings("unused")
  public static String getJsBuildJs(HDLmProtocolTypes protocol,
                                    String secureHostName, 
                                    String hostName,
                                    String divisionName,
                                    String siteName,
                                    ArrayList<HDLmMod> mods, 
                                    HDLmSession sessionObj,
                                    HDLmLogMatchingTypes logRuleMatching,
                                    String serverName) {
    if (protocol == null) {
		  String  errorText = "Protocol string passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
    /* This check is no longer in use. We now allow for a null secure host name 
       to be passed to this routine. This will happen if no proxy definition was
       found for the current host name. This is no longer considered to be an 
       error condition. */ 
    /*
		if (secureHostName == null) {
		  String  errorText = "Secure host name string passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
    */
		if (hostName == null) {
		  String  errorText = "Host name string passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
		if (divisionName == null) {
		  String  errorText = "Division name string passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
		if (siteName == null) {
		  String  errorText = "Site name string passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
		if (mods == null) {
		  String  errorText = "Modifications array passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
    if (sessionObj == null) {
		  String  errorText = "Session object passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
    if (logRuleMatching == null) {
		  String  errorText = "Log rule matching reference passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
    if (serverName == null) {
		  String  errorText = "Server name string passed to getJsBuildJs is null";
      throw new NullPointerException(errorText);
		}
    HDLmBuildLines  builder;
    String          actualJS;
    String          fixedJSName = null;
    boolean         useCreateFixedJS = false;
    /* This routine is passed some JSON for the current session.
       Get a session object from the session JSON and get some 
       values from the object. */      
    String        sessionIdJava = sessionObj.getSessionId();
    String        sessionIndexStr = sessionObj.getIndex();
    String        sessionParametersStr = sessionObj.getParameters();
    ArrayList<Double>   sessionParametersArray = HDLmMain.getParametersArray(sessionParametersStr);
    /* This code is clearly no longer in use. However, some related
       code is very much in use. */ 
    if (1 == 2) {
      actualJS = HDLmUtility.fileGetContents("HDLmBuildJsOld.txt");
      return actualJS;
    }
    /* Check if the 'fixed JS' flag is set or not. If the flag is
       set, check if the fixed JavaScript file already exists. If
       it does, just read it and return it to the caller. */
    if (useCreateFixedJS) {
    	fixedJSName = HDLmDefines.getString("HDLMFIXEDFILENAME");
    	boolean   fileExists = HDLmUtility.fileExists(fixedJSName);
    	if (fileExists) {
        actualJS = HDLmUtility.fileGetContents(fixedJSName);
        return actualJS;
    	}   	
    }
    /* If the modifications array is empty (a common case), then 
       just return an empty JavaScript program to the caller. The 
       modifications array will (typically) be empty if the current
       path value did not match any actual modifications. 
       
       This code is no longer in use. This code built an empty 
       JavaScript program if there were no modifications. This 
       prevented visit records from being generated. */
    if (mods.size() == 0 &&
    		mods.size() != 0)
      return "<script></script>";
    /* Build the JavaScript used to implement the modifications */
    builder = new HDLmBuildLines("JS");
    builder.addLine("<script>");
'''

# This Java code builds the HDLmApplyMods function
docJavaApplyMods = \
'''
    /* Start the JavaScript function that applies all of the modifications */
    builder.addLine("  function HDLmApplyMods(readyState, HDLmIndexValue) {");
    /* Set the path value string */
    builder.addLine("    let pathValueStr = document.location.pathname;");
    /* Build a JavaScript object with all of the modifications */
    builder.addLine("    const modsArray = [");
    /* Add each of the modifications */
    int         counter;
    int         modsCount = mods.size(); 
    String      newLine;
    counter = 0;
    for (HDLmMod mod: mods) {
      counter++;
      newLine = " ".repeat(24);
      newLine += mod.getJsonSpecialSerializeNulls();
      if (counter < modsCount)
        newLine += ",";
      builder.addLine(newLine);
    }
    String  logRuleMatchingString;
    if (logRuleMatching == HDLmLogMatchingTypes.LOGMATCHINGYES)
      logRuleMatchingString = "true";
    else
      logRuleMatchingString = "false";
    Double   arrayEntry;
    String   forceSelectString = HDLmDefines.getString("HDLMFORCEVALUE");
    builder.addLine("                      ];");
    /* Build the session ID value */
    builder.addLine("    const sessionIdJS = '" + sessionIdJava + "';");
    /* Build the parameter values array */ 
    builder.addLine("    const parametersArray = HDLmGetParametersArray();"); 
    /* Get the number of modifications */
    builder.addLine("    let modsArrayLength = modsArray.length;");
    /* Process all of the modifications. Actually we are only interested
       in extract or notify modifications at this point. What we really
       want to do is to run the extracts and notifies and save the extracted 
       values. */
    builder.addLine("    for (let i=0; i < modsArrayLength; i++) {");
    builder.addLine("      let curMod = modsArray[i];");
    builder.addLine("      try {");
    /* Handle each type of modification. We only really process extract
       and notify modifications here. */
    builder.addLine("        switch (curMod.type) {");
    /* Check if the current modification is an extract */
    builder.addLine("          case 'extract': {");
    /* Assuming that the current modification is really a extract, then we 
       should have one or more values associated with it. Try to extract
       the current value and save the current value. */
    builder.addLine("            let nodeList = HDLmFind(curMod, false);");
    builder.addLine("            let nodeListLen = nodeList.length;");
    builder.addLine("            for (let j = 0; j < nodeListLen; j++) {");
    builder.addLine("              let curNode = nodeList[j];");
    /* If the value has already been extracted, then we don't want to extract
       it again */
    builder.addLine("              if (HDLmSavedExtracts.hasOwnProperty(curMod.name) &&");
    builder.addLine("                  HDLmSavedExtracts[curMod.name] != null)");
    builder.addLine("                continue;"); 
    /* Extract the text value of the current node */ 
    builder.addLine("              let oldText = curNode.textContent;");
    builder.addLine("              HDLmSavedExtracts[curMod.name] = oldText;");
    builder.addLine("            }");
    builder.addLine("            break;");
    builder.addLine("          }");
    /* Check if the current modification is a notify */
    builder.addLine("          case 'notify': {");
    /* Assuming that the current modification is really a notify, then we 
       should have one or more values associated with it. Try to extract
       the current value and save the current value. */
    builder.addLine("            for (let j = 0; j < curMod.valuesCount; j++) {");
    builder.addLine("              let searchText = curMod.values[j];");
    builder.addLine("              searchText = HDLmModifySearch(searchText);");
    /* If the value has already been extracted, then we don't want to extract
       it again */
    builder.addLine("              if (HDLmSavedNotifies.hasOwnProperty(searchText) &&");
    builder.addLine("                  HDLmSavedNotifies[searchText] != null)");
    builder.addLine("                continue;");
    builder.addLine("              let searchValue = HDLmObtainValue(searchText);");
    builder.addLine("              HDLmSavedNotifies[searchText] = searchValue;");
    builder.addLine("            }");
    builder.addLine("            break;");
    builder.addLine("          }");
    /* Handle (by ignoring it) the default case */
    builder.addLine("          default: {");
    builder.addLine("            break;");
    builder.addLine("          }");
    builder.addLine("        }");
    builder.addLine("      }");
    builder.addLine("      catch (errorObj) {");
    builder.addLine("        console.log(errorObj);");
    builder.addLine("        let errorStr = HDLmErrorToString(errorObj);");
    builder.addLine("        let nameStr = curMod.name;"); 
    builder.addLine("        let siteNameStr = '" + siteName + "';");
    builder.addLine("        let divisionNameStr ='" + divisionName + "';");
    builder.addLine("        let hostNameStr = '" + hostName + "';");
    builder.addLine("        let builtStr = 'Modification (' + nameStr + ') Host (' + hostNameStr + ') Error (' + errorStr + ')';");
    builder.addLine("        console.log(builtStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'modification', nameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'siteName', siteNameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'divisionName', divisionNameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'hostName', hostNameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'sessionId', sessionIdJS);");
    builder.addLine("        HDLmSendData(errorStr);");
    builder.addLine("      }");
    builder.addLine("    }");
    /* Process each of the modifications */
    builder.addLine("    for (let i=0; i < modsArrayLength; i++) {");
    builder.addLine("      let curMod = modsArray[i];");
    builder.addLine("      try {");
    builder.addLine("        HDLmApplyMod(pathValueStr,");
    builder.addLine("                     curMod,");
    builder.addLine("                     sessionIdJS,"); 
    builder.addLine("                     HDLmIndexValue,");
    builder.addLine("                     parametersArray,"); 
    builder.addLine("                     '" + hostName + "',");  
    builder.addLine("                     '" + hostName + "',"); 
    builder.addLine("                     '" + divisionName + "',");       
    builder.addLine("                     '" + siteName + "',"); 
    if (secureHostName != null) 
      builder.addLine("                     '" + secureHostName + "',");
    else
      builder.addLine("                     null,"); 
    builder.addLine("                     '" + forceSelectString + "',"); 
    builder.addLine("                     " + logRuleMatchingString + ",");
    builder.addLine("                     readyState);");
    builder.addLine("      }");
    builder.addLine("      catch (errorObj) {");
    builder.addLine("        console.log(errorObj);");
    builder.addLine("        let errorStr = HDLmErrorToString(errorObj);");
    builder.addLine("        let nameStr = curMod.name;");
    builder.addLine("        let siteNameStr = '" + siteName + "';");
    builder.addLine("        let divisionNameStr ='" + divisionName + "';");
    builder.addLine("        let hostNameStr = '" + hostName + "';");
    builder.addLine("        let builtStr = 'Modification (' + nameStr + ') Host (' + hostNameStr + ') Error (' + errorStr + ')';");
    builder.addLine("        console.log(builtStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'modification', nameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'siteName', siteNameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'divisionName', divisionNameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'hostName', hostNameStr);");
    builder.addLine("        errorStr = HDLmUpdateJsonStr(errorStr, 'sessionId', sessionIdJS);");
    builder.addLine("        HDLmSendData(errorStr);");
    builder.addLine("      }");
    builder.addLine("    }");
    /* Finish the current JavaScript function */
    builder.addLine("  }");
'''

# This Java code builds the HDLmBuildError function
docJavaBuildError = \
'''
    /* Start the JavaScript function that reports an error */
    builder.addLine("  function HDLmBuildError(errSeverity, curType, errNumber, errText) {");
    builder.addLine("    let errorStr = '';");
    builder.addLine("    errorStr += '" + HDLmDefines.getString("HDLMPREFIX") + "' + ' ';");
    builder.addLine("    errorStr += errSeverity + ' ';");
    builder.addLine("    errorStr += curType + ' ';");
    builder.addLine("    errorStr += errNumber.toString() + ' ';");
    builder.addLine("    errorStr += errText;");
    builder.addLine("    console.log(errorStr);");
    /* Finish the current JavaScript function */
    builder.addLine("  }");
'''

# This Java code builds the HDLmChangeAttributes function
docJavaChangeAttributes = \
'''
    /* Start the JavaScript function that changes zero or more node attributes */
    builder.addLine("  function HDLmChangeAttributes(curNode, jsonText) {");
    builder.addLine("    let changesObj = JSON.parse(jsonText);");
    builder.addLine("    for (const keyValue in changesObj) {");
    builder.addLine("      if (!changesObj.hasOwnProperty(keyValue))");
    builder.addLine("        continue;");
    builder.addLine("      let changesValue = changesObj[keyValue];");
    builder.addLine("      if (changesValue == null)");
    builder.addLine("        curNode.removeAttribute(keyValue);");
    builder.addLine("      else {");
    builder.addLine("        if (keyValue == 'class') {");
    builder.addLine("          HDLmClassAddEntry(curNode, changesValue);");
    builder.addLine("        }");
    builder.addLine("        else {");
    builder.addLine("          curNode.setAttribute(keyValue, changesValue);");
    builder.addLine("        }");
    builder.addLine("      }");
    builder.addLine("    }");
    /* Finish the current JavaScript function */
    builder.addLine("  }");
'''

# This Java code builds the HDLmGetAttributesString function
docJavaGetAttributesString = \
'''
    /* Start the JavaScript function that returns all of the attributes of a node 
       as a string */ 
    builder.addLine("  function HDLmGetAttributesString(curNode) {");
    builder.addLine("    let outputStr = '';");
    builder.addLine("    if (!curNode.hasAttributes())");
    builder.addLine("      return outputStr;");
    builder.addLine("    let attrs = curNode.attributes;");
    builder.addLine("    let attrsLength = attrs.length;");
    builder.addLine("    for (let i = attrsLength - 1; i >= 0; i--) {");
    builder.addLine("      if (outputStr != '')");
    builder.addLine("       outputStr += ' ';");
    builder.addLine("       outputStr += attrs[i].name + '=' + \\"'\\" + attrs[i].value + \\"'\\";");
    builder.addLine("    }");
    builder.addLine("    return outputStr;");
    /* Finish the current JavaScript function */
    builder.addLine("  }");
'''

# This Java code builds the HDLmGetLookupIndex function
docJavaGetLookupIndex = \
'''
    /* Build a JavaScript function that returns a value(s) index for a rule name */    
    builder.addLine("  /* Get the lookup value (if possible) for a rule name.");
    builder.addLine("     Return the lookup value to the caller. This routine");
    builder.addLine("     returns 'undefined' (with no quotes) if the rule");
    builder.addLine("     name is known to this routine. */");
    builder.addLine("  function HDLmGetLookupIndex(ruleName) {");
    builder.addLine("    /* console.log(ruleName); */");
    builder.addLine("    let lookupData = {");
    /* Get the overall set of index information */
    JsonArray   indexJsonArray = getIndexJsonArray(); 
    /* Check if the JSON array is valid or not */
		if (!indexJsonArray.isJsonArray()) {
	 	  String  errorText = "JSON array in getJSBuildJs is invalid";
	 	  HDLmAssert.HDLmAssertAction(false, errorText);
	  }
		/* Get the JSON array size */
    int   indexJsonArraySize = indexJsonArray.size();
    /* Set a boolean (not a Boolean) based on whether debug logging 
       is enabled or not. This is used to avoid the overhead of
       logging, when debug logging is not enabled. */
    boolean   logIsDebugEnabled = LOG.isDebugEnabled();
    /* Get the needed JSON */
		if (logIsDebugEnabled) {
		  LOG.debug("In HDLmGetLookupIndex");
		  LOG.debug(sessionIndexStr);
	  }
    /* Convert the index string to an index value, if possible */
    double  sessionIndexValue = 0.0;
    if (sessionIndexStr != null &&
    		!sessionIndexStr.equals("null"))  
    	sessionIndexValue = Double.parseDouble(sessionIndexStr);    	 
    /* Check all of the websites looking for a matching website */
    for (int i=0; i < indexJsonArraySize; i++) {
    	JsonElement   indexJsonElement = indexJsonArray.get(i);
    	String  jsonHostName = HDLmJson.getJsonString(indexJsonElement, "website");
    	/* Check if the host names match. If they do, we have a matching website. */
    	if (hostName.equals(jsonHostName)) {
    		JsonArray   rulesJsonArray = HDLmJson.getJsonArray(indexJsonElement, "rules");
    		JsonArray   choicesJsonArray = HDLmJson.getJsonArray(indexJsonElement, "choices");
        /* Check if the JSON arrays are valid or not */
    		if (!rulesJsonArray.isJsonArray()) {
    	 	  String  errorText = "JSON array in getJSBuildJs is invalid";
    	 	  HDLmAssert.HDLmAssertAction(false, errorText);
    	  }
    		if (!choicesJsonArray.isJsonArray()) {
    	 	  String  errorText = "JSON array in getJSBuildJs is invalid";
    	 	  HDLmAssert.HDLmAssertAction(false, errorText);
    	  }
    		/* Get the JSON array sizes */
    		int         rulesJsonArraySize = rulesJsonArray.size();
    		int         choicesJsonArraySize = choicesJsonArray.size();
    		/* If possible, get the choices array entry for use below */
    		JsonArray   choiceJsonArray = null;
        if (sessionIndexStr != null &&
        		!sessionIndexStr.equals("null")) { 
         	double      indexValue = sessionIndexValue * choicesJsonArraySize;
        	int         indexValueInt = (int) Math.floor(indexValue);
        	choiceJsonArray = (JsonArray) choicesJsonArray.get(indexValueInt);
          /* Check if the JSON array is valid or not */
      		if (!choiceJsonArray.isJsonArray()) {
      	 	  String  errorText = "JSON array in getJSBuildJs is invalid";
      	 	  HDLmAssert.HDLmAssertAction(false, errorText);
      	  }
        }    		
    		/* Process all of the rules for the website */
    		counter = 0;
        for (int j=0; j < rulesJsonArraySize; j++) {
        	counter++;
        	/* Add the rule name to the output */
        	JsonElement   ruleJsonElement = rulesJsonArray.get(j);
      		if (!ruleJsonElement.isJsonPrimitive()) {
      			HDLmAssert.HDLmAssertAction(false, "JSON element is not a JSON primitive value");
      		}
        	String        ruleName = ruleJsonElement.getAsString();
          newLine = " ".repeat(23);
          newLine += "'"; 
          newLine += ruleName;
          /* Add some JSON syntax */
          newLine += "': ";
          /* Use the index value to pick an array element */
          if (sessionIndexStr == null ||
          		sessionIndexStr.equals("null"))
          	newLine += "null";
          else {
            JsonElement   choiceJsonElement = choiceJsonArray.get(j); 
        		if (!choiceJsonElement.isJsonPrimitive()) {
        			HDLmAssert.HDLmAssertAction(false, "JSON element is not a JSON primitive value");
        		}
            String  choiceJsonString = choiceJsonElement.getAsString();
            newLine += choiceJsonString;
          }          
          if (counter < rulesJsonArraySize)  
            newLine += ",";       
          builder.addLine(newLine);
        }
    	}   	
    }   
    builder.addLine("                     };");
    builder.addLine("    let lookupIndex = lookupData[ruleName];");
    builder.addLine("    /* console.log(lookupIndex); */");
    builder.addLine("    return lookupIndex;");
    builder.addLine("  }");  
'''

# This Java code builds the HDLmGetParametersArray function
docJavaGetParametersArray = \
'''
    /* Start the JavaScript function that returns all of the parameters 
       as a array */ 
    builder.addLine("  function HDLmGetParametersArray() {");
    builder.addLine("    let outputStr = '';");
    builder.addLine("    const parametersArray = [");
    counter = 0;
    int   sessionParametersArrayLength = sessionParametersArray.size();
    for (int i = 0; i < sessionParametersArrayLength; i++) {
      counter++;
      newLine = " ".repeat(30);
      arrayEntry = sessionParametersArray.get(i);
      if (arrayEntry == null)
        newLine += "null";
      else
        newLine += arrayEntry;
      if (counter < sessionParametersArrayLength)
        newLine += ",";
      builder.addLine(newLine);
    }
    builder.addLine("                            ];");
    builder.addLine("    return parametersArray;");
    /* Finish the current JavaScript function */
    builder.addLine("  }");
'''

# This Java code builds the HDLmGetPHash function
docJavaGetPHash = \
'''
    /* The next routine tries to get a perceptual hash value for
       a URL (the part of the URL that starts with two slashes).
       The caller provides the URL. This routine builds the network
       request and sends it. Of course, the answer comes back later
       and is ignored. No callback routines are provided or used. */
    builder.addLine("  function HDLmGetPHash(urlStr) {");
    builder.addLine("    /* Build the AJAX object */");
    builder.addLine("    let xHttpReq = new XMLHttpRequest();");
    String   protocolStringGetPHash;
    protocolStringGetPHash = protocol.toString().toLowerCase();
    builder.addLine("    let serverNameValue = '" + serverName + "';");
    builder.addLine("    let urlVal = '" + protocolStringGetPHash + "://' + serverNameValue + '/" + HDLmConfigInfo.getPHashName() + "';");
    builder.addLine("    xHttpReq.open('POST', urlVal);");
    builder.addLine("    urlStr = encodeURIComponent(urlStr);");
    builder.addLine("    xHttpReq.send(urlStr);");
    /* Finish the current JavaScript function */ 
    builder.addLine("  }");
'''
# This Java code sends links and events back to the server
docJavaHandleLinksAndEvents = \
'''
    /* Send a message to the server for the current link and some events
       as they occur */
    builder.addLine("  {");    
    /* Set a few value for use later. Some of these values are used many
       times. Note that the session ID is part of the JavaScript program
       that is sent from the server to the client. */
    builder.addLine("    let hostNameStr = location.hostname;");
    builder.addLine("    let linkStr = location.href;");
    builder.addLine("    let pathNameStr = document.location.pathname;");
    builder.addLine("    let sessionIdValue = '" + sessionIdJava + "';");
    /* Get JSON for the current web page and send it to the server */
    builder.addLine("    let eventJson = HDLmGetJsonForLink(linkStr, hostNameStr, pathNameStr, sessionIdValue)");
    /* We really don't want to send event data to the server at this time.
       The event data makes the server log file too large. */
    builder.addLine("    /* HDLmSendData(eventJson); */");
    /* Process all of the keys (really events) for the current window */
    builder.addLine("    Object.keys(window).forEach(key => {"); 
    /* A few events are not of interest to us. We ignore them. */
    builder.addLine("      if (key.startsWith('onmouse'))");
    builder.addLine("        return;");
    builder.addLine("      if (key.startsWith('onpointer'))");
    builder.addLine("        return;"); 
    /* The regular expression below is used to check if the current key starts
       with 'on'. If the current key does start with 'on', then we probably 
       have a key associated with an event. */
    builder.addLine("      if (/^on/.test(key)) {");
    /* The next statement is used to add an event listener for the current key */
    builder.addLine("        window.addEventListener(key.slice(2), event => {");  
    /* The next statement is used to get the name of the current event */
    builder.addLine("          let eventName = HDLmGetObjectName(event);"); 
    /* The next statement is used to get some JSON for the current event.
       After we get the JSON, we send it to the server. */
    builder.addLine("          let eventJson = HDLmGetJsonForEventObject(event, eventName, hostNameStr, pathNameStr, sessionIdValue)");
    /* We really don't want to send event data to the server at this time.
       The event data makes the server log file too large. */
    builder.addLine("          /* HDLmSendData(eventJson); */");
    builder.addLine("        });");
    builder.addLine("      }"); 
    builder.addLine("    });");
    builder.addLine("  };");
'''    

# This is a late set of Java code
docJavaLate = \
'''
    /* Create a shared variable that will contain the saved updates */
    builder.addLine("  let HDLmSavedUpdates = new Object();");
    /* Create a shared variable that will contain the extracted values
       used for extract processing */
    builder.addLine("  let HDLmSavedExtracts = new Object();");
    /* Create a shared variable that will contain the extracted values
       used for notify processing */
    builder.addLine("  let HDLmSavedNotifies = new Object();");
    /* Create a global variable that shows that the update scripts
       have been loaded. This variable is defined with var rather 
       than let so that the window object will be modified by this
       statement. The browser extension (HDLmExtensionNodeIden.js) 
       checks this variable to see if update scripts have already
       been loaded. */
    builder.addLine("  var HDLmCheckVariable = true;");
    /* Build the perceptual hash values object */
    counter = 0;
    builder.addLine("  const HDLmPHashObject = {");
    Map<String, String>  mapObj = HDLmPHashCache.getMap();
    long  mapSize = mapObj.size();
		for (Map.Entry<String, String> entry: mapObj.entrySet()) {
	    String  key = entry.getKey();
	    String  value = entry.getValue();
      counter++;
      newLine = " ".repeat(28);
        newLine += "\\\"";
        newLine += key;
        newLine += "\\\":\\\"";
        newLine += value;
        newLine += "\\\"";
        if (counter < mapSize)
          newLine += ",";
      builder.addLine(newLine);
    }
    builder.addLine("                          };");
    /* Define the JavaScript function that sends any data back to the
       server */ 
    String   protocolStringLower;
    protocolStringLower = protocol.toString().toLowerCase();
    builder.addLine("  function HDLmSendData(dataStr) {");
    /* Set the host name string */
    builder.addLine("    dataStr = '" + HDLmDefines.getString("HDLMPOSTDATA") + "=" + "' + dataStr;");
    builder.addLine("    let httpReq = new XMLHttpRequest();");
    builder.addLine("    let serverNameValue = '" + serverName + "';");
    builder.addLine("    let urlStr = '" + protocolStringLower + "://' + serverNameValue + '/" + HDLmDefines.getString("HDLMPOSTDATA") + "';");
    builder.addLine("    httpReq.open('POST', urlStr);");
    builder.addLine("    httpReq.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');");
    builder.addLine("    dataStr = encodeURIComponent(dataStr);");
    builder.addLine("    httpReq.send(dataStr);");
    builder.addLine("  }");
    /* Define the JavaScript function that sends the update information
       back to the server */ 
    builder.addLine("  function HDLmSendUpdates(savedUpdates, reasonStr, weightStr, errorStr) {");
    builder.addLine("    savedUpdates.reason = reasonStr;");
    builder.addLine("    savedUpdates.weight = weightStr;");
    builder.addLine("    savedUpdates.error = errorStr;");
    builder.addLine("    let updateStr = JSON.stringify(savedUpdates);");
    builder.addLine("    HDLmSendData(updateStr);");
    builder.addLine("  }");
    /* Store the index value in the generated JavaScript 
       program. This is done so that the index value can 
       be used by the generated JavaScript program. */
    if (sessionIndexStr == null ||
        sessionIndexStr.equals("null"))
      builder.addLine("  let HDLmIndexValue = null;");
    else
    	builder.addLine("  let HDLmIndexValue = " + sessionIndexStr + ";");
    /* Create several CSS entries that will cause certain
       DOM entries to be color-coded as need be */ 
    builder.addLine("  HDLmClassAddCss('.HDLmClassPrimary'," +  
                                      "'background-color: yellow');");
    builder.addLine("  HDLmClassAddCss('.HDLmClassBackground'," + 
                                      "'filter: grayscale(100%)');");  
    /* Add some JavaScript for creating and using a mutation observer */
    builder.addLine("  let HDLmObsTargetNode = document;");
    /* Options for the observer (which mutations to observe) */
    builder.addLine("  let HDLmObsConfig = {attributes: true, childList: true, subtree: true};");
    /* Callback function to execute when mutations are observed */
    builder.addLine("  let HDLmObsCallback = function (mutationsList, HDLmObsObserver) {");
    builder.addLine("    /* console.log(document.readyState); */");
    builder.addLine("    let forceReadyState = false;");
    builder.addLine("    if (document.location.hostname == 'www.themarvelouslandofoz.com' &&");
    builder.addLine("        document.readyState == 'interactive')");
    builder.addLine("      forceReadyState = true;");
    builder.addLine("    HDLmApplyMods(document.readyState, HDLmIndexValue);");
    builder.addLine("    if (document.readyState == 'complete' ||");
    builder.addLine("        forceReadyState == true) {");
    builder.addLine("      HDLmApplyMods(document.readyState, HDLmIndexValue);");
    builder.addLine("    };");
    builder.addLine("  };");
    /* Create an observer instance linked to the callback function */
    builder.addLine("  let HDLmObsObserver = new MutationObserver(HDLmObsCallback);");
    /* Start observing the target node for configured mutations */
    builder.addLine("  HDLmObsObserver.observe(HDLmObsTargetNode, HDLmObsConfig);");
    /* Set the path value string */
    builder.addLine("  let pathValueStr = document.location.pathname;");     
    /* Build a local modification with all of the right values set, so that
       it can be passed to the apply modification routine. This must be done
       at the end of the JavaScript program so that all of the other routines
       will have been processed and as a consequence, available. */  
    builder.addLine("  let curMod = {};");      
    builder.addLine("  curMod.enabled = true;");  
    String  modificationName = HDLmDefines.getString("HDLMLOADPAGEMODNAME");
    builder.addLine("  curMod.name = '" + modificationName + "';"); 
    builder.addLine("  curMod.parameter = -1;");   
    builder.addLine("  curMod.path = '//.*/';");   
    builder.addLine("  curMod.pathre = true;");   
    String  modificationType = HDLmModTypes.VISIT.toString().toLowerCase();
    builder.addLine("  curMod.type = '" + modificationType + "';");     
    builder.addLine("  curMod.values = [ 'Yes' ];"); 
    builder.addLine("  curMod.valuesCount = 1;");   
    /* Build the session ID value */
    builder.addLine("  const sessionIdJS = '" + sessionIdJava + "';");
    /* Build the parameter values array */
    builder.addLine("  const parametersArray = HDLmGetParametersArray()");
    /* Set the ready state value to unknown (at least for now) */
    builder.addLine("  const readyState = 'unknown';");
    /* Create an object. An object is required because only objects
       can be modified. */ 
    builder.addLine("  HDLmApplyMod(pathValueStr,"); 
    builder.addLine("               curMod,");  
    builder.addLine("               sessionIdJS,");
    builder.addLine("               HDLmIndexValue,");
    builder.addLine("               parametersArray,");
    builder.addLine("               '" + hostName + "',");  
    builder.addLine("               '" + hostName + "',"); 
    builder.addLine("               '" + divisionName + "',");      
    builder.addLine("               '" + siteName + "',");
    if (secureHostName != null) 
      builder.addLine("               '" + secureHostName + "',"); 
    else
      builder.addLine("               null,");
    builder.addLine("               '" + forceSelectString + "',");
    builder.addLine("               '" + logRuleMatchingString + "',");
    builder.addLine("               readyState);");
    /* Finish the entire set of JavaScript */
    builder.addLine("</script>");
    actualJS = builder.getLinesWithSuffix("\\r\\n");
		/* The next set of code rebuilds the fixed JavaScript file. This code
		   is not normally executed because we want to make sure we are actually
		   getting the fixed JavaScript from the routine that builds the 
		   JavaScript. */ 
		if (useCreateFixedJS) {
		  HDLmUtility.fileClearContents(fixedJSName);
		  /* Declare a few values for converting the string */
		  int             i;
		  int             actualJSLen;
		  StringBuilder   actualJSAdjustedBuilder = new StringBuilder();
		  /* Build the output string */
		  actualJSLen = actualJS.length();
		  String  curStr;
		  for (i = 0; i < actualJSLen; i++) {
		  	char  curChar = actualJS.charAt(i);
		  	/* Check for a few special characters */
		  	if (curChar == '\\u1000')  
		  	  curStr = "\\\\u1000";		  
		  	else if (curChar == '\\u1001')  
	  	    curStr = "\\\\u1001";
        else if (curChar == '\\u1002')  
	  	    curStr = "\\\\u1002";
        else if (curChar == '\\u1003')  
	  	    curStr = "\\\\u1003";
        else if (curChar == '\\u1004')  
	  	    curStr = "\\\\u1004";
        else if (curChar == '\\u1005')  
	  	    curStr = "\\\\u1005";
        else if (curChar == '\\u1006')  
	  	    curStr = "\\\\u1006";
        else if (curChar == '\\u1007')  
	  	    curStr = "\\\\u1007";
        else if (curChar == '\\u1008')  
	  	    curStr = "\\\\u1008";
        else if (curChar == '\\u1009')  
	  	    curStr = "\\\\u1009";
        else if (curChar == '\\u100a')  
	  	    curStr = "\\\\u100a";
        else if (curChar == '\\u100b')  
	  	    curStr = "\\\\u100b";
        else if (curChar == '\\u100c')  
	  	    curStr = "\\\\u100c";
        else if (curChar == '\\u100d')  
	  	    curStr = "\\\\u100d";
        else if (curChar == '\\u100e')  
	  	    curStr = "\\\\u100e";
        else if (curChar == '\\u100f')  
	  	    curStr = "\\\\u100f";
        else if (curChar == '\\u1010')  
	  	    curStr = "\\\\u1010";
        else if (curChar == '\\u1011')  
	  	    curStr = "\\\\u1011";
        else if (curChar == '\\u1012')  
	  	    curStr = "\\\\u1012";
        else if (curChar == '\\u1013')  
	  	    curStr = "\\\\u1013";
        else if (curChar == '\\u1014')  
	  	    curStr = "\\\\u1014";
        else if (curChar == '\\u1015')  
	  	    curStr = "\\\\u1015";
        else if (curChar == '\\u1016')  
	  	    curStr = "\\\\u1016";
        else if (curChar == '\\u1017')  
	  	    curStr = "\\\\u1017";
        else if (curChar == '\\u1018')  
	  	    curStr = "\\\\u1018";
        else if (curChar == '\\u1019')  
	  	    curStr = "\\\\u1019";
        else if (curChar == '\\u101a')  
	  	    curStr = "\\\\u101a";
        else if (curChar == '\\u101b')  
	  	    curStr = "\\\\u101b";
        else if (curChar == '\\u101c')  
	  	    curStr = "\\\\u101c";
        else if (curChar == '\\u101d')  
	  	    curStr = "\\\\u101d";
        else if (curChar == '\\u101e')  
	  	    curStr = "\\\\u101e";
        else if (curChar == '\\u101f')  
	  	    curStr = "\\\\u101f";
        else if (curChar == '\\u1020')  
	  	    curStr = "\\\\u1020";
        else if (curChar == '\\u1021')  
	  	    curStr = "\\\\u1021";
        else if (curChar == '\\u1022')  
	  	    curStr = "\\\\u1022";
        else if (curChar == '\\u1023')  
	  	    curStr = "\\\\u1023";
        else if (curChar == '\\u1024')  
	  	    curStr = "\\\\u1024";
        else if (curChar == '\\u1025')  
	  	    curStr = "\\\\u1025";
        else if (curChar == '\\u1026')  
	  	    curStr = "\\\\u1026";
        else if (curChar == '\\u1027')  
	  	    curStr = "\\\\u1027";
        else if (curChar == '\\u1028')  
	  	    curStr = "\\\\u1028";
        else if (curChar == '\\u1029')  
	  	    curStr = "\\\\u1029";
        else if (curChar == '\\u102a')  
	  	    curStr = "\\\\u102a";
        else if (curChar == '\\u102b')  
	  	    curStr = "\\\\u102b";
        else if (curChar == '\\u102c')  
	  	    curStr = "\\\\u102c";
        else if (curChar == '\\u102d')  
	  	    curStr = "\\\\u102d";
        else if (curChar == '\\u102e')  
	  	    curStr = "\\\\u102e";
        else if (curChar == '\\u102f')  
	  	    curStr = "\\\\u102f";
        else if (curChar == '\\u1030')  
	  	    curStr = "\\\\u1030";
        else if (curChar == '\\u1031')  
	  	    curStr = "\\\\u1031";
        else if (curChar == '\\u1032')  
	  	    curStr = "\\\\u1032";
        else if (curChar == '\\u1033')  
	  	    curStr = "\\\\u1033";
        else if (curChar == '\\u1034')  
	  	    curStr = "\\\\u1034";
        else if (curChar == '\\u1035')  
	  	    curStr = "\\\\u1035";
        else if (curChar == '\\u1036')  
	  	    curStr = "\\\\u1036";
        else if (curChar == '\\u1037')  
	  	    curStr = "\\\\u1037";
        else if (curChar == '\\u1038')  
	  	    curStr = "\\\\u1038";
        else if (curChar == '\\u1039')  
	  	    curStr = "\\\\u1039";       
		  	else {
			  	curStr = "";
			  	curStr += curChar;
		  	}	  	
		  	actualJSAdjustedBuilder.append(curStr);
		  }		  
		  /* Write out the modified string */
		  String  actualJSAdjusted = actualJSAdjustedBuilder.toString();
		  HDLmUtility.filePutAppend(fixedJSName, 
		  		                      actualJSAdjusted);
		}		
    return actualJS;
  } 
'''

# This Java code starts the Java function that 
# returns the Java JSON object    
docJavaLiteralPrefix = \
'''
  /* This Java function returns a JSON object 
     with the web site name and the index values
     in it. */
  public static JsonArray  getIndexJsonArray() {
    class getIndexJsonArrayLocal {
      /* Declare a string that will have JSON in it */
      final static String  jsonString = 
'''

# This Java code ends the Java function that 
# returns the Java JSON object 
docJavaLiteralSuffix = \
'''
        "";
			/* Create a new JSON parser for use below */
	    static JsonParser  parser = new JsonParser();  
	    /* Convert the JSON string to a JSON array */
	    static JsonArray   rvJsonArray = (JsonArray) parser.parse(jsonString);
  	}
		/* Return the JSON object to the caller */
    return getIndexJsonArrayLocal.rvJsonArray;
  }
}
'''

# Each instance of this class has a dictionary of name mappings and handles 
# name substitutions 
class ChangeNames(object):
  # The __init__ method creates an instance of the class      
  def __init__(self):
    self.nameCount = 0
    self.nameDict = dict()
  # Add a variable name to the name map 
  def addName(self, varName, shortNames):
    # Add a variable name to the name map
    self.nameCount += 1 
    newName = shortNames.getNext()
    self.nameDict[varName] = newName
  # Add a list of variable names to the name map
  def addNames(self, varNames, shortNames): 
    # Process each name in the list
    for varName in varNames:
      self.addName(varName, shortNames)
  # Change just one name passed by the caller. If the name is
  # is not found in the map (dictionary), then None is 
  # returned to the caller 
  def changeName(self, name):
    # Check for the name in the dictionary
    if name in self.nameDict:
      return self.nameDict[name]
    return None 
  # Update a string by replacing all of the long names
  # with short names
  def changeNamesReplace(self, line):
    # Process all of the keys in the dictionary
    for key in self.nameDict:
      value = self.nameDict[key]
      line = line.replace(key, value)
    return line 

# Each instance of this class provides a set of short variable names
class ShortNames(object):
  # The __init__ method creates an instance of the class      
  def __init__(self):
    self.letterList = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    self.letterListLen = len(self.letterList)
    self.nameLength = 1
    self.letterCount = 0
    self.numberCount = 0
  # Get the next short name and return it to the caller. 
  def getNext(self): 
    # Handle each of the possible name lengths
    if self.nameLength == 1:
      self.letterCount += 1
      # Check for a very special case. We must never return i, j, or k
      # to the caller. These single-letter names tend to be used for 
      # other purposes.
      if self.letterCount == 9:
        self.letterCount += 3
      nextValue = self.letterList[self.letterCount-1:self.letterCount]
      if self.letterCount == 52:
        self.letterCount = 0
        self.nameLength += 1
    # Handle short names that have a letter and one number
    elif self.nameLength == 2:
      self.numberCount += 1
      nextValue = self.letterList[self.letterCount:self.letterCount+1] + \
                  str(self.numberCount - 1)
      # Check if we have used up the curent letter and must switch 
      # to the next letter
      if self.numberCount == 10 and self.letterCount < 51:
        self.letterCount += 1
        self.numberCount = 0 
      # Check if we have used up the last letter
      if self.numberCount == 10 and self.letterCount >= 51:
        self.letterCount = 0
        self.numberCount = 0
        self.nameLength += 1
    elif self.nameLength == 3:
      self.numberCount += 1
      nextValue = self.letterList[self.letterCount:self.letterCount+1] + \
                  str(self.numberCount - 1).zfill(2)
      # Check if we have used up the curent letter and must switch 
      # to the next letter
      if self.numberCount == 100 and self.letterCount < 51:
        self.letterCount += 1
        self.numberCount = 0
      # Check if we have used up the last letter
      if self.numberCount == 100 and self.letterCount >= 51:
        self.letterCount = 0
        self.numberCount = 0
        self.nameLength += 1
    elif self.nameLength == 4:
      self.numberCount += 1
      nextValue = self.letterList[self.letterCount:self.letterCount+1] + \
                  str(self.numberCount - 1).zfill(3)
      # Check if we have used up the curent letter and must switch 
      # to the next letter
      if self.numberCount == 1000 and self.letterCount < 51:
        self.letterCount += 1
        self.numberCount = 0
      # Check if we have used up the last letter
      if self.numberCount == 1000 and self.letterCount >= 51:
        self.letterCount = 0
        self.numberCount = 0
        self.nameLength += 1
    elif self.nameLength == 5:
      self.numberCount += 1
      nextValue = self.letterList[self.letterCount:self.letterCount+1] + \
                  str(self.numberCount - 1).zfill(4)
      # Check if we have used up the curent letter and must switch 
      # to the next letter
      if self.numberCount == 10000 and self.letterCount < 51:
        self.letterCount += 1
        self.numberCount = 0
      # Check if we have used up the last letter
      if self.numberCount == 10000 and self.letterCount >= 51:
        self.letterCount = 0
        self.numberCount = 0
        self.nameLength += 1
    else:
      raise ValueError('We have run out of short variable names')
    return nextValue  

# Add a few prefix characters to each line
def addPrefix(inLines, prefixChar, count):
  # Build some code from the input 
  out = []
  # Process each input line
  for line in inLines:
    prefix = prefixChar * count
    line = prefix + line    
    out.append(line)   
  return out

# Build some Java code and non-Java code from a set of input lines
def addBuilder(inLines, codeType):
  # Build some Java code from the input lines 
  out = []
  # Process each input line
  for line in inLines:
    quoteChar = '"'
    # We can really only change the quote character if we are
    # not generating Java code.  
    if (codeType != 'Java'):
      if line.find('"') >= 0:
        quoteChar = "'"
    newLine = '    '
    if (codeType == 'Java'):
      newLine += 'builder.addLine('
    else:
      newLine += '$builder->addLine('
    newLine += quoteChar
    # For Java we really need to escape some characters
    if (codeType == 'Java'):
      line = lineFixJava(line, quoteChar)
    # For code other than Java we really need to escape some characters
    if (codeType != 'Java'): 
      charBackslash = '\\'
      charDollar = '$'
      charLetterS = 's'
      stringTwoBackslashs = charBackslash + charBackslash
      stringBackslashLetterS = charBackslash + charLetterS
      stringBackslashDollar = charBackslash + charDollar
      stringTwoBackslashsLetterS = stringTwoBackslashs + charLetterS
      stringTwoBackslashsDollar = stringTwoBackslashs + charDollar
      if line.find(stringBackslashLetterS) != -1:
        line = line.replace(stringBackslashLetterS, stringTwoBackslashsLetterS)
      if line.find(stringBackslashDollar) != -1:
        line = line.replace(stringBackslashDollar, stringTwoBackslashsDollar) 
    # Remove any trailing whitespace. This makes it easier to 
    # run the Java unit testing programs
    line = line.rstrip()
    newLine += line
    newLine += quoteChar
    newLine += ');' 
    out.append(newLine)   
  return out

# Build a choices JSON dictionary literal and return it
# to the caller
def buildChoicesLiteral():
  dictLiteral = \
  [
    {"website": "www.yogadirect.com", 
    "generated": "2024-06-13T01:51:52Z",
    "rules": ["Change Banner","Change Add To Cart"],
    "choices":
[
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,6],
[5,0],
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[0,6],
[1,0],
[2,1],
[3,2],
[4,3],
[5,4],
[0,5],
[1,6],
[2,0],
[3,1],
[4,2],
[5,3],
[0,4],
[1,5],
[2,6],
[3,0],
[4,1],
[5,2],
[0,3],
[1,4],
[2,5],
[3,6],
[4,0],
[5,1],
[0,2],
[1,3],
[2,4],
[3,5]
]
    }
  ]
  # Return the dictionary literal to the caller
  return dictLiteral

# Build a choices JSON dictionary literal and return it
# to the caller
def buildChoicesLiteralOld():
  dictLiteral = \
  [
    { "website": "www.yogadirect.com",
      "generated": "2000-10-31T01:30:00.000-05:00",
      "rules": ["Change Add To Cart", "Change Banner"],
      "choices":
[
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3],
[0,4],
[1,5],
[2,0],
[3,1],
[4,2],
[5,3],
[6,4],
[7,5],
[0,0],
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
[6,0],
[7,1],
[0,2],
[1,3],
[2,4],
[3,5],
[4,0],
[5,1],
[6,2],
[7,3]
]
  }
]
# Return the dictionary literal to the caller
  return dictLiteral

# Build some Java code from a doc literal
def buildCode(data):
  # Split the doc literal into separate lines. The doc literal is used
  # to build some Java code. 
  inCode = data.splitlines();
  if (len(inCode) > 0):
    inCode.pop(0)
  # Build some code from the input 
  out = []
  # Add each line of code
  for line in inCode:
    out.append(line)   
  return out

# Build a few function with JavaScript in them
def buildFunctions():
  # Build some Java code 
  out = []
  # Add each line of code
  line = '    /* Build a set of functions that contain the JavaScript that is stored'
  out.append(line)  
  line = '       in each of rules. Note that JavaScript is only store in script rules. */'
  out.append(line)
  line = '    for (HDLmMod mod: mods) {'
  out.append(line)
  line = "    	/* Skip the current modification if it is not a 'script' (without"
  out.append(line)
  line = '  	     the quotes) modification */'
  out.append(line)
  line = '    	if (mod.getType() != HDLmModTypes.SCRIPT)'
  out.append(line)
  line = '        continue;'
  out.append(line)
  line = '    	/* Get the modified name of the rule */'
  out.append(line)
  line = '    	String  newName = HDLmMod.replaceInString(mod.getName());'
  out.append(line)
  line = '        /* Handle each of the values of the current modification */'
  out.append(line)
  line = '        int   valueCount = mod.getValues().size();'
  out.append(line)
  line = '        for (int i = 0; i < valueCount; i++) {'
  out.append(line)
  line = '          /* Get the current value */'
  out.append(line)
  line = '          String  curValue = mod.getValues().get(i);'
  out.append(line)
  line = '          /* Build the function with the JavaScript in it */'
  out.append(line)
  line = '          newLine = "  function HDLmExecute" + newName + i + "() {";'
  out.append(line)
  line = '          builder.addLine(newLine);'
  out.append(line)
  line = '          ArrayList<String>   curValues = new ArrayList<String>(Arrays.asList(curValue.split("/n")));'
  out.append(line) 
  line = '          for (int j = 0; j < curValues.size(); j++) {'
  out.append(line)
  line = '            String  curLine = curValues.get(j);'
  out.append(line)
  line = '            builder.addLine("    " + curLine);'
  out.append(line)  
  line = '          }'
  out.append(line)
  line = '          newLine = "  }";'
  out.append(line)
  line = '          builder.addLine(newLine);'
  out.append(line)
  line = '      }'
  out.append(line)
  line = '    }' 
  out.append(line)   
  return out

# Build a function with a set of nested switches inside it. 
# The switches invoke the functions that contain the JavaScript.
# The outer switch is for the rule name. The inner switch is for
# the current 'choice' number (the actual choice does not have
# any quotes). Note taat the generated Java/JavaScript function
# is not really in use. A different mechianism is used to invoke
# JavaScript functions by name.
def buildSwitches():
  # Build some Java code 
  out = []
  # Add each line of code
  line = '    /* Build a function that contains a set of nested switches.'
  out.append(line)  
  line = '       The nested switches invoke the functions with JavaScript'
  out.append(line)
  line = '       in them. */'
  out.append(line)
  line = '    newLine = "  function HDLmExecuteSwitch(modName, choiceNumber) {";'
  out.append(line)
  line = '		builder.addLine(newLine);'
  out.append(line)
  # Build a switch on the rule name 
  line = '    newLine = "    switch (modName) {";'
  out.append(line)
  line = '		builder.addLine(newLine);'
  out.append(line)
  # Each modificaion (rule) that has JavaScript in it will have a case
  # constructed for it. What this means in practice is that rule with 
  # type other than 'script' (without the quotes) will be skipped and 
  # not generate a case. 
  line = '    for (HDLmMod mod: mods) {'
  out.append(line)
  line = "    	/* Skip the current modification if it is not a 'script' (without"
  out.append(line)
  line = '  	     the quotes) modification */'
  out.append(line)
  line = '    	if (mod.getType() != HDLmModTypes.SCRIPT)'
  out.append(line)
  line = '        continue;'
  out.append(line)
  line = '    	String  curModName = mod.getName();'
  out.append(line)
  line = '      newLine = "      case \'" + curModName + "\':";'
  out.append(line)
  line = '		  builder.addLine(newLine);'
  out.append(line) 
  line = '    	String  curModNameInternal = HDLmMod.replaceInString(curModName);'
  out.append(line)
  # Build a switch on the choice number
  line = '      newLine = "        switch (choiceNumber) {";'
  out.append(line)
  line = '		  builder.addLine(newLine);'
  out.append(line)
  # Each choice will have a case constructed for it
  line = '     	/* Handle each of the values of the current modification */'
  out.append(line)
  line = '    	int   valueCount = mod.getValues().size();'
  out.append(line)
  line = '	  	for (int i = 0; i < valueCount; i++) {'
  out.append(line)
  # Build a case for the current choice number
  line = '      newLine = "          case " + i + ":";'
  out.append(line)
  line = '		  builder.addLine(newLine);'
  out.append(line) 
  # Build the function call for the current choice number
  line = '        newLine = "            HDLmExecute" + curModNameInternal + i + "();";'
  out.append(line)
  line = '		    builder.addLine(newLine);'
  out.append(line)
  line = '        newLine = "            break;";'
  out.append(line)
  line = '		    builder.addLine(newLine);'
  out.append(line) 
  # Build some code that terminates the inner Java (not JavaScript)
  # loop  
  line = '      }' 
  out.append(line) 
  # Build some code that creates the default case for the inner switch
  line = '      newLine = "          default:";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line)
  line = '      newLine = "            let errorText = \\"Invalid choice value - \\" + choiceNumber" + ";";' 
  out.append(line)
  line = '  		builder.addLine(newLine);'
  out.append(line)
  line = '      newLine = "            HDLmBuildError(\'Error\', \'Choice\', 63, errorText);";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line)
  line = '      newLine = "            break;";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line)  
  # Terminate the inner (choice number) switch 
  line = '      newLine = "        }";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line)
  # Build some code that terminates the outer Java (not JavaScript)
  # loop
  line = '    }' 
  out.append(line) 
  # Build some code that creates the default case for the outer switch
  line = '      newLine = "      default:";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line)
  line = '      newLine = "        let errorText = \\"Invalid rule name value - \\" + modName;";' 
  out.append(line)
  line = '  		builder.addLine(newLine);'
  out.append(line)
  line = '      newLine = "        HDLmBuildError(\'Error\', \'RuleName\', 62, errorText);";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line)
  line = '      newLine = "        break;";'
  out.append(line)
  line = '	  	builder.addLine(newLine);'
  out.append(line) 
  # Terminate the outer (rule name) switch
  line = '    newLine = "    }";'
  out.append(line)
  line = '		builder.addLine(newLine);'
  out.append(line)
  # Terminate the function
  line = '    newLine = "  }";'
  out.append(line)
  line = '		builder.addLine(newLine);'
  out.append(line)
  return out

# Build some Java code from a literal
def buildJavaFromLiteral(literalValue, outArray, indentValue, addComma): 
  # Set the prefix string
  prefixStr = '        '
  # Get the type of the literal value as a string for
  # use below
  typeLiteralValue = str(type(literalValue))
  # Check the type of the literal value. Different code
  # is needed for each type.
  if typeLiteralValue == "<class 'dict'>":
    # Start the JSON object
    outString = prefixStr + '"' + ' '*indentValue + '{" +'   
    outArray.append(outString)
    indentValue += 2
    keyCount = 0
    keyLen = len(literalValue)
    # Process each key-value pair in the dictionary
    for dictKey in literalValue: 
      # Increment the key count
      keyCount += 1
      outString = prefixStr + '"' + ' '*indentValue + '\\"' + dictKey + '\\":' + '" +'   
      outArray.append(outString)
      dictValue = literalValue[dictKey] 
      typeValue = str(type(dictValue))  
      commaAlreadyAdded = False
      commaValue = ''
      # if we now have a list as the value, handle the
      # list
      if typeValue == "<class 'list'>":
        indentValue += 2
        addComma = False
        # Add a comma, if need be
        if keyCount < keyLen and commaAlreadyAdded == False:
          addComma = True
          commaAlreadyAdded = True
        outArray = buildJavaFromLiteral(dictValue, outArray, indentValue, addComma)
        addComma = False
        indentValue -= 2
      # Check for a string value
      elif typeValue == "<class 'str'>":    
        # Add a trailing comma, if need be  
        if keyCount < keyLen:     
          commaAlreadyAdded = True
          commaValue = ','
        # Add the value to the JSON object
        indentValue += 2
        outString = prefixStr + '"' + ' '*indentValue + '\\"' + dictValue + '\\"' + commaValue + '" +'
        indentValue -= 2
        outArray.append(outString)
      # Add a comma if need be
      if keyCount < keyLen and commaAlreadyAdded == False:
        outString = prefixStr + '"' + ' '*indentValue + '," +'
        outArray.append(outString)
        commaAlreadyAdded = True
    # Finish the JSON object
    indentValue -= 2
    outString = prefixStr + '"' + ' '*indentValue + '}" +'   
    outArray.append(outString)
  # Check list literal
  elif typeLiteralValue == "<class 'list'>":
    # Start the JSON object
    outString = prefixStr + '"' + ' '*indentValue + '[" +'   
    outArray.append(outString)
    indentValue += 2
    itemCount = 0
    itemLen = len(literalValue)
    # Process each item in the list
    for item in literalValue: 
      # Increment the item count
      itemCount += 1
      typeItem = str(type(item))  
      commaAlreadyAdded = False
      commaValue = ''
      # Check for a dictionary value
      if typeItem == "<class 'dict'>":
        indentValue += 0
        outArray = buildJavaFromLiteral(item, outArray, indentValue, addComma)
        indentValue -= 0
      # Check for an integer value
      elif typeItem == "<class 'int'>":    
        # Add a trailing comma, if need be  
        commaAlreadyAdded = False
        commaValue = ''
        if itemCount < itemLen:     
          commaAlreadyAdded = True
          commaValue = ','
        # Add the value to the JSON object
        outString = prefixStr + '"' + ' '*indentValue + '' + str(item) + '' + commaValue + '" +'
        outArray.append(outString)
      # if we now have a list as the item, handle the
      # list
      elif typeItem == "<class 'list'>":
        # Check for a very special case. If they current
        # item is list with length of two or more, then 
        # we must handle this as a special case. 
        itemEntryLen = len(item)
        if itemEntryLen >= 2:
          # Start the string 
          outValue = ''
          entryCount = 0  
          entryLen = len(item)
          # Build up the value
          for itemEntry in item:
            entryCount += 1
            outValue += str(itemEntry)  
            if entryCount < entryLen:
              outValue += ','
          # Add a trailing comma, if need be  
          commaAlreadyAdded = False
          commaValue = ''
          # Add a trailing comma, if need be  
          if itemCount < itemLen and commaAlreadyAdded == False:    
            commaAlreadyAdded = True
            commaValue = ','
          # Add the item value to the JSON object
          outString = prefixStr + '"' + ' '*indentValue + '[' + outValue + ']' + commaValue + '" +'
          outArray.append(outString)
          continue      
        # Add a comma, if need be
        if itemCount < itemLen and commaAlreadyAdded == False:
          addComma = True
          commaAlreadyAdded = True
        outArray = buildJavaFromLiteral(item, outArray, indentValue, addComma)
        addComma = False
      # Check for a string value
      elif typeItem == "<class 'str'>":    
        # Add a trailing comma, if need be  
        if itemCount < itemLen:     
          commaAlreadyAdded = True
          commaValue = ','
        # Add the value to the JSON object
        outString = prefixStr + '"' + ' '*indentValue + '\\"' + item + '\\"' + commaValue + '" +'
        outArray.append(outString)
      # Fail if any other type is found
      else:
        raise ValueError('Unknown item type')
      # Add a comma, if need be
      if itemCount < itemLen and commaAlreadyAdded == False:
        outString = prefixStr + '"' + ' '*indentValue + '," +'
        outArray.append(outString)
        commaAlreadyAdded = True
    # Finish the JSON object
    indentValue -= 2
    commaValue = ''
    if addComma == True:
      commaValue = ','
    outString = prefixStr + '"' + ' '*indentValue + ']' + commaValue + '" +'   
    outArray.append(outString)
  # Fail if any other type is found
  else:
    raise ValueError('Unknown literal type')
  return outArray

# This routine displays a set of lines  
def displayLines(inData):
  # Process all of the lines in the input data
  for line in inData:  
    print(line)
  return 

# This routine gets a set of tokens from a string. The caller 
# provides the string and the quote character (more than one
# quote character can be passed). A vector is returned to the
# caller unless an exception is detected. If an exception is 
# detected, then None is return to the caller.
def getTokensFromString(inStr, quoteChar):
  errorDetected = False 
  try:
    inStrVec = HDLmString.getTokens(inStr, quoteChars = quoteChar)
  except:
    errorDetected = True;
  if errorDetected:
    return None
  return inStrVec

# Fix some characters by expanding them into Java-friendly sequences.
# This set of changes are required so that proper Java code can be
# geneated.
def lineFixJava(line, quoteChar):
  # Define some characters that are used in the code below
  charBackslash = '\\'
  charDollar = '$'
  charDoubleQuote = '"'
  charLetterN = 'n'
  charLetterS = 's'
  charLeftParen = '('
  charPeriod = '.'
  charRightParen = ')'
  charSlash = '/'
  # Define some strings that are used in the code below
  stringBackslashDollar = charBackslash + charDollar
  stringBackslashDoubleQuote = charBackslash + charDoubleQuote
  stringBackslashLeftParen = charBackslash + charLeftParen
  stringBackslashLetterN = charBackslash + charLetterN
  stringBackslashLetterS = charBackslash + charLetterS
  stringBackslashPeriod = charBackslash + charPeriod
  stringBackslashRightParen = charBackslash + charRightParen
  stringBackslashSlash = charBackslash + charSlash
  stringTwoBackslashs = charBackslash + charBackslash
  stringTwoBackslashsDollar = stringTwoBackslashs + charDollar
  stringTwoBackslashsLeftParen = stringTwoBackslashs + charLeftParen
  stringTwoBackslashsLetterN = stringTwoBackslashs + charLetterN
  stringTwoBackslashsLetterS = stringTwoBackslashs + charLetterS
  stringTwoBackslashsPeriod = stringTwoBackslashs + charPeriod
  stringTwoBackslashsRightParen = stringTwoBackslashs + charRightParen
  stringTwoBackslashsSlash = stringTwoBackslashs + charSlash
  # Replace some characters with Java-friendly sequences
  line = line.replace(quoteChar, stringBackslashDoubleQuote)
  line = line.replace(stringBackslashLetterN, stringTwoBackslashsLetterN)
  line = line.replace(stringBackslashLetterS, stringTwoBackslashsLetterS)
  line = line.replace(stringBackslashDollar, stringTwoBackslashsDollar)
  line = line.replace(stringBackslashPeriod, stringTwoBackslashsPeriod)
  line = line.replace(stringBackslashSlash, stringTwoBackslashsSlash)
  line = line.replace(stringBackslashLeftParen, stringTwoBackslashsLeftParen)
  line = line.replace(stringBackslashRightParen, stringTwoBackslashsRightParen)
  return line

# Fix some characters by removing Java-friendly sequences and
# replacing them with what we hope were the original sequences
def lineUnFixJava(line, quoteChar):
  # Define some characters that are used in the code below
  charBackslash = '\\'
  charDollar = '$'
  charDoubleQuote = '"'
  charLetterN = 'n'
  charLetterS = 's'
  charLeftParen = '('
  charPeriod = '.'
  charRightParen = ')'
  charSlash = '/'
  # Define some strings that are used in the code below
  stringBackslashDollar = charBackslash + charDollar
  stringBackslashDoubleQuote = charBackslash + charDoubleQuote
  stringBackslashLeftParen = charBackslash + charLeftParen
  stringBackslashLetterN = charBackslash + charLetterN
  stringBackslashLetterS = charBackslash + charLetterS
  stringBackslashPeriod = charBackslash + charPeriod
  stringBackslashRightParen = charBackslash + charRightParen
  stringBackslashSlash = charBackslash + charSlash
  stringTwoBackslashs = charBackslash + charBackslash
  stringTwoBackslashsDollar = stringTwoBackslashs + charDollar
  stringTwoBackslashsLeftParen = stringTwoBackslashs + charLeftParen
  stringTwoBackslashsLetterN = stringTwoBackslashs + charLetterN
  stringTwoBackslashsLetterS = stringTwoBackslashs + charLetterS
  stringTwoBackslashsPeriod = stringTwoBackslashs + charPeriod
  stringTwoBackslashsRightParen = stringTwoBackslashs + charRightParen
  stringTwoBackslashsSlash = stringTwoBackslashs + charSlash
  # Replace some characters with Java-friendly sequences
  line = line.replace(stringBackslashDoubleQuote, quoteChar)
  line = line.replace(stringTwoBackslashsLetterN, stringBackslashLetterN)
  line = line.replace(stringTwoBackslashsLetterS, stringBackslashLetterS)
  line = line.replace(stringTwoBackslashsDollar, stringBackslashDollar)
  line = line.replace(stringTwoBackslashsPeriod, stringBackslashPeriod)
  line = line.replace(stringTwoBackslashsSlash, stringBackslashSlash)
  line = line.replace(stringTwoBackslashsLeftParen, stringBackslashLeftParen)
  line = line.replace(stringTwoBackslashsRightParen, stringBackslashRightParen)
  return line

# Change some of the tokens for JavaScript minification
def minifyChangeTokens(tokVec, changeNames, line, noMatchDict, replaceNames): 
  if ('case " + i' in line):
    print(line)
  # Get the number of tokens
  tokVecLen = len(tokVec)
  # Process all of the tokens
  for i in range(tokVecLen):
    curTok = tokVec[i]
    curTokType = curTok.tokType
    # Assume we can't compress multiple blanks 
    numberOfBlanks = None
    # The code below removes leading blanks in some cases.
    # The removal of leading blanks is a big deal. Testing
    # has shown that removing leading blanks results in a 
    # large reduction is network transfer size.
    if curTokType == HDLmTokenTypes.space and \
       i >= 5                             and \
       tokVec[i-1].value == '\u1000'      and \
       tokVec[i-2].value == '('           and \
       tokVec[i-3].value == 'addLine'     and \
       tokVec[i-4].value == '.'           and \
       tokVec[i-5].value == 'builder':
      numberOfBlanks = 0
    if curTokType == HDLmTokenTypes.space and \
       i >= 5                             and \
       tokVec[i-1].value == '\u1000'      and \
       tokVec[i-2].value == ''            and \
       tokVec[i-3].value == '='           and \
       tokVec[i-4].value == ''            and \
       tokVec[i-5].value == 'newLine':
      numberOfBlanks = 0
    # In some cases, we can change multiple blanks into
    # a single blank. This is not possible in all cases.
    if curTokType == HDLmTokenTypes.space     and \
       i > 0                                  and \
       tokVec[i-1].value == 'let'             and \
       len(curTok.value) >= 2: 
      numberOfBlanks = 1
    # In some cases, we can change any number of blanks
    # into a zero-length string. This is not possible 
    # in all cases.
    nextToken = None
    if (tokVecLen > (i+1)):
      nextToken = tokVec[i+1]
    if curTokType == HDLmTokenTypes.space     and \
       i > 0                                  and \
       tokVec[i-1].value == 'case'            and \
       len(curTok.value) >= 1: 
      # The number of blanks that should come after
      # as 'case' (without the quotes) depends on 
      # the next token
      if (nextToken != None)              and \
          nextToken.value == '\u1000':
        numberOfBlanks = 1
      else:
        numberOfBlanks = 0
    # Check if the prior token and next token are 
    # parentheses of some kind. Set some values if 
    # this is true. 
    priorTokenRightParen = False
    if i > 0 and tokVec[i-1].value == ')':
      priorTokenRightParen = True 
    nextTokenLeftParen = False
    if (i+1) < len(tokVec) and tokVec[i+1].value == '(':
      nextTokenLeftParen = True 
    # Check if the current space token has one or   
    # more spaces and is followed by an operator token.
    # If all of these conditions are met, then we can
    # set a value showing that the spaces should be 
    # removed.
    if curTokType        == HDLmTokenTypes.space      and \
       len(curTok.value) >= 1                         and \
       (tokVecLen - i)   >= 2                         and \
       tokVec[i+1].tokType == HDLmTokenTypes.operator and \
       priorTokenRightParen == False                  and \
       nextTokenLeftParen == False:
      numberOfBlanks = 0
    # Check if the current space token has one or   
    # more spaces and is preceeded by an operator token
    # that is not a right parenthesis and the next token
    # is not a left parenthesis. If all of these conditions 
    # are met, then we can set a value showing that the 
    # spaces should be removed.
    if curTokType          == HDLmTokenTypes.space    and \
       len(curTok.value)   >= 1                       and \
       i                   >  0                       and \
       tokVec[i-1].tokType == HDLmTokenTypes.operator and \
       priorTokenRightParen == False                  and \
       nextTokenLeftParen == False:
      numberOfBlanks = 0
    # Check if the current space token has one or   
    # more spaces and is preceeded by a semicolon token.
    # This happens in JavaScript 'for' (without the quotes)
    # statements. If all of these conditions are met, then
    # we can set a value showing that the spaces should be 
    # removed.
    if curTokType          == HDLmTokenTypes.space   and \
       len(curTok.value)   >= 1                      and \
       i                   >  0                      and \
       tokVec[i-1].tokType == HDLmTokenTypes.unknown and \
       tokVec[i-1].value   == ';':
      numberOfBlanks = 0
    # Check if the current token can be compressed or not
    if numberOfBlanks != None:
      curTok.value = curTok.value[0:numberOfBlanks] 
    # Report all cases where we were not able to convert 
    # multiple blanks into a single blank. This is not  
    # always possible. This code is disabled for now.
    if curTokType == HDLmTokenTypes.space and \
       i > 0                              and \
       i == 0                             and \
       len(curTok.value) >= 2:
      print(len(curTok.value), line)
    # We can only change variable names in some types of 
    # tokens
    if curTokType != HDLmTokenTypes.identifier:
      continue
    # Check if we have a prior token and if the prior token is a
    # period. We don't want to make any changes in this case. Of 
    # course, the prior period token might be part of an ellipsis.
    priorToken = None
    priorPriorToken = None
    priorPriorPriorToken = None
    if i > 0:
      priorToken = tokVec[i-1]
    if i > 1:
      priorPriorToken = tokVec[i-2]
    if i > 2:
      priorPriorPriorToken = tokVec[i-3]
    # Check for a prior ellipses
    priorEllipses = False
    if priorToken != None           and \
       priorPriorToken != None      and \
       priorPriorPriorToken != None and \
       priorToken.value == '.'      and \
       priorPriorToken.value == '.' and \
       priorPriorPriorToken.value == '.': 
      priorEllipses = True
    # Make sure there was a prior token. If we don't have a prior
    # token, then we can't make any changes to the current token.
    if priorToken == None:
      continue
    # Check for a special case where we don't want to change the
    # variable name. We don't want to change the variable name if
    # the prior token is a period that is not part of an ellipses.   
    if priorToken.value == '.' and priorEllipses == False:
      continue
    # The code that actually changes variable names has been 
    # commented out for now
    tempValue = changeNames.changeName(curTok.value)
    if tempValue == None:
      curName = curTok.value
      if curName not in noMatchDict:
        noMatchDict[curName] = [line]
      else:
        noMatchDict[curName].append(line)
    # Check if we are being asked to replace variable names
    # with shorter names. This is not generally true, but
    # could be true.
    if replaceNames == True:
      if tempValue != None:
        curTok.value = tempValue
  return None

# This routine does some work on a set of lines.
# The idea is that minified JavaScript will be 
# smaller than the original JavaScript. 
def minifyJavaScript(inData, noMatchDict, replaceNames):
  # Create the objects used to change variable names
  shortNames = ShortNames()
  changeNames = ChangeNames()
  changeNames.addNames(glbVarList, shortNames)
  # Don't assume that we won't be replacing variable names 
  # with shorter names
  replaceNames = replaceNames
  # Initialize a few values
  inComment = False
  # Create an array for all of the output lines
  outData = []
  # Process all of the lines in the input data
  for line in inData:  
    # Check if the current line is going to be used to 
    # build JavaScript or not. If not, then just add 
    # the current line to the output array. This has 
    # (desired) effect of including Java comments in 
    # the Java code. Note that this code is commented
    # out for now. We want to use the standard minifier
    # on the Java code. 
    # if line.find('builder.addLine("') < 0:
      # outData.append(line)
      # continue
    # The code below is used to handle JavaScript code.
    # Comments are removed as need be.
    lineComment = False
    # Check for starting and/or ending quotes
    quoteStart = line.find('/* ')
    quoteEnd = line.find(' */')
    stringDotAsteriskSlash = line.find('.*/')
    quoteSlashAsteriskAsterisk = line.find('/**')
    if quoteStart >= 0 or quoteSlashAsteriskAsterisk >= 0 or line.endswith('/*'):
      inComment = True
    if quoteEnd >= 0 and stringDotAsteriskSlash < 0:
      inComment = False
      lineComment = True
    # Skip the current line, if we are in a comment of some kind
    if inComment or lineComment:
      continue    
    # Build the string that contains the characters we consider
    # to be quotes. If we are not replacing long variable names 
    # with short variable names, then it is imperative than we
    # consider back tics to be a type of quote character.
    quoteChars = "'"  
    if replaceNames == False:
      quoteChars += "`"
    # The following lines are use to set breakpoints
    if 'protocolStringLower' in line: 
      line = line
    # Do some work on the current line. Note that some lines
    # are skipped below.
    replaceStr = line.rstrip()
    replaceStr = replaceOneCharacter(replaceStr, '"', '\u1000')
    replaceStr = replaceOneCharacter(replaceStr, "'", '\u1001')
    replaceVec = getTokensFromString(replaceStr, quoteChars) 
    if replaceVec != None:
      minifyChangeTokens(replaceVec, changeNames, line, noMatchDict, replaceNames)
      tempStr = HDLmString.convertTokens(replaceVec)
      replaceStr = replaceOneCharacter(tempStr, '\u1001', "'")
      replaceStr = replaceOneCharacter(replaceStr, '\u1000', '"')
    # Add the current line to the output lines
    outData.append(replaceStr)
  return outData

# This routine does some work on a set of lines. 
# The idea is that minified JavaScript will be 
# smaller than the original JavaScript. This 
# routine is not in use.
def minifyJavaScriptNotUsed(inData, noMatchDict, replaceNames):
  # Create the objects used to change variable names
  shortNames = ShortNames()
  changeNames = ChangeNames()
  changeNames.addNames(glbVarList, shortNames)
  # Initialize a few values
  inComment = False
  printFlag = False
  # Create an array for all of the output lines
  outData = []
  # Process all of the lines in the input data
  for line in inData:
    replaceStr = replaceDoubleQuotes(line.rstrip())
    replaceVec = getTokensFromString(replaceStr, "'")
    if replaceVec != None:
      minifyChangeTokens(replaceVec, changeNames, line, noMatchDict, replaceNames)
      tempStr = HDLmString.convertTokens(replaceVec)
      restoreStr = restoreDoubleQuotes(tempStr)
      if line.rstrip() != restoreStr:
        print(' ')
        print(line)
        print(replaceStr)
        print(tempStr)
        print(restoreStr)    
    # Check if the current line starts a comment or ends 
    # a comment, or both. As a first step we make a copy 
    # of the current line with no leading or trailing 
    # blanks
    builderAddLineStart = False
    builderAddLineEnd = False
    lineComment = False
    # Make a simple copy of the current line
    lineStrip = line
    lineStrip = lineStrip.rstrip() 
    # Look for a very specific prefix and remove the prefix
    lineFind = lineStrip.find('builder.addLine("')
    if lineFind >= 0:
      builderAddLineStart = True
      lineStrip = lineStrip[lineFind + 17:]
    # Look for a very specific suffix and remove the suffix
    if lineStrip.endswith('");'):
      builderAddLineEnd = True
      lineStrip = lineStrip[:-3]
    # Build a sum equal to the number or lines that begin and/or
    # end with a specific value
    builderSum = 0
    if builderAddLineStart:
      builderSum += 1
    if builderAddLineEnd:
      builderSum += 1
    # Remove leading and trailing blanks, but only for some
    # lines
    if builderSum == 2:
      lineStrip = lineStrip.strip()
      if lineStrip.startswith('/* '):
        inComment = True
      if lineStrip.endswith(' */'):
        inComment = False
        lineComment = True
      # Skip the current line, if we are in a comment of some kind
      if inComment or lineComment:
        continue
      # We assume that we can change variable names. That might not be
      # true.
      # changeVariableNames = True
      # Change some of the variable names in the current line
      # lineStripUnFix = lineUnFixJava(lineStrip, '"')  
      # lineStripVec = HDLmString.getTokens(lineStripUnFix, quoteChars = "'\"")
      # lineStripVecLen = len(lineStripVec)
      # count = -1
      # while (count + 1) < lineStripVecLen:
      #   count += 1
      #   token = lineStripVec[count]
        # Check for an identifier token
      #   if token.tokType != HDLmTokenTypes.identifier:
      #     continue
        # Check if we have a prior token and if the prior token is a
        # period. We don't want to make any changes in this case.
      #   if count > 0:
      #     priorToken = lineStripVec[count-1]
      #     if priorToken.value == '.':
      #       continue
        # token.value = changeNames.changeName(token.value)
      # lineStripOut = HDLmString.convertTokens(lineStripVec)
      # lineStripFix = lineFixJava(lineStripOut, '"')
      # lineStrip = lineStripFix
      # If the conversion was not successful, then we can't change
      # any variable names
      # printFlag = False
      # if lineStrip != lineStripOut and lineStrip.find('let urlStr =') >= 500:
      #   printFlag = True
      # if printFlag:
      #   print(' ')
      #   print(line)
      #   print(lineStrip)
      #   print(lineStripFix)
      #   print(lineStripOut)
    # At this point we may want to rebuild the current line
    if builderAddLineStart:
      lineStrip = '    builder.addLine("' + lineStrip
    if builderAddLineEnd:
      lineStrip = lineStrip + '");'
    if printFlag:
      print(lineStrip)
    line = lineStrip
    # Add the current line to the output lines
    outData.append(line)
  return outData 

# This routine replaces double quotes with a special character from 
# the Laotian language. Laotian was chosen because it is very rare 
# in the English speacking world.
def replaceDoubleQuotes(inStr):
  outStr = inStr
  outStrLen = len(outStr)
  for i in range(outStrLen):
    if outStr[i] == '"':
      outStr = outStr[:i] + '\u0ed6' + outStr[i+1:]
  return outStr

# This routine replaces one character with another. The original
# character might be a single quote, double quote, or a character
# from the Laotian language. Laotian has been used because it is 
# very rare in the English speacking world. The input string is  
# not changed in any way.
def replaceOneCharacter(inStr, inChar, outChar):
  outStr = inStr
  outStrLen = len(outStr)
  for i in range(outStrLen):
    if outStr[i] == inChar:
      outStr = outStr[:i] + outChar + outStr[i+1:]
  return outStr

# This routine replaces a string with another string in an 
# array of lines. The input array is not changed in any way.
# The output array (possibily changed) is returned to the
# caller.  
def replaceString(inData, oldStr, newStr):
  # Create the output array
  outData = []
  # Process all of the lines in the input datacle
  for line in inData:  
    newLine = line.replace(oldStr, newStr)
    outData.append(newLine)
  return outData

# This routine restores double quotes that were replaced with 
# a special character from the Laotian language. Laotian was
# chosen because it is very rare in the English speacking world.
def restoreDoubleQuotes(inStr):
  outStr = inStr
  outStrLen = len(outStr)
  for i in range(outStrLen):
    if outStr[i] == '\u0ed6':
      outStr = outStr[:i] + '"' + outStr[i+1:]
  return outStr

# Write the entire no match dictionary into 
# a file
def writeNoMatchDict(noMatchFileName, noMatchDict):
  # Write all of the identifiers that did not match 
  # to a file
  noMatchData = []
  keyCount = 0
  for key in sorted(noMatchDict.keys()):
    keyCount += 1     
    noMatchLine = 'Possible variable ' + key
    noMatchData.append(noMatchLine)
    curLines = noMatchDict[key]
    for curLine in curLines:
      noMatchData.append(curLine)
  HDLmUtility.writeOutputFile(noMatchData, noMatchFileName)

# Handle startup 
def startup():
  print(os.getcwd())
  os.chdir(glbPythonWorkPath)   
    
# Main program
def main():   
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()  
  # Start the program
  startup()  
  addComma = False
  indentValue = 0
  literalDict = buildChoicesLiteral() 
  outArray = []
  outArray = buildJavaFromLiteral(literalDict, outArray, indentValue, addComma)
  # Create a dictionary for all of the names that don't match
  noMatchDict = dict()
  # Build the Java script
  inData = HDLmUtility.readInputFile(glbInfile, 'cp1252')
  inData = addPrefix(inData, ' ', 2)
  inData = addBuilder(inData, 'Java')
  outData = []
  outData.extend(buildCode(docJavaFirst))
  outData.extend(inData)
  outData.extend(buildCode(docJavaApplyMods))
  outData.extend(buildCode(docJavaBuildError))
  outData.extend(buildCode(docJavaChangeAttributes)) 
  outData.extend(buildFunctions())
  # The switches built by the call below don't seem
  # to be in use
  # outData.extend(buildSwitches())
  outData.extend(buildCode(docJavaGetAttributesString))
  outData.extend(buildCode(docJavaGetLookupIndex))
  outData.extend(buildCode(docJavaGetParametersArray))
  outData.extend(buildCode(docJavaGetPHash))
  outData.extend(buildCode(docJavaHandleLinksAndEvents))
  outData.extend(buildCode(docJavaLate))
  outData.extend(buildCode(docJavaLiteralPrefix))
  outData.extend(outArray)
  outData.extend(buildCode(docJavaLiteralSuffix))
  # The call below was added just for debugging. It should only
  # be enabled for debugging and is otherwise unneeded.
  # displayLines(outData)
  suffix = 'NoCompression'
  outDataNoCompression = replaceString(outData, glbOutFile, glbOutFile + suffix)
  HDLmUtility.writeOutputFile(outDataNoCompression, glbJavaFilePath + glbOutFile + suffix + '.java')
  # The calls below causes the code to be compressed
  # in several ways 
  replaceNames = False
  outDataCompressBlanks = minifyJavaScript(outData, noMatchDict, replaceNames) 
  replaceNames = True
  outDataCompressBlanksAndNames = minifyJavaScript(outData, noMatchDict, replaceNames) 
  # Write the compressed JavaScript code to a set of files 
  suffix = 'CompressBlanks'
  outDataCompressBlanks = replaceString(outDataCompressBlanks, glbOutFile, glbOutFile + suffix)
  HDLmUtility.writeOutputFile(outDataCompressBlanks, glbJavaFilePath + glbOutFile + suffix + '.java')
  suffix = 'CompressBlanksAndNames'
  outDataCompressBlanksAndNames = replaceString(outDataCompressBlanksAndNames, glbOutFile, glbOutFile + suffix)
  HDLmUtility.writeOutputFile(outDataCompressBlanksAndNames, glbJavaFilePath + glbOutFile + suffix + '.java')
  # Write the no match dictionary to a file
  writeNoMatchDict(glbNoMatchFile, noMatchDict)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()