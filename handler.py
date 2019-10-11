import server
import time
import threading
import rect
import random
import client
import math

def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

class Handler:

    working = True
    lastFrameTime = time.time()

    clientList = {}

    def __init__(self, host, port, serverDataAction, gameLogicAction):
        self.server = server.Server(host, port)
        self.readingThread = threading.Thread(target=self.reading)
        self.readingThread.setDaemon(True)
        self.serverDataAction = serverDataAction
        self.gameLogicAction = gameLogicAction
        self.clientLock = threading.Lock()

    def startReading(self):
        self.readingThread.start()

    def reading(self):
        while self.working:
            data, addr = self.server.listen()
            if (data == None):
                continue
            self.serverDataAction(data, addr)

    def startGameLogic(self):
        while self.working:
            currentTime = time.time()
            dt = currentTime - self.lastFrameTime
            self.lastFrameTime = currentTime
            self.gameLogicAction(dt)

    #client operations
    def addClient(self, addr):
        with self.clientLock:
            self.clientList[addr] = client.Client(addr)

    def removeClient(self, addr):
        with self.clientLock:
            del self.clientList[addr]

    def getClient(self, addr):
        with self.clientLock:
            return self.clientList[addr]

    def clientExists(self, addr):
        with self.clientLock:
            if addr in self.clientList:
                return True
        return False

    def sendTo(self, data, client):
        self.server.send(data, client.addr)

    def sentToAll(self, data):
        with self.clientLock:
            for client in self.clientList.values():
                self.sendTo(data, client)