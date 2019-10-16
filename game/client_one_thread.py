import time
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

    def addNewIMessage(self, packet):
        self.iMessages.append(packet)

    def getFirstIMessage(self):
        return self.iMessages[0]

    def removeFirstIMessage(self):
        del self.iMessages[0]

    def iMessagesExist(self):
        return len(self.iMessages) > 0

    def holdConnection(self):
        self.lastMessageTime = time.time()

    def checkConnection(self, seconds):
        if ((time.time() - self.lastMessageTime) > seconds):
            return False
        else:
            return True

    def send(self, packet):
        self.server.send(json.dumps(packet), self.addr)