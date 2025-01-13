# Class for providing a set of GUI extended editor functions. No instances
# of this class are ever created.
 
from HDLmDefines                  import *
from HDLmExtensionBothManageRules import *
from HDLmGlobals                  import *
from HDLmTree                     import *

class HDLmGXE(object):
  # Create (if need be) the new site node, that will be the parent
  # of the new node we are creating 
  @staticmethod
  def buildSiteNode(hostName, treeNodeType):
    # Find or create the site node that will be the parent for the 
    # newly created node 
    newSiteNodePath = HDLmGXE.buildSiteNodePath(hostName, treeNodeType);
    # print(newSiteNodePath) 
    updateDatabaseFalse = False
    newSiteNode = HDLmTree.buildSiteNode(newSiteNodePath, 
                                         updateDatabaseFalse, 
                                         treeNodeType)
    return newSiteNode 
  # This routine does all of the work needed to build a new node path 
  # for a site node. The site node path is returned to the caller. 
  @staticmethod
  def buildSiteNodePath(hostName, treeNodeType):
    # Create a complete path to the node we are about to create (perhaps) 
    newNodePath = []
    newNodePath.append(HDLmDefines.getString('HDLMTOPNODENAME'))
    newNodePath.append(HDLmDefines.getString('HDLMCOMPANIESNODENAME'))
    newNodePath.append(hostName)
    # Check if we are building a node path for a rule or a data value 
    if treeNodeType == HDLmTreeTypes.data:
      newNodePath.append(HDLmDefines.getString('HDLMDATANODENAME'))
    if treeNodeType == HDLmTreeTypes.rules:
      newNodePath.append(HDLmDefines.getString('HDLMRULESNODENAME'))
    newNodePath.append(HDLmDefines.getString('HDLMDIVISIONNODENAME'))
    newNodePath.append(HDLmDefines.getString('HDLMSITENODENAME'))
    # Find or create the site node that will be the parent for the 
    # newly created node 
    newSiteNodePath = newNodePath[0:HDLmDefines.getNumber('HDLMSITENODEPATHLENGTH')]
    return newSiteNodePath
  # Set the current value of the rules updated flag 
  @staticmethod
  def rulesUpdatedSet(): 
    if HDLmGlobals.activeEditorType == HDLmEditorTypes.gxe: 
      HDLmExtensionBothManageRules.rulesUpdatedSet(True) 