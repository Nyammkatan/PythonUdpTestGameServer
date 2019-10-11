import time
from threading import Lock

class Client:

    ready = False
    lastMessageTime = 0
    
    def __init__(self, addr, handler):
        self.handler = handler
        self.addr = addr
        self.lastMessageTime = time.time()
        self.lock = Lock()

    def holdConnection(self):
        self.lastMessageTime = time.time()

    def checkConnection(self, seconds):
        if (time.time() - self.lastMessageTime > seconds):
            return False
        else:
            return True

    def send(self, data):
        with self.lock:
            self.handler.server.send(data, self.addr)