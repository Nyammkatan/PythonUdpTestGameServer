import server
import time
import threading
import rect
import random
import handler
import json

class Helper:

    timer = 0
    timerStateUpdate = 0
    list1 = []

    def serverDataAction(self, data, addr):
        self.handler.getClient(addr).ready = True
        print(data)

    def gameLogicAction(self, dt):
        self.timer += dt
        if (self.timer > 5):
            self.initRects()
            self.timer = 0
        self.timerStateUpdate += dt
        if (self.timerStateUpdate > 0.1):
            self.timerStateUpdate -= 0.1
            self.sendStates()
        for i in self.list1:
            i.update(dt)
            if i.y > 450:
                self.list1.remove(i)

    def sendStates(self):
        num = 0
        for i in self.list1:
            num += 1
            state = i.getState()
            self.handler.sentToAll(json.dumps(state))
        print(str(num)+" states")

    def initRects(self):
        print("creating rects")
        for i in range(20):
            r = rect.Rect(random.randrange(0, 640), i)
            self.list1.append(r)

    def __init__(self):
        self.handler = handler.Handler("", 9999, self.serverDataAction, self.gameLogicAction)
        self.handler.startReading()
        self.handler.startGameLogic()
        pass

helper = Helper()