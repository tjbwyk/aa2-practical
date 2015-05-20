__author__ = 'kostas'


class Player(object):

    def __init__(self, x, y, environment):

        self.x = x
        self.y = y
        environment.add_player(self)
        self.max_x = environment.width
        self.max_y = environment.length