import server
import time
import rect
import random
import handler
import json

class Helper:

    timer = 0
    timerStateUpdate = 0
    list1 = []

    def serverDataAction(self, data, addr):
        if (not self.handler.clientExists(addr)):
            self.handler.addClient(addr)
        client = self.handler.getClient(addr)
        client.ready = True
        client.holdConnection()

    def gameLogicAction(self, dt):
        #rects creating
        self.timer += dt
        if (self.timer > 5):
            self.initRects()
            self.timer = 0

        #sending states
        self.timerStateUpdate += dt
        if (self.timerStateUpdate > 0.1):
            self.timerStateUpdate -= 0.1
            self.sendStates()

        #game logic rects
        for i in self.list1:
            i.update(dt)
            if i.y > 450:
                self.list1.remove(i)

        #game logic clients time
        with self.handler.clientLock:
            for a in list(self.handler.clientList.keys()):
                c = self.handler.clientList[a]
                if (not c.checkConnection(1)):
                    del self.handler.clientList[a]
                    print("removing client "+str(a))

    def sendStates(self):
        num = 0
        for i in self.list1:
            num += 1
            state = i.getState()
            self.handler.sentToAll(json.dumps(state))

    def initRects(self):
        for i in range(20):
            r = rect.Rect(random.randrange(0, 640), i)
            self.list1.append(r)

    def __init__(self):
        self.handler = handler.Handler("", 9999, self.serverDataAction, self.gameLogicAction)
        self.handler.startReading()
        self.handler.startGameLogic()
        pass

helper = Helper()