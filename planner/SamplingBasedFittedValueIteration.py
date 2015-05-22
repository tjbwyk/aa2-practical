from math import pi, sin, cos
from random import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time
from models.Predator import Predator


class SamplingBasedFittedValueIteration(object):
    """The Sampling-based Fitted Value Iteration algorithm, approximating the value function of the states.
    """

    def __init__(self, env, gamma=0.9, n_states=100, n_actions=10, n_targets=10, threshold=1e-1):
        """
        :param env: initial environment
        :param n_states: number of sample states
        :param n_actions: number of sample actions for each sample state
        :param n_targets: number of sample target state for each action
        :return:
        """
        self.env = env
        self.gamma = gamma
        self.n_states = n_states
        self.n_actions = n_actions
        self.n_targets = n_targets
        self.threshold = threshold

        # initialize theta = 0
        self.theta = np.zeros(self.env.state.dim)

    def fit(self):
        timer = time.clock()
        # randomly sample m states
        sample_states = [self.env.state.sampling() for i in range(self.n_states)]

        y = np.zeros(self.n_states)
        x = np.zeros((self.n_states, self.env.state.dim))
        converged = False
        t = 0
        while not converged:
            for i in range(self.n_states):
                state_current = sample_states[i]
                if self.env.is_over(state_current):
                    y[i] = self.env.get_reward(state_current)
                else:
                    for j in range(self.n_actions):
                        action = rand_circle(radius=1.5)
                        q = 0
                        for k in range(self.n_targets):
                            state_next = state_current.copy()
                            state_next.update(action, np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]]))
                            q += self.env.get_reward(state_current) + self.gamma * self.get_value(state_next)
                        q /= self.n_targets
                        y[i] = q if q > y[i] else y[i]
                x[i] = state_current.phi()
            new_theta = np.linalg.lstsq(x, y)[0]
            if np.linalg.norm(self.theta - new_theta) < self.threshold:
                converged = True
            self.theta = new_theta
            print 'iteration #' + str(t) + ': theta=' + str(self.theta)
            t += 1

        print 'Running time: ' + str(time.clock() - timer) + 's'

    def plot(self):
        x = np.arange(0, 10, 0.1)
        y = np.arange(0, 10, 0.1)
        X, Y = np.meshgrid(x, y)
        Z = [[self.get_value(self.env.state_type(self.env, Predator(self.env, X[j,i], Y[j,i]), self.env.state.prey)) for i in range(x.size)] for j in range(y.size)]
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('Oranges'), linewidth=0)
        plt.show()

    def get_value(self, state):
        return np.dot(self.theta, state.phi())

    def get_actions(self, state):
        pass


def rand_circle(radius=1):
    t = 2 * pi * random()
    u = random() + random()
    r = 2 - u if u > 1 else u
    return [radius * r * cos(t), radius * r * sin(t)]

