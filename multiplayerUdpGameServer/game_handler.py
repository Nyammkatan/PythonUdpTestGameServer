import math
import time
import json

class GameHandler:

    lastFrameTime = time.time()
    timerStateUpdate = 0
    allGameObjects = {}
    stateUpdateTimeInterval = 0.1

    def __init__(self, server):
        self.server = server
        self.startGameLogic()

    def startGameLogic(self):
        while self.server.working:
            currentTime = time.time()
            dt = currentTime - self.lastFrameTime
            self.lastFrameTime = currentTime
            
            self.updateStates(dt)
            self.update(dt)

    def updateStates(self, dt):
        self.timerStateUpdate += dt
        if (self.timerStateUpdate > self.stateUpdateTimeInterval):
            self.timerStateUpdate -= self.stateUpdateTimeInterval
            self.sendIdAndState()

    def update(self, dt):
        pass

    def getFilterIdKeys(self, client, idListKeys):
        return idListKeys

    def sendIdAndState(self):
        for client in list(self.server.getClientList().values()):
            if (client.ready):
                idListKeys = self.getFilterIdKeys(client, list(self.allGameObjects.keys()))
                packet = self.createPacket(client, False, 0)
                packet["id"] = idListKeys
                client.send(packet)
                for i in idListKeys:
                    packet = self.createPacket(client, False, 1)
                    packet = self.allGameObjects[i].getState(packet)
                    client.send(packet)

    def getCounter(self, client, important):
        value = 0
        if (not important):
            value = client.ni_packet_number_counter
            client.ni_packet_number_counter+=1
            if (client.ni_packet_number_counter >= self.server.maxPacketNumberRange):
                client.ni_packet_number_counter = 0
        else:
            value = client.i_packet_number_counter
            client.i_packet_number_counter+=1
            if (client.i_packet_number_counter >= self.server.maxPacketNumberRange):
                client.i_packet_number_counter = 0
        return value

    def createPacket(self, client, important, p_id):
        packet = {}
        packet["im"] = 1 if important else 0
        packet["p_id"] = p_id
        with client.counterLock:
            packet["num"] = self.getCounter(client, important)
        return packet