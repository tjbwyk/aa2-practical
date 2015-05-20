__author__ = 'kostas'
from Player import Player
from random import random
import numpy as np


class Predator(Player):

    def __init__(self, x, y, environment):
        super.init(x, y, environment)
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

    def move(self, current_state):

        n = 50
        actions = np.array(self.sample_action_space(n))

        next_states = actions + current_state
        values = self.policy.lm.predict(next_states)
        index = np.argmax(values)

        new_state = next_states(index)

        self.x = new_state(0)
        self.y = new_state(1)

