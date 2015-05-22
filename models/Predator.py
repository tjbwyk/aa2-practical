from numpy.random import random
from models.Player import Player

class Predator(Player):

    def __init__(self, env, x, y):
        super(self.__class__, self).__init__(env, x, y)

    def sampling(self):
        sample_x = random() * self.env.width
        sample_y = random() * self.env.height
        return Predator(self.env, sample_x, sample_y)