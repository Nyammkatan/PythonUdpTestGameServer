import helper
import rect
import random

class Game(helper.Helper):

    timer = 0

    def readFromClient(self, data, client):
        client.ready = True

    def disconnectOfClient(self, client):
        print(str(client.addr)+" disconnected")

    def getFilterIdKeys(self, client, idListKeys):
        return idListKeys

    def update(self, dt):
        self.timer += dt
        if (self.timer > 0.25):
            self.initRects()
            self.timer = 0

        for i in list(self.allGameObjects.keys()):
            self.allGameObjects[i].update(dt)
            if self.allGameObjects[i].y > 800:
                del self.allGameObjects[i]

    id_index = 0
    def initRects(self):
        for i in range(5):
            r = rect.Rect(random.randrange(0, 640), self.id_index)
            self.id_index += 1
            self.allGameObjects[self.id_index] = r

game = Game()