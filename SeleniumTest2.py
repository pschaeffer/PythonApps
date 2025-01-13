from   datetime import timezone
from   HDLmBuildLines  import *
from   HDLmHtml        import *
from   HDLmString      import *
from   HDLmUrl         import *
from   HDLmUtility     import *
from   HDLmWebSite     import *
from   selenium import webdriver
from   selenium.webdriver.common import desired_capabilities
from   selenium.webdriver.common.by import By
from   selenium.webdriver.common.keys import Keys
from   selenium.webdriver.support.select import Select
from   skimage.metrics import structural_similarity as ssim
import argparse 
import cv2
import datetime
import matplotlib.pyplot as plt
# import mouseinfo 
import numpy as np
import platform
import sys 
import time
import urllib

# The list below contains the standard browser names. These names must be
# converted to other strings to start/stop applications (browsers in this
# case), find files, etc. Note that Microsoft Edge is listed as Microsoft
# Edge and just Edge. 
glbBrowserTypes = ['Brave Browser', 'Chrome', 'Dolphin Browser', 'Edge', 
                   'Firefox', 'Internet Explorer', 'Microsoft Edge',
                   'Opera', 'Safari', 'UC Browser',
                    'Yandex']

# All of the known languages are listed below
glbLanguageList = ['EN', 'FR', 'DE', 'ES', 'PT', 'IT',
                   'JA', 'CN', 'TW', 'HI', 'KO']

# The next global variable contains the code that does node
# identification
glbNodeIdenJS = \
"""
/* This is the JavaScript function that reports an error */
function HDLmBuildError(severity, type, number, text) {
  let errorStr = '';
  errorStr += 'HDLm' + ' ';
  errorStr += severity + ' ';
  errorStr += type + ' ';
  errorStr += number.toString() + ' ';
  errorStr += text;
  console.log(errorStr);
}
/* This function does a case insensitive string comparison. Of course,
   this function can be changed as need be to use better case insensitive
   string comparisons. This routine will return true if the strings
   are equal. This routine will return false if the strings are not
   equal. */
function HDLmCompareCaseInsensitive(firstStr, secondStr) {
  return firstStr.localeCompare(secondStr, undefined, { sensitivity: 'accent' }) === 0;
}
/* This JavaScript function tries to find a set of HTML elements 
   (DOM elements) that match the node identifier passed by the
   caller. The DOM is always searched using one of the built-in
   DOM functions. 

   A copy of this code is use to test for ambiguous sets of node
   identifier information in the browser extension code. The code
   in the copy is a slightly modified version of this code. */ 
function HDLmFindNodeIden(curMod, nodeIdenTracing) {
  let   nodeElement;
  let   nodeElements = [];
  let   nodeIden = curMod.nodeiden;
  let   nodeList = []; 
  let   nodeAttributes = nodeIden.attributes;
  let   nodeCounts = nodeIden.counts;
  let   nodeType = nodeIden.type;
  /* We need to use a different function depending on the type
     of node identifier */
  switch (nodeType) {
    /* We may be searching by tag name. This might work in some
       cases. */
    case 'tag': {
      let nodeTag = nodeAttributes.tag;
      nodeElements = document.getElementsByTagName(nodeTag);
      break;
    }
    /* We may be searching by id. This will only work if the id
       values are permanent, rather than generated. Generated id
       values change each time a web page is loaded. As a consequence,
       they can not be used. */
    case 'id': {
      let nodeId = nodeAttributes.id;
      nodeElement = document.getElementById(nodeId);
      if (nodeElement != null)
        nodeElements = [nodeElement];
      else
        nodeElements = [];
      break;   
    }
    /* We may be searching by class name. Class names tend to be 
       relatively permanent and hence are a good thing to search
       for. Of course, an HTML DOM node can have more than one 
       class name. The first class name is always used. */
    case 'class': {
      let nodeClassList = nodeAttributes.class;
      let nodeClass = nodeClassList[0];
      nodeElements = document.getElementsByClassName(nodeClass);
      break; 
    }
    /* We may be searching by name. This will work in some cases. */
    case 'name': {
      let nodeName = nodeAttributes.name;
      nodeElements = document.getElementsByName(nodeName);
      break;
    }
    default: {
      let errorText = "Invalid node identifier type value - " + nodeType;
      HDLmBuildError('Error', 'NodeIden', 40, errorText);
      break;
    }
  }   
  /* Save the number of node elements found in a local variable. This variable
     is used in several places below. */
  let   nodeElementsLength = nodeElements.length;
  /* Check if node identifier tracing is active or not. Trace the 
     number of nodes, if need be. */
  if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
    let   errorText = `Node identifier - get for (${nodeType}) returned (${nodeElementsLength}) nodes`;
    HDLmBuildError('Trace', 'NodeIden', 41, errorText);
  }
  /* Check for a very special case. If the original node identifier collection
     found just one DOM HTML element for the current type and if current document
     search also found just one DOM HTML element for the current type, then we 
     may be done. We specify a different type of attribute check in this case. */
  let nodeIdenCheckType = 'full';
  if (nodeCounts[nodeType] == 1 && nodeElementsLength == 1)
    nodeIdenCheckType = 'partial';
  /* At this point we have a set of HTML node elements. Some of them
     may really match the node identifier criteria. Others may not. */
  nodeList = HDLmFindNodeIdenCheck(nodeElements, 
                                   nodeIden, 
                                   nodeIdenCheckType,
                                   nodeIdenTracing);
  return nodeList;
}
/* This routine takes a list of HTML node elements and checks each one.
   If an HTML node matches the current attributes (well enough), it is
   added to the output list of HTML nodes that is returned to the caller. */
function HDLmFindNodeIdenCheck(nodeElements, 
                               nodeIden, 
                               nodeIdenCheckType,
                               nodeIdenTracing) {
  let nodeList = [];
  for (let currentElement of nodeElements) {
    let   nodeCurrentAttributes = nodeIden.attributes;
    let   currentMatchValue = HDLmFindNodeIdenMatch(currentElement, 
                                                    nodeCurrentAttributes,
                                                    nodeIdenTracing);
    /* Check if node identifier tracing is active or not. Trace the 
       match value, if need be. */
    if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
      let   errorText = `Node identifier - current match value (${currentMatchValue}) for element (${currentElement})`;
      HDLmBuildError('Trace', 'NodeIden', 41, errorText);
    }
    if (currentMatchValue < 0.95)
      continue;
    /* We now need to check the attributes of the parent of the current
       HTML DOM element, if possible */
    let   parentElement = currentElement.parentElement;
    if (parentElement != null) {
      let   nodeParentAttributes = nodeIden.parent;
      let   parentMatchValue = HDLmFindNodeIdenMatch(parentElement, 
                                                     nodeParentAttributes,
                                                     nodeIdenTracing);
      /* Check if node identifier tracing is active or not. Trace the 
         match value, if need be. */
      if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
        let   errorText = `Node identifier - parent match value (${parentMatchValue}) for element (${parentElement})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
      }
      if (parentMatchValue < 0.95)
        continue;
    } 
    nodeList.push(currentElement);    
  }
  return nodeList;
}
/* This routine takes one HTML node element and checks how well it matches 
   a set of attributes. The final match score is returned to the caller. 
   The final match score is a floating-point value in the range of 0.0
   to 1.0. The HTML DOM element (node element) and the expected node
   attributes are passed by the caller. */ 
function HDLmFindNodeIdenMatch(nodeElement, nodeAttributes, nodeIdenTracing) {
  let   denominator = 0.0;
  let   nodeActualValue;
  let   nodeAttributeTagUpper = nodeAttributes.tag.toUpperCase();
  let   numerator = 0.0;
  let   numeratorIncrementValue;
  /* Check for a quick exit. If the tag name doesn't match, then 
     we are done. We insist that the tag name match immediately
     and exactly. */
  if (nodeElement.tagName != nodeAttributeTagUpper)
    return 0.0;
  /* Check all of the attributes passed by the caller. Get the
     set of keys for each of the attributes. The keys are used
     to obtain the expected and actual value of each attribute. */
  let nodeAttributeKeys = Object.keys(nodeAttributes);
  for (let nodeAttributeKey of nodeAttributeKeys) {
    numeratorIncrementValue = 0.0;
    /* Always bump the denominator. This is done for all 
       attributes including those that don't match. */
    denominator++;
    /* Get the current node attributes expected value from the node
       attributes passed by the caller. Note that these are the 
       expected values. For most attributes this is a string. For
       class attributes, this is an array of class names. */
    let nodeAttributeValue = nodeAttributes[nodeAttributeKey];
    /* Check if the attribute we want is the tag. The tag is not really 
       an attribute. Special case code is needed to handle the tag.
       A special call is needed to get the actual tag name of the 
       DOM element. This call will always return the tag name in 
       uppercase. As a consequence, the expected value must also be
       changed to uppercase. */
    if (nodeAttributeKey == 'tag') {
      nodeActualValue = nodeElement.tagName;
      nodeAttributeValue = nodeAttributeValue.toUpperCase();
      /* Check if node identifier tracing is active or not. Trace the 
         attribute values, if need be. */
      if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
        let   errorText;
        let   traceValue = 0.0;
        if (nodeActualValue != null &&
            nodeAttributeValue == nodeActualValue)
          traceValue = 1.0;
        errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
      }
      /* If we don't have a value that we can compare, then we are done */
      if (nodeActualValue == null)
        continue;
      /* Compare the expected value and the actual value. If they are the
         same, then we can increment the numerator. */
      if (nodeAttributeValue == nodeActualValue)
        numeratorIncrementValue = 1.0;
    }
    /* Check if the attribute we want is the class. The class in the
       DOM element is always just one string. However, the DOM class
       string can have several class names in it. The code below
       extracts the first actual (DOM) class name and the first 
       expected class name. */ 
    else if (nodeAttributeKey == 'class') {
      let nodeActualValueString = nodeElement.getAttribute('class');
      if (nodeActualValueString != null) { 
        /* Split the class attribute into an array of values */
        let nodeActualValueSplitArray = nodeActualValueString.split(' '); 
        let nodeActualValueSplitArrayLen = nodeActualValueSplitArray.length;
        let nodeActualValueSplit = [];
        /* Check if each value ends with a newline. Remove the newline. Add
           all of the remaining entries to the output array, if the remaining
           length is greater than zero. */
        for (let i = 0; i < nodeActualValueSplitArrayLen; i++) {
          /* Get the current value */
          let nodeActualValueSplitValue = nodeActualValueSplitArray[i];
          /* Remove the trailing newline character, if need be */
          if (nodeActualValueSplitValue.endsWith('\n')) {
            let nodeActualValueSplitValueLen = nodeActualValueSplitValue.length;
            nodeActualValueSplitValue = nodeActualValueSplitValue.substr(0, nodeActualValueSplitValueLen-1);
          }
          /* If the remaining length is greater than zero, add the value to the 
             output array */
          if (nodeActualValueSplitValue.length > 0)
            nodeActualValueSplit.push(nodeActualValueSplitValue);
        }
        /* Check if we can actually get the actual value from the output 
           array */
        if (nodeActualValueSplit.length > 0)
          nodeActualValue = nodeActualValueSplit[0];
        else
          nodeActualValue = null;
      }
      else
        nodeActualValue = null;
      /* Check if node identifier tracing is active or not. Trace the 
         attribute values, if need be. */
      if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
        let   errorText;
        let   traceValue = 0.0;
        if (nodeActualValue != null &&
            nodeAttributeValue.includes(nodeActualValue))
          traceValue = 1.0;
        errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
      }
      /* If we don't have a value that we can compare, then we are done */
      if (nodeActualValue == null)
        continue;
      /* Check if the actual value (the first actual class value) is one of 
         the expected class values. If this is true, then we can increment
         the numerator. */
      if (nodeAttributeValue.includes(nodeActualValue))
        numeratorIncrementValue = 1.0;
    } 
    /* Check if the attribute we want is the inner text. The inner
       text is not really an attribute. Special case code is needed 
       to handle the inner text. A special call is needed to get the
       actual inner text (if any) for a DOM element. Note that the
       inner text (if any) is always converted to lower case. This 
       is because the inner text has a bad habit of changing case, 
       as the browser window changes size. To make the inner text 
       more stable, we always convert it to lower case.*/
    else if (nodeAttributeKey == 'innertext') {
      let nodeIndexOf;
      let nodeInnerText = nodeElement.innerText;
      if ((typeof nodeInnerText) == 'undefined')
        nodeInnerText = null;
      if (nodeInnerText != null) {
        nodeIndexOf = nodeInnerText.indexOf('¦');
        if (nodeIndexOf >= 0)
          nodeInnerText = nodeInnerText.substring(0, nodeIndexOf);
        nodeIndexOf = nodeInnerText.indexOf('\n');
        if (nodeIndexOf >= 0)
          nodeInnerText = nodeInnerText.substring(0, nodeIndexOf);
        nodeInnerText = nodeInnerText.toLowerCase().trim();
        if (nodeInnerText.length > 20)
          nodeInnerText = nodeInnerText.substring(0, 20);
      }
      nodeActualValue = nodeInnerText;
      /* Check if node identifier tracing is active or not. Trace the 
         attribute values, if need be. */
      if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
        let   errorText;
        let   traceValue = 0.0;
        if (nodeActualValue != null &&
            HDLmCompareCaseInsensitive(nodeAttributeValue, nodeActualValue))
          traceValue = 1.0;
        errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
      }
      /* If we don't have a value that we can compare, then we are done */
      if (nodeActualValue == null)
        continue;
      /* Compare the expected value and the actual value. If they are the
         same, then we can increment the numerator. */
      if (HDLmCompareCaseInsensitive(nodeAttributeValue, nodeActualValue))
        numeratorIncrementValue = 1.0;
    }
    /* Check if the attribute we want is the perceptual hash. The
       perceptual hash is not really an attribute and cannot be 
       compared. Note that the actual DOM will naver have a node
       with a perceptual hash value. */
    else if (nodeAttributeKey == 'phash') {
      /* Use the attribute value as the actual value. This way they
         will always compare as equal. */
      nodeActualValue = nodeAttributeValue;
      /* Check if node identifier tracing is active or not. Trace the 
         attribute values, if need be. */
      if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
        let   errorText;
        let   traceValue = 0.0;
        if (nodeActualValue != null &&
            HDLmCompareCaseInsensitive(nodeAttributeValue, nodeActualValue))
          traceValue = 1.0;
        errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
      }
      /* If we don't have a value that we can compare, then we are done */
      if (nodeActualValue == null)
        continue;
      /* Compare the expected value and the actual value. If they are the
         same, then we can increment the numerator. */
      if (HDLmCompareCaseInsensitive(nodeAttributeValue, nodeActualValue))
        numeratorIncrementValue = 1.0;
    }
    /* Check if the attribute we want is the source (src). Generally 
       src values can be compared in a completely conventional way. 
       However, if the source is a URL (very common) and if we have 
       a perceptual hash value for the URL, then we really want to
       compare the perceptual hash value, not the URL for the image. 
       This is a very complex process (to say the least). */
    else if (nodeAttributeKey == 'src') {
      nodeActualValue = nodeElement.getAttribute(nodeAttributeKey); 
      let   nodePHashCheck = false;
      /* The dummy loop below is used to allow break to work */
      while (true) {
        let   nodeActualIndex;
        let   nodeActualPHash;
        let   nodeActualUrl; 
        let   nodeAttributesPHashSimilarity;
        /* Check if the actual node value is null. This can happen
           if the source is provided by CSS. */
        if (nodeActualValue == null)
          break; 
        /* Try to find the URL in the actual source */
        nodeActualIndex = nodeActualValue.indexOf('http');
        if (nodeActualIndex < 0)
          break;
        nodeActualUrl = HDLmRemoveProtocol(nodeActualValue);  
        /* Try to get the perceptual hash value for the current URL */
        nodeActualPHash = HDLmFindPHash(nodeActualUrl);
        if (nodeActualPHash == null) {
          HDLmGetPHash(nodeActualUrl);
          break;
        }
        /* Get the current node attributes perceptual hash expected value
           from the node attributes passed by the caller. Note that this
           is an expected value. This should be a 64-bit number returned 
           as a 16-digit hexadecimal string. */   
        if (nodeAttributes.hasOwnProperty('phash') == false)
          break;
        let nodeAttributesPHashValue = nodeAttributes['phash'];
        /* At this point we can compare the perceptual hash values and 
           show that a perceptual hash comparison was completed */
        nodeAttributesPHashSimilarity = HDLmHammingDistanceAdjusted(nodeAttributesPHashValue, 
                                                                    nodeActualPHash);
        nodePHashCheck = true;
        /* Check if node identifier tracing is active or not. Trace the 
           perceptual hash values, if need be. */
        if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
          let   errorText;
          errorText = `Node identifier - key (perceptual hash) actual (${nodeActualPHash}) expected (${nodeAttributesPHashValue})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
          errorText = `Node identifier - key (perceptual hash) comparison value (${nodeAttributesPHashSimilarity})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        }
        /* Check if the perceptual hash simularity value is low enough */
        if (nodeAttributesPHashSimilarity < 0.10) {
          numeratorIncrementValue = 1.0;
        }
        break;
      }
      /* The code below only needs to be executed if we were not able
         to compare the perceptual hash values */
      if (nodePHashCheck == false) {
        /* Check if node identifier tracing is active or not. Trace the 
           attribute values, if need be. */
        if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
          let   errorText;
          let   traceValue = 0.0;
          if (nodeActualValue != null &&
              nodeAttributeValue == nodeActualValue)
            traceValue = 1.0;
          errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
          errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        } 
        /* If we don't have a value that we can compare, then we are done */
        if (nodeActualValue == null)
          continue;
        /* Compare the expected value and the actual value. If they are the
           same, then we can increment the numerator. */
        if (nodeAttributeValue == nodeActualValue)
          numeratorIncrementValue = 1.0;
      }
    }
    /* Check if the attribute we want is the style. Generally styles
       can be compared in a completely conventional way. However, if
       the style uses a background image and if we have a perceptual
       hash value for the background image, then we really want to
       compare the perceptual hash value, not the URL for the image. 
       This is a very complex process (to say the least). */
    else if (nodeAttributeKey == 'style') {
      nodeActualValue = nodeElement.getAttribute(nodeAttributeKey); 
      let   nodePHashCheck = false;
      /* The dummy loop below is used to allow break to work */
      while (true) {
        let   nodeActualIndex;
        let   nodeActualPHash;
        let   nodeActualUrl; 
        let   nodeAttributesPHashSimilarity;
        /* Check if the actual node value is null. This can happen
           if the style is provided by CSS. */
        if (nodeActualValue == null)
          break; 
        /* Check for a required keyword in the style */
        nodeActualIndex = nodeActualValue.indexOf('background-image');
        if (nodeActualIndex < 0)
          break;
        /* Try to find the URL in the actual style */
        nodeActualIndex = nodeActualValue.indexOf('url("http');
        if (nodeActualIndex < 0)
          break;
        nodeActualUrl = nodeActualValue.substr(nodeActualIndex+5);
        /* Get rid of the trailing part of the URL */
        nodeActualIndex = nodeActualUrl.indexOf('")');
        if (nodeActualIndex < 0)
          break
        nodeActualUrl = nodeActualUrl.substring(0, nodeActualIndex);
        nodeActualUrl = HDLmRemoveProtocol(nodeActualUrl);  
        /* Try to get the perceptual hash value for the current URL */
        nodeActualPHash = HDLmFindPHash(nodeActualUrl);
        if (nodeActualPHash == null) {
          HDLmGetPHash(nodeActualUrl);
          break;
        }
        /* Get the current node attributes perceptual hash expected value
           from the node attributes passed by the caller. Note that this
           is an expected value. This should be a 64-bit number returned 
           as a 16-digit hexadecimal string. */   
        if (nodeAttributes.hasOwnProperty('phash') == false)
          break;
        let nodeAttributesPHashValue = nodeAttributes['phash'];
        /* At this point we can compare the perceptual hash values and 
           show that a perceptual hash comparison was completed */
        nodeAttributesPHashSimilarity = HDLmHammingDistanceAdjusted(nodeAttributesPHashValue, 
                                                                    nodeActualPHash);
        nodePHashCheck = true;
        /* Check if node identifier tracing is active or not. Trace the 
           perceptual hash values, if need be. */
        if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
          let   errorText;
          errorText = `Node identifier - key (perceptual hash) actual (${nodeActualPHash}) expected (${nodeAttributesPHashValue})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
          errorText = `Node identifier - key (perceptual hash) comparison value (${nodeAttributesPHashSimilarity})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        }
        /* Check if the perceptual hash simularity value is low enough */
        if (nodeAttributesPHashSimilarity < 0.10) {
          numeratorIncrementValue = 1.0;
        }
        break;
      }
      /* The code below only needs to be executed if we were not able
         to compare the perceptual hash values */
      if (nodePHashCheck == false) {
        /* Check if node identifier tracing is active or not. Trace the 
           attribute values, if need be. */
        if (nodeIdenTracing == HDLmNodeIdenTracing.all) {
          let   errorText;
          let   traceValue = 0.0;
          if (nodeActualValue != null &&
              nodeAttributeValue == nodeActualValue)
            traceValue = 1.0;
          errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
          errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
          HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        } 
        /* If we don't have a value that we can compare, then we are done */
        if (nodeActualValue == null)
          continue;
        /* Compare the expected value and the actual value. If they are the
           same, then we can increment the numerator. */
        if (nodeAttributeValue == nodeActualValue)
          numeratorIncrementValue = 1.0;
      }
    }
    /* For all other attributes, we can just extract the actual 
       attribute value from the DOM element */
    else {
      nodeActualValue = nodeElement.getAttribute(nodeAttributeKey); 
      /* Check if the attribute we want is href. Special case code 
         is needed for handling href. Basically, we need to remove
         the protocol and host before we do any matching on href.
         This was done in building the node identifier. */
      if (nodeAttributeKey == 'href') 
        nodeActualValue = HDLmRemoveHost(nodeActualValue); 
      /* Check if node identifier tracing is active or not. Trace the 
         attribute values, if need be. */
      if (nodeIdenTracing == HDLmNodeIdenTracing.all {
        let   errorText;
        let   traceValue = 0.0;
        if (nodeActualValue != null &&
            nodeAttributeValue == nodeActualValue)
          traceValue = 1.0;
        errorText = `Node identifier - key (${nodeAttributeKey}) actual (${nodeActualValue}) expected (${nodeAttributeValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
        errorText = `Node identifier - key (${nodeAttributeKey}) comparison value (${traceValue})`;
        HDLmBuildError('Trace', 'NodeIden', 41, errorText);
      } 
      /* If we don't have a value that we can compare, then we are done */
      if (nodeActualValue == null)
        continue;
      /* Compare the expected value and the actual value. If they are the
         same, then we can increment the numerator. */
      if (nodeAttributeValue == nodeActualValue)
        numeratorIncrementValue = 1.0;
    }
    /* Possibly increment the numerator */
    numerator += numeratorIncrementValue;
  }
  return numerator / denominator;
}
/* The next routine takes an input URL and removes the protocol
   and the host name from it (if they are present). The returned
   value is the path string followed by the search string followed
   by the fragment string. */
function HDLmRemoveHost(urlStr) {
  /* Check if the passed URL string has a colon in it. If it does
     not have a colon, then we can just return the input string 
     to the caller. */
  if (urlStr.indexOf(':') < 0)
    return urlStr;
  /* Build a URL object from the input string */
  let urlObj = new URL(urlStr);
  /* Return the part of the URL after the protocol, host name,
     and port number */
  return urlStr.substring(urlObj.origin.length);
}
"""

