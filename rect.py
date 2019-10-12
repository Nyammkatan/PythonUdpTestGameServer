import random
import handler

class Rect:

    id = -1
    x = 0.0
    y = -400
    a = 0.0
    vy = 250

    def __init__(self, x, id):
        self.x = x
        self.a = random.randrange(0, 360)
        self.id = id

    def update(self, dt):
        self.y+=self.vy*dt
        self.a+=200*dt
        
    def getState(self, packet):
        packet["x"] = handler.truncate(self.x, 2)
        packet["y"] = handler.truncate(self.y, 2)
        packet["a"] = handler.truncate(self.a, 2)
        packet["id"] = self.id
        return packet


    