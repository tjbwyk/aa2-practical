__author__ = 'kostas'
from Player import Player
from random import random
import numpy as np


class Predator(Player):

    def __init__(self, x, y, environment):
        Player.__init__(self, x, y, environment)
        self.policy = None

    def set_policy(self, policy):
        self.policy = policy

    @staticmethod
    def random_action():
        x = random() * 1.5
        y = random() * 1.5
        return [x, y]

    def sample_action_space(self, n):
        actions = []
        for i in range(0, n):
            actions.append(self.random_action())
        return actions

    def move(self):

        max1 = 0
        new_state = []
        current_state = np.array([self.x, self.y])
        n = 500
        actions = np.array(self.sample_action_space(n))

        next_states = np.remainder(actions + current_state, [self.max_x, self.max_y])
        for i in next_states:
            value = np.dot(self.policy.theta, i)
            if value > max1:
                max1 = value
                new_state = i

        self.x = new_state[0]
        self.y = new_state[1]