# Specify the output file name prefix
glbOutputFilePrefix = 'TestResults'

# All of the known ticket packages are listed below
glbPackageList = ['stan', 'combo', 'all']

# The lists below are standard and non-standard CSS property names. Some of these
# property names return actual values. Other property names return empty strings. 
glbPropertiesBackground = ['background', 'background-attachment', 
                           'background-color', 'background-image', 'background-position', 
                           'background-repeat']
glbPropertiesBorder = ['border-color', 'border-style', 'border-radius', 'border-width',
                       'border-width-bottom', 'border-width-left', 'border-width-right', 'border-width-top']
glbPropertiesBox = ['border-width-bottom', 'border-width-left', 'border-width-right', 'border-width-top',
                    'margin-bottom', 'margin-left', 'margin-right', 'margin-top',
                    'padding-bottom', 'padding-left', 'padding-right', 'padding-top']
glbPropertiesCss = ['background', 'color', 'font', 'margin', 'padding', 'text-align', 'width']
glbPropertiesFont = ['font-family', 'font-size', 'font-style', 'font-variant', 'font-weight', 'line-height']
glbPropertiesMargin = ['margin-bottom', 'margin-left', 'margin-right', 'margin-top']
glbPropertiesPadding = ['padding', 'padding-bottom', 'padding-left', 'padding-right', 'padding-top']
glbPropertiesShorthand = ['animation', 'background', 'border', 'border-bottom', 'border-color', 
                          'border-left', 'border-radius', 'border-right', 'border-style', 'border-top',
                          'border-width', 'column-rule', 'columns', 'flex', 'flex-flow', 'font', 'grid', 'grid-area',
                          'grid-column', 'grid-row', 'grid-template', 'list-style', 'margin', 'offset', 'outline',
                          'overflow', 'padding', 'place-content', 'place-items', 'place-self',
                          'text-decoration', 'transition']
glbPropertiesCssList = ['align-content', 'align-items', 'align-self', 'all', 'animation', 'animation-delay', 
                        'animation-direction', 'animation-duration', 'animation-fill-mode', 'animation-iteration-count', 
                        'animation-name', 'animation-play-state', 'animation-timing-function', 'backface-visibility', 
                        'background', 'background-attachment', 'background-blend-mode', 'background-clip', 'background-color', 
                        'background-image', 'background-origin', 'background-position', 'background-repeat', 'background-size', 
                        'block-size',
                        'border', 
                        'border-block-end-color', 'border-block-start-color', 
                        'border-bottom', 'border-bottom-color', 'border-bottom-left-radius', 'border-bottom-right-radius', 
                        'border-bottom-style', 'border-bottom-width', 'border-collapse', 'border-color', 'border-image', 
                        'border-image-outset', 'border-image-repeat', 'border-image-slice', 'border-image-source', 
                        'border-image-width',
                        'border-inline-end-color', 'border-inline-start-color',                        
                        'border-left', 'border-left-color', 'border-left-style', 'border-left-width', 
                        'border-radius', 'border-right', 'border-right-color', 'border-right-style', 'border-right-width', 
                        'border-spacing', 'border-style', 'border-top', 'border-top-color', 'border-top-left-radius', 
                        'border-top-right-radius', 'border-top-style', 'border-top-width', 'border-width', 'bottom', 
                        'box-decoration-break', 'box-shadow', 'box-sizing', 'caption-side', 'caret-color', '@charset', 
                        'clear', 'clip', 'clip-path', 'color', 'column-count', 'column-fill', 'column-gap', 'column-rule', 
                        'column-rule-color', 'column-rule-style', 'column-rule-width', 'column-span', 'column-width', 
                        'columns', 'content', 'counter-increment', 'counter-reset', 'cursor', 'direction', 'display', 
                        'empty-cells', 'filter', 'flex', 'flex-basis', 'flex-direction', 'flex-flow', 'flex-grow', 
                        'flex-shrink', 'flex-wrap', 'float', 'font', '@font-face', 'font-family', 'font-kerning', 
                        'font-size', 'font-size-adjust', 'font-stretch', 'font-style', 'font-variant', 'font-weight', 
                        'grid', 'grid-area', 'grid-auto-columns', 'grid-auto-flow', 'grid-auto-rows', 'grid-column', 
                        'grid-column-end', 'grid-column-gap', 'grid-column-start', 'grid-gap', 'grid-row', 'grid-row-end', 
                        'grid-row-gap', 'grid-row-start', 'grid-template', 'grid-template-areas', 'grid-template-columns', 
                        'grid-template-rows', 'hanging-punctuation', 'height', 'hyphens', '@import', 
                        'inline-size',
                        'insert-block-end', 'insert-block-start', 'insert-inline-end', 'insert-inline-end',
                        'isolation', 
                        'justify-content', '@keyframes', 'left', 'letter-spacing', 'line-height', 'list-style', 
                        'list-style-image', 'list-style-position', 'list-style-type', 'margin',
                        'margin-block-end', 'margin-block-start',
                        'margin-bottom', 
                        'margin-inline-end', 'margin-inline-start',
                        'margin-left', 'margin-right', 'margin-top', 'max-height', 'max-width', '@media', 'min-height', 
                        'min-width', 'mix-blend-mode', 'object-fit', 'object-position', 'opacity', 'order', 'outline', 
                        'outline-color', 'outline-offset', 'outline-style', 'outline-width', 'overflow', 'overflow-x', 
                        'overflow-y', 'padding', 
                        'padding-block-end', 'padding-block-start',
                        'padding-bottom',
                        'padding-inline-end', 'padding-inline-start',
                        'padding-left', 'padding-right', 'padding-top',
                        'page-break-after', 'page-break-before', 'page-break-inside', 'perspective', 'perspective-origin',
                        'pointer-events', 'position', 'quotes', 'resize', 'right', 'scroll-behavior', 'tab-size', 
                        'table-layout', 'text-align', 'text-align-last', 'text-decoration', 'text-decoration-color', 
                        'text-decoration-line', 'text-decoration-style', 'text-indent', 'text-justify', 'text-overflow', 
                        'text-shadow', 'text-transform', 'top', 'transform', 'transform-origin', 'transform-style', 
                        'transition', 'transition-delay', 'transition-duration', 'transition-property', 
                        'transition-timing-function', 'unicode-bidi', 'user-select', 'vertical-align', 'visibility', 
                        'white-space', 'width', 'word-break', 'word-spacing', 'word-wrap', 'writing-mode', 'z-index']

