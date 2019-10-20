import game.server_one_thread as server
import game.game_handler_one_thread as game_handler
import random
import utils.worldModule as worldModule
import json
import os

world = None

class Game(game_handler.GameHandler):

    id_index = 0

    def newClientJoined(self, client):
        print("new client "+str(client.addr))

    def disconnectOfClient(self, client):
        print("disconnecting "+str(client.addr))

    def getSimplePacket(self, client, packet):
        client.ready = True
        if (packet["p_id"] == -1):
            chunkx = packet["x"]/60
            chunky = packet["y"]/60
            mapPacket = self.createSimplePacket(client, 5) #5 - map chunk
            mapPacket["i"] = chunky
            mapPacket["j"] = chunkx
            mapPacket["array"] = []
            for i in range(5):
                mapPacket["array"].append([])
                for j in range(5):
                    mapPacket["array"][i][j] = world.array[0][0]
            client.send(mapPacket)

    def getImportantPacket(self, client, packet):
        client.ready = True

    def getFilterIdKeys(self, client, idListKeys):
        return idListKeys

    def update(self, dt):
        pass

    def stateAction(self):
        pass

    def __init__(self, world):
        super().__init__(server.Server("", 9999, self, 1000))

def getWorld(worldName, isNew):
    if (isNew):
        print("Creating world")
        name = worldName
        seed = None
        world = worldModule.WorldClass(name, seed, None)
        save(world)
        return world
    else:
        print("Opening world")
        with open("worlds/"+worldName+".world", "r") as content_file:
            content = content_file.read()
        worldDict = json.loads(content)
        seed = None
        world = worldModule.WorldClass(worldName, seed, worldDict["array"])
        return world

def save(world):
    worldDict = {}
    worldDict["name"] = world.name
    worldDict["array"] = world.array
    worldStr = json.dumps(worldDict)
    if not os.path.exists("worlds"):
        os.makedirs("worlds")
    f = open("worlds/"+world.name+".world","w+")
    f.write(worldStr)
    f.close()
    print("World saved")

world = getWorld("TestWorld", False)
print("World initalized")
print("Starting game server")
game = Game(world)