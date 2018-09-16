import random

from utility.common import get_valid_actions_all


class RandomPlayer:
    @staticmethod
    def choose_action(state):
        valid_actions = get_valid_actions_all(state)
        return random.choice(valid_actions)
