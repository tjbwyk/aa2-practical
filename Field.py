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
        :return: np.array [1x2] or [1x1]
        """
        pred_location = [self.predators[0].x, self.predators[0].y]
        prey_location = [self.prey.x, self.prey.y]
        result = self.state2vector(pred_location, prey_location)

        return result

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
                rx = uniform(0, boundary_x)
                ry = uniform(0, boundary_y)

                current_sample = np.array([rx, ry])
                samples.append(current_sample)

        return samples

    def printme(self):

        d = self.find_distance()
        print "%0.2f, %0.2f | %0.2f, %0.2f -- %0.2f"\
              % (self.predators[0].x, self.predators[0].y, self.prey.x, self.prey.y, d)

    def get_reward(self, state):
        """
        The R (Reward) function
        :param state: 
        :return:
        """
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

        state = self.get_current_state()
        if self.state.dim == 2:
            dist = math.sqrt(sum(state**2))
        elif self.state.dim == 1:
            dist = state

        return dist

    def state2vector(self, pred_loc, prey_loc):
        """
        Returns the vector representation of the state
        :param pred_loc: location of the predator
        :param prey_loc: location of the prey
        :return: np.array [1x2] or [1x1]
        """
        res1 = pred_loc[0] - prey_loc[0]
        if res1 > (self.width / 2.0):
            res1 = self.width - pred_loc[0] + prey_loc[0]
        elif res1 < -(self.width / 2.0):
            res1 = pred_loc[0] + self.width - prey_loc[0]

        res2 = pred_loc[1] - prey_loc[1]
        if res2 > (self.height / 2.0):
            res2 = self.height - pred_loc[1] + prey_loc[1]
        elif res2 < -(self.height / 2.0):
            res1 = pred_loc[1] + self.height - prey_loc[1]

        if self.state.dim == 1:
            result = np.array([math.sqrt(res1**2 + res2**2)])
        elif self.state.dim == 2:
            result = np.array([res1, res2])
        return result

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

    def run_n_times(self, n):
        """
        Runs the simulation n times and returns the average steps and time needed for the predator to catch the prey
        :param n: number of times to run the simulation
        :return: average_steps_per_episode, average_duration_per_episode
        """
        avg_steps = 0
        avg_time = 0
        for i in range(n):

            steps = 0
            start_time = time.time()

            while not self.game_over():
                steps += 1
                self.predators[0].move()
                self.prey.move()

            duration = time.time() - start_time
            avg_steps += steps
            avg_time += duration

            self.predators[0].x, self.predators[0].y = 0, 0
            self.prey.x, self.prey.y = 5, 5

        avg_steps /= n
        avg_time /= n
        return avg_steps, avg_time