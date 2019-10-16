import time
from threading import Lock
import json

class Client:

    ready = False
    iMessages = []

    lastPacketNumber = -1
    lastIPacketNumber = -1

    ni_packet_number_counter = 0
    i_packet_number_counter = 0
    
    def __init__(self, addr, server):
        self.addr = addr
        self.server = server
        self.lastMessageTime = time.time()
        self.sendingLock = Lock()
        self.iMessagesLock = Lock()
        self.counterLock = Lock()

    def addNewIMessage(self, packet):
        with self.iMessagesLock:
            self.iMessages.append(packet)

    def getFirstIMessage(self):
        with self.iMessagesLock:
            return self.iMessages[0]

    def removeFirstIMessage(self):
        with self.iMessagesLock:
            del self.iMessages[0]

    def iMessagesExist(self):
        with self.iMessagesLock:
            return len(self.iMessages) > 0

    def holdConnection(self):
        self.lastMessageTime = time.time()

    def checkConnection(self, seconds):
        if ((time.time() - self.lastMessageTime) > seconds):
            return False
        else:
            return True

    def send(self, packet):
        with self.sendingLock:
            self.server.send(json.dumps(packet), self.addr)