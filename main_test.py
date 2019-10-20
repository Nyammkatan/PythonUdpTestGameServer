import game.server_one_thread as server
import game.game_handler_one_thread as game_handler
import random
import rect

class Game(game_handler.GameHandler):

    timer = 0
    id_index = 0

    def newClientJoined(self, client):
        print("new client "+str(client.addr))
        packet = self.cr
        eateIPacket(client, 0)
        packet["data"] = "greeting packet"
        client.addNewIMessage(packet)

    def disconnectOfClient(self, client):
        print("disconnecting "+str(client.addr))

    def getSimplePacket(self, client, packet):
        client.ready = True

    def getImportantPacket(self, client, packet):
        client.ready = True
        print("Client: "+packet["data"])

    def objectInTheCenter(self, o):
        if (abs(o.x-320) < 1000):
            if (abs(o.y-240) < 1000):
                return True
        return False

    def getFilterIdKeys(self, client, idListKeys):
        return list(filter(lambda x: self.objectInTheCenter(self.allGameObjects[x]), idListKeys))

    def update(self, dt):
        self.timer += dt
        if (self.timer > 0.1):
            self.initRects()
            self.timer = 0

        for i in list(self.allGameObjects.keys()):
            self.allGameObjects[i].update(dt)
            if self.allGameObjects[i].y > 1200:
                del self.allGameObjects[i]

    def initRects(self):
        for i in range(10):
            r = rect.Rect(random.randrange(0, 1920), self.id_index)
            self.id_index += 1
            self.allGameObjects[self.id_index] = r

    def __init__(self):
        super().__init__(server.Server("", 9999, self, 1000))

game = Game()