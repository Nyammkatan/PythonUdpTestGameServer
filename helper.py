import server
import time
import rect
import random
import handler
import json
from threading import Lock

class Helper:
    
    timerStateUpdate = 0
    allGameObjects = {}
    
    stateUpdateTimeInterval = 0.1
    clientCheckConnectionTime = 1

    def readFromClient(self, packet, client):
        pass

    def readImportantFromClient(self, packet, client):
        pass

    def readResponseFromClient(self, packet, client):
        pass

    def disconnectOfClient(self, client):
        pass

    def serverDataAction(self, data, addr):
        if (not self.handler.clientExists(addr)):
            self.handler.addClient(addr)
        client = self.handler.getClient(addr)
        try:
            packet = json.loads(data)
            if (packet["im"] == 0):
                self.readFromClient(packet, client)
            elif (packet["im"] == 1):
                self.readImportantFromClient(packet, client)
            elif (packet["im"] == 2):
                self.readResponseFromClient(packet, client)
            client.holdConnection()
        except:
            pass

    def gameLogicAction(self, dt):
        self.timerStateUpdate += dt
        if (self.timerStateUpdate > self.stateUpdateTimeInterval):
            self.timerStateUpdate -= self.stateUpdateTimeInterval
            self.sendIdAndState()

        #game logic clients time
        with self.handler.clientLock:
            for a in list(self.handler.clientList.keys()):
                c = self.handler.clientList[a]
                if (not c.checkConnection(self.clientCheckConnectionTime)):
                    client = self.handler.clientList[a]
                    del self.handler.clientList[a]
                    self.disconnectOfClient(client)
                    break

        self.update(dt)

    def update(self, dt):
        pass

    def getFilterIdKeys(self, client, idListKeys):
        return idListKeys

    ni_packet_number_counter = 0
    i_packet_number_counter = 0

    def getCounter(self, important):
        value = 0
        if (not important):
            value = self.ni_packet_number_counter
            self.ni_packet_number_counter+=1
            if (self.ni_packet_number_counter >= 1000):
                self.ni_packet_number_counter = 0
        else:
            value = self.i_packet_number_counter
            self.i_packet_number_counter+=1
            if (self.i_packet_number_counter >= 1000):
                self.i_packet_number_counter = 0
        return value

    def createPacket(self, important, p_id):
        packet = {}
        packet["im"] = 1 if important else 0
        packet["p_id"] = p_id
        with self.counterLock:
            packet["num"] = self.getCounter(important)
        return packet

    def sendIdAndState(self):
        with self.handler.clientLock:
            for client in self.handler.clientList.values():
                if (client.ready):
                    idListKeys = self.getFilterIdKeys(client, list(self.allGameObjects.keys()))
                    packet = self.createPacket(False, 0)
                    packet["id"] = idListKeys
                    data = json.dumps(packet)
                    client.send(data)
                    for i in idListKeys:
                        packet = self.createPacket(False, 1)
                        packet = self.allGameObjects[i].getState(packet)
                        client.send(json.dumps(packet))

    def __init__(self):
        self.handler = handler.Handler("", 9999, self.serverDataAction, self.gameLogicAction)
        self.counterLock = Lock()
        self.handler.startReading()
        self.handler.startGameLogic()
        pass