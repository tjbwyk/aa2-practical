from models import Predator

__author__ = 'Tommy'

import math.sqrt
import numpy as np


class State(object):

    def __init__(self, predator=None, prey=None):
        self.predator = predator.copy()
        self.prey = prey.copy()
        self.dim = 0

    def update(self, a_predator, a_prey):
        self.predator.move(a_predator)
        self.prey.move(a_prey)


class RelativePositionState(State):

    def __init__(self, predator=None, prey=None):
        super(self, predator, prey)
        self.dim = 3

    def phi(self):
        diff_x = self.prey.x - self.predator.x
        diff_y = self.prey.y - self.predator.y
        return np.array([1, diff_x, diff_y])

    def sampling(self):
        sample_predator = self.sampling()
        sample_prey = self.sampling()
        return RelativePositionState(sample_predator, sample_prey)

    def copy(self):
        return RelativePositionState(self.predator, self.prey)


class EuclideanDistanceState(State):

    def __init__(self, sample_predator, sample_prey):
        super(self, sample_predator, sample_prey)
        self.dim = 2

    def phi(self):
        diff_x = self.prey.x - self.predator.x
        diff_y = self.prey.y - self.predator.y
        return np.array([1, np.linalg.norm([diff_x, diff_y])])

    def sampling(self):
        sample_predator = self.sampling()
        sample_prey = self.sampling()
        return EuclideanDistanceState(sample_predator, sample_prey)

    def copy(self):
        return RelativePositionState(self.predator, self.prey)