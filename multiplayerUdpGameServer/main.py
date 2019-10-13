import server
import game_handler
import random
import rect

class Game(game_handler.GameHandler):

    timer = 0
    id_index = 0

    def newClientJoined(self, client):
        print("new client "+str(client.addr))

    def disconnectOfClient(self, client):
        print("disconnecting "+str(client.addr))

    def getSimplePacket(self, client, packet):
        client.ready = True

    def getImportantPacket(self, client, packet):
        client.ready = True

    def getFilterIdKeys(self, client, idListKeys):
        return idListKeys

    def update(self, dt):
        self.timer += dt
        if (self.timer > 0.2):
            self.initRects()
            self.timer = 0

        for i in list(self.allGameObjects.keys()):
            self.allGameObjects[i].update(dt)
            if self.allGameObjects[i].y > 1000:
                del self.allGameObjects[i]

    def initRects(self):
        for i in range(5):
            r = rect.Rect(random.randrange(0, 640), self.id_index)
            self.id_index += 1
            self.allGameObjects[self.id_index] = r

    def __init__(self):
        super().__init__(server.Server("", 9999, self))

print("new version")
game = Game()