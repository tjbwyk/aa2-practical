__author__ = 'kostas'


class Field(object):
    """
    Models the environment:
    Responsibilities:
    - Maintaining a list of agents
    - coordination of the steps in an episode
      - triggering the agents to pick their next action
      - calculate next state and rewards based on actions
      - return
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []
        self.steps = 0

    def add_player(self, player):

        self.players.append(player)

    def get_current_state(self):

        diff_x = self.players(0).x - self.players(1).x
        diff_y = self.players(0).y - self.players(1).y