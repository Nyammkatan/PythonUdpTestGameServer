import server
import time
import rect
import random
import handler
import json

class Helper:
    
    timerStateUpdate = 0
    stateUpdateTimeInterval = 0.1
    clientCheckConnectionTime = 1
    allGameObjects = {}

    def readFromClient(self, data, client):
        pass

    def disconnectOfClient(self, client):
        pass

    def serverDataAction(self, data, addr):
        if (not self.handler.clientExists(addr)):
            self.handler.addClient(addr)
        client = self.handler.getClient(addr)
        self.readFromClient(data, client)
        client.holdConnection()

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

    def createPacket(self, important, p_id):
        packet = {}
        packet["im"] = 1 if important else 0
        packet["p_id"] = p_id
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
        self.handler.startReading()
        self.handler.startGameLogic()
        pass