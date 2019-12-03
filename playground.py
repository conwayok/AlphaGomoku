# playground for testing and playing against ai

import random
import time

import alpha_gomoku_common
from gui import GUI
from players import AGC_v4_2, forced_actions_v2, AGC_v4_3, Pirate_D, HumanPlayer
from utility.defines import *

show_gui = True
# show_gui = False

# player1 = random_player.RandomPlayer()
# player1 = HumanPlayer.HumanPlayer()
# player1 = AGC_v4_2.AGCPlayer(1, 'agc_v4_2_7680_games.h5')
player1 = AGC_v4_3.AGCPlayer(1, 'agc_v4_3_7660_games.h5')
# player1 = AGC_v4_2_forced_actions.AGCPlayer(1, 'agc_v4_2_7680_games.h5')
# player1 = forced_actions_v2.ForcedActionsV2(1)
# player2 = random_player.RandomPlayer()
# player2 = HumanPlayer.HumanPlayer()
# player2 = AGC_v4_3.AGCPlayer(2, 'agc_v4_3_3720_games.h5')
# player2 = AGC_v4_2.AGCPlayer(2, 'agc_v4_2_4420_games.h5')
player2 = Pirate_D.Player(2)
# player2 = forced_actions_v2.ForcedActionsV2(2)

gui_delay_secs = 0
games_to_play = 100
print_results_interval = 1

player_1_wins = 0
player_2_wins = 0
ties = 0

show_move_times = False
start_time = 0

for games_played in range(games_to_play):
    # initialize board state
    state = [[0 for col in range(BOARD_WIDTH)] for row in range(BOARD_WIDTH)]
    game_over = False
    moves_left = BOARD_WIDTH * BOARD_WIDTH

    # set first player
    current_player = random.choice([1, 2])

    # play the game
    while not game_over:
        if show_move_times:
            start_time = time.time()

        if current_player == 1:
            action = player1.choose_action(state)
            if state[action[0]][action[1]] != 0:
                print('space already occupied!')
            else:
                state[action[0]][action[1]] = 1
        else:
            action = player2.choose_action(state)
            if state[action[0]][action[1]] != 0:
                print('space already occupied!')
            else:
                state[action[0]][action[1]] = 2

        moves_left -= 1

        if show_gui:
            GUI.display(state)
            time.sleep(gui_delay_secs)

        if alpha_gomoku_common.detect_win(state, current_player):
            print('last action:', action)
            if current_player == 1:
                player_1_wins += 1
            else:
                player_2_wins += 1
            game_over = True

        # detect tie
        if moves_left == 0:
            game_over = True
            print('tie')
            ties += 1

        if show_move_times:
            if current_player == 1:
                print('player 1:', time.time() - start_time)
            else:
                print('player 2:', time.time() - start_time)

        # swap players
        current_player = 2 if current_player == 1 else 1

    if (games_played + 1) % print_results_interval == 0:
        print('player 1 wins:', player_1_wins, '\nplayer 2 wins:', player_2_wins, '\nties:', ties, '\n')
