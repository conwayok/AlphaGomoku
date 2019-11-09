import random

# from utility.common import get_valid_actions_all
import common


class RandomPlayer:
    @staticmethod
    def choose_action(state):
        valid_actions = common.get_valid_actions_all(state)
        return random.choice(valid_actions)
