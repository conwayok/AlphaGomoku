#  Alpha-Gomoku-Conway
import math

import numpy as np
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.regularizers import l2

import alpha_gomoku_common
from utility.defines import BOARD_SIZE
from utility.defines import BOARD_WIDTH

C_CUPT = 8
PLAYOUT_COUNT = 400


class AGC:
    def __init__(self, model_path=None):
        in_x = network = Input((4, BOARD_WIDTH, BOARD_WIDTH))
        # conv layers
        network = Conv2D(filters=128, kernel_size=(5, 5), padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(1e-4))(network)
        network = Conv2D(filters=128, kernel_size=(5, 5), padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(1e-4))(network)
        network = Conv2D(filters=128, kernel_size=(5, 5), padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(1e-4))(network)
        # action policy layers
        policy_net = Conv2D(filters=4, kernel_size=(1, 1), data_format="channels_first", activation="relu",
                            kernel_regularizer=l2(1e-4))(network)
        policy_net = Flatten()(policy_net)
        self.policy_net = Dense(BOARD_SIZE, activation="softmax", kernel_regularizer=l2(1e-4))(policy_net)
        # state value layers
        value_net = Conv2D(filters=2, kernel_size=(1, 1), data_format="channels_first", activation="relu",
                           kernel_regularizer=l2(1e-4))(network)
        value_net = Flatten()(value_net)
        value_net = Dense(64, kernel_regularizer=l2(1e-4))(value_net)
        self.value_net = Dense(1, activation="tanh", kernel_regularizer=l2(1e-4))(value_net)

        self.model = Model(inputs=in_x, outputs=[self.policy_net, self.value_net])
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(0.001))

        if model_path is not None:
            self.model.load_weights(model_path)
            print('loaded model from', model_path)

    def train(self, examples):
        # examples: list of examples, each example is of form [board, target p, target v]
        input_boards, target_ps, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_ps = np.asarray(target_ps)
        target_vs = np.asarray(target_vs)
        self.model.fit(x=input_boards, y=[target_ps, target_vs], batch_size=64, epochs=16, verbose=True)

    def predict(self, board):
        for action in alpha_gomoku_common.get_valid_actions(board):
            board[action[0]][action[1]] = 1
            win = alpha_gomoku_common.detect_win(board, 1)
            board[action[0]][action[1]] = 0
            if win:
                return [0 if alpha_gomoku_common.index_to_pos(i) != action else 1 for i in range(BOARD_SIZE)], 0.99
            # state_copy = copy.deepcopy(board)
            # state_copy[action[0]][action[1]] = 1
            # if common.detect_win(state_copy, 1):
            #     return [0 if common.index_to_pos(i) != action else 1 for i in range(BOARD_SIZE)], 0.99

        # nn_input: 4*15*15, numpy array
        nn_input = self.convert_to_nn_readable(board)
        p, v = self.model.predict(nn_input)
        return p[0], v[0][0]

    @staticmethod
    def convert_to_nn_readable(state):
        input_layer_1 = [[1 if p == 1 else 0 for p in col] for col in state]  # self positions
        input_layer_2 = [[1 if p == 2 else 0 for p in col] for col in state]  # enemy positions

        # if self is first player
        if np.sum(input_layer_1) == np.sum(input_layer_2):
            # input_layer_3 = [[1 for col in range(15)] for row in range(15)]
            # input_layer_4 = [[0 for col in range(15)] for row in range(15)]
            input_layer_3 = np.full((BOARD_WIDTH, BOARD_WIDTH), 1)
            input_layer_4 = np.full((BOARD_WIDTH, BOARD_WIDTH), 0)

        # if self is second player
        else:
            # input_layer_3 = [[0 for col in range(15)] for row in range(15)]
            # input_layer_4 = [[1 for col in range(15)] for row in range(15)]
            input_layer_3 = np.full((BOARD_WIDTH, BOARD_WIDTH), 0)
            input_layer_4 = np.full((BOARD_WIDTH, BOARD_WIDTH), 1)

        nn_input = np.expand_dims([input_layer_1, input_layer_2, input_layer_3, input_layer_4], 0)
        return nn_input

    def save_nn(self, name):
        name += '.h5'
        self.model.save_weights(name)
        print('model saved to', name)


class AGCPlayer:
    def __init__(self, player_num, model_path=None):
        self.brain = AGC(model_path)
        self.player_num = player_num
        self.enemy_num = 2 if self.player_num == 1 else 1
        self.name = 'AGC_v4'

    @staticmethod
    def convert_to_p1_perspective(state):
        return [[n - 1 if n == 2 else n * 2 for n in row] for row in state]

    def choose_action(self, state):
        if self.player_num == 2:
            state_p1 = self.convert_to_p1_perspective(state)
        else:
            state_p1 = state

        probs, _ = self.brain.predict(state_p1)
        valid_actions = alpha_gomoku_common.get_valid_actions(state, distance=2)
        prob_mask = np.array([1 if alpha_gomoku_common.index_to_pos(i) in valid_actions else 0 for i in range(BOARD_SIZE)])
        probs *= prob_mask
        return alpha_gomoku_common.index_to_pos(np.argmax(probs))
