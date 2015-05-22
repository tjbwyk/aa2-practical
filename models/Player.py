class Player(object):

    def __init__(self, env, x, y):
        self.env = env
        self.x = x
        self.y = y

    def move(self, d0, d1=None):
        if d1:
            dx = d0
            dy = d1
        else:
            dx = d0[0]
            dy = d0[1]

        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x += self.env.width
        if self.y < 0:
            self.y += self.env.height
        if self.x >= self.env.width:
            self.x -= self.env.width
        if self.y >= self.env.height:
            self.y -= self.env.height

