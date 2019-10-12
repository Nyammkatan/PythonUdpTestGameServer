import random
import handler

class Rect:

    id = -1
    x = 0.0
    y = -400
    a = 0.0
    vy = 250

    state = {
        'id':-1,
        'x':0,
        'y':0,
        'a':0

    }

    def __init__(self, x, id):
        self.x = x
        self.a = random.randrange(0, 360)
        self.id = id

    def update(self, dt):
        self.y+=self.vy*dt
        self.a+=200*dt
        #if (self.a >= 360):
        #    self.a -= 360

    def getState(self):
        self.state["x"] = handler.truncate(self.x, 2)
        self.state["y"] = handler.truncate(self.y, 2)
        self.state["a"] = handler.truncate(self.a, 2)
        self.state["id"] = self.id
        return self.state


    