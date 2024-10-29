# Class for providing a set of web sockets functions. No instances of this
# class are ever created.

from   HDLmConfigInfo  import * 
from   HDLmEmpty       import *
from   HDLmUtility     import *
import asyncio
import copy 
import jsons
import types
import websocket

class HDLmWebSockets(object):
  # Values that we are going to send are accumulated in the list below.
  # The WebSocket open routine takes an (the only) entry from this list
  # and sends it.
  contentSendValue = []
  # This routine returns a promise that yields either a string
  # with the complete set of modifications or an error. The 
  # promise is thenable. 
  def getModifications(messageRoutine=None):
    # console.log('In HDLmWebSockets.getModifications', HDLmUtility.getHostName()) 
    # console.log(HDLmWebSockets.contentSendValue) 
    #
    # Create an empty object
    getModEmpty = HDLmEmpty()
    # Build a message with the required information     
    sendJsonStr = jsons.dumps(getModEmpty)
    sendJsonStr = HDLmUtility.updateJsonStr(sendJsonStr, 'HDLmRequestType', 'getModPart')
    sendJsonStr = HDLmUtility.updateJsonStr(sendJsonStr, 'HDLmUrlValue', 'window.location.href')
    # console.log('In getModifications', sendJsonStr) 
    HDLmWebSockets.contentSendValue.append(sendJsonStr)
    # Build the callback function that will be used to handle the
    # WebSocket message that is returned by the caller. Note that
    # this routine is a closure and get important values from the
    # environment where it is defined. 
    def messageCallback(ws, wsMessage):
      # Provide an exception handler for the entire callback 
      try:
        currentWebSocket = ws
        # Close the WebSocket, if need be 
        if currentWebSocket != None:
          currentWebSocket.close()
        # Pass the WebSocket message to the appropriate handler 
        if messageRoutine != None:
          messageRoutine(wsMessage)
      except Exception as e: 
        errorText = HDLmError.reportError(e, 'messageCallback') 
    # Open a connnection to another process 
    HDLmWebSockets.openWebSocketConnection(messageCallback) 
    return  
  # This method creates a modified tree node with a set 
  # of fields removed from original tree node. Note that 
  # the original tree node is not modified and a modified 
  # copy of the original tree node is returned to the caller. 
  @staticmethod
  def modifiedTreeNode(treePos):
    # print('In HDLmWebSockets.modifiedTreeNode', treePos) 
    # Create a temporary copy of the current tree node. This is
    # done so that we can make changes to the temporary copy that
    # will not affect the original tree node. 
    tempPos = types.SimpleNamespace() 
    treePosVars = vars(treePos)
    for var in treePosVars:
      setattr(tempPos, var, copy.deepcopy(getattr(treePos, var)))
    if hasattr(tempPos, 'children'):
      del tempPos.children
    if hasattr(tempPos, 'containerWidget'):
      del tempPos.containerWidget
    if hasattr(tempPos, 'id'):
      del tempPos.id
    # Remove the saved details from the current node, if need be 
    if hasattr(tempPos, 'savedDetails'):
      del tempPos.savedDetails
    # Return the modified tree node to the caller 
    return tempPos
  # This method is the WebSocket message handler. This method runs
  # as part of a content script. This method does the actual work
  # of receiving a WebSocket message. 
  @staticmethod
  def onMessageWebSocketContent(ws):
    # Build an object from the JSON we just received. Get the
    # request type from the JSON. 
    # eventObj = jsons.loads(event.data) 
    currentWebSocket = ws
  # This method is the WebSocket open handler. This method runs as
  # part of a content script. This method does the actual work of
  # sending a WebSocket message to (hopefully) the receiver. 
  @classmethod
  def onOpenWebSocketContent(cls, ws):
    # print('In HDLmWebSockets.onOpenWebSocketContent', event) 
    # print(event) 
    currentWebSocket = ws
    # print(currentWebSocket) 
    # print(HDLmWebSockets.contentSendValue) 
    # Check if the send array is empty. We have nothing to send
    # if the send array is empty. 
    if len(HDLmWebSockets.contentSendValue) == 0:
      return
    # Get and remove the first entry from the send array and
    # send it 
    messageStr = HDLmWebSockets.contentSendValue.pop(0)
    # print(messageStr, HDLmWebSockets.contentSendValue)     
    currentWebSocket.send(messageStr)    
    # At the point, we used to close the WebSocket port in all cases. This is no longer
    # possible because we expect to receive messages from the server in some cases. Of
    # course, this means that the WebSocket must remain open. 
    messageObj = jsons.loads(messageStr)
    # This is the web sockets on open routine. In most cases, we
    # want to close the socket right here. However, in at least
    # two important cases, this is not true. We want to leave the
    # web socket open so that we can get and use the reply. 
    if 'HDLmRequestType' in messageObj: 
      messageRequestType = messageObj['HDLmRequestType']
      if messageRequestType.startswith('getImage') == False and \
         messageRequestType.startswith('getMod')   == False and \
         messageRequestType.startswith('getText')  == False:
        currentWebSocket.close() 
  # The next routine establishes a Web Sockets connection to another
  # process 
  @staticmethod
  def openWebSocketConnection(messageCallback):
    # print('In HDLmWebSockets.openWebSocketConnection', messageCallback) 
    # The port number is hardcoded below. The port number is actually
    # a configuration value. However, we can not use configuration
    # values here. 
    if 1 == 2:
      # These value are for the Electron JS application 
      newWebTargetPort = 8102
      newWebTargetScheme = 'ws'
      newWebTargetSite = '127.0.0.1' 
    elif 1 == 2:
      # These values are for the proxy server running locally under Eclipse 
      newWebTargetPort = 80
      newWebTargetScheme = 'ws'
      newWebTargetSite = '127.0.0.1' 
    else:
      # These values are for proxy server running in the cloud 
      newWebTargetPort = 443
      newWebTargetScheme = 'wss'
      newWebTargetSite = HDLmConfigInfo.getServerName()
    # Build the string used as the target for the new WebSocket connection   
    newWebTargetPathValue = 'HDLmWebSocketServer'
    newWebTarget = newWebTargetScheme + '://' + newWebTargetSite + ':' + \
      str(newWebTargetPort) + '/' + newWebTargetPathValue + '/'
    # Set the value of the routine that should be called for each inbound 
    # message
    if messageCallback == None:
      onMessage = HDLmWebSockets.onMessageWebSocketContent
    else:
      onMessage = messageCallback
    # Create and open the new WebSocket
    ws = websocket.WebSocketApp(newWebTarget,
                                on_message=onMessage,
                                on_open=HDLmWebSockets.onOpenWebSocketContent)
    ws.run_forever()
  # This method sends an add tree node request to the server. The add tree 
  # node request adds one tree node. 
  @staticmethod
  def sendAddTreeNodeRequest(treePos):
    # console.log('In HDLmWebSockets.sendAddTreeNodeRequest', treePos) 
    # Create a temporary copy of the current tree node. This is
    # done so that we can make changes to the temporary copy that
    # will not affect the original tree node. 
    tempPos = HDLmWebSockets.modifiedTreeNode(treePos)
    # Convert the temporary object into a string 
    tempPosStr = jsons.dumps(tempPos)
    # Open a connnection to another process 
    HDLmWebSockets.sendCurrentRequest(tempPosStr, 'addTreeNode') 
  # Send the current request to the server. The caller provides
  #  all of the information needed for the current request. This
  #  routine does the actual work. 
  @staticmethod
  def sendCurrentRequest(jsonStr, requestType):  
    # print('HDLmWebSockets.sendCurrentRequest', jsonStr, requestType)  
    # print(jsonStr) 
    # print(requestType) 
    # Open a connnection to another process 
    jsonStr = HDLmUtility.updateJsonStr(jsonStr, 'HDLmRequestType', requestType) 
    valueStrJson = False 
    jsonStr = HDLmUtility.updateJsonStr(jsonStr, 'HDLmCopyElements', valueStrJson)
    windowLocationHref = 'window.location.href'
    jsonStr = HDLmUtility.updateJsonStr(jsonStr, 'HDLmUrlValue',  windowLocationHref)
    # print(window)
    # print(window.location.href)
    # print(jsonStr)
    # print('In sendCurrentRequest', jsonStr)
    HDLmWebSockets.contentSendValue.insert(0, jsonStr)
    webSocketsMessageCallbackNone = None
    HDLmWebSockets.openWebSocketConnection(webSocketsMessageCallbackNone) 
  # This method sends an update tree node request to the server. The 
  # update tree node request updates one tree node.
  @staticmethod
  def sendUpdateTreeNodeRequest(treePos):
    # Create a temporary copy of the current tree node. This is
    # done so that we can make changes to the temporary copy that
    # will not affect the original tree node. 
    tempPos = HDLmWebSockets.modifiedTreeNode(treePos)
    # Convert the temporary object into a string 
    tempPosStr = jsons.dumps(tempPos)
    # Open a connnection to another process 
    HDLmWebSockets.sendCurrentRequest(tempPosStr, 'updateTreeNode')