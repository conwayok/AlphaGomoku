# training routine for AGC

import random
import time

from gui import GUI
# from players import AGC_v4
from players import AGC_v4_2, AGC_v4_3
from utility.defines import BOARD_SIZE
from utility.defines import BOARD_WIDTH
from utility.mcts import *

iterations = 1000
games_per_iteration = 20

show_gui = True
show_move_times = True

training_data = []  # [(state, target p, target v), (...), ......]
unprepared_training_data = []


def start_training():
    # agc = AGC_v4_2.AGC('agc_v4_2_4420_games.h5')
    # agc = AGC_v4_3.AGC('agc_v4_3_4120_games.h5')
    agc = AGC_v4_3.AGC()
    for _ in range(1, iterations + 1):
        mcts_player = MCTSPlayer(1, agc, c_puct=AGC_v4_3.C_CUPT, playout_count=AGC_v4_3.PLAYOUT_COUNT)
        mcts_player.player.valid_actions_distance = 2
        print('ITERATION', _)
        print('Generating data...')
        generate_data(_, mcts_player)
        print('Done generating data, training data on nn')
        train_data_on_nn(mcts_player, agc)
        if _ % 1 == 0:
            agc.save_nn('agc_v4_3_' + str(4120 + _ * games_per_iteration) + '_games')


def generate_data(iteration_num, mcts_player):
    global unprepared_training_data
    for games_played in range(1, games_per_iteration + 1):
        # initialize board state
        state = [[0 for col in range(BOARD_WIDTH)] for row in range(BOARD_WIDTH)]
        game_over = False
        moves_left = BOARD_WIDTH * BOARD_WIDTH

        current_player = random.choice([1, 2])

        training_data_temp = []

        endgame_reward = -1

        if show_gui:
            GUI.display(state)

        if show_move_times:
            moves = 0

        # play the game
        while not game_over:

            if show_move_times:
                move_start_time = time.time() * 1000
                moves += 1

            if current_player == 1:
                mcts_player.player_num = 1

                state_p1_np = np.array(state)
                action, probs = mcts_player.choose_action_training(state_p1_np)
                if state[action[0]][action[1]] != 0:
                    print('space already occupied!')
                else:
                    state[action[0]][action[1]] = 1
            else:
                mcts_player.player_num = 2

                state_p1_np = np.array(convert_to_p1_perspective(state))
                action, probs = mcts_player.choose_action_training(state_p1_np)
                if state[action[0]][action[1]] != 0:
                    print('space already occupied!')
                else:
                    state[action[0]][action[1]] = 2

            moves_left -= 1

            # save to training data temp
            if current_player == 1:
                training_data_temp.append((state_p1_np, 1))
            else:
                training_data_temp.append((state_p1_np, 2))

            if show_gui:
                GUI.display(state)

            # detect win/lose
            if common.detect_win(state, current_player):
                game_over = True
                if current_player == 1:
                    endgame_reward = 1

            # detect tie
            if moves_left == 0:
                game_over = True

            # swap players
            current_player = 2 if current_player == 1 else 1

            if show_move_times:
                print('move', moves, 'time', str(time.time() * 1000 - move_start_time), 'ms')

        if show_move_times:
            moves = 0

        unprepared_training_data += [
            [state_data[0], None, endgame_reward] if state_data[1] == 1 else [state_data[0], None, -endgame_reward] for
            state_data in
            training_data_temp]

        print('ITERATION', iteration_num, 'Games played', games_played, '/', games_per_iteration)


def create_training_example(unprepared_data, mcts):
    print('processing data for training')
    # all visited_states should be nn readable (p1 perspective, np array)
    # training_data contents: [(state in np array type and p1 perspective, None, endgame_reward)]
    for index in range(len(unprepared_data)):
        if np.count_nonzero(unprepared_data[index][0]) == 0:
            unprepared_data[index][1] = [1 if i == 112 else 0 for i in range(BOARD_SIZE)]
        else:
            state_bytes = np.array(unprepared_data[index][0]).tobytes()
            counts = [mcts.sa_n[(state_bytes, i)] if (state_bytes, i) in mcts.sa_n else 0 for i in range(BOARD_SIZE)]
            counts_sum = sum(counts)
            real_probs = [c / counts_sum for c in counts]
            unprepared_data[index][1] = real_probs

    rotated_training_data = []

    for state_data in unprepared_data:
        state_rotation1 = np.rot90(state_data[0])
        state_rotation2 = np.rot90(state_rotation1)
        state_rotation3 = np.rot90(state_rotation2)

        probs_2d = np.reshape(state_data[1], (15, 15))
        probs_rotation1 = np.rot90(probs_2d).flatten()
        probs_rotation2 = np.rot90(probs_2d, 2).flatten()
        probs_rotation3 = np.rot90(probs_2d, 3).flatten()

        endgame_reward = state_data[2]

        rotated_training_data += [[state_rotation1, probs_rotation1, endgame_reward],
                                  [state_rotation2, probs_rotation2, endgame_reward],
                                  [state_rotation3, probs_rotation3, endgame_reward]]

    unprepared_data += rotated_training_data

    global training_data

    training_data = [[convert_to_nn_readable(step_data[0]), step_data[1], step_data[2]] for step_data in
                     unprepared_data]


def convert_to_p1_perspective(state):
    return [[n - 1 if n == 2 else n * 2 for n in row] for row in state]


def convert_to_nn_readable(state):
    input_layer_1 = np.array([[1 if p == 1 else 0 for p in col] for col in state])  # self positions
    input_layer_2 = np.array([[1 if p == 2 else 0 for p in col] for col in state])  # enemy positions

    # if self is first player
    if np.sum(input_layer_1) == np.sum(input_layer_2):
        input_layer_3 = np.array([[1 for col in range(15)] for row in range(15)])  # input layer 3 will be all 1
        input_layer_4 = np.array([[0 for col in range(15)] for row in range(15)])  # input layer 4 will be all 0
    # if self is second player
    else:
        input_layer_3 = np.array([[0 for col in range(15)] for row in range(15)])  # input layer 3 will be all 0
        input_layer_4 = np.array([[1 for col in range(15)] for row in range(15)])  # input layer 4 will be all 1

    nn_input = np.array([input_layer_1, input_layer_2, input_layer_3, input_layer_4])
    return nn_input


def train_data_on_nn(mcts_player, agc):
    create_training_example(unprepared_training_data, mcts_player.player)
    agc.train(training_data)
    training_data.clear()
    unprepared_training_data.clear()


start_training()
