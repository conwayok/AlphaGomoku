import copy

import numpy as np
import detect_win

BOARD_WIDTH = 15
WIN_REQUIRE = 5
BOARD_SIZE = BOARD_WIDTH ** 2


# the state is a 2d list
# this function returns a list of lists
# each list is a coordinate of an empty space
# valid action == a space that has at least one of the eight neighboring spaces occupied
def get_valid_actions(state, distance=1):
    occupied_spaces = []

    for row_num, entire_row in enumerate(state):
        for col_num, number in enumerate(entire_row):
            if number != 0:
                occupied_spaces.append([row_num, col_num])

    if len(occupied_spaces) == 0:
        return [(7, 7)]

    valid_actions = []
    # check 8 directions for every pos
    # check directions: up, down, left, right, up left, up right, down left, down right
    directions = [[1, 0], [-1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    for occupied_pos in occupied_spaces:
        for direction in directions:
            check_pos = occupied_pos[:]
            for _ in range(distance):
                check_pos[0] += direction[0]
                check_pos[1] += direction[1]
                # if out of bounds
                if (check_pos[0] < 0 or check_pos[0] >= BOARD_WIDTH) or (
                        check_pos[1] < 0 or check_pos[1] >= BOARD_WIDTH):
                    break
                if state[check_pos[0]][check_pos[1]] == 0 and (check_pos[0], check_pos[1]) not in valid_actions:
                    valid_actions.append((check_pos[0], check_pos[1]))
    return valid_actions


def get_valid_actions_1d(state, distance=1):
    return [pos_to_index(a) for a in get_valid_actions(state, distance)]


def get_possible_next_states(state, player_num):
    possible_next_states = []
    valid_actions = get_valid_actions(state)
    for action in valid_actions:
        next_state = copy.deepcopy(state)
        next_state[action[0]][action[1]] = player_num
        possible_next_states.append(next_state)
    return possible_next_states


def index_to_pos(num):
    qr = divmod(num + 1, 15)

    # if remainder is 0
    if qr[1] == 0:
        return qr[0] - 1, 14

    else:
        return qr[0], qr[1] - 1


def pos_to_index(pos):
    return pos[0] * 15 + pos[1]


# 1 if win, -1 if lose, else 0
def get_reward(state, player_num):
    enemy_num = 2 if player_num == 1 else 1
    if detect_win.detect_win(state, player_num):
        return 1
    elif detect_win.detect_win(state, enemy_num):
        return -1
    else:
        return 0


def get_valid_actions_all(state):
    valid_actions = []
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_WIDTH):
            if state[i][j] == 0:
                valid_actions.append((i, j))
    if len(valid_actions) == BOARD_SIZE:
        return [(7, 7)]
    return valid_actions


# def detect_win(state, player_num):
#     num_of_matches = 0
#
#     string_pattern = '11111' if player_num == 1 else '22222'
#
#     state_np = np.array(state)
#
#     # all the lines in the state (vertical, horizontal, diagonal)
#     lines_list = []
#
#     # find matches function
#     def find_matches():
#         nonlocal num_of_matches
#         nonlocal lines_list
#         # find matches:
#         for s in lines_list:
#             num_of_matches += s.count(string_pattern)
#         return num_of_matches
#
#     # get the rows:
#     lines_list.extend([''.join(str(n) for n in row) for row in state])
#
#     if find_matches() > 0:
#         return True
#
#     lines_list.clear()
#
#     # get the columns:
#     rotated_state_np = np.rot90(state_np)
#     lines_list.extend([''.join(str(n) for n in row) for row in rotated_state_np.tolist()])
#
#     if find_matches() > 0:
#         return True
#
#     lines_list.clear()
#
#     # get the diagonals:
#     lines_list.extend(
#         [''.join(str(n) for n in state_np.diagonal(i).tolist()) for i in range(-BOARD_WIDTH + 1, BOARD_WIDTH)])
#
#     if find_matches() > 0:
#         return True
#
#     lines_list.clear()
#
#     lines_list.extend(
#         [''.join(str(n) for n in rotated_state_np.diagonal(i).tolist()) for i in range(-BOARD_WIDTH + 1, BOARD_WIDTH)])
#
#     if find_matches() > 0:
#         return True
#
#     return False
