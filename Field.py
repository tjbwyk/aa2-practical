__author__ = 'kostas'

from Player import Player
from State import *
from random import uniform


class Field(object):
    """

    """

    def __init__(self, width, height, state_type=RelativeDistanceState()):
        self.width = width
        self.height = height
        self.state = state_type
        self.predators = []
        self.prey = None
        self.steps = 0

    def add_player(self, player):

        if isinstance(player, Player):
            self.predators.append(player)
        else:
            self.prey = player

    def get_current_state(self):
        res = []
        if self.state.dim == 2:
            diff_x = self.predators[0].x - self.prey.x
            diff_y = self.predators[0].y - self.prey.y
            res = diff_x, diff_y
        elif self.state.dim == 1:
            diff_x = (self.predators[0].x - self.prey.x)**2
            diff_y = (self.predators[0].y - self.prey.y)**2
            res = math.sqrt(diff_x + diff_y)

        return res

    def game_over(self):
        """
        True, if the prey is within a radius of 1 from the predator, else false.
        :return: boolean
        """
        dist = 0
        state = self.get_current_state()
        if self.state.dim == 2:
            dist = sum(state**2)
        elif self.state.dim == 1:
            dist = state

        return dist < 1

    def generate(self, m):
        """
        Uniformly samples m number of states from the state space S
        :param m: number of states to sample
        :return: list of states sampled
        """
        samples = []
        boundary_x = self.width / 2.0
        boundary_y = self.length / 2.0

        if self.state.dim == 1:
            for i in range(0, m):
                rx = uniform(0, boundary_x)
                ry = uniform(0, boundary_y)

                current_sample = math.sqrt(rx**2 + ry**2)
                samples.append(current_sample)

        elif self.state.dim == 2:
            for i in range(0, m):
                rx = uniform(- boundary_x, boundary_x)
                ry = uniform(- boundary_y, boundary_y)

                current_sample = np.array([rx, ry])
                samples.append(current_sample)

        return samples