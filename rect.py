import random
import handler

class Rect:

    id = -1
    x = 0.0
    y = 0.0
    a = 0.0
    vy = 100

    state = {
        'id':id,
        'x':0,
        'y':0,
        'a':0

    }

    def __init__(self, x, id):
        self.x = x
        self.a = random.randrange(0, 360)
        self.id = id
        self.state["id"] = id

    def update(self, dt):
        self.y+=self.vy*dt
        self.a+=20*dt
        if (self.a >= 360):
            self.a -= 360

    def getState(self):
        self.state["x"] = handler.truncate(self.x, 2)
        self.state["y"] = handler.truncate(self.y, 2)
        self.state["a"] = handler.truncate(self.a, 2)
        return self.state


    