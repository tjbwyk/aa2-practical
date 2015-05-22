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
        self.planner = self.planner_type(self)
        self.planner.fit()
        self.planner.plot()

    def run_n_times(self, n):
        """
        Runs the simulation n times and returns the average steps and time needed for the predator to catch the prey
        :param n: number of times to run the simulation
        :return: average_steps_per_episode, average_duration_per_episode
        """
        avg_steps = 0
        state_init = self.state.copy()
        for i in range(n):
            steps = 0
            self.state = state_init.copy()
            while not self.game_over():
                steps += 1
                self.state.pred
                self.predators[0].move()
                self.prey.move()

            avg_steps += steps

        avg_steps /= n
        return avg_steps
    #
    # def add_player(self, player):
    #
    #     if isinstance(player, Player):
    #         self.predators.append(player)
    #     else:
    #         self.prey = player
    #
    # def get_current_state(self):
    #     res = []
    #     if self.state.dim == 2:
    #         diff_x = self.predators[0].x - self.prey.x
    #         diff_y = self.predators[0].y - self.prey.y
    #         res = diff_x, diff_y
    #     elif self.state.dim == 1:
    #         diff_x = (self.predators[0].x - self.prey.x)**2
    #         diff_y = (self.predators[0].y - self.prey.y)**2
    #         res = math.sqrt(diff_x + diff_y)
    #
    #     return res
    #
    # def game_over(self):
    #     """
    #     True if the prey is within a radius of 1 from the predator
    #     :return: boolean
    #     """
    #     dist = 0
    #     state = self.get_current_state()
    #     if self.state.dim == 2:
    #         dist = sum(state**2)
    #     elif self.state.dim == 1:
    #         dist = state
    #
    #     return dist < 1
    #
    # def generate(self, m):
    #     """
    #     Uniformly samples #m states from S
    #     :param m: number of states to sample
    #     :return: list of states sampled
    #     """
    #     samples = []
    #     boundary_x = self.width / 2.0
    #     boundary_y = self.length / 2.0
    #
    #     if self.state.dim == 1:
    #         for i in range(0, m):
    #             rx = uniform(0, boundary_x)
    #             ry = uniform(0, boundary_y)
    #
    #             current_sample = math.sqrt(rx**2 + ry**2)
    #             samples.append(current_sample)
    #
    #     elif self.state.dim == 2:
    #         for i in range(0, m):
    #             rx = uniform(- boundary_x, boundary_x)
    #             ry = uniform(- boundary_y, boundary_y)
    #
    #             current_sample = np.array([rx, ry])
    #             samples.append(current_sample)
    #
    #     return samples