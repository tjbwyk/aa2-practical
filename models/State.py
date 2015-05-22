from copy import copy
import numpy as np
from models.Field import rand_circle


class State(object):

    def __init__(self, env, pred, prey):
        self.env = env
        self.pred = copy(pred)
        self.prey = copy(prey)
        self.dim = 0

    def get_rel_abs_pos(self):
        diff_x = np.abs(self.prey.x - self.pred.x)
        diff_y = np.abs(self.prey.y - self.pred.y)
        diff_x = diff_x if diff_x < self.env.width - diff_x else self.env.width - diff_x
        diff_y = diff_y if diff_y < self.env.height - diff_y else self.env.height - diff_y
        return diff_x, diff_y

    def get_distance(self):
        diff_x, diff_y = self.get_rel_abs_pos()
        return np.linalg.norm([diff_x, diff_y])

    def is_over(self):
        return self.get_distance() < 1

    def get_actions(self):
        a_pred = [0, 0]
        maxV = -2147483648
        for i in range(100):
            state_sample = self.copy()
            a_pred_sample = rand_circle(1.5)
            state_sample.update(a_pred_sample, [0, 0])
            V = self.env.planner.get_value(state_sample)
            if V > maxV:
                maxV = V
                a_pred = a_pred_sample

        a_prey = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]])
        return a_pred, a_prey

    def update(self, a_pred, a_prey):
        self.pred.move(a_pred)
        self.prey.move(a_prey)

class Distance2DState(State):

    def __init__(self, env, pred, prey):
        super(self.__class__, self).__init__(env, pred, prey)
        self.dim = 3

    def phi(self):
        diff_x, diff_y = self.get_rel_abs_pos()
        return np.array([1, diff_x, diff_y])

    def sampling(self):
        sample_pred = self.pred.sampling()
        sample_prey = self.prey.sampling()
        return Distance2DState(self.env, sample_pred, sample_prey)

    def copy(self):
        return Distance2DState(self.env, self.pred, self.prey)

class DistanceState(State):

    def __init__(self, env, pred, prey):
        super(self.__class__, self).__init__(env, pred, prey)
        self.dim = 2

    def phi(self):
        diff_x, diff_y = self.get_rel_abs_pos()
        return np.array([1, np.linalg.norm([diff_x, diff_y])])

    def sampling(self):
        sample_pred = self.pred.sampling()
        sample_prey = self.prey.sampling()
        return DistanceState(self.env, sample_pred, sample_prey)

    def copy(self):
        return DistanceState(self.env, self.pred, self.prey)