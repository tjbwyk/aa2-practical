from math import pi, cos, sin
from random import random
import time


class Field(object):
    """

    """

    def __init__(self, width=None, height=None, state_type=None, planner_type=None):
        self.width = width
        self.height = height
        self.state_type = state_type
        self.planner_type = planner_type
        self.state = None
        self.planner = None

    def set_state_type(self, state_type):
        self.state_type = state_type

    def set_planner_type(self, planner_type):
        self.planner_type = planner_type

    def set_planner(self, field, gamma, ns, na, nt, thres):
        self.planner = self.planner_type(field, gamma, ns, na, nt, thres)

    def add_players(self, pred, prey):
        self.state = self.state_type(self, pred, prey)

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    @staticmethod
    def get_reward(state):
        if state.get_distance() < 1:
            return 1
        else:
            return 0

    @staticmethod
    def is_over(state):
        return state.get_distance() < 1

    def learn(self):
        self.planner.fit()
        self.planner.plot()

    def run_n_times(self, n):
        """
        Runs the simulation n times and returns the average steps and time needed for the predator to catch the prey
        :param n: number of times to run the simulation
        :return: average_steps_per_episode, average_duration_per_episode
        """
        avg_steps = 0
        avg_time = 0
        state_init = self.state.copy()
        for i in range(n):
            steps = 0
            timer = time.clock()
            self.state = state_init.copy()
            while not self.is_over(self.state):
                steps += 1
                # print "episode#%d step#%d: Predator(%.2f, %.2f), Prey(%.2f, %.2f)"\
                #       % (i + 1, steps - 1, self.state.pred.x, self.state.pred.y, self.state.prey.x, self.state.prey.y)
                a_pred, a_prey = self.state.get_actions()
                self.state.update(a_pred, a_prey)

            avg_steps += steps
            avg_time += time.clock() - timer

        avg_steps /= 1.0 * n
        avg_time /= 1.0 * n
        return avg_steps, avg_time

def rand_circle(radius=1):
    t = 2 * pi * random()
    u = random() + random()
    r = 2 - u if u > 1 else u
    return [radius * r * cos(t), radius * r * sin(t)]

