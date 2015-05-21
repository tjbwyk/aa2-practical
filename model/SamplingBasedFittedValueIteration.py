from math import pi, sin, cos, sqrt
from random import random
import numpy as np
import copy
from sklearn import linear_model

__author__ = 'Tommy'


class SamplingBasedFittedValueIteration(object):
    """The Sampling-based Fitted Value Iteration algorithm, approximating the value function of the states.
    """

    def __init__(self, env_init, state_init, n_states=100, n_actions=10, n_targets=5, thres=0.1, gamma=0.9):
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
        self.thres = thres
        self.gamma = gamma
        self.converged = False
        # initialize theta = 0
        self.theta = np.zeros(len(self.state_init))

    def fit(self):
        # randomly sample m states
        sample_states = self.env_init.generate(self.n_states)
        # initializing y
        y = np.zeros(self.n_states)
        prev_v = np.zeros(self.n_states)

        while not self.converged:
            for i in range(self.n_states):
                state_current = sample_states[i]

                for j in range(self.n_actions):

                    action = rand_circle(radius=1.5)
                    q = 0

                    # y.append(0)

                    for k in range(self.n_targets):
                        noise = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]])
                        state_next = self.bellman(state_current, action, noise)
                        q += self.env_init.get_reward(state_current) + self.gamma * self.get_value(state_next)
                    q /= self.n_targets
                    y[i] = q if q > y[i] else y[i]

            # TODO: implement the linear regression here

            self.theta = np.array(np.linalg.lstsq(sample_states, y)[0])
            v = np.dot(sample_states, self.theta)
            if np.max(v - prev_v) < self.thres:
                self.converged = True
            prev_v = np.array(v)

        # self.theta = lm.get_params()
        # self.theta <- linear regression

    def get_value(self, state):
        return np.dot(self.theta, state)

    def get_actions(self, state):
        pass

    def bellman(self, state, action, noise):

        if len(state) == 2:
            state_next = np.remainder(state + action - noise, [self.env_init.width, self.env_init.height])
        else:
            pred_x = (self.env_init.predators[0].x + action[0]) % self.env_init.width
            pred_y = (self.env_init.predators[0].y + action[1]) % self.env_init.height
            prey_x = (self.env_init.prey.x + noise[0]) % self.env_init.width
            prey_y = (self.env_init.prey.y + noise[1]) % self.env_init.height
            state_next = sqrt((pred_x - prey_x)**2 + (pred_y - prey_y)**2)
        return state_next



def rand_circle(radius=1):
    t = 2 * pi * random()
    u = random() + random()
    r = 2 - u if u > 1 else u
    return [radius * r * cos(t), radius * r * sin(t)]

