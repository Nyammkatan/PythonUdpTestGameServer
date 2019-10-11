import time

class Client:

    ready = False
    lastMessageTime = 0
    
    def __init__(self, addr):
        self.addr = addr
        self.lastMessageTime = time.time()

    def holdConnection(self):
        self.lastMessageTime = time.time()

    def checkConnection(self, seconds):
        if (time.time() - self.lastMessageTime > seconds):
            return False
        else:
            return True