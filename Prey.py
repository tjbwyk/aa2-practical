__author__ = 'kostas'
from Player import Player
from random import random
import numpy as np


class Prey(Player):

    def __init__(self, x, y, environment):
        Player.__init__(self, x, y, environment)

    def move(self):

        current_state = np.array([self.x, self.y])
        noise = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]])

        new_state = np.remainder(current_state + noise, [self.max_x, self.max_y])

        self.x = new_state[0]
        self.y = new_state[1]

