import game.server_one_thread as server
import game.game_handler_one_thread as game_handler
import random
import utils.worldModule as worldModule

class Game(game_handler.GameHandler):

    id_index = 0

    def newClientJoined(self, client):
        print("new client "+str(client.addr))

    def disconnectOfClient(self, client):
        print("disconnecting "+str(client.addr))

    def getSimplePacket(self, client, packet):
        client.ready = True

    def getImportantPacket(self, client, packet):
        client.ready = True

    def objectInTheCenter(self, o):
        if (abs(o.x-320) < 1000):
            if (abs(o.y-240) < 1000):
                return True
        return False

    def getFilterIdKeys(self, client, idListKeys):
        return list(filter(lambda x: self.objectInTheCenter(self.allGameObjects[x]), idListKeys))

    def update(self, dt):
        pass

    def __init__(self):
        super().__init__(server.Server("", 9999, self, 1000))

def getWorld(worldName):
    print("Starting game server")
    if (worldName is None):
        print("Creating world")
        world = worldModule.WorldClass(None)
        return world
    else:
        pass

print("Server starting")
game = Game()