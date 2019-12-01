import random

# from utility.common import get_valid_actions_all
import alpha_gomoku_common


class RandomPlayer:
    @staticmethod
    def choose_action(state):
        valid_actions = alpha_gomoku_common.get_valid_actions_all(state)
        return random.choice(valid_actions)
