from sklearn.linear_model import LinearRegression
from math import pi, sin, cos
from random import random
import numpy as np
import copy

__author__ = 'Tommy'

class SamplingBasedFittedValueIteration(object):
    """The Sampling-based Fitted Value Iteration algorithm, approximating the value function of the states.
    """

    def __init__(self, env_init, state_init, n_states=1000, n_actions=10, n_targets=100):
        """
        :param env_init: initial environment
        :param state_init: initial state
        :param n_states: number of sample states
        :param n_actions: number of sample actions for each sample state
        :param n_targets: number of sample target state for each action
        :return:
        """
        self.env_init = copy.deepcopy(env_init)
        self.state_init = copy.deepcopy(state_init)
        self.n_states = n_states
        self.n_actions = n_actions
        self.n_targets = n_targets

        # initialize theta = 0
        self.theta = np.zeros(self.state_init.dim)

    def fit(self):
        # randomly sample m states
        sample_states = [self.state_init.sampling() for i in range(self.n_states)]

        y = []
        x = []
        for i in range(self.n_states):
            state_current = sample_states[i]
            for j in range(self.n_actions):
                action = rand_circle(radius=1.5)
                q = 0
                y.append(0)
                for k in range(self.n_targets):
                    state_next = state_current.copy()
                    state_next.update(action, np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]]))
                    q += self.env.get_reward(state_current) + self.env.gamma * self.get_value(state_next)
                q /= k
                y[i] = q if q > y[i] else y[i]
                x.append(state_current.phi())
        self.theta = np.linalg.lstsq(x, y)[0]

    def get_value(self, state):
        return np.dot(self.theta, state.phi())

    def get_actions(self, state):
        pass


def rand_circle(radius=1):
    t = 2 * pi * random()
    u = random() + random()
    r = 2 - u if u > 1 else u
    return [radius * r * cos(t), radius * r * sin(t)]

