import socket
import client_one_thread as client
import time
import json

class Server:

    clientList = {}
    maxPacketNumberRange = 1000
    disconnectTime = 2

    def __init__(self, host, port, worker, maxPacketNumberRange):
        self.maxPacketNumberRange = maxPacketNumberRange
        self.worker = worker
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.bufferSize = 1024

    def setBufferSize(self, bufferSize):
        self.bufferSize = bufferSize

    def listen(self):
        try:
            data, addr = self.sock.recvfrom(self.bufferSize)
            return data.decode("ascii"), addr
        except:
            return None, None

    def send(self, data, addr):
        self.sock.sendto(data.encode("ascii"), addr)

    def addClient(self, addr):
        c = client.Client(addr, self)
        self.clientList[addr] = c
        return c

    def removeClient(self, addr):
        del self.clientList[addr]

    def getClientList(self):
        return self.clientList

    def reading(self):
        data, addr = self.listen()
        if (data != None):
            try:
                c = None
                if (not addr in self.getClientList()):
                    c = self.addClient(addr)
                    self.worker.newClientJoined(c)
                else:
                    c = self.getClientList()[addr]
                packet = json.loads(data)
                self.receivingMessageFromClient(c, packet)
            except:
                pass

    def checkPacketNumber(self, numberReceived, client):
        if ( (numberReceived > client.lastPacketNumber) or ( (numberReceived < (self.maxPacketNumberRange/2)) and (client.lastPacketNumber > (self.maxPacketNumberRange/2)) ) ):
            client.lastPacketNumber = numberReceived
            return True
        return False

    def checkIPacketNumber(self, numberReceived, client):
        if ( (numberReceived > client.lastIPacketNumber) or ( (numberReceived < (self.maxPacketNumberRange/2)) and (client.lastIPacketNumber > (self.maxPacketNumberRange/2)) ) ):
            client.lastIPacketNumber = numberReceived
            return True
        return False

    def getSimplePacket(self, client, packet):
        self.worker.getSimplePacket(client, packet)

    def getImportantPacket(self, client, packet):
        self.worker.getImportantPacket(client, packet)

    def receivingMessageFromClient(self, client, packet):
        client.holdConnection()
        if (packet["im"] == 0): #not important packet
            if (self.checkPacketNumber(packet["num"], client)):
                self.getSimplePacket(client, packet)
        elif (packet["im"] == 1): #important packet
            if (self.checkIPacketNumber(packet["num"], client)):
                self.getImportantPacket(client, packet)
            client.send({"im":2, "num":packet["num"]})
        elif (packet["im"] == 2): #response
            client.removeFirstIMessage()

    def removeDisconnectedClients(self):
        for key in list(self.getClientList().keys()):
            client = self.clientList[key]
            if (not client.checkConnection(self.disconnectTime)):
                self.removeClient(key)
                self.worker.disconnectOfClient(client)

    def writing(self):
        self.removeDisconnectedClients()
        for key in self.getClientList().keys():
            client = self.clientList[key]
            if (client.iMessagesExist()):
                iMessage = client.getFirstIMessage()
                client.send(iMessage)