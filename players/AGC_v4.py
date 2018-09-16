from keras import Input, Model
from keras.layers import Conv2D, Flatten, Dense
from keras.optimizers import Adam
from keras.regularizers import l2

from utility.common import *


class AGC:
    def __init__(self, model_path=None):
        in_x = network = Input((3, BOARD_WIDTH, BOARD_WIDTH))
        # conv layers
        network = Conv2D(filters=128, kernel_size=(5, 5), padding='same', data_format='channels_first',
                         activation='relu', kernel_regularizer=l2(1e-4))(network)
        network = Conv2D(filters=128, kernel_size=(5, 5), padding='same', data_format='channels_first',
                         activation='relu', kernel_regularizer=l2(1e-4))(network)
        network = Conv2D(filters=256, kernel_size=(5, 5), padding='same', data_format='channels_first',
                         activation='relu', kernel_regularizer=l2(1e-4))(network)
        network = Conv2D(filters=512, kernel_size=(5, 5), padding='same', data_format='channels_first',
                         activation='relu', kernel_regularizer=l2(1e-4))(network)
        # action policy layers
        policy_net = Conv2D(filters=4, kernel_size=(1, 1), data_format='channels_first', activation='relu',
                            kernel_regularizer=l2(1e-4))(network)
        policy_net = Flatten()(policy_net)
        self.policy_net = Dense(BOARD_SIZE, activation='softmax', kernel_regularizer=l2(1e-4))(policy_net)
        # state value layers
        value_net = Conv2D(filters=2, kernel_size=(1, 1), data_format='channels_first', activation='relu',
                           kernel_regularizer=l2(1e-4))(network)
        value_net = Flatten()(value_net)
        value_net = Dense(64, kernel_regularizer=l2(1e-4))(value_net)
        self.value_net = Dense(1, activation='tanh', kernel_regularizer=l2(1e-4))(value_net)

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
        # nn_input: 3*15*15, numpy array
        nn_input = self.convert_to_nn_readable(board)
        p, v = self.model.predict(nn_input)
        return p[0], v[0]

    @staticmethod
    def convert_to_nn_readable(state):
        # states passed into here should be converted to player 1 perspective
        input_layer_1 = np.array([[1 if p == 1 else 0 for p in col] for col in state])  # self positions
        input_layer_2 = np.array([[1 if p == 2 else 0 for p in col] for col in state])  # enemy positions

        # if self is first player
        if np.sum(input_layer_1) == np.sum(input_layer_2):
            input_layer_3 = np.array([[1 for col in range(15)] for row in range(15)])
        # if self is second player
        else:
            input_layer_3 = np.array([[0 for col in range(15)] for row in range(15)])

        nn_input = np.expand_dims([input_layer_1, input_layer_2, input_layer_3], 0)
        # nn_input = np.array([[input_layer_1, input_layer_2, input_layer_3]])
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

    @staticmethod
    def convert_to_p1_perspective(state):
        return [[1 if n == 2 else 2 for n in row] for row in state]

    def choose_action(self, state):
        if self.player_num == 2:
            state_p1 = self.convert_to_p1_perspective(state)
        else:
            state_p1 = state

        probs, _ = self.brain.predict(state_p1)
        valid_actions = get_valid_actions(state, distance=2)
        prob_mask = np.array([1 if index_to_pos(i) in valid_actions else 0 for i in range(BOARD_SIZE)])
        probs *= prob_mask
        nn_action = index_to_pos(np.argmax(probs))
        return nn_action
