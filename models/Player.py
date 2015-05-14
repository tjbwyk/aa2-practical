__author__ = 'Tommy'


class Player(object):

    def __init__(self, x, y, x_max, y_max):
        self.x = x
        self.y = y
        self.x_max = x_max
        self.y_max = y_max

    def move(self, dxy):
        self.move(dxy[0], dxy[1])

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x += self.x_max
        if self.y < 0:
            self.y += self.y_max
        if self.x >= self.x_max:
            self.x -= self.x_max
        if self.y >= self.y_max:
            self.y -= self.y_max