# AI player using a 'forced action' strategy
import gomoku_pattern_detection

import random
import copy
import alpha_gomoku_common


class ForcedActionsV2:
    def __init__(self, player_num):
        self.player_num = player_num
        self.enemy_num = 1 if self.player_num == 2 else 2

    def choose_action(self, state):
        valid_actions = alpha_gomoku_common.get_valid_actions(state)

        # force win
        for action in valid_actions:
            next_state = copy.deepcopy(state)
            next_state[action[0]][action[1]] = self.player_num
            if gomoku_pattern_detection.detect_pattern(next_state, 'ooooo', self.player_num) >= 1:
                return action

        # force block
        if gomoku_pattern_detection.detect_pattern(state, 'oooo-', self.enemy_num):
            for action in valid_actions:
                next_state = copy.deepcopy(state)
                next_state[action[0]][action[1]] = self.player_num
                if gomoku_pattern_detection.detect_pattern(next_state, 'oooo-', self.enemy_num) == 0:
                    return action

        if gomoku_pattern_detection.detect_pattern(state, 'oo-oo', self.enemy_num):
            for action in valid_actions:
                next_state = copy.deepcopy(state)
                next_state[action[0]][action[1]] = self.player_num
                if gomoku_pattern_detection.detect_pattern(next_state, 'oooo-', self.enemy_num) == 0:
                    return action

        if gomoku_pattern_detection.detect_pattern(state, 'ooo-o', self.enemy_num):
            for action in valid_actions:
                next_state = copy.deepcopy(state)
                next_state[action[0]][action[1]] = self.player_num
                if gomoku_pattern_detection.detect_pattern(next_state, 'oooo-', self.enemy_num) == 0:
                    return action

        if gomoku_pattern_detection.detect_pattern(state, '-ooo-', self.enemy_num):
            for action in valid_actions:
                next_state = copy.deepcopy(state)
                next_state[action[0]][action[1]] = self.player_num
                if gomoku_pattern_detection.detect_pattern(next_state, '-ooo-', self.enemy_num) == 0:
                    return action

        if gomoku_pattern_detection.detect_pattern(state, '-oo---', self.enemy_num) >= 2:
            for action in valid_actions:
                next_state = copy.deepcopy(state)
                next_state[action[0]][action[1]] = self.player_num
                if gomoku_pattern_detection.detect_pattern(next_state, '-oo---', self.enemy_num) == 0:
                    return action

        # try to win
        for action in valid_actions:
            next_state = copy.deepcopy(state)
            next_state[action[0]][action[1]] = self.player_num
            if gomoku_pattern_detection.detect_pattern(next_state, '-oooo-', self.player_num) >= 1:
                return action

        for action in valid_actions:
            next_state = copy.deepcopy(state)
            next_state[action[0]][action[1]] = self.player_num
            if gomoku_pattern_detection.detect_pattern(next_state, '-ooo--', self.player_num) >= 2:
                return action

        for action in valid_actions:
            next_state = copy.deepcopy(state)
            next_state[action[0]][action[1]] = self.player_num
            if gomoku_pattern_detection.detect_pattern(next_state, '-ooo--', self.player_num) >= 1:
                return action

        return random.choice(alpha_gomoku_common.get_valid_actions(state))
