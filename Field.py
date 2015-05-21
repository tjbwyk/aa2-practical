__author__ = 'kostas'

from Player import Player
from State import *
from random import uniform
import time
import math
from Predator import Predator


class Field(object):
    """

    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = None
        self.predators = []
        self.prey = None
        self.steps = 0

    def set_state_type(self, state):
        self.state = state

    def add_player(self, player):

        if isinstance(player, Predator):
            self.predators.append(player)
        else:
            self.prey = player

    def get_current_state(self):
        """
        Returns the current state of the world
        :return:
        """
        res = []
        if self.state.dim == 2:
            diff_x = self.predators[0].x - self.prey.x
            if abs(diff_x) > self.width / 2.0:
                if diff_x < 0:
                    diff_x %= (self.width / 2.0)
                else:
                    diff_x = - (self.width - self.predators[0].x + self.prey.x)
            diff_y = self.predators[0].y - self.prey.y
            if abs(diff_y) > self.height / 2.0:
                if diff_y < 0:
                    diff_y %= (self.height / 2.0)
                else:
                    diff_y = - (self.height - self.predators[0].y + self.prey.y)
            res = np.array([diff_x, diff_y])
        elif self.state.dim == 1:
            diff_x = (self.predators[0].x - self.prey.x)**2
            diff_y = (self.predators[0].y - self.prey.y)**2
            res = np.array([math.sqrt(diff_x + diff_y)])

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
        boundary_y = self.height / 2.0

        if self.state.dim == 1:
            for i in range(0, m):
                rx = uniform(- boundary_x, boundary_x)
                ry = uniform(- boundary_y, boundary_y)

                current_sample = np.array([math.sqrt(rx**2 + ry**2)])
                samples.append(current_sample)

        elif self.state.dim == 2:
            for i in range(0, m):
                rx = uniform(- boundary_x, boundary_x)
                ry = uniform(- boundary_y, boundary_y)

                current_sample = np.array([rx, ry])
                samples.append(current_sample)

        return samples

    def printme(self):

        d = self.find_distance()
        print "%0.2f, %0.2f | %0.2f, %0.2f -- %0.2f"\
              % (self.predators[0].x, self.predators[0].y, self.prey.x, self.prey.y, d)

    def run(self):
        """
        Runs one simulation of the world
        :return:
        """
        steps = 0
        self.printme()
        start_time = time.time()

        while not self.game_over():
            steps += 1
            self.predators[0].move()
            self.prey.move()
            self.printme()

        duration = time.time() - start_time
        print "Steps:", steps
        print "Duration:", duration

    def get_reward(self, state):

        dist = 0
        if self.state.dim == 2:
            dist = math.sqrt(sum(state**2))
        elif self.state.dim == 1:
            dist = state
        if dist < 1:
            return 1
        else:
            return 0

    def find_distance(self):

        dist = 0
        state = self.get_current_state()
        if self.state.dim == 2:
            dist = math.sqrt(sum(state**2))
        elif self.state.dim == 1:
            dist = state

        return dist