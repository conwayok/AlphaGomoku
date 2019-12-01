# implementation of the mcts algorithm, modified from https://github.com/suragnair/alpha-zero-general
import common
import math

import numpy as np

from utility.defines import BOARD_SIZE

EPS = 1e-8


class MCTS:
    # all inputs to mcts should be converted to player 1's perspective
    # all states entering this class should be numpy arrays
    def __init__(self, policy_value_obj, c_puct, playout_count):
        if policy_value_obj is None:
            self.policy_value_obj = self.RandomPolicyValueClass()
        else:
            self.policy_value_obj = policy_value_obj  # the class responsible for supplying p and v
        # "s": state, a 2d numpy array representation of the board
        # "a": action, an action is a tuple: (row, col)
        # "q": Q value, how good the state is
        # "n": number of times
        # "p": probabilities

        self.sa_q = {}  # {s, a: Q value}
        self.sa_n = {}  # {s, a : num of times the edge s, a has been visited}
        self.s_n = {}  # {s : num of times s has been visited}
        self.s_p = {}  # {s : probability values}

        self.valid_actions_distance = 1

        self.c_puct = c_puct  # a constant for the PUCT algorithm
        self.playout_count = playout_count  # num of playouts before actually doing the action

        self.s_r = {}  # {s, reward of state s}
        self.s_valid_moves = {}  # {s, valid moves for state s}

    # for pure mcts play
    class RandomPolicyValueClass:
        @staticmethod
        def predict(state):
            return [1 / 225 for _ in range(225)], 0

    @staticmethod
    def convert_perspective(state):
        return np.array([[n - 1 if n == 2 else n * 2 for n in row] for row in state.tolist()])

    # all states entering this function should be player 1's perspective
    def search(self, state_p1_np):
        # s_bytes = np.array_str(state_p1_np)
        s_bytes = state_p1_np.tobytes()
        s_list = state_p1_np.tolist()

        # check if reward is assigned to this state yet
        if s_bytes not in self.s_r:
            self.s_r[s_bytes] = common.get_reward(s_list, 1)

        # if is terminal state, return
        if self.s_r[s_bytes] != 0 or np.count_nonzero(state_p1_np) == BOARD_SIZE:
            return -self.s_r[s_bytes]

        # check if is leaf node
        # if is leaf node, will have no move probabilities yet
        if s_bytes not in self.s_p:
            probs, value = self.policy_value_obj.predict(s_list)
            valid_actions_1d = common.get_valid_actions_1d(s_list, self.valid_actions_distance)
            self.s_valid_moves[s_bytes] = valid_actions_1d

            # mask = [1 if a in valid_actions_1d else 0 for a in range(BOARD_SIZE)]
            # probs = np.array([probs[i] * mask[i] for i in range(BOARD_SIZE)])
            probs = np.array([probs[a] if a in valid_actions_1d else 0 for a in range(BOARD_SIZE)])
            probs_sum = np.sum(probs)

            # if probs_sum is 0, set all probs to equal numbers
            # and print error
            if probs_sum == 0:
                probs = np.array([1 / probs.size for _ in range(probs.size)])
                print('warning: all moves masked')

            # re-normalize
            elif probs_sum != 1:
                probs /= probs_sum

            self.s_p[s_bytes] = probs
            self.s_n[s_bytes] = 0

            return -value

        # if code reaches here it means the state is not a leaf node
        # if not leaf node, select the next node
        best_node_score = float('-inf')
        best_action = -1

        for a in self.s_valid_moves[s_bytes]:
            if (s_bytes, a) in self.sa_q:
                u = self.c_puct * self.s_p[s_bytes][a] * math.sqrt(self.s_n[s_bytes]) / (1 + self.sa_n[(s_bytes, a)])
                score = self.sa_q[(s_bytes, a)] + u  # q + u
            else:
                u = self.c_puct * self.s_p[s_bytes][a] * math.sqrt(self.s_n[s_bytes] + EPS)
                score = u

            if score > best_node_score:
                best_node_score = score
                best_action = a

        next_s = self.convert_perspective(state_p1_np)
        best_action_2d = common.index_to_pos(best_action)
        next_s[best_action_2d[0]][best_action_2d[1]] = 2

        value = self.search(next_s)

        if (s_bytes, best_action) in self.sa_q:
            sa_n = self.sa_n[(s_bytes, best_action)]
            self.sa_q[(s_bytes, best_action)] = (self.sa_n[(s_bytes, best_action)] * self.sa_q[
                (s_bytes, best_action)] + value) / (sa_n + 1)
            self.sa_n[(s_bytes, best_action)] = sa_n + 1

        else:
            self.sa_q[(s_bytes, best_action)] = value
            self.sa_n[(s_bytes, best_action)] = 1

        self.s_n[s_bytes] += 1
        return -value

    def get_probs(self, state_p1_np):
        for _ in range(self.playout_count):
            self.search(state_p1_np)

        state_bytes = state_p1_np.tobytes()
        counts = [self.sa_n[(state_bytes, i)] if (state_bytes, i) in self.sa_n else 0 for i in range(BOARD_SIZE)]
        counts_sum = sum(counts)

        if counts_sum == 0:
            valid_actions_1d = common.get_valid_actions_1d(state_p1_np.tolist(), self.valid_actions_distance)
            prob = 1 / len(valid_actions_1d)
            probs = [prob if i in valid_actions_1d else 0 for i in range(BOARD_SIZE)]
            print('counts_sum is 0!')
        else:
            probs = [i / counts_sum for i in counts]
        return probs


class MCTSPlayer:
    def __init__(self, player_num, policy_value_obj=None, c_puct=5, playout_count=400):
        self.player = MCTS(policy_value_obj, c_puct, playout_count)
        self.player_num = player_num

    def choose_action(self, state):
        if self.player_num == 2:
            state = self.convert_to_p1_perspective(state)

        state_np = np.array(state)
        if np.count_nonzero(state_np) == 0:
            best_action = (7, 7)
        else:
            probs = self.player.get_probs(state_np)
            best_action = common.index_to_pos(probs.index(max(probs)))

        return best_action

    @staticmethod
    def convert_to_p1_perspective(state):
        return [[n - 1 if n == 2 else n * 2 for n in row] for row in state]

    # also returns the probs
    def choose_action_training(self, state_p1_np):

        # if board is empty, place piece in middle
        if np.count_nonzero(state_p1_np) == 0:
            best_action = (7, 7)
            probs = np.zeros(225)
            probs[112] = 1
            return best_action, np.array(probs)

        probs = self.player.get_probs(state_p1_np)
        best_action = common.index_to_pos(probs.index(max(probs)))
        return best_action, probs
