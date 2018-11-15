# playground for testing and playing against ai

import random
import time

from gui import GUI
from players import random_player
from utility.common import *
import detect_win

show_gui = True
# show_gui = False

player1 = random_player.RandomPlayer()
# player1 = HumanPlayer.HumanPlayer()
# player1 = AGC_v4.AGCPlayer(1)
player2 = random_player.RandomPlayer()
# player2 = HumanPlayer.HumanPlayer()
# player2 = AGC_v4.AGCPlayer(2)

gui_delay_secs = 0
games_to_play = 1000
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

        if detect_win.detect_win(state, current_player):
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
