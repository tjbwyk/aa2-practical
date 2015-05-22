from math import pi, sin, cos, sqrt
from random import random
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import copy
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model

__author__ = 'Tommy'


class SamplingBasedFittedValueIteration(object):
    """The Sampling-based Fitted Value Iteration algorithm, approximating the value function of the states.
    """

    def __init__(self, env_init, state_init, n_states=100, n_actions=10, n_targets=10, thres=0.1, gamma=0.9):

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
        self.theta = np.zeros(self.env_init.state.dim)

    def fit(self):
        # randomly sample m states
        sample_states = self.env_init.generate(self.n_states)
        # initializing y
        y = np.zeros(self.n_states)
        prev_v = np.zeros(self.n_states)

        prev_theta = 0

        while not self.converged:
            for i in range(self.n_states):
                state_current = sample_states[i]

                for j in range(self.n_actions):

                    if self.env_init.state.dim == 2:
                        action = rand_circle(radius=1.5)
                    elif self.env_init.state.dim == 1:
                        action = (random() * 3) - 1.5

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
            print self.theta
            if np.abs(self.theta - prev_theta) < self.thres:
                self.converged = True
            prev_theta = self.theta

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
            state_next = state + action % sqrt(((self.env_init.width/2.0)**2 + (self.env_init.height/2.0)**2))
        return state_next

    def draw_value_func(self):
        x = np.arange(-5, 5, 0.1)
        y = np.arange(-5, 5, 0.1)
        X, Y = np.meshgrid(x, y)
        if self.env_init.state.dim == 2:
            Z = [[self.get_value([X[j, i], Y[j, i]]) for i in range(x.size)] for j in range(y.size)]
        else:
            Z = [[self.get_value(np.linalg.norm([X[j, i], Y[j, i]]))[0] for i in range(x.size)] for j in range(y.size)]

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('Oranges'), linewidth=0, vmin=-1, vmax=1)
        ax.set_zlim(-1, 1)
        plt.show()


def rand_circle(radius=1):
    t = 2 * pi * random()
    u = random() + random()
    r = 2 - u if u > 1 else u
    return [radius * r * cos(t), radius * r * sin(t)]
