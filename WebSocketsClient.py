import _thread as thread
import time
import websocket 

def onMessage(ws, message):
  print('In onMessage')
  print('Message is ' + message)

def onError(ws, error):
  print('In onError')
  print(error)

def onClose(ws):
  print('In onClose')

def onOpen(ws):
  print('In onOpen')
  def run(*args):
    for i in range(3):
        time.sleep(1)
        ws.send("Hello %d" % i) 
    time.sleep(1)
    ws.close()
    print("Thread terminating...")
  thread.start_new_thread(run, ())


if __name__ == "__main__":
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("wss://owo.dnsalias.com/api/socket/",
                              on_message = onMessage,
                              on_error = onError,
                              on_close = onClose)
  ws.on_open = onOpen
  ws.run_forever()