# The literal below lists all of the test cases. Of course, new test
# cases can be added at any time.
glbTests = [              
             # Check if the bottom CTA button is wider than the overall site logo (top center)
             ['Open page for start of tests',       {'Script Id': 1, 'Test Case': 1, 'Step Number': 1}, 'testHomePageStart'],
             ['For start reset language to en-US',  {'Script Id': 1, 'Test Case': 1, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['For start examine CTA',              {'Script Id': 1, 'Test Case': 1, 'Step Number': 3}, 'testBottomCta'],
             ['For start CTA/Button is no wider',   {'Script Id': 1, 'Test Case': 1, 'Step Number': 4}, 'testCheckNoWider'],
             ['Close page for start of tests',      {'Script Id': 1, 'Test Case': 1, 'Step Number': 5}, 'testHomePageEnd'],
             # Check if a set of fields are not pre-populated 
             ['Open page for packages',             {'Script Id': 2, 'Test Case': 4, 'Step Number': 1}, 'testHomePageStart'],
             ['For start reset language to en-US',  {'Script Id': 2, 'Test Case': 4, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Click on CTA in top right nav',      {'Script Id': 2, 'Test Case': 4, 'Step Number': 3}, 'testClickTopRightCta'],
             ['Click CTA for buying tickets',       {'Script Id': 2, 'Test Case': 4, 'Step Number': 4, 'Test Language': 'EN'}, 
                                                                                                       'testCtaBuyingTickets'],
             ['Select CTA for Morning Package',     {'Script Id': 2, 'Test Case': 4, 'Step Number': 5, 'Test Language': 'EN'},
                                                                                                       'testSelectMorning'],
             ['Select 1 ticket for the Adult',      {'Script Id': 2, 'Test Case': 4, 'Step Number': 6}, 'testSelectOneAdultTicket'],
             ['Click next',                         {'Script Id': 2, 'Test Case': 4, 'Step Number': 7, 'Test XPath': 
                                                                                                       '//*[@id="next-btn"]'},
                                                                                                       'testClickXPath'],
             ['Click on No Thanks',                 {'Script Id': 2, 'Test Case': 4, 'Step Number': 8, 'Test Language': 'EN'},
                                                                                                       'testClickNoThanks'],
             ['Advance date and pick time',         {'Script Id': 2, 'Test Case': 4, 'Step Number': 9, 'Test Language': 'EN'},
                                                                                                       'testAdvanceDateAndTime'],
             ['Click checkout',                     {'Script Id': 2, 'Test Case': 4, 'Step Number': 10, 'Test XPath': 
                                                                                                        '//*[@id="cart-proceed-to-checkout-btn"]'},
                                                                                                        'testClickXPath'],          
             ['Click shipping',                     {'Script Id': 2, 'Test Case': 4, 'Step Number': 11, 'Test XPath': 
                                                                                                        '//*[@id="shipping-continue-shipping-btn"]'},
                                                                                                        'testClickXPath'],
             ['Click credit',                       {'Script Id': 2, 'Test Case': 4, 'Step Number': 12, 'Test XPath': 
                                                     '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[3]/div/div/div[1]/div/div/label'},
                                                                                                        'testClickXPath'],
             ['Click continue',                     {'Script Id': 2, 'Test Case': 4, 'Step Number': 13}, 'testClickContinue'],
             ['No pre-populated data',              {'Script Id': 2, 'Test Case': 4, 'Step Number': 14}, 'testNoPrePopulated'],
             ['Close page for packages',            {'Script Id': 2, 'Test Case': 4, 'Step Number': 15}, 'testHomePageEnd'],
             ['Repeat for the other two',           {'Script Id': 2, 'Test Case': 4, 'Step Number': 16}, 'testRepeatOtherTwo'],    
             # Check two specific tags for specific English language values
             ['Open page for new language',         {'Script Id': 3, 'Test Case': 3, 'Step Number': 1}, 'testHomePageStart'],
             ['Reset language to en-US',            {'Script Id': 3, 'Test Case': 3, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Select a different language',        {'Script Id': 3, 'Test Case': 3, 'Step Number': 3, 'Test Language': 'FR'}, 
                                                                                                       'testSpecifyForeignLanguage'],
             ['Re-enter URL',                       {'Script Id': 3, 'Test Case': 3, 'Step Number': 4, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Last two tabs on the right',         {'Script Id': 3, 'Test Case': 3, 'Step Number': 5}, 'testLastTwoTabs'],
             ['Close page for new language',        {'Script Id': 3, 'Test Case': 3, 'Step Number': 6}, 'testHomePageEnd'],
             # Check if a set of CTA fields and related fields use the same text
             ['Open page for matching text',        {'Script Id': 4, 'Test Case': 2, 'Step Number': 1}, 'testHomePageStart'],
             ['Matching text reset first',          {'Script Id': 4, 'Test Case': 2, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Matching text reset second',         {'Script Id': 4, 'Test Case': 2, 'Step Number': 3, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Matching text click top right',      {'Script Id': 4, 'Test Case': 2, 'Step Number': 4}, 'testClickTopRightCta'],
             ['Matching text check text matches',   {'Script Id': 4, 'Test Case': 2, 'Step Number': 5, 'Test Language': 'EN'}, 
                                                                                                       'testMatchingText'],
             ['Close page for matching text',       {'Script Id': 4, 'Test Case': 2, 'Step Number': 6}, 'testHomePageEnd'],
             # Verify that https is used for a set of ticket purchasing related pages
             ['Open page for secure',               {'Script Id': 5, 'Test Case': 5, 'Step Number': 1}, 'testHomePageStart'],
             ['Secure text reset',                  {'Script Id': 5, 'Test Case': 5, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Secure check 1',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 3}, 'testVerifySecure'],
             ['Click on CTA for secure',            {'Script Id': 5, 'Test Case': 5, 'Step Number': 4}, 'testClickTopRightCta'],
             ['Secure check 2',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 5}, 'testVerifySecure'],
             ['Click CTA for secure',               {'Script Id': 5, 'Test Case': 5, 'Step Number': 6, 'Test Language': 'EN'}, 
                                                                                                       'testCtaBuyingTickets'],
             ['Secure check 3',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 7}, 'testVerifySecure'],
             ['Click CTA for Morning secure',       {'Script Id': 5, 'Test Case': 5, 'Step Number': 8, 'Test Language': 'EN'}, 
                                                                                                       'testSelectMorning'],
             ['Secure check 4',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 9}, 'testVerifySecure'],
             ['Select 1 ticket for secure',         {'Script Id': 5, 'Test Case': 5, 'Step Number': 10}, 'testSelectOneAdultTicket'],
             ['Secure check 5',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 11}, 'testVerifySecure'],
             ['Secure Click next',                  {'Script Id': 5, 'Test Case': 5, 'Step Number': 12, 'Test XPath': 
                                                                                                        '//*[@id="next-btn"]'},
                                                                                                        'testClickXPath'],
             ['Secure check 6',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 13}, 'testVerifySecure'],
             ['Secure click on No Thanks',          {'Script Id': 5, 'Test Case': 5, 'Step Number': 14, 'Test Language': 'EN'}, 
                                                                                                        'testClickNoThanks'],
             ['Secure check 7',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 15}, 'testVerifySecure'],
             ['Secure advance date and pick time',  {'Script Id': 5, 'Test Case': 5, 'Step Number': 16, 'Test Language': 'EN'}, 
                                                                                                        'testAdvanceDateAndTime'],
             ['Secure check 8',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 17}, 'testVerifySecure'],
             ['Secure click checkout',              {'Script Id': 5, 'Test Case': 5, 'Step Number': 18, 'Test XPath': 
                                                                                                        '//*[@id="cart-proceed-to-checkout-btn"]'},
                                                                                                        'testClickXPath'],
             ['Secure click shipping',              {'Script Id': 5, 'Test Case': 5, 'Step Number': 19, 'Test XPath': 
                                                                                                        '//*[@id="shipping-continue-shipping-btn"]'},
                                                                                                        'testClickXPath'],
             ['Secure check 9',                     {'Script Id': 5, 'Test Case': 5, 'Step Number': 20}, 'testVerifySecure'],
             ['Secure click credit',                {'Script Id': 5, 'Test Case': 5, 'Step Number': 21, 'Test XPath': 
                                                     '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[3]/div/div/div[1]/div/div/label'},
                                                                                                       'testClickXPath'],
             ['Secure check 10',                    {'Script Id': 5, 'Test Case': 5, 'Step Number': 22}, 'testVerifySecure'],
             ['Secure click continue',              {'Script Id': 5, 'Test Case': 5, 'Step Number': 23}, 'testClickContinue'],
             ['Secure check 11',                    {'Script Id': 5, 'Test Case': 5, 'Step Number': 24}, 'testVerifySecure'],
             ['Close page for secure',              {'Script Id': 5, 'Test Case': 5, 'Step Number': 25}, 'testHomePageEnd'],
             # Check the background video
             ['Open page for background video',     {'Script Id': 6, 'Test Case': 6, 'Step Number': 1}, 'testHomePageStart'],
             ['Background video reset',             {'Script Id': 6, 'Test Case': 6, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Check moving background video',      {'Script Id': 6, 'Test Case': 6, 'Step Number': 3}, 'testCheckVideo'],
             ['Close page for background video',    {'Script Id': 6, 'Test Case': 6, 'Step Number': 4}, 'testHomePageEnd'],
             # Check if test fits inside button
             ['Open page for text fits inside',     {'Script Id': 7, 'Test Case': 7, 'Step Number': 1}, 'testHomePageStart'],
             ['Text fits inside reset',             {'Script Id': 7, 'Test Case': 7, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Check if text fits inside button',   {'Script Id': 7, 'Test Case': 7, 'Step Number': 3}, 'testCheckText'],
             ['Close page for text fits inside',    {'Script Id': 7, 'Test Case': 7, 'Step Number': 4}, 'testHomePageEnd'],
             # Check currencies and descriptions after clicking the bottom CTA
             ['Open page for chosen language',      {'Script Id': 8, 'Test Case': 8, 'Step Number': 1}, 'testHomePageStart'],
             ['Chosen language reset to en-US',     {'Script Id': 8, 'Test Case': 8, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Chosen language buy tickets',        {'Script Id': 8, 'Test Case': 8, 'Step Number': 3}, 'testClickBottomCta'],
             ['Chosen language pick package',       {'Script Id': 8, 'Test Case': 8, 'Step Number': 4, 'Test Language': 'EN'}, 
                                                                                                       'testCtaBuyingTickets'],
             ['Chosen language buy now',            {'Script Id': 8, 'Test Case': 8, 'Step Number': 5}, 'testSelectMorning'],
             ['Close page for chosen language',     {'Script Id': 8, 'Test Case': 8, 'Step Number': 6}, 'testHomePageEnd'],
             ['Open page for chosen language(s)',   {'Script Id': 8, 'Test Case': 8, 'Step Number': 7}, 'testHomePageStart'],
             ['Chosen language(s) reset to en-US',  {'Script Id': 8, 'Test Case': 8, 'Step Number': 8, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Select a different language(s)',     {'Script Id': 8, 'Test Case': 8, 'Step Number': 9, 'Test Language': 'FR'}, 
                                                                                                       'testSpecifyForeignLanguage'],
             ['Chosen language(s) buy tickets',     {'Script Id': 8, 'Test Case': 8, 'Step Number': 10}, 'testClickBottomCta'],
             ['Chosen language(s) pick package',    {'Script Id': 8, 'Test Case': 8, 'Step Number': 11, 'Test Language': 'FR'}, 
                                                                                                        'testCtaBuyingTickets'],
             ['Chosen language(s) buy now',         {'Script Id': 8, 'Test Case': 8, 'Step Number': 12, 'Test Language': 'FR'}, 
                                                                                                        'testSelectMorning'],
             ['Chosen language(s) description',     {'Script Id': 8, 'Test Case': 8, 'Step Number': 13, 'Test Language': 'FR'},
                                                                                                        'testCheckDescription'],
             ['Chosen language(s) currency symbol', {'Script Id': 8, 'Test Case': 8, 'Step Number': 14, 'Test Language': 'FR'}, 
                                                                                                        'testCheckCurrency'],
             ['Close page for chosen language(s)',  {'Script Id': 8, 'Test Case': 8, 'Step Number': 15}, 'testHomePageEnd'],
             ['Chosen language(s) repeat',          {'Script Id': 8, 'Test Case': 8, 'Step Number': 16, 'Test First':
                                                                                                        'Open page for chosen language(s)',
                                                                                                        'Test Last':
                                                                                                        'Close page for chosen language(s)'}, 
                                                                                                        'testRepeatAll'],
             # Check currencies and descriptions after clicking the top-right CTA
             ['Open page for top buy',              {'Script Id': 9, 'Test Case': 9, 'Step Number': 1}, 'testHomePageStart'],
             ['Top buy reset to en-US',             {'Script Id': 9, 'Test Case': 9, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                       'testEnterPathName'],
             ['Top buy buy tickets',                {'Script Id': 9, 'Test Case': 9, 'Step Number': 3}, 'testClickTopRightCta'],
             ['Top buy pick package',               {'Script Id': 9, 'Test Case': 9, 'Step Number': 4, 'Test Language': 'EN'}, 
                                                                                                       'testCtaBuyingTickets'],
             ['Top buy buy now',                    {'Script Id': 9, 'Test Case': 9, 'Step Number': 5, 'Test Language': 'EN'},
                                                                                                       'testSelectMorning'],
             ['Top buy description',                {'Script Id': 9, 'Test Case': 9, 'Step Number': 6, 'Test Language': 'EN'}, 
                                                                                                       'testCheckDescription'],
             ['Top buy currency symbol',            {'Script Id': 9, 'Test Case': 9, 'Step Number': 7, 'Test Language': 'EN'},
                                                                                                       'testCheckCurrency'],
             ['Close page for top buy',             {'Script Id': 9, 'Test Case': 9, 'Step Number': 8}, 'testHomePageEnd'],
             ['Open page for top buy foreign',      {'Script Id': 9, 'Test Case': 9, 'Step Number': 9}, 'testHomePageStart'],
             ['Top buy foreign reset to en-US',     {'Script Id': 9, 'Test Case': 9, 'Step Number': 10, 'Test Path Name': 'en-US/'},
                                                                                                        'testEnterPathName'],
             ['Top buy different foreign language', {'Script Id': 9, 'Test Case': 9, 'Step Number': 11, 'Test Language': 'FR'}, 
                                                                                                        'testSpecifyForeignLanguage'],
             ['Top buy foreign buy tickets',        {'Script Id': 9, 'Test Case': 9, 'Step Number': 12}, 'testClickTopRightCta'],
             ['Top buy foreign pick package',       {'Script Id': 9, 'Test Case': 9, 'Step Number': 13, 'Test Language': 'FR'}, 
                                                                                                        'testCtaBuyingTickets'],
             ['Top buy buy now',                    {'Script Id': 9, 'Test Case': 9, 'Step Number': 14, 'Test Language': 'FR'},
                                                                                                        'testSelectMorning'],
             ['Top buy foreign description',        {'Script Id': 9, 'Test Case': 9, 'Step Number': 15, 'Test Language': 'FR'}, 
                                                                                                        'testCheckDescription'],
             ['Top buy foreign currency symbol',    {'Script Id': 9, 'Test Case': 9, 'Step Number': 16, 'Test Language': 'FR'}, 
                                                                                                        'testCheckCurrency'],
             ['Close page for top buy foreign',     {'Script Id': 9, 'Test Case': 9, 'Step Number': 17}, 'testHomePageEnd'],
             ['Top buy foreign repeat',             {'Script Id': 9, 'Test Case': 9, 'Step Number': 18, 'Test First':
                                                                                                        'Open page for top buy foreign',
                                                                                                        'Test Last':
                                                                                                        'Close page for top buy foreign'}, 
                                                                                                        'testRepeatAll'],
             # Check if the two-letter language code in the upper-right hand corner matches the language we are actually using
             ['Open page for language code',        {'Script Id': 10, 'Test Case': 10, 'Step Number': 1}, 'testHomePageStart'],
             ['Language code reset to en-US',       {'Script Id': 10, 'Test Case': 10, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                         'testEnterPathName'],
             ['Language code foreign language',     {'Script Id': 10, 'Test Case': 10, 'Step Number': 3, 'Test Language': 'FR'}, 
                                                                                                         'testSpecifyForeignLanguage'],
             ['Language code description',          {'Script Id': 10, 'Test Case': 10, 'Step Number': 4, 'Test Language': 'FR'}, 
                                                                                                         'testCheckLanguage'],
             ['Close page for language code',       {'Script Id': 10, 'Test Case': 10, 'Step Number': 5}, 'testHomePageEnd'],
             ['Language code each language repeat', {'Script Id': 10, 'Test Case': 10, 'Step Number': 6, 'Test First':
                                                                                                         'Open page for language code',
                                                                                                         'Test Last':
                                                                                                         'Close page for language code'}, 
                                                                                                         'testRepeatLanguage'], 
             # Checks if a URL has changed from its original value. This will happen if a link on a test system
             # points back to the production system.
             ['Open page for checkURL',             {'Script Id': 11, 'Test Case': 11, 'Step Number': 1}, 'testHomePageStart'],
             ['CheckURL text reset',                {'Script Id': 11, 'Test Case': 11, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                         'testEnterPathName'],
             ['CheckURL check 1',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 3}, 'testCheckUrl'],
             ['CheckUrl different language(s)',     {'Script Id': 11, 'Test Case': 11, 'Step Number': 4, 'Test Language': 'FR'}, 
                                                                                                         'testSpecifyForeignLanguage'],
             ['CheckURL check 2',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 5}, 'testCheckUrl'],
             ['Click on CTA for checkURL',          {'Script Id': 11, 'Test Case': 11, 'Step Number': 6}, 'testClickTopRightCta'],
             ['CheckURL check 3',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 7}, 'testCheckUrl'],
             ['Click CTA for checkURL',             {'Script Id': 11, 'Test Case': 11, 'Step Number': 8, 'Test Language': 'FR'}, 
                                                                                                         'testCtaBuyingTickets'],
             ['CheckURL check 4',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 9}, 'testCheckUrl'],
             ['Click CTA for Morning checkURL',     {'Script Id': 11, 'Test Case': 11, 'Step Number': 10, 'Test Language': 'FR'}, 
                                                                                                          'testSelectMorning'],
             ['CheckURL check 5',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 11}, 'testCheckUrl'],
             ['Select 1 ticket for checkURL',       {'Script Id': 11, 'Test Case': 11, 'Step Number': 12}, 'testSelectOneAdultTicket'],
             ['CheckURL check 6',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 13}, 'testCheckUrl'],
             ['CheckURL Click next',                {'Script Id': 11, 'Test Case': 11, 'Step Number': 14, 'Test XPath': 
                                                                                                          '//*[@id="next-btn"]'},
                                                                                                          'testClickXPath'],
             ['CheckURL check 7',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 15}, 'testCheckUrl'],
             ['CheckURL click on No Thanks',        {'Script Id': 11, 'Test Case': 11, 'Step Number': 16, 'Test Language': 'FR'},
                                                                                                          'testClickNoThanks'],
             ['CheckURL check 8',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 17}, 'testCheckUrl'],
             ['CheckURL advance date / pick time',  {'Script Id': 11, 'Test Case': 11, 'Step Number': 18, 'Test Language': 'FR'}, 
                                                                                                          'testAdvanceDateAndTime'],
             ['CheckURL check 9',                   {'Script Id': 11, 'Test Case': 11, 'Step Number': 19}, 'testCheckUrl'],
             ['CheckURL click checkout',            {'Script Id': 11, 'Test Case': 11, 'Step Number': 20, 'Test XPath': 
                                                                                                          '//*[@id="cart-proceed-to-checkout-btn"]'},
                                                                                                          'testClickXPath'],
             ['CheckURL check 10',                  {'Script Id': 11, 'Test Case': 11, 'Step Number': 21}, 'testCheckUrl'],
             ['CheckURL click shipping',            {'Script Id': 11, 'Test Case': 11, 'Step Number': 22, 'Test XPath': 
                                                                                                          '//*[@id="shipping-continue-shipping-btn"]'},
                                                                                                          'testClickXPath'],
             ['CheckURL check 11',                  {'Script Id': 11, 'Test Case': 11, 'Step Number': 23}, 'testCheckUrl'],
             ['CheckURL click credit',              {'Script Id': 11, 'Test Case': 11, 'Step Number': 24, 'Test XPath': 
                                                     '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[3]/div/div/div[1]/div/div/label'},
                                                                                                          'testClickXPath'],
             ['CheckURL check 12',                  {'Script Id': 11, 'Test Case': 11, 'Step Number': 25}, 'testCheckUrl'],
             ['CheckURL click continue',            {'Script Id': 11, 'Test Case': 11, 'Step Number': 26}, 'testClickContinue'],
             ['CheckURL check 13',                  {'Script Id': 11, 'Test Case': 11, 'Step Number': 27}, 'testCheckUrl'],
             ['Close page for checkURL',            {'Script Id': 11, 'Test Case': 11, 'Step Number': 28}, 'testHomePageEnd'],
             ['CheckURL repeat all',                {'Script Id': 11, 'Test Case': 11, 'Step Number': 29, 'Test First':
                                                                                                          'Open page for checkURL',
                                                                                                          'Test Last':
                                                                                                          'Close page for checkURL'}, 
                                                                                                          'testRepeatAll'],
             # Check if http is automatically replaced by https. This is done for one specific web page.
             ['Open page for protocol code',        {'Script Id': 12, 'Test Case': 12, 'Step Number': 1}, 'testHomePageStart'],
             ['Protocol code reset to en-US',       {'Script Id': 12, 'Test Case': 12, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                         'testEnterPathName'],
             ['Protocol code foreign language',     {'Script Id': 12, 'Test Case': 12, 'Step Number': 3, 'Test Language': 'FR'}, 
                                                                                                         'testSpecifyForeignLanguage'],
             ['Protocol code description',          {'Script Id': 12, 'Test Case': 12, 'Step Number': 4, 'Test Language': 'FR'}, 
                                                                                                         'testCheckProtocol'],
             ['Close page for protocol code',       {'Script Id': 12, 'Test Case': 12, 'Step Number': 5}, 'testHomePageEnd'],
             ['Protocol code each language repeat', {'Script Id': 12, 'Test Case': 12, 'Step Number': 6, 'Test First':
                                                                                                         'Open page for protocol code',
                                                                                                         'Test Last':
                                                                                                         'Close page for protocol code'}, 
                                                                                                         'testRepeatLanguage'], 
             # Check for host names. In other words, check for non-relative URLs. Check a few specific web pages.
             ['Open page for href code',            {'Script Id': 13, 'Test Case': 13, 'Step Number': 1}, 'testHomePageStart'],
             ['Href code reset to en-US',           {'Script Id': 13, 'Test Case': 13, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                         'testEnterPathName'],
             ['Href code foreign language',         {'Script Id': 13, 'Test Case': 13, 'Step Number': 3, 'Test Language': 'FR'}, 
                                                                                                         'testSpecifyForeignLanguage'],
             ['Href code description 1',            {'Script Id': 13, 'Test Case': 13, 'Step Number': 4, 'Test Language': 'FR'}, 
                                                                                                         'testCheckHrefs'],
             ['Href code bottom CTA',               {'Script Id': 13, 'Test Case': 13, 'Step Number': 5}, 'testClickBottomCta'],
             ['Href code description 2',            {'Script Id': 13, 'Test Case': 13, 'Step Number': 6, 'Test Language': 'FR'}, 
                                                                                                         'testCheckHrefs'],
             ['Close page for href code',           {'Script Id': 13, 'Test Case': 13, 'Step Number': 7}, 'testHomePageEnd'],
             ['Href code each language repeat',     {'Script Id': 13, 'Test Case': 13, 'Step Number': 8, 'Test First':
                                                                                                         'Open page for href code',
                                                                                                         'Test Last':
                                                                                                         'Close page for href code'}, 
                                                                                                         'testRepeatLanguage'], 
             # Check for host names. In other words, check for non-relative URLs. Scan the entire web site.
             ['Open page for web site code',        {'Script Id': 14, 'Test Case': 14, 'Step Number': 1}, 'testHomePageStart'],
             ['Web site code reset to en-US',       {'Script Id': 14, 'Test Case': 14, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                         'testEnterPathName'],
             ['Web site code foreign language',     {'Script Id': 14, 'Test Case': 14, 'Step Number': 3, 'Test Language': 'FR'}, 
                                                                                                         'testSpecifyForeignLanguage'],
             ['Web site code description',          {'Script Id': 14, 'Test Case': 14, 'Step Number': 4, 'Test Language': 'FR'}, 
                                                                                                         'testCheckWebSite'],
             ['Close page for web site code',       {'Script Id': 14, 'Test Case': 14, 'Step Number': 5}, 'testHomePageEnd'],
             ['Web site code each language repeat', {'Script Id': 14, 'Test Case': 14, 'Step Number': 6, 'Test First':
                                                                                                         'Open page for web site code',
                                                                                                         'Test Last':
                                                                                                         'Close page for web site code'}, 
                                                                                                         'testRepeatLanguage'], 
             # Check for scheme values other than https. Scan the entire web site.
             ['Open page for scheme code',          {'Script Id': 15, 'Test Case': 15, 'Step Number': 1}, 'testHomePageStart'],
             ['Scheme code reset to en-US',         {'Script Id': 15, 'Test Case': 15, 'Step Number': 2, 'Test Path Name': 'en-US/'},
                                                                                                         'testEnterPathName'],
             ['Scheme code foreign language',       {'Script Id': 15, 'Test Case': 15, 'Step Number': 3, 'Test Language': 'FR'}, 
                                                                                                         'testSpecifyForeignLanguage'],
             ['Scheme code description',            {'Script Id': 15, 'Test Case': 15, 'Step Number': 4, 'Test Language': 'FR'}, 
                                                                                                         'testCheckScheme'],
             ['Close page for scheme code',         {'Script Id': 15, 'Test Case': 15, 'Step Number': 5}, 'testHomePageEnd'],
             ['Scheme code each language repeat',   {'Script Id': 15, 'Test Case': 15, 'Step Number': 6, 'Test First':
                                                                                                         'Open page for scheme code',
                                                                                                         'Test Last':
                                                                                                         'Close page for scheme code'}, 
                                                                                                         'testRepeatLanguage'], 
             # Check if the web site works with and without the www. prefix
             ['Open page for prefix code',          {'Script Id': 16, 'Test Case': 16, 'Step Number': 1}, 'testHomePageStart'],
             ['Prefix code reset to en-US',         {'Script Id': 16, 'Test Case': 16, 'Step Number': 2,  'Test Path Name': 'en-US/'},
                                                                                                          'testEnterPathName'],
             ['Prefix code description',            {'Script Id': 16, 'Test Case': 16, 'Step Number': 3}, 'testHostNamePrefix'],
             ['Close page for prefix code',         {'Script Id': 16, 'Test Case': 16, 'Step Number': 4}, 'testHomePageEnd'],
           ]

# Each instance of this class has all of the information about
# the current context. The context shows what type of application,
# we are testing, what operating system we are running on, and
# what website we are testing. The caller should pass a common
# application name.
class Context(object):
  # The __init__ method creates an instance of the class
  def __init__(self, applicationNameStr, operatingSystemName, webSiteStr):
    self.applicationName = applicationNameStr
    self.applicationAbbreviation = getApplicationAbbreviation(applicationNameStr)
    self.browserDriver = None
    self.internalUseOnlyFlag = False
    self.osName = operatingSystemName
    self.outLinesList = None
    self.reportOnlyErrorsFlag = False
    self.switchToFlag = False
    self.webSite = webSiteStr
  # Get the current application abbreviation and return it to the caller
  def getAbbreviation(self):
    return self.applicationAbbreviation
  # Get the current application name and return it to the caller
  def getApplication(self):
    return self.applicationName
  # Get the browser driver and return it to the caller 
  def getBrowserDriver(self):
    return self.browserDriver
  # Get the internal use only flag and return it to the caller
  def getInternalUseOnly(self):
    return self.internalUseOnlyFlag
  # Get the current operating system name and return it to the caller
  def getOs(self):
    return self.osName
  # Get the list of lines and return it to the caller
  def getOutLines(self):
    return self.outLinesList
  # Get the report only errors flag and return it to the caller
  def getReportOnlyErrors(self):
    return self.reportOnlyErrorsFlag
  # Get the switch to status (the flag) of the context and return
  # it to the caller
  def getSwitchToFlag(self):
    return self.switchToFlag
  # Get the current website URL and return it to the caller
  def getWebSite(self):
    return self.webSite
  # Store a reference to the browser driver in the current 
  # context object
  def setBrowserDriver(self, browserDriver):
    # Clear the switch to flag, if need be
    if browserDriver == None:
      self.switchToFlag = False
    else:
      if self.browserDriver != browserDriver:
        self.switchToFlag = False
    # Store the new browser reference
    self.browserDriver = browserDriver
  # Set the internal use only flag 
  def setInternalUseOnly(self, internalOnly):
    self.internalUseOnlyFlag = internalOnly
  # Store a reference to the object used to accumulate 
  # output lines
  def setOutLines(self, outLines):
    self.outLinesList = outLines
  # Set the report only errors flag 
  def setReportOnlyErrors(self, reportOnly):
    self.reportOnlyErrorsFlag = reportOnly
  # Switch back to the default frame, if need be
  def switchBack(self):
    # We don't need to do anything if the switch back has
    # already been done
    if self.switchToFlag == False:
      return
    # The switch back must be done at this point
    browser = self.browserDriver
    browser.switch_to.defaultContent()
    self.switchToFlag = False 
    return
  # Switch to a specific frame (really iframe) if need be
  def switchTo(self, frameName):
    # We don't need to do anything if the switch has already 
    # been done
    if self.switchToFlag == True:
      return
    # The switch must be done at this point
    browser = self.browserDriver
    browser.switch_to.frame(frameName)
    self.switchToFlag = True
    return

# Each instance of this class has all of the information about
# one level. A level might be all of the possible languages or
# the possible package types. Of course, a level might just be
# a subset of the possible languages. A level can be incremented
# but will wrap when it reaches the end of the list of choices.
class Level(object):
  # The __init__ method creates an instance of the class
  def __init__(self, listOfChoices):
    # Make sure the list of choices is not empty
    assert len(listOfChoices) > 0, 'List of choices is empty'
    self.choices = listOfChoices
    self.numberOfChoices = len(listOfChoices)
    self.currentIndex = 0
    self.wrap = False
    return
  # Get the current choice and return it to the caller
  def getChoice(self):
    return self.choices[self.currentIndex]
  # Get the current wrap value
  def getWrap(self):
    return self.wrap
  # Increment the current choice value. Set the wrap flag
  # as need be.
  def increment(self):
    self.currentIndex += 1
    if self.currentIndex >= self.numberOfChoices:
      self.currentIndex = 0
      self.wrap = True
    else:
      self.wrap = False
    return self.currentIndex
  # Reset the currnt index value to zero
  def reset(self):
    self.currentIndex = 0
    return

# Each instance of this class has all of the information about
# a set of levels. A good analogy might be a three-digit number.
# each digit is one level. The entire number is a set of three
# levels. A number of operations can be done on instances of this
# class.
class Levels(object):
  # The __init__ method creates an instance of the class. This
  # method must be passed a list where each entry in the list
  # is a level. Each entry in the list must be all of the
  # possible choices for that level.
  def __init__(self, listOfLevels):
    # Make sure the list of choices is not empty
    assert len(listOfLevels) > 0, 'List of levels is empty'
    self.levels = []
    self.numberOfLevels = len(listOfLevels)
    self.overflow = False
    for levelInfo in listOfLevels:
      newLevelObj = Level(levelInfo)
      self.levels.append(newLevelObj)
    return
  # Get the current set of choices and return them to the caller
  def getChoices(self):
    choices = []
    for level in self.levels:
      choice = level.getChoice()
      choices.append(choice)
    return choices
  # This method returns the current overflow status to the
  # caller
  def getOverflow(self):
    return self.overflow
  # This method increments the current set of levels. Ths
  # concept is to increment the lowest level and then
  # continue incrementing until wrapping stops of an
  # overflow occurs.
  def increment(self):
    index = 0
    while True:
      # Get the current level
      currentLevel = self.levels[index]
      # Increment the current level
      currentLevel.increment()
      # Check if we have wrapped
      currentWrap = currentLevel.getWrap()
      # If the increment of the current level has not
      # caused a wrap, then we are done
      if currentWrap == False:
        break
      # The increment of the current level did cause a wrap.
      # We must continue to the next level, if any.
      index += 1
      if index >= self.numberOfLevels:
        self.overflow = True
        break
      else:
        self.overflow = False
    return
  # Reset all of the currnt index values to zero and reset
  # the overflow flag
  def reset(self):
    for level in self.levels:
      level.reset
    self.overflow = False
    return

# Build a line describing the current environment and add it to the lines object
def addContextLine(context, outLines):
  # Get the current browser name
  line = ''
  line += '"'
  line += context.getApplication()
  line += '"'
  # Get the current web site
  line += ','
  line += '"'
  line += context.getWebSite()
  line += '"'
  # Get the current operating system
  line += ','
  line += '"'
  line += context.getOs()
  line += '"'
  # Get the date and time
  dt = datetime.datetime.now()
  dateStr = dt.strftime("%Y-%m-%d")
  line += ','
  line += '"'
  line += dateStr
  line += '"'
  timeStr = dt.strftime("%H:%M:%S")
  line += ','
  line += '"'
  line += timeStr
  line += '"'
  outLines.addLine(line)

# Build the standard heading line string and add it to the lines object
def addHeadingLine(outLines):
  heading = '"Timestamp","Script Id","Test Case","Step Number","Description","Language","Package","Result"'
  outLines.addLine(heading)

# Build a line describing the current set of tests and add it to the lines object
def addTestsLine(outLines, firstTest, lastTest):
  # Check for none values
  if firstTest == None:
    firstTest = 'None'
  if lastTest == None:
    lastTest = 'None'
  line = '"' + firstTest + '","' + lastTest + '"'
  outLines.addLine(line)

# Build the file name for the results file
def buildFileName(browserName, suffix):
  fileName = ''
  # Add the capitalized browser name  
  fileName += HDLmString.capitalize(browserName)
  # Get the date and time
  dt = datetime.datetime.now()
  fileName += dt.strftime("%Y%m%d")
  fileName += '_'
  fileName += dt.strftime("%H%M%S")
  # Add the file suffix, if need be
  if suffix != None and suffix != '':
    fileName += '.' + suffix
  return fileName

# Build a JavaScript properties list assignment statement from 
# a list of JavaScript properties 
def buildJavaScriptProperties(propertyList):
# Build the properties string 
  propCount = -1
  scriptProp = "let properties = ["
  for property in propertyList:
    propCount += 1
    if propCount > 0:
      scriptProp += ', '
    scriptProp += "'" + property + "'"
  scriptProp += "];"   
  return scriptProp

# Build a line describing a test and the result(s)
def buildResultLine(*args):
  # Start the new line
  outLine = ''
  index = -1
  for arg in args:
    index += 1
    # Add a trailing comma, if need be
    if index > 0:
      outLine += ','
    # Put each value in quotes
    outLine += '"'
    # Add each value to the output line
    if arg == None:
      nextValue = ''
    # CSV files require that double quotes be converted to two double quotes
    else:
      nextValue = str(arg)
      nextValue = nextValue.replace('"', '""')
      nextValue = nextValue.replace('\n', '')
    outLine += nextValue
    # Put each value in quotes
    outLine += '"'
  return outLine

# This function clicks on the eleemnt passed by the caller
def clickOnSomething(element):
  # Try to click on the element 
  element.click()
  return 

# Compare two rectangles. If the second rectangle fits inside (including 
# having the same borders) the first rectangle, return true. Otherwise,
# return false.
def compareRectangles(firstRect, secondRect):
  # Get the top-left and bottom-right values for each rectangle
  firstTL = [firstRect['y'], firstRect['x']]
  firstBR = [firstRect['y'] + firstRect['height'], firstRect['x'] + firstRect['width']]
  secondTL = [secondRect['y'], secondRect['x']]
  secondBR = [secondRect['y'] + secondRect['height'], secondRect['x'] + secondRect['width']]
  # Make sure the top-left and bottom-right values are OK 
  if secondTL[0] >= firstTL[0] and \
     secondTL[1] >= firstTL[1] and \
     secondBR[0] <= firstBR[0] and \
     secondBR[1] <= firstBR[1]:
    return True
  return False

# Build a map from the class name list. The class names list
# is a list of all of the class names for a set of zero or more
# elements. For example, if there were exactly two elements, 
# then the list passed to this routine would have two entries.
# Each entry is a string made up of all of the class names for
# an element separated by blanks.
def convertClassNamesToMap(classNamesList):
  # Create the initial outut map
  outMap = dict()
  nameList = ['all', 'all-inclusive', 'stan', 'standard', 'combo', 'combination', 'vip', 'vip']
  # Set the initial value for a counter so that it will zero after
  # the first increment operation
  counter = -1
  # Scan each of the lists of class names passed by the 
  # caller
  for listEntry in classNamesList:
    counter += 1
    # Check if a series of strings appear in each set of class names
    for i in range(1, len(nameList), 2):
      # Get a search string that might appear in a string made up of
      # class names
      searchStr = nameList[i]
      # Check if we can find the search string in the string comprised
      # of class names
      if listEntry.find(searchStr) > 0:
        packageName = nameList[i-1]
        outMap[packageName] = counter
  return outMap

# Convert a map of values. The input map have a string for each
# value. Each of the string values is converted to a list. The
# list has the numeric value from the string and the text part
# of the string.
def convertMapValues(mapValues):
  outMap = dict()
  for key, value in mapValues.items():
    outMap[key] = getListFromValue(value)
  return outMap

# This function enters a URL. The caller provides the complete 
# URL including protocol string. Note that this routine does
# not return anything to the caller. 
def enterUrl(browser, urlStr):
  browser.get(urlStr)
  return 

# Find elements (zero, one, or more) by class name. Return the 
# list of matching elements.
def findByClass(driver, className):
  # Get all of the matching web elements
  # elements = driver.find_elements_by_class_name(className)
  elements = driver.find_elements(By.CLASS_NAME, className)
  return elements

# This routine will find one (and only one) element by class
# name and click on it. The number of matching elements must
# be exactly one. The one element will be returned to the 
# caller.
def findByClassClick(context, className, iframeName = ''):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Switch to the target iFrame, if need be
  switched = False
  # Check if we have already switched to the iFrame
  if iframeName != '':
    switchedFlag = context.getSwitchToFlag()
    if switchedFlag == False:
      context.switchTo(iframeName)
      switched = True
  # Get the matching element
  element = findByClassOne(browser, className)
  element.click()
  # Switch back to the parent frame, if need be
  if switched:
    context.switchBack()
  return element

# This routine will find one (and only one) element by class
# name and click on it, if there is only one. Otherwise, a 
# None value will be returned to the caller. The number of
# matching elements must be exactly one. The one element will
# be returned to the caller. If there is more than one element 
# that matches the class name, an error will be raised. 
def findByClassIfOneClick(driver, className):
  # Get the matching elements
  elements = findByClass(driver, className)
  elementsLen = len(elements)
  # Check the number of elements
  if elementsLen == 0:
    return None
  if elementsLen > 1:
    raise SystemError("Too many elements matched class name - " + className)
  # We can now click on the element
  element = elements[0]
  clickOnSomething(element)
  return element

# Find one (and only one) element by class name. Return the a map with
# all of the properties convert to easier to use values. 
def findByClassGetMap(driver, className, propertyList):
  # Get all of the properties requested by the caller
  rv = findByClassGetProperties(driver, className, propertyList)
  # Each of the properties will have a value like '25px'. Convert
  # each of the values to a list where the first list element is
  # floating-point value (25.0 in this case) and the second list
  # element is a string ('px' in this case).
  rv = convertMapValues(rv)
  return rv

# Find one (and only one) element by class name. Return the properties 
# of the element. 
def findByClassGetProperties(driver, className, propertyList):
  # Turn the class name into a query selector
  className = '.' + className
  # Get and return the list of properties
  rv = findByQueryGetProperties(driver, className, propertyList)
  return rv

# Find one (and only one) element by class name. Return the rectangle
# for the one matching element using JavaScript APIs. Note that the 
# returned value are adjusted for the margin, border, and padding if
# need be.
def findByClassGetRectAdjusted(driver, className):
  # Build a list with the properties we need to obtain
  propertiesBox = ['border-width-bottom', 'border-width-left', 'border-width-right', 'border-width-top',
                   'margin-bottom', 'margin-left', 'margin-right', 'margin-top',
                   'padding-bottom', 'padding-left', 'padding-right', 'padding-top']
  # Get the raw values using JavaScript
  rawRect = findByClassGetRectJavaScript(driver, className)
  # Get a set of converted property values
  rawMap = findByClassGetMap(driver, className, propertiesBox)
  borderBottom = rawMap['border-width-bottom'][0]
  borderLeft = rawMap['border-width-left'][0]
  borderRight = rawMap['border-width-right'][0]
  borderTop = rawMap['border-width-top'][0]
  marginBottom = rawMap['margin-bottom'][0]
  marginLeft = rawMap['margin-left'][0]
  marginRight = rawMap['margin-right'][0]
  marginTop = rawMap['margin-top'][0]
  paddingBottom = rawMap['padding-bottom'][0]
  paddingLeft = rawMap['padding-left'][0]
  paddingRight = rawMap['padding-right'][0]
  paddingTop = rawMap['padding-top'][0]
  # Get a few total values
  totalTop = borderTop + marginTop + paddingTop
  totalRight = borderRight + marginRight + paddingRight
  totalBottom = borderBottom + marginBottom + paddingBottom
  totalLeft = borderLeft + marginLeft + paddingLeft
  # Get a few final values
  finalX = rawRect['x'] + totalLeft
  finalY = rawRect['y'] + totalTop
  finalH = rawRect['height'] - totalTop - totalBottom
  finalW = rawRect['width'] - totalLeft - totalRight
  # Build the final return value
  rv = dict()
  rv['x'] = finalX
  rv['y'] = finalY
  rv['height'] = finalH
  rv['width'] = finalW
  return rv

# Find one (and only one) element by class name. Return the rectangle
# for the one matching element using JavaScript APIs.
def findByClassGetRectJavaScript(driver, className):
  # Build the CSS selector
  selector = '.' + className
  # Build the main script string
  scriptStr = "let element = document.querySelector('" + selector + "');" + \
              "let rv = element.getBoundingClientRect();" + \
              "return rv;"   
  # Execute the script string
  rv = driver.execute_script(scriptStr)
  return rv

# Find one (and only one) element by class name. Return the rectangle
# for the one matching element using Selenium APIs.
def findByClassGetRectSelenium(driver, className):
  # Get the one matching element
  element = findByClassOne(driver, className)
  return element.rect

# Find one (and only one) element by class name. Return the one
# matching element.
def findByClassOne(driver, className):
  # Get all of the matching web elements
  elements = findByClass(driver, className)
  # Check if only one element matched the class name
  if len(elements) != 1:
    if len(elements) == 0:
      raise SystemError("No elements matched class name - " + className)
    else:
      raise SystemError("Too many elements matched class name - " + className)
  return elements[0]

# Find elements (zero or one) by id name. Return the 
# matching element or None.
def findById(driver, idName):
  # Get the matching web element
  element = driver.find_element_by_id(idName)
  return element

# This routine will find one (and only one) element by id
# name and click on it, if there is only one. Otherwise, a 
# None value will be returned to the caller. The number of
# matching elements must be exactly one. The one element will
# be returned to the caller.  
def findByIdIfFoundClick(driver, idName):
  # Get the matching element
  element = findById(driver, idName)
  if element != None:
    elementsLen = 1
  else:
    elementsLen = 0
  # Check the number of elements
  if elementsLen == 0:
    return None
  if elementsLen > 1:
    raise SystemError("Too many elements matched id name - " + idName)
  # We can now click on the element 
  clickOnSomething(element)
  return element

# This routine will try to find one or more nodes using a node
# identification string. The node identification string is 
# actually JSON that identifies one or more nodes. The list
# of nodes is returned to the caller. Note that invalid nodes
# are removed, before this list is returned.
def findByNodeIden(driver, nodeIdenStr):
  # Build the main script string
  scriptStr = '' 
  scriptStr += 'var  nodeIdenStr = \'' + nodeIdenStr + '\';'
  scriptStr += 'var  nodeIdenJSON = JSON.parse(nodeIdenStr);'
  scriptStr += 'var  curMod = new Object();'
  scriptStr += 'curMod.nodeiden = nodeIdenJSON;'
  scriptStr += 'var  rv = HDLmFindNodeIden(curMod, false);'
  scriptStr += 'return rv;'
  scriptStr += glbNodeIdenJS
  # Change all newline characters in the Python literal to something
  # that will end up as a newline in JavaScript
  scriptStr = scriptStr.replace('(\'\n\')', '(\'\\n\')')
  # Execute the script string
  rvFromDriver = driver.execute_script(scriptStr)
  # We now need to go through the list returned by the driver
  # and get rid of any bad entries
  rv = []
  for element in rvFromDriver:
    if element.size['height'] > 0.0:
      rv.append(element)
  return rv

# This routine will find one (and only one) element using a node 
# identifier expression and click on it. The number of matching 
# elements must be exactly one. The one element will be returned 
# to the caller.
def findByNodeIdenClick(driver, nodeIdenStr):
  # Get the matching element
  element = findByNodeIdenOne(driver, nodeIdenStr)
  element.click()
  return element

# Find one (and only one) element using a node identifier. Return the one
# matching element.
def findByNodeIdenOne(driver, nodeIdenStr):
  # Get all of the matching web elements
  elements = findByNodeIden(driver, nodeIdenStr)
  # Check if only one element matched the node identifier 
  if len(elements) != 1:
    if len(elements) == 0:
      raise SystemError("No elements matched the node identifier - " + nodeIdenStr)
    else:
      raise SystemError("Too many elements matched the node identifier - " + nodeIdenStr)
  return elements[0]   

# Find one (and only one) element using a query selector. The caller must
# pass a finished query selector. Return the properties of the selected
# element. 
def findByQueryGetProperties(driver, selector, propertyList):
  # Build the properties string 
  scriptProp = buildJavaScriptProperties(propertyList)
  # Build the main script string
  scriptStr = "let element = document.querySelector('" + selector + "');" + \
              scriptProp + \
              "let rv = {};" + \
              "let computedStyle = window.getComputedStyle(element, null);" + \
              "for (const property of properties) {" + \
              "  rv[property] = computedStyle.getPropertyValue(property);" + \
              "}" + \
              "return rv;"   
  # Execute the script string
  rv = driver.execute_script(scriptStr)
  return rv

# Find one (and only one) element using a query selector. The caller must
# pass a finished query selector. Set an attribute of the element to the 
# value passed by the caller. 
def findByQuerySetAttribute(driver, selector, attributeStr, valueStr):
  # Build the main script string
  scriptStr = "let element = document.querySelector('" + selector + "');" + \
              "element." + attributeStr + " = '" + valueStr + "';" 
  # Execute the script string
  rv = driver.execute_script(scriptStr)
  return rv

# Find elements (zero, one, or more) by XPath expression. Return the 
# list of matching elements.
def findByXPath(driver, pathStr):
  # Get all of the matching web elements
  elements = driver.find_elements_by_xpath(pathStr)
  return elements

# This routine will find one (and only one) element by XPath
# expression and click on it. The number of matching elements
# must be exactly one. The one element will be returned to the 
# caller.
def findByXPathClick(driver, pathStr):
  # Get the matching element
  element = findByXPathOne(driver, pathStr)
  element.click()
  return element

# Find one (and only one) element by XPath expression. Return the one
# matching element.
def findByXPathOne(driver, pathStr):
  # Get all of the matching web elements
  elements = findByXPath(driver, pathStr)
  # Check if only one element matched the XPath expression
  if len(elements) != 1:
    if len(elements) == 0:
      raise SystemError("No elements matched the XPath expression - " + pathStr)
    else:
      raise SystemError("Too many elements matched the XPath expression - " + pathStr)
  return elements[0]    

# This function takes a standard application name and converts it to an
# abbreviation. The abbreviation is used to build file names and for
# other purposes. The caller should pass a common application name.
# Note that Microsoft Edge is listed as Microsoft Edge and just Edge.
def getApplicationAbbreviation(applicationName):
  # Build the application dictionary
  applicationDict = {'Brave Browser': 'BB', 'Chrome': 'CH', 'Dolphin Browser': 'DB', 'Edge': 'ED',
                     'Firefox': 'FF', 'Internet Explorer': 'IE', 'Microsoft Edge': 'ED',
                     'Opera': 'OP', 'Safari': 'SF', 'UC Browser': 'UC',
                     'Yandex': 'YN'}
  # Check if the App(lication) name is invalid
  if applicationName not in applicationDict:
    raise ValueError('Invalid application name - ' + applicationName)
  return applicationDict[applicationName]

# This function takes a standard application name and converts it to an
# Selenium driver application name. The Selenium driver application name
# is the name that can actually be started and/or stopped. The caller
# should pass a common application name. Note that Microsoft Edge is 
# listed as Microsoft Edge and just Edge.
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

# This function gets the arguments passed by the caller (if any). Default
# values are provided as need be. 
def getArgs():
  # Set a few default values
  fullBrowserName = 'Firefox'
  urlStr = 'oneworldobservatory.com'
  # urlStr = 'themarvelouslandofoz.com'
  # Build the argument parser object
  parser = argparse.ArgumentParser()
  # Add a few arguements
  parser.add_argument('Browser', nargs='?', default=fullBrowserName, 
                       help='specify the web browser to be used')
  parser.add_argument('URL', nargs='?', default=urlStr,
                      help='specify the URL to be used')
  parser.add_argument('-e', '--errors', action="store_true", default=False,
                      help='only report errors')
  parser.add_argument('-i', '--internal', action="store_true", default=False,
                      help='internal use only')
  result = parser.parse_args()  
  # Build the browser dictionary
  browserDict = {'Brave': 'Brave Browser', 'Chrome': 'Chrome', 'Dolphin': 'Dolphin Browser', 
                 'Edge': 'Microsoft Edge', 'Firefox': 'Firefox', 'Ie': 'Internet Explorer',
                 'Opera': 'Opera', 'Safari': 'Safari', 'Uc': 'UC Browser',
                 'Yandex': 'Yandex'}
  # Check the browser name
  browserName = result.Browser
  browserName = HDLmString.capitalize(browserName)
  # Check if the browser name is known or not
  if browserName not in browserDict:
    raise ValueError('Invalid browser name - ' + browserName)
  # Get the full browser name 
  fullBrowserName = browserDict[browserName]
  if fullBrowserName == None:
    raise SystemError("No browser full name for - " + browserName)
  return result

# Get an attribute from an element
def getAttribute(element, attributeStr):
  return element.get_attribute(attributeStr)

# Get a set of attribute values from the current web page
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

# Get a set of class name for a specific tag name. The caller
# passes the desired tag name. All elemements with that tag
# name are located and all of the class names for each element
# are returned to the caller. 
def getClassNamesByTagName(browser, tagName):
  # Build the main script string
  scriptStr = "let values = [];" + \
              "let elements = [];" + \
              "elements = document.getElementsByTagName('" + tagName + "');" + \
              "for (element of elements) {" + \
              "  let classText = element.className;" + \
              "  values.push(classText);" + \
              "}" + \
              "return values;"   
  # Execute the script string
  values = browser.execute_script(scriptStr)
  return values

# This function takes a standard language code (always two letters in
# uppercase) and returns the corresponding language suffix. For example,
# 'en-US' is returned for 'EN'. Note that the standard code for Chinese
# is actually 'zh' (note the use or lower case). However, we use 'CN' 
# and 'TW" to distingush between simplified Chinese and standard Chinese.
def getLanguagePathName(languageCode):
  # Build the language dictionary
  languageDict = {'EN': 'en-US', 'FR': 'fr-FR', 'DE': 'de-DE',
                  'ES': 'es', 'PT': 'pt-BR', 'IT': 'it-IT',
                  'JA': 'ja-JP', 'CN': 'zh-CN', 'TW': 'zh-TW',
                  'HI': 'hi-IN', 'KO': 'ko-KR'}
  # Check if the language code is invalid
  if languageCode not in languageDict:
    raise ValueError('Invalid language code - ' + languageCode)
  # Get the languaget text path name
  languagePathName = languageDict[languageCode]
  if languagePathName == None:
    raise SystemError("No language path name for - " + languageCode)
  return languagePathName

# Get a list of values from one value passed by the caller.
# If the caller passes an empty strig, a default value is
# used instead. This routine always returns a list. The
# first value is always a float-point value built from the
# the value passed by the caller. The second value is always
# the type obtained from the value passed by the caller. 
def getListFromValue(value = '0px'):
  # Check if the caller passed an empty string
  if value == '':
    value = '0px'
  # Convert the value to a list of tokens
  tokens = HDLmString.getTokens(value)
  # Get the initial string for the numeric value and number type
  numericValue = tokens[0].getValue()
  numericType = tokens[1].getValue() 
  # Check if the second token is a period. If this is true, we
  # must continue checking. 
  if len(tokens) >= 2 and \
     tokens[1].getType() == HDLmTokenTypes.operator and \
     tokens[1].getValue() == '.':
    numericValue += '.'
    # The third token could be a second set of digits or 
    # it could be the numeric type
    if len(tokens) >= 3 and \
       tokens[2].getType() == HDLmTokenTypes.integer:
      numericValue += tokens[2].getValue()
      numericType = tokens[3].getValue() 
    # It appears that the third token is not a set of 
    # digits. We assume that the third token must be
    # the type value.
    else:
      numericType = tokens[2].getValue() 
    # Convert the numeric value to floating-poing
  numericValue = float(numericValue)
  return [numericValue, numericType]

# Get the name of current operating system
def getOperatingSystemName():
  osName = platform.system() 
  if osName == 'Darwin':
    osName = 'Macintosh'
  return osName

# This function returns a Python version string and a platform
# version string
def getPythonVersion():
  outStr = 'Python {0} on {1}'.format(sys.version, sys.platform)
  return outStr

# Get the text from an element
def getText(element):
  return element.text

# Get the text fromm an element using a class to find the
# element. This only works if there is one (and exactly
# one) element for the class name. If there no elements
# for the class name, this routine will return None. If
# there are more than one element for the class name, 
# this routine will raise an error.
def getTextclass(driver, className):  
  # Get the list of elements (zero, one, or many) that match
  # the class name passed by the caller
  elements = findByClass(driver, className)
  elementsLen = len(elements)
  # Check the number of elements
  if elementsLen == 0:
    return None
  if elementsLen > 1:
    raise SystemError("Too many elements matched class name - " + className)
  # We can get the actual text and return it to the caller
  element = elements[0]
  text = getText(element)
  return text

# Scan a web site and get all of the links from the
# web site. Return the dictionary of links to the caller. 
def getWebSiteDict(browser, webSiteHost):
  # Build the web site object for use below
  webSite = HDLmWebSite(webSiteHost)
  # Add the home page to the web site object
  webSite.addPage('/')
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
      enterUrl(browser, urlStr)
  # Define a local function that gets the links from
  # a web page
  def getPageHrefs():
    hrefsFromAttributes = getAttributes(browser, 'href')
    hrefs = []
    for href in hrefsFromAttributes:
      if href == '#' or \
         href.startswith('javascript'):
        continue
      hrefs.append(href)
    return hrefs
  # Try to get all of the links for the current web site
  webSite.update(getPageFunc, getPageHrefs)
  # Returh all of the links to caller as a dictionary
  return webSite.getDict()
  
# This function runs a set of tests using each of the packages
def repeatPackages(nestLevel, context, runDict, firstTest, lastTest):
  newDict = runDict.copy()
  # Build the levels instance
  packageList = ['all', 'combo', 'stan']
  levelsObj = Levels([packageList])
  levelsObj.reset()
  # Process each of the packages
  while True:
    # Get the current set of choices
    currentPackage = levelsObj.getChoices()[0]
    newDict['Test Package'] = currentPackage
    runTests(nestLevel, context, glbTests, newDict,
             firstTest, lastTest)
    # Increment the levels object and check for overflow. If the
    # overflow flag is set, then we are done.
    levelsObj.increment()
    overflowFlag = levelsObj.getOverflow()
    if (overflowFlag):
      break
  return True

# The routine below was created to run a specific test. It seems to 
# have worked correctly.
def runTest(context, runDict):
  nestLevel = 1
  testHomePageStart(nestLevel, context, runDict)
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  webStr = 'https://www.oneworldobservatory.com/favicon.ico'
  webStr = 'https://www.oneworldobservatory.com/it-IT/static/img/header-desktop.jpg'
  for i in range(5):
    enterUrl(browser, webStr)
  return

# This function runs all of the tests. The list of tests is
# passed to this routine. Each of the tests is run and the
# results are presented. Note that values passed via the run
# dictionary take precedence over values obtain from each 
# test case. 
def runTests(nestLevel, context, testList, runDict, firstTest = None, lastTest = None):
  outLines = context.getOutLines()
  internalUseOnlyFlag = context.getInternalUseOnly() 
  # Get some values set by the caller, if any
  runFile = runDict.get('Test File', None)
  runFirst = runDict.get('Test First', None)
  runLanguage = runDict.get('Test Language', None)
  runLast = runDict.get('Test Last', None)
  runPackage = runDict.get('Test Package', None)
  runPathName = runDict.get('Test Path Name', None)
  runXPath = runDict.get('Test XPath', None)
  # At this point, we may want to add a line to the output file.
  # The possibile line describes the current set of tests. Of 
  # course, we only want to do this at the first nesting level
  # and we are not running in internal use only mode. 
  if nestLevel == 0 and not internalUseOnlyFlag:
    addTestsLine(outLines, firstTest, lastTest)
  # Check if the first test value is actually set. If the first test value
  # is actually set, convert it to a rule index value.
  if firstTest != None:
    ruleIndex = -1
    for test in testList:
      ruleIndex += 1
      if firstTest == test[0]:
        firstTest = ruleIndex
        break
  # Check if the last test value is actually set. If the first test value
  # is actually set, convert it to a rule index value.
  if lastTest != None:
    ruleIndex = -1
    for test in testList:
      ruleIndex += 1
      if lastTest == test[0]:
        lastTest = ruleIndex
        break
  # Increment the nesting level
  nestLevel += 1
  # Run each of the tests
  ruleIndex = -1
  for test in testList:
    # Increment the rule index value
    ruleIndex += 1
    # Check if the current rule is before the first rule we should
    # actually run
    if firstTest != None:
      if ruleIndex < firstTest:
        continue
    # Check if the current rule is after the last rule we should
    # actually run
    if lastTest != None:
      if ruleIndex > lastTest:
        continue
    # Get some information about the current rule
    testName = test[0]
    testDict = test[1]
    # Remove a few entries from the dictionary, if need be
    runDict.pop('Test File', None)
    runDict.pop('Test First', None)
    runDict.pop('Test Language', None)
    runDict.pop('Test Last', None)
    runDict.pop('Test Package', None)
    runDict.pop('Test Path Name', None)
    runDict.pop('Test XPath', None)
    # Add the test file to the dictionary, if need be
    runDict['Test File'] = runFile
    if runDict['Test File'] == None:
      runDict['Test File'] = testDict.get('Test File', None)
    # Add the first test to the dictionary, if need be
    runDict['Test First'] = runFirst
    if runDict['Test First'] == None:
      runDict['Test First'] = testDict.get('Test First', None)
    # Add the test language to the dictionary, if need be
    runDict['Test Language'] = runLanguage
    if runDict['Test Language'] == None:
      runDict['Test Language'] = testDict.get('Test Language', None)
    # Add the last test to the dictionary, if need be
    runDict['Test Last'] = runLast
    if runDict['Test Last'] == None:
      runDict['Test Last'] = testDict.get('Test Last', None)
    # Add the test package to the dictionary, if need be
    runDict['Test Package'] = runPackage
    if runDict['Test Package'] == None:
      runDict['Test Package'] = testDict.get('Test Package', None)
    # Add the test path name to the dictionary, if need be
    runDict['Test Path Name'] = runPathName
    if runDict['Test Path Name'] == None:
      runDict['Test Path Name'] = testDict.get('Test Path Name', None)
    # Add the test XPath to the dictionary, if need be
    runDict['Test XPath'] = runXPath
    if runDict['Test XPath'] == None:
      runDict['Test XPath'] = testDict.get('Test XPath', None)
    # Get the text function
    testFunction = test[2] 
    testRoutine = eval(testFunction)
    # Try to actually run the test. This fails from time to time (for many
    # reasons. Report the results of the test if possible.
    try:
      results = testRoutine(nestLevel, context, runDict)
    except Exception as e:
      print('In runTests invoking testRoutine')
      print(str(testRoutine))
      print(str(e))
      results = [str(e)]
    # Report the results of the test
    scriptId = test[1]['Script Id']
    testCase = test[1]['Test Case']
    stepNumber = test[1]['Step Number']
    description = test[0]
    testLanguage = runDict['Test Language']
    testPackage = runDict['Test Package']
    if testPackage != None:
      testPackage = HDLmString.capitalize(testPackage)
    # If we do not have a list of lists, then we must create 
    # one. The code below assumes that we have a list of lists.  
    if not isinstance(results[0], list):
      results = [results]
    # Process each of the results. The number of results may
    # be one or it may be greater than one. 
    for result in results:
      # Get the first value from the current list
      resultFirst = result[0]
      # Check if the current result should be reported or not
      resultReport = True
      # Check if only error results should be reported
      if context.getReportOnlyErrors() == True:
        resultType = type(resultFirst)
        if resultType == type(bool()):
          if resultFirst == True:
            resultReport = False
        else:
          if resultFirst == 'Bypassed' or resultFirst == 'Ignore': 
            resultReport = False
      # Build a line describing the test and the result(s)
      if resultReport:
        resultLineDateTime = datetime.datetime.now()
        resultLineTime = resultLineDateTime.strftime('%Y-%m-%dT%H:%M:%S.%f')
        # We used to use a very different result time format that Excel had 
        # trouble formatting when it was loaded from a CSV file. We now use
        # something closed to standard ISO timestamps. This appears to work. 
        #
        # resultLineTime = str(datetime.datetime.now().time())
        resultLine = buildResultLine(resultLineTime,
                                     scriptId, testCase, stepNumber, description, 
                                     testLanguage, testPackage, *result)
        # Add the result line to the collection of output lines
        outLines.addLine(resultLine)
        outLines.writeOutputFile() 
  return

# Handle shutdown 
def shutdown(browser, cpuTimeStart, wallTimeStart):  
  if browser != None:
    browser.quit()
  return

# Handle starting a specific driver. Return the driver to the
# caller. This function takes a standard application name.
def startDriver(browserName):
  # Get the driver name from the application (browser) name
  driverName = getApplicationDriverName(browserName)
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

# Handle startup. This function takes a standard application name.
def startup(browserName):  
  # Start the browser
  browser = startDriver(browserName)
  # Load the standard homepage
  browser.get('http://www.oneworldobservatory.com')
  browser.quit()
  browser = None
  return browser

# This function advances the date and picks a time for some packages
def testAdvanceDateAndTime(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # Get the current ticket package from the run dictionary
  package = runDict['Test Package']
  # We need very different code for English versus other languages
  if language != 'EN':
    # Advance the month
    classStr = 'icon-solid-right-arrow'
    element = findByClassClick(context, classStr, 'override')
    # Pick the first day
    time.sleep(3)
    xpathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div/table/tbody/tr[1]/td[7]/span/span/button/span'
    element = findByXPathClick(browser, xpathStr)
    # Pick the 9:00 AM time slot. This can not be done for
    # the All-Inclusive package. This is a certain type of
    # special case code. 
    if package != 'all': 
      time.sleep(3)
      xpathStr = '//*[@id="datetime-time-0"]'
      element = findByXPathClick(browser, xpathStr)
    # Click on the next button
    time.sleep(3)
    xpathStr = '//*[@id="datetime-next-btn"]'
    element = findByXPathClick(browser, xpathStr)
    return [True]
  # The code below only applies to English
  if package == 'all':
    return ['Bypassed', 'Package', HDLmString.capitalize(package)]
  # Advance the month
  classStr = 'icon-solid-right-arrow'
  element = findByClassClick(context, classStr, 'override')
  # Pick the first day
  time.sleep(3)
  xpathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div/table/tbody/tr[1]/td[7]/span/span/button/span'
  element = findByXPathClick(browser, xpathStr)
  # Click on the next button
  time.sleep(3)
  xpathStr = '//*[@id="datetime-next-btn"]'
  element = findByXPathClick(browser, xpathStr)
  # Pick the 9:00 AM time slot 
  time.sleep(3)
  xpathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/div[2]/div[2]/div/div/fieldset/div[2]/div[1]/div/div/div[1]/label'
  element = findByXPathClick(browser, xpathStr)
  # Click on the next button
  time.sleep(3)
  xpathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[2]/button'
  element = findByXPathClick(browser, xpathStr)
  return [True]  

# This function tries to find the bottom CTA button. This function returns
# true if the CTA button can be found. This function returns false if the
# CTA button can not be found.
def testBottomCta(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Try to find the bottom CTA button
  className = 's-slide-call-to-action'
  className = 's-slider-slide__button'
  elem = findByClassOne(browser, className)
  # Set the final return value
  rv = [False, 'Bottom CTA button Not found', className]
  if elem != None:
    rv = [True]
  return rv

# This function finds and checks a currency symbol 
def testCheckCurrency(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # Get the current ticket package from the run dictionary
  package = runDict['Test Package']
  # Based on the current language and package, get the package description information
  dictKey = language + package
  rv = [True]
  # Get and check the ticket price
  pathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/span[4]'
  # Special case code for traditional Chinese with the standard package  
  if dictKey == 'TWstan':
    pathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/span[1]'
  element = findByXPathOne(browser, pathStr)
  elementText = getText(element)
  if not elementText.startswith('$'):
    rv = [False, 'Currency does not start with a dollar sign', '$', elementText]
  return rv

# This function finds and checks a package description
def testCheckDescription(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # Get the current ticket package from the run dictionary
  package = runDict['Test Package']
  packageDict = {'all': 'All-Inclusive', 'combo': 'Combination', 'stan': 'Standard'}
  # Build the language and package dictionary
  languageDict = {'ENstan':  [4, 'STANDARD EXPERIENCE includes these benefits:', 'Elevators, See Forever Theater, Sky Portal & City Pulse'], 
                  'ENcombo': [5, 'COMBINATION EXPERIENCE includes these benefits:', 'Experience Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater, Sky Portal & City Pulse'],
                  'ENall':   [6, 'ALL-INCLUSIVE EXPERIENCE includes these benefits:', 'Experience Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater, Sky Portal & City Pulse'],
                  'FRstan':  [3, 'LE FORFAIT SIMPLE inclut les prestations suivantes​nbsp​:​', 'Les attractions Global Welcome Center, Voices, Foundations, les ascenseurs SkyPod, le théâtre See Forever, le Sky Portal et City Pulse.'],
                  'FRcombo': [5, 'LE FORFAIT DÉCOUVERTE inclut les prestations suivantes :', 'Les attractions Global Welcome Center, Voices, Foundations, les ascenseurs SkyPod, le théâtre See Forever, le Sky Portal et City Pulse.'],
                  'FRall':   [5, 'LE FORFAIT INTÉGRAL inclut les prestations suivantes :', "La visite de chacun des trois niveaux de l'observatoire (étages 100 à 102)"],
                  'DEstan':  [4, 'Das STANDARD-ERLEBNIS umfasst folgende Vorzüge:', 'Aufzügen, See Forever Theater, Sky Portal & City Pulse'],
                  'DEcombo': [6, 'Das KOMBI-ERLEBNIS umfasst folgende Vorzüge:', 'Aufzügen, See Forever Theater, Sky Portal & City Pulse'],
                  'DEall':   [7, 'Das ALL-INCLUSIVE ERLEBNIS umfasst folgende Vorzüge:', 'Aufzügen, See Forever Theater, Sky Portal & City Pulse'],
                  'ESstan':  [4, 'La EXPERIENCIA ESTÁNDAR incluye estos beneficios:', 'SkyPod, See Forever Theater, Sky Portal y City Pulse.'],
                  'EScombo': [5, 'La EXPERIENCIA COMBINADA incluye estos beneficios:', 'Descubra Global Welcome Center, Voices, Foundations, los elevadores SkyPod, See Forever Theater, Sky Portal y City Pulse.'],
                  'ESall':   [6, 'La EXPERIENCIA INTEGRAL incluye estos beneficios:', 'Descubra Global Welcome Center, Voices, Foundations, los elevadores SkyPod, See Forever Theater, Sky Portal y City Pulse.'],
                  'PTstan':  [4, 'A EXPERIÊNCIA PADRÃO inclui estes benefícios:', 'SkyPod, Cinema See Forever, Sky Portal e City Pulse'],
                  'PTcombo': [5, 'A EXPERIÊNCIA COMBINAÇÃO inclui estes benefícios:', 'Acesso ao Global Welcome Center, Voices, Foundations, Elevadores SkyPod, Cinema See Forever, Sky Portal e City Pulse'],
                  'PTall':   [6, 'A EXPERIÊNCIA COM TUDO INCLUÍDO inclui estes benefícios:', 'Acesso ao Global Welcome Center, Voices, Foundations, Elevadores SkyPod, Cinema See Forever, Sky Portal e City Pulse'],
                  'ITstan':  [4, "L'ESPERIENZA STANDARD comprende questi vantaggi:", 'SkyPod, del See Forever Theater, dello Sky Portal e del City Pulse'],
                  'ITcombo': [5, "L'ESPERIENZA COMBINATA include questi vantaggi:", 'Vivi le emozioni del Global Welcome Center, di Voices, delle Foundations, degli ascensori SkyPod, del See Forever Theater, dello Sky Portal e del City Pulse'],
                  'ITall':   [6, "L'ESPERIENZA ALL-INCLUSIVE comprende questi vantaggi:", 'Vivi le emozioni del Global Welcome Center, di Voices, delle Foundations, degli ascensori SkyPod, del See Forever Theater, dello Sky Portal e del City Pulse'],
                  'JAstan':  [3, 'スタンダード体験には次の特典がついています::', 'Global Welcome Center、Voices、Foundations、Skypod エレベーター、See forever シアター、Sky Portal、City Pulse での体験 .'],
                  'JAcombo': [5, 'コンビネーション体験には次の特典がついています:', 'Global Welcome Center、Voices、Foundations、Skypod エレベーター、See forever シアター、City Pulse での体験'],
                  'JAall':   [6, '営業時間内ならいつでもご来場いただけます オールインクルーシブ体験には次の特典がついています', 'Global Welcome Center、Voices、Foundations、Skypod エレベーター、See forever シアター、City Pulse での体験'],
                  'CNstan':  [3, '标准体验包括以下礼遇', '体验 Global Welcome Center、Voices、Foundations、SkyPod 电梯、See Forever 剧院、Sky Portal 和 City Pulse'],
                  'CNcombo': [5, '组合体验包括以下礼遇:', '体验 Global Welcome Center、Voices、Foundations、SkyPod 电梯、See Forever 剧院和 City Pulse'],
                  'CNall':   [6, '全包体验包括以下礼遇::', '体验 Global Welcome Center、Voices、Foundations、SkyPod 电梯、See Forever 剧院和 City Pulse'],
                  'TWstan':  [3, '標準體驗包括下列好處:', '體驗 Global Welcome Center、Voices、Foundations、SkyPod 電梯、See Forever 劇院、Sky Portal 和 City Pulse'],
                  'TWcombo': [5, '組合體驗包括下列好處:', '體驗 Global Welcome Center、Voices、Foundations、SkyPod 電梯、See Forever 劇院和 City Pulse'],
                  'TWall':   [6, '全包體驗包括下列好處:', '體驗 Global Welcome Center、Voices、Foundations、SkyPod 電梯、See Forever 劇院和 City Pulse.'],
                  'HIstan':  [3, 'स्टैंडर्ड एक्सपीरिएंस में ये फ़ायदे शामिल हैं::', 'Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater, Sky Portal, और City Pulse देखें'],
                  'HIcombo': [5, 'एक्सपीरिएंस में ये फ़ायदे शामिल हैं:', 'Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater और City Pulse देखें .'],
                  'HIall':   [6, 'ऑल-इन्क्लूसिव एक्सपीरिएंस में ये फ़ायदे शामिल हैं:', '• Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater और City Pulse देखें.'],
                  'KOstan':  [3, '스탠다드 관람에는 다음과 같은 혜택이 포함됩니다.:', 'Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater, Sky Portal, City Pulse 체험'],
                  'KOcombo': [5, '콤비네이션 체험에는 다음과 같은 혜택이 포함됩니다:', 'Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater, City Pulse 체험'],
                  'KOall':   [6, '올인클루시브 체험에는 다음과 같은 혜택이 포함됩니다:', '• Global Welcome Center, Voices, Foundations, SkyPod Elevators, See Forever Theater, City Pulse 체험']}
  # Based on the current language and package, get the package description information
  dictKey = language + package
  packageInfo = languageDict[dictKey]
  rv = [True]
  # Get and check the overall package description
  pathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[1]/div/div/div[2]/div[3]/div/p[1]/b[1]/span'
  # Special case code for Portugese with the standard package
  if dictKey == 'PTstan':
    pathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[1]/div/div/div[2]/div[3]/div/p[1]/table/tbody/tr/td/span/span/span/span/span/span/b'
  element = findByXPathOne(browser, pathStr)
  elementText = getText(element)
  packageInfoStr = packageInfo[1]
  if elementText != packageInfoStr:
    firstDifference = HDLmString.findFirstDifference(elementText, packageInfoStr)
    rv = [False, 'Invalid overall package description found', 
          packageInfo[1], elementText, len(packageInfoStr), 
          len(elementText), firstDifference]
  # Get and check the last line of the package description
  pathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[1]/div/div/div[2]/div[3]/div/p[1]/ul/li['
  pathStr += str(packageInfo[0])
  pathStr += ']/span'
  # Special case code for Portugese with the standard package
  if dictKey == 'PTstan':
    pathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[1]/div/div/div[2]/div[3]/div/p[1]/table/tbody/tr/td/ul[2]/li/span'
  element = findByXPathOne(browser, pathStr)
  elementText = getText(element)
  packageInfoStr = packageInfo[2]
  if elementText != packageInfoStr:
    firstDifference = HDLmString.findFirstDifference(elementText, packageInfoStr)
    rv = [False, 'Invalid last line package description found', 
          packageInfoStr, elementText, len(packageInfoStr),
          len(elementText), firstDifference]
  return rv

# This function checks the hrefs on a web page
def testCheckHrefs(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Set a few initial values
  errorCount = 0
  errorList = []
  # Get each of the hrefs from the current page
  hrefs = getAttributes(browser, 'href')
  # Check each href value
  for href in hrefs:
    # Check for, and skip, a bad href. For some reason we get some
    # values (for hrefs) that just don't make sense. We must skip
    # these values.
    if href.startswith('javascript:'):
      continue
    # Convert the href into a URL object
    hrefObj = HDLmUrl(href, prUrlOk=True, relativeUrl=True, semiSep=False)
    hostName = hrefObj.getHost()
    if hostName == None:
      continue
    # Check if the host name is really a problem
    if hostName.find('oneworldobservatory') < 0 and \
       hostName.find('owo-web-uat.corebine') < 0:
      continue
    # At this point we have an invalid href
    errorCount += 1
    # Add the current error to the list of errors
    curError = [False, 'Href may not use an absolute URL', href]
    errorList.append(curError)
  # Check if any errors were found
  if errorCount == 0: 
    rv = [True]
  else:
    rv = errorList
  return rv

# This function finds and checks a language code 
def testCheckLanguage(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # print('testCheckLanguage language=', language)
  # Fix the actual language code in one case
  if language == 'JP':
    language = 'JA'
  languageLower = language.lower()
  rv = [True]
  # Test the new node identification string
  nodeIdenStr = '{"type":"tag","attributes":{"tag":"span","innertext":"zy"},"counts":{"tag":9},"parent":{"href":"","class":["s-navigation__menu-link"],"target":"_self","tag":"a","innertext":"zy"}}'
  nodeIdenStr = nodeIdenStr.replace('zy', languageLower)
  element = findByNodeIdenOne(browser, nodeIdenStr)
  elementText = getText(element)
  # Check if the actual language code is/was the expected language code
  if language != elementText:
    rv = [False, 'Invalid two-letter language code found', language, elementText]
  return rv

# This function checks if the bottom CTA button is no larger than
# the top banner
def testCheckNoWider(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the rectangle for each HTML element
  classNameStr = 's-slide-call-to-action'
  classNameStr = 's-slider-slide__button' 
  blockRect = findByClassGetRectAdjusted(browser, classNameStr)
  textRect = findByClassGetRectAdjusted(browser, 's-slider-slide__footer') 
  compareOut = compareRectangles(blockRect, textRect)
  # Return the compare value to the caller
  if compareOut:
    return [True]
  return [False, 'Bottom CTA may be larger than top banner']

# This function checks if a URL is using https
def testCheckProtocol(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current browser URL
  browserUrl = browser.current_url
  browserUrlObj = HDLmUrl(browserUrl)
  browserOriginalUrl = browserUrlObj.getOriginalUrl()
  # Change https to http and run the URL
  webStr = browserOriginalUrl.replace("https", "http")
  enterUrl(browser, webStr)
  # Get the current browser URL
  browserUrl = browser.current_url
  browserUrlObj = HDLmUrl(browserUrl)
  # Get the scheme. The scheme should be https, but may not 
  # be.
  scheme = browserUrlObj.getScheme()
  # Check if we switched to https (as we should have)  
  if scheme == 'https': 
    rv = [True]
  else:
    rv = [False, 'Invalid URL scheme found', webStr]
  return rv

# This function checks a web site for insecure schemes.
# In other words, this function checks for any use of
# http (rather than https). 
def testCheckScheme(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Set a few initial values
  errorCount = 0
  errorList = []
  # Get all of the links from the current web site
  webSiteHostName = context.getWebSite()
  hrefsDict = getWebSiteDict(browser, webSiteHostName)
  # Check each href value
  for href in hrefsDict:
    # Check if the current URL is really an Email address. We 
    # don't want to treat Email addresses as URLs. 
    if href.find("mailto:") >= 0:
      continue
    # Convert the href into a URL object. This may result in
    # an exception in some cases. Skip the href if we detect
    # an exception.
    try:
      hrefObj = HDLmUrl(href, prUrlOk=True, relativeUrl=True)
    except Exception as e:
      print('In testCheckScheme using HDLmUrl')
      print(href)
      print(str(e))
      continue
    # Get the host scheme (if any) from the URL object
    hostScheme = hrefObj.getScheme()
    if hostScheme == None:
      continue
    # Check if the host scheme is really a problem
    if hostScheme == 'https':
      continue
    # At this point we have an invalid href scheme
    errorCount += 1
    # Add the current error to the list of errors
    hrefDictValue = hrefsDict[href]
    baseUrl = hrefDictValue[1]
    curError = [False, 'Invalid URL scheme found', href, baseUrl]
    errorList.append(curError)
  # Check if any errors were found
  if errorCount == 0: 
    rv = [True]
  else:
    rv = errorList
  return rv

# This function checks if a set of text fits entirely inside the CTA/button.
# This check is done by checking for the image that should come before the
# text and the image that should come after the text.
def testCheckText(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Store the class string
  classStr = 's-slide-call-to-action__link'
  selectorStr = '.' + classStr
  # Change the element text using JavaScript
  findByQuerySetAttribute(browser, selectorStr, 'innerHTML', 'Reserve Tickets')
  # Get the rectangle for each HTML element
  blockRect = findByClassGetRectAdjusted(browser, 's-slide-call-to-action')
  textRect = findByClassGetRectAdjusted(browser, 's-slide-call-to-action__link') 
  compareOut = compareRectangles(blockRect, textRect)
  # Return the compare value to the caller
  if compareOut:
    return [True]
  return [False, 'Test amy not fit inside bottom CTA button']

# This function checks if the URL has changed from the original value
def testCheckUrl(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get and check the current browser URL
  browserUrl = browser.current_url
  browserUrlObj = HDLmUrl(browserUrl)
  browserHost = browserUrlObj.getHost()
  if browserHost.startswith('www.'):
    browserHost = browserHost[4:]
  # Get and check the current context host name
  contextHost = context.getWebSite()
  if contextHost.startswith('www.'):
    contextHost = contextHost[4:]
  if browserHost == contextHost:
    rv = [True]
  else:
    rv = [False, 'URL host name has changed when it should not have', contextHost, browserHost]
  return rv

# This function checks if the background video is playing
def testCheckVideo(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the Region associated with the primary applicaton window
  browser.save_screenshot("imageFirst.png")
  # Wait for a while  
  time.sleep(5)
  browser.save_screenshot("imageSecond.png")
  # Read the images into image objects
  imageFirst = cv2.imread("imageFirst.png")
  imageSecond = cv2.imread("imageSecond.png")
  score = ssim(imageFirst, imageSecond, multichannel=True)
  # Set the final return value
  if score >= 0.9:
    rv = [False, 'Background video does not appear to be playing']
  else:
    rv = [True] 
  return rv

# This function checks a web site 
def testCheckWebSite(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Set a few initial values
  errorCount = 0
  errorList = []
  # Get all of the links from the current web site
  webSiteHostName = context.getWebSite()
  hrefsDict = getWebSiteDict(browser, webSiteHostName)
  # Check each href value
  for href in hrefsDict:
    # Check if the current URL is really an Email address. We 
    # don't want to treat Email addresses as URLs. 
    if href.find("mailto:") >= 0:
      continue
    # Convert the href into a URL object. This may result in
    # an exception in some cases. Skip the href if we detect
    # an exception.
    try:
      hrefObj = HDLmUrl(href, prUrlOk=True, relativeUrl=True)
    except Exception as e:
      print('In testCheckWebSite using HDLmUrl')
      print(href)
      print(str(e))      
      continue
    # Get the host name (if any) from the URL object
    hostName = hrefObj.getHost()
    if hostName == None:
      continue
    # Check if the host name is really a problem
    if hostName.find('oneworldobservatory') < 0 and \
       hostName.find('owo-web-uat.corebine') < 0:
      continue
    # At this point we have an invalid href
    errorCount += 1
    # Add the current error to the list of errors
    hrefDictValue = hrefsDict[href]
    baseUrl = hrefDictValue[1]
    curError = [False, 'Href may not use a relative URL', href, baseUrl]
    errorList.append(curError)
  # Check if any errors were found
  if errorCount == 0: 
    rv = [True]
  else:
    rv = errorList
  return rv

# This function tries to find the bottom CTA button. This function returns
# true if the CTA button can be found. This function returns false if the
# CTA button can not be found. After the bottom CTA button is found, it is
# clicked on. Note that this code only supports French for now.
def testClickBottomCta(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  rv = [False, 'Bottom CTA button not found']
  # Try to find the bottom CTA button
  ctaNodeIdenStr = '{"type":"class","attributes":{"href":"/fr-FR/buy-tickets/","class":["btn","btn-primary"],"target":"","tag":"a","innertext":"acheter des billets"},"counts":{"tag":62,"class":4},"parent":{"class":["button-container"],"tag":"div","innertext":"acheter des billets"},"grandparent":{"class":["carousel-caption","d-md-block"],"tag":"div","innertext":"acheter des billets"}}'
  elem = findByNodeIdenOne(browser, ctaNodeIdenStr)
  # Set the final return value
  if elem != None:
    elem.click()
    rv = True
  return [rv]

# This function tries to find the continue button, and if the
# continue button is found, click on it. This routine may not
# actually find a continue button.
def testClickContinue(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Try to click on the continue button
  element = findByIdIfFoundClick(browser, 'billing-continue-btn')
  if element != None:
    return [True]
  element = findByIdIfFoundClick(browser, 'payment-continue-btn')
  if element != None:
    return [True]
  # Report an error because we did not find the continue button
  errorList = []
  curError = [False, 'Continue button not found by Id']
  errorList.append(curError)
  return rv 

# This function finds and clicks on the 'No Thanks' button,
# if the current package has a 'No Thanks' button 
def testClickNoThanks(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # Get the current ticket package from the run dictionary
  package = runDict['Test Package']
  # Based on the language, possibly just return to the caller
  if language != 'EN':
    return ['Bypassed', 'Language', language]
  # Based on the current ticket package, set the file name
  if package == 'all':
    return ['Bypassed', 'Package', HDLmString.capitalize(package)]
  elif package == 'combo':
    return ['Bypassed', 'Package', HDLmString.capitalize(package)]
  elif package == 'stan':
    xpathStr = '/html/body/div[1]/div[1]/div[4]/div/div/div/div/div/div[5]/span' 
  # Switch to the iframe
  context.switchTo('override')
  # Try to click on the correct package
  element = findByXPathClick(browser, xpathStr)
  return [True]

# This function tries to click on the CTA button in the
# top right of the standard home page
def testClickTopRightCta(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Click on the CTA button in the top right of the home page
  nodeIdenStr = '{"type":"tag","attributes":{"tag":"span","innertext":"buy tickets"},"counts":{"tag":8},"parent":{"href":"/en-US/buy-tickets","class":["s-navigation__menu-link"],"target":"_self","tag":"a","innertext":"buy tickets"}}'
  nodeIdenStr = '{"type":"tag","attributes":{"tag":"span","innertext":"acheter des billets"},"counts":{"tag":8},"parent":{"href":"/fr/acheter-des-billets","class":["s-navigation__menu-link"],"target":"_self","tag":"a","innertext":"acheter des billets"}}'
  # Testing has shown that we can't really use node identifiers to locate the
  # CTA DOM entry. Sadly, we have to use XPath.
  # element = findByNodeIdenClick(browser, nodeIdenStr)  
  pathStrOld = '/html/body/div[1]/div/div/div[2]/div/div/div/nav/ul/li[1]/section/a'
  pathStrNew = '/html/body/div[1]/header/div/div/div/div/nav/ul/li[1]/a/span'
  element = findByXPathClick(browser, pathStrNew)
  return [True]

# This function finds and clicks on an element found using an 
# XPath. The XPath is obtained from the current test. 
def testClickXPath(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current XPath value from the run dictionary
  xpathStr = runDict['Test XPath']
  # Try to click on the correct eleement
  element = findByXPathClick(browser, xpathStr)
  return [True]

# This function finds and clicks on one of the buy now buttons.
# The correct package is selected based on what ticket package 
# we are currently handling.
def testCtaBuyingTickets(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get rid of the warning popup, if need by
  findByClassIfOneClick(browser, 'm-interstitial-close-btn')
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # Get the current ticket package from the run dictionary
  package = runDict['Test Package']
  # Get all of the class names for each elememt that has a specific
  # tag name
  classNameList = getClassNamesByTagName(browser, 'article')
  # Build a map from the class name list. The map shows were 
  # each package is located. The order of the packages can (and
  # does) change. 
  packageMap = convertClassNamesToMap(classNameList)
  # Based on the current ticket package, set the file name
  firstPartStr = '/html/body/div[1]/main/section[1]/section/div/div/div/div/article['
  lastPartStr = ']/header/div[3]/div/div/a'  
  firstPartStr = '/html/body/div[1]/main/section[1]/section/div/section/div/div/article['
  lastPartStr = ']/header/div/div[3]/div/div/a'
  articleNumber = packageMap[package] + 1
  xpathStr = firstPartStr + str(articleNumber) + lastPartStr 
  # Try to click on the correct package
  element = findByXPathClick(browser, xpathStr)
  return [True]

# This function enters a path name provided by the test case
def testEnterPathName(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Try to get the test path name provided by the test case
  testPathName = runDict['Test Path Name']
  # Get the website domain name
  webStr = context.getWebSite()
  if testPathName != '':
    webStr = 'https://' + webStr + '/' + testPathName
  enterUrl(browser, webStr)
  return [True]

# This function terminates the browser driver 
def testHomePageEnd(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Check if the browser driver value is set
  if browser == None:
    return ['Bypassed', 'No browser']
  # Terminate the browser driver
  browser.quit()
  browser = None
  context.setBrowserDriver(browser) 
  return ['Ignore']

# This function loads the home page of the application
def testHomePageStart(nestLevel, context, runDict):
  browserName = context.getApplication() 
  browserObj = startDriver(browserName)
  context.setBrowserDriver(browserObj)
  # The links we need to click on, may not show up right away. We need to
  # tell the driver to wait for links to appear.
  timeWait = 30
  browserObj.implicitly_wait(timeWait)
  browserObj.set_page_load_timeout(timeWait)
  webStr = 'https://' + context.getWebSite()
  enterUrl(browserObj, webStr)
  rv = True
  return ['Ignore']

# This function checks if the web site can be accessed
# with and without the wwww. prefix
def testHostNamePrefix(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the web site domain name. Remove the www. prefix
  # if need be.
  webStr = context.getWebSite()
  webStr = HDLmString.removePrefix(webStr, 'www.')
  # Run each of the tests 
  webStrUrl = 'https://' + webStr + '/' 
  enterUrl(browser, webStrUrl)
  webStrUrl = 'https://' + 'www.' + webStr + '/' 
  enterUrl(browser, webStrUrl)
  return [True]

# Make sure the last two tabs on the home page are in English
def testLastTwoTabs(nestLevel, context, runDict):
  rv = [True]
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Make sure a few fields are set correctly
  nodeIdenStr = '{"type":"tag","attributes":{"tag":"span","innertext":"more"},"counts":{"tag":8},"parent":{"href":"","class":["s-navigation__menu-link"],"target":"_blank","tag":"a","innertext":"more"}}'
  element = findByNodeIdenOne(browser, nodeIdenStr)
  text = getText(element)
  if text.upper() != 'MORE':
    print('The field that should be More, has - ', text)
    rv = [False, 'Invalid tab value found', 'More', text]
  nodeIdenStr = '{"type":"tag","attributes":{"tag":"span","innertext":"en"},"counts":{"tag":8},"parent":{"href":"","class":["s-navigation__menu-link"],"target":"_self","tag":"a","innertext":"en"}}'
  element = findByNodeIdenOne(browser, nodeIdenStr)  
  text = getText(element)
  if text != 'EN':
    print('The field that should be EN, has -', text)
    rv = [False, 'Invalid tab value found', 'EN', text]
  return rv

# This function checks if all of the CTA text fields match
def testMatchingText(nestLevel, context, runDict):
  rv = [True]
  textList = []
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Try to get the text from the top right CTA
  element = findByXPathOne(browser, '/html/body/div[1]/div/div/div[2]/div/div/div/nav/ul/li[1]/section/a')
  textTopRight = getText(element)
  # Build the list of XPath values
  xpathList = ['/html/body/div[1]/main/section[1]/section/div/div/div/div/article[1]/header/div[3]/div/div/a',
               '/html/body/div[1]/main/section[1]/section/div/div/div/div/article[2]/header/div[3]/div/div/a',
               '/html/body/div[1]/main/section[1]/section/div/div/div/div/article[3]/header/div[3]/div/div/a']
  # Get each of the text values using the XPath list
  for xpath in xpathList:
    element = findByXPathOne(browser, xpath)
    xpathText = getText(element)
    textList.append(xpathText)
  # Check if the text in each of the CTA buttons matches
  for text in textList:
    if text != textTopRight:
      rv = [False, 
            'At least one of the purchase text values does not match', 
            textTopRight, text]
  return rv

# Check a bunch of fields and make they don't contain any 
# pre-populated data
def testNoPrePopulated(nestLevel, context, runDict):
  rv = [True]
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Build the field list
  fieldList = ['//*[@id="fname"]'   , 'First name'        , '//*[@id="middleInitial"]', 'MI'          , '//*[@id="email"]'               , 'Email', 
               '//*[@id="address1"]', 'Address'           , '//*[@id="lname"]'        , 'Last name'   , '//*[@id="emailConfirmation"]'   , 'Email confirmation', 
               '//*[@id="address2"]', 'Apt/Suite'         , '//*[@id="phone"]'        , 'Phone number', '//*[@id="billing-country-name"]', 'Country', 
               '//*[@id="zip"]'     , 'Zip or postal code', '//*[@id="inputCity"]'    , 'City'        , '//*[@id="billing-state-name"]'  , 'State/Province']
  # Process each of the fields
  for i in range(0, len(fieldList), 2):
    fieldName = fieldList[i+1]
    fieldXPath = fieldList[i] 
    # Set the expected text
    expectedText = ''
    if fieldName == 'Country':
      expectedText = 'string:US'
    # Make sure a few fields are empty
    element = findByXPathOne(browser, fieldXPath)
    text = getAttribute(element, 'value')
    if text != expectedText:
      print(fieldName, text)
      rv = [False, 'Invalid prepopulated field found', fieldName, text]
  return rv

# Run all of the languages and packages tests again
def testRepeatAll(nestLevel, context, runDict):
  newDict = runDict.copy()
  # Build the levels instance
  languageList = glbLanguageList
  # languageList = ['EN', 'FR']
  # languageList = ['FR']
  # languageList = ['TW']
  # languageList = ['HI']
  # languageList = ['EN']
  # languageList = ['CN']
  languageList = ['PT']
  packageList = glbPackageList
  # packageList = ['stan', 'combo', 'all']
  # packageList = ['all']
  # packageList = ['stan'] 
  # packageList = ['stan', 'combo'] 
  # packageList = ['stan'] 
  packageList = ['stan'] 
  levelsObj = Levels([languageList, packageList])
  levelsObj.reset()
  # Specify the first and last test
  firstTest = newDict['Test First']
  lastTest = newDict['Test Last']
  # Process each of the choices
  while True:
    # Get the current set of choices
    currentLanguage = levelsObj.getChoices()[0]
    currentPackage = levelsObj.getChoices()[1]
    newDict['Test Language'] = currentLanguage
    newDict['Test Package'] = currentPackage
    runTests(nestLevel, context, glbTests, newDict,
             firstTest, lastTest)
    # Increment the levels object and check for overflow. If the
    # overflow flag is set, then we are done.
    levelsObj.increment()
    overflowFlag = levelsObj.getOverflow()
    if (overflowFlag):
      break
  return ['Ignore']

# This function runs a set of tests using the other packages
def testRepeatOtherTwo(nestLevel, context, runDict):
  newDict = runDict.copy()
  # Run the combination tests
  newDict['Test Package'] = 'combo'
  runTests(nestLevel, context, glbTests, newDict,
           'Open page for packages',
           'Close page for packages')
  # Run the standard tests
  newDict['Test Package'] = 'stan'
  runTests(nestLevel, context, glbTests, newDict,
           'Open page for packages',
           'Close page for packages')
  return ['Ignore']

# Run the language test with all of the languages 
def testRepeatLanguage(nestLevel, context, runDict):
  newDict = runDict.copy()
  # Build the levels instance
  languageList = glbLanguageList
  levelsObj = Levels([languageList])
  levelsObj.reset()
  # Specify the first and last test
  firstTest = newDict['Test First']
  lastTest = newDict['Test Last']
  # Process each of the choices
  while True:
    # Get the current set of choices
    currentLanguage = levelsObj.getChoices()[0]
    newDict['Test Language'] = currentLanguage
    runTests(nestLevel, context, glbTests, newDict,
             firstTest, lastTest)
    # Increment the levels object and check for overflow. If the
    # overflow flag is set, then we are done.
    levelsObj.increment()
    overflowFlag = levelsObj.getOverflow()
    if (overflowFlag):
      break
  return ['Ignore']

# This function finds and clicks on the CTA for the Morning Package. 
# Note that the concept of the morning package only applies to the
# All-Inclusive package. This code is bypassed (below) in all other
# cases.
def testSelectMorning(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Wait for a while and switch to the iframe
  time.sleep(5)
  context.switchTo('override')
  # Get the current ticket package from the run dictionary
  package = runDict['Test Package']
  if package != 'all':
    return ['Bypassed', 'Package', HDLmString.capitalize(package)]
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  if language != 'EN':
    return ['Bypassed', 'Package', HDLmString.capitalize(package)]
  # Switch to the next month
  element = findByXPathClick(browser, 
    '/html/body/div[1]/div[1]/div[4]/div/div/div[2]/div[4]/div[2]/div/div/div/table/thead/tr[1]/td[3]/span')
  # Pick the first day
  time.sleep(5)
  element = findByXPathClick(browser, 
    '/html/body/div[1]/div[1]/div[4]/div/div/div[2]/div[4]/div[2]/div/div/div/table/tbody/tr[1]/td[7]/span/span/button/span[1]')
  # Try to select the morning package
  element = findByXPathClick(browser, 
                             '/html/body/div[1]/div[1]/div[4]/div/div/div[2]/div[5]/div[1]/div[2]/ul/li[1]/div/div[4]/button')
  return [True]

# This function finds and clicks on the adult ticket counter to request 
# one adult ticket
def testSelectOneAdultTicket(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Increment the adult ticket counter
  element = findByXPathClick(browser, 
    '/html/body/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/ng-form/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div/div/span[2]/button/span')
  return [True]

# This function finds and clicks on the language menu. This code will 
# only work if the current language is English. Note that this routine
# in its current form, can not be used to specifiy English as the 
# target language.
def testSpecifyForeignLanguage(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get the current language from the run dictionary
  language = runDict['Test Language']
  # print('testSpecifyForeignLanguage language =', language)
  # Build the language dictionary
  languageDict = {'EN': '1', 'FR': '2', 'DE': '3',
                  'ES': '4', 'PT': '5', 'IT': '6',
                  'JA': '7', 'CN': '8', 'TW': '9',
                  'HI': '10', 'KO': '11'}
  # Bring down the language menu by clicking on it  
  nodeIdenStr = '{"type":"class","attributes":{"class":["nav-lang"],"tag":"span","innertext":"en"},"counts":{"tag":35,"class":2},"parent":{"href":"#","tag":"a","innertext":"en"},"grandparent":{"class":["menu-item-has-children","lang-separator"],"tag":"li","innertext":"en"}}'
  findByNodeIdenClick(browser, nodeIdenStr)
  # Set each of the node identification strings
  nodeIdenStrEN = '{"type":"tag","attributes":{"href":"/","tag":"a","innertext":"english"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"english"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrFR = '{"type":"tag","attributes":{"href":"/fr-FR","tag":"a","innertext":"français"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"français"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrDE = '{"type":"tag","attributes":{"href":"/de-DE","tag":"a","innertext":"deutsch"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"deutsch"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrES = '{"type":"tag","attributes":{"href":"/es","tag":"a","innertext":"español"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"español"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrPT = '{"type":"tag","attributes":{"href":"/pt-BR","tag":"a","innertext":"português"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"português"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrIT = '{"type":"tag","attributes":{"href":"/it-IT","tag":"a","innertext":"italiano"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"italiano"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrJA = '{"type":"tag","attributes":{"href":"/ja-JP","tag":"a","innertext":"日本語"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"日本語"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrCN = '{"type":"tag","attributes":{"href":"/zh-CN","tag":"a","innertext":"中文"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"中文"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrTW = '{"type":"tag","attributes":{"href":"/zh-TW","tag":"a","innertext":"台語"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"台語"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrHI = '{"type":"tag","attributes":{"href":"/hi-IN","tag":"a","innertext":"हिंदी"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"हिंदी"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  nodeIdenStrKO = '{"type":"tag","attributes":{"href":"/ko-KR","tag":"a","innertext":"한국어"},"counts":{"tag":62},"parent":{"tag":"li","innertext":"한국어"},"grandparent":{"class":["sub-menu","sl_norewrite"],"tag":"ul","innertext":"english"}}'
  # Put the node identification strings in a list
  nodeIdenStrs = []
  nodeIdenStrs.append(nodeIdenStrFR)  
  nodeIdenStrs.append(nodeIdenStrDE)  
  nodeIdenStrs.append(nodeIdenStrES)  
  nodeIdenStrs.append(nodeIdenStrPT)  
  nodeIdenStrs.append(nodeIdenStrIT)  
  nodeIdenStrs.append(nodeIdenStrJA)  
  nodeIdenStrs.append(nodeIdenStrCN)  
  nodeIdenStrs.append(nodeIdenStrTW)  
  nodeIdenStrs.append(nodeIdenStrHI)  
  nodeIdenStrs.append(nodeIdenStrKO)  
  # Convert the language code (typically two letters in uppercase) to a list index number
  langPosition = languageDict[language] 
  langPosition = int(langPosition) - 2
  # print('testSpecifyForeignLanguage langPosition =', langPosition)
  # if langPosition < 0:
  #   print('testSpecifyForeignLanguage nodeIdenStrs[langPosition] =', nodeIdenStrs[langPosition])
  # Try to click on the correct entry
  if langPosition >= 0:
    element = findByNodeIdenClick(browser, nodeIdenStrs[langPosition])
  return [True]

# This function verifies that the browser connection is secure 
def testVerifySecure(nestLevel, context, runDict):
  # Get the browser driver object for use below
  browser = context.getBrowserDriver()
  # Get and check the current URL
  browserUrl = browser.current_url
  if browserUrl.startswith('https'):
    rv = [True]
  else:
    rv = [False, 'Invalid URL scheme or protocol found']
  return rv

# Main program
def main():   
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  # Get the operating system name
  osName = getOperatingSystemName()
  # Get some values provided by the invoker or use default values
  result = getArgs()
  internalUseOnlyFlag = result.internal
  browserName = HDLmString.capitalize(result.Browser)
  urlStr = result.URL
  # Create the object used to accumulate output lines and add the
  # heading line
  outLines = HDLmBuildLines()
  outputFileName = buildFileName(browserName, 'csv')
  outLines.setFileName(outputFileName)
  # We only really need a heading line if we are not running
  # in internal use only mode
  if not internalUseOnlyFlag:  
    addHeadingLine(outLines)  
  # Build the overall context object
  context = Context(browserName, osName, urlStr)
  context.setOutLines(outLines)
  context.setReportOnlyErrors(result.errors)
  context.setInternalUseOnly(internalUseOnlyFlag)
  # Add an output line describing the current environment. This 
  # step is only really needed if we are not running in internal 
  # use only mode. 
  if not internalUseOnlyFlag:
    addContextLine(context, outLines)
    outLines.writeOutputFile()
  nestLevel = 0
  runDict = {'Test Package': 'all'}
  # Start processing
  # browser = startup(browserName)
  browser = None
  # Run a few tests
  # Test set 1
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for start of tests',
  #          'Close page for start of tests') 
  # Test set 2
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for packages',
  #          'Close page for packages')
  # Test set 2 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Repeat for the other two',
  #          'Repeat for the other two')
  # Test set 3
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for new language',
  #          'Close page for new language')
  # Test sets 4 and 5
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for matching text',
  #          'Close page for secure')
  # Test sets 6 and 7
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for background video',
  #          'Close page for text fits inside')
  # Test set 8
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for chosen language',
  #          'Close page for chosen language(s)')
  # Test set 8 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #         'Chosen language(s) repeat',
  #         'Chosen language(s) repeat')
  # Test sets 8 and 9
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for chosen language',
  #          'Close page for top buy foreign')
  # Test set 9 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Top buy foreign repeat',
  #          'Top buy foreign repeat')
  # Test set 10
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for language code',
  #          'Close page for language code')
  # Test set 10 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Language code each language repeat',
  #          'Language code each language repeat')
  # Test set 11
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for checkURL',
  #          'Close page for checkURL')
  # Test set 11 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'CheckURL repeat all',
  #          'CheckURL repeat all')
  # Test set 12
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for protocol code',
  #          'Close page for protocol code')
  # Test set 12 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Protocol code each language repeat',
  #          'Protocol code each language repeat')
  # Test set 13
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for href code',
  #          'Close page for href code')
  # Test set 13 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Href code each language repeat',
  #          'Href code each language repeat')
  # Test set 14
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for web site code',
  #          'Close page for web site code')
  # Test set 14 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Web site code each language repeat',
  #          'Web site code each language repeat')
  # Test set 15
  runTests(nestLevel, context, glbTests, runDict,
           'Open page for scheme code',
           'Close page for scheme code')
  # Test set 15 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Scheme code each language repeat',
  #          'Scheme code each language repeat')
  # Test set 16
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for prefix code',
  #          'Close page for prefix code')
  # Test set 1
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for start of tests',
  #          'Close page for start of tests')
  # Test set 1 - Partial
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for start of tests',
  #          'For start examine CTA')
  # Test set 2
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for packages',
  #          'Close page for packages')
  # Test sets 1 and 2
  # runTests(nestLevel, context, glbTests, runDict,
  #        'Open page for start of tests',
  #        'Repeat for the other two')
  # Test set 3
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for new language',
  #          'Close page for new language')
  # Test set 4
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for matching text',
  #          'Close page for matching text')
  # Test set 6 
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for background video',
  #          'Close page for background video')
  # Test set 7
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for text fits inside',
  #          'Close page for text fits inside')
  # Test set 8 (second part)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for chosen language(s)',
  #          'Close page for chosen language(s)')
  # Test set 8 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Chosen language(s) repeat',
  #          'Chosen language(s) repeat')
  # Test set 9
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for top buy',
  #          'Close page for top buy')
  # Test set 9 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Top buy foreign repeat',
  #          'Top buy foreign repeat')
  # Test set 10
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for language code',
  #          'Close page for language code')
  # Test set 10 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Language code each language repeat',
  #          'Language code each language repeat')
  # Test set 11
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for checkURL',
  #          'Close page for checkURL')
  # test set 11 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'CheckURL repeat all',
  #          'CheckURL repeat all')
  # Test sets 1 through 9 (repeat)
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for start of tests',
  #          'Top buy foreign repeat')
  # Test sets 10 through 13
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for language code',
  #          'Href code each language repeat')
  # Test sets 14 through 16
  # runTests(nestLevel, context, glbTests, runDict,
  #          'Open page for web site code',
  #          'Close page for prefix code')
  # Run all of the tests
  # runTests(nestLevel, context, glbTests, runDict)
  # Run a specific test
  # runTest(context, runDict)
  # End processing
  shutdown(browser, cpuTimeStart, wallTimeStart)
  # Check if we are running in internal use only mode. If not,
  # write the collected output lines to a file. If we are running
  # in internal use only mode, the collect lines need to be writter
  # to standard output.
  if not internalUseOnlyFlag:
    outLines.writeOutputFile()
  else:
    for line in outLines.getLines():
      print(line)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took. This output is not needed
  # or wanted if we are running in internal use only 
  # mode. 
  if not internalUseOnlyFlag:
    print('CPU    ', cpuTimeEnd - cpuTimeStart)
    print('Elapsed', wallTimeEnd - wallTimeStart) 

# Actual starting point
if __name__ == "__main__":
  main()