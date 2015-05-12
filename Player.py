__author__ = 'kostas'


class Player(object):

    def __init__(self, x, y, environment):

        self.x = x
        self.y = y
        environment.add_player(self)
        self.max_x = environment.width
        self.max_y = environment.length

    def move(self, x_offset, y_offset):

        self.x = (self.x + x_offset) % self.max_x
        self.y = (self.y + y_offset) % self.max_y