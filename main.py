import server
import time
import rect
import random
import handler
import json

class Helper:

    timer = 0
    timerStateUpdate = 0
    list1 = {}

    def serverDataAction(self, data, addr):
        if (not self.handler.clientExists(addr)):
            self.handler.addClient(addr)
        client = self.handler.getClient(addr)
        client.ready = True
        client.holdConnection()

    def gameLogicAction(self, dt):
        #rects creating
        self.timer += dt
        if (self.timer > 2):
            self.initRects()
            self.timer = 0

        #sending id
        #sending states
        self.timerStateUpdate += dt
        if (self.timerStateUpdate > 0.2):
            self.timerStateUpdate -= 0.2
            self.sendId()
            self.sendState()

        #game logic rects
        for i in list(self.list1.keys()):
            self.list1[i].update(dt)
            if self.list1[i].y > 480:
                del self.list1[i]

        #game logic clients time
        with self.handler.clientLock:
            for a in list(self.handler.clientList.keys()):
                c = self.handler.clientList[a]
                if (not c.checkConnection(1)):
                    del self.handler.clientList[a]
                    print("removing client "+str(a))

    def sendId(self):
        packet = {"p_id":0}
        idli = list(self.list1.keys())
        packet["id"] = idli
        data = json.dumps(packet)
        self.handler.sentToAll(data)

    def sendState(self):
        for i in self.list1.values():
            state = i.getState()
            state["p_id"] = 1
            self.handler.sentToAll(json.dumps(state))

    id_index = 0
    def initRects(self):
        for i in range(10):
            r = rect.Rect(random.randrange(0, 640), self.id_index)
            self.id_index += 1
            self.list1[self.id_index] = r

    def __init__(self):
        self.handler = handler.Handler("", 9999, self.serverDataAction, self.gameLogicAction)
        self.handler.startReading()
        self.handler.startGameLogic()
        pass

helper = Helper()