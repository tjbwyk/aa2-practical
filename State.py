__author__ = 'kostas'

import math
import numpy as np


class State(object):

    def __init__(self, env):
        self.environment = env

    def request(self):
        pass


class RelativeDistanceState(State):

    def __init__(self, environment):
        State.__init__(self, environment)
        self.dim = 2

    def request(self):

        diff_x = self.environment.players(0).x - self.environment.players(1).x
        diff_y = self.environment.players(0).y - self.environment.players(1).y

        return np.array([diff_x, diff_y])


class EuclideanDistanceState(State):

    def __init__(self, environment):
        State.__init__(self, environment)
        self.dim = 1

    def request(self):

        diff_x = (self.environment.players(0).x - self.environment.players(1).x)**2
        diff_y = (self.environment.players(0).y - self.environment.players(1).y)**2

        return np.array([math.sqrt(diff_x + diff_y)])
