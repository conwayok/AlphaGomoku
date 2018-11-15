# distutils: language = c++
from libcpp cimport bool

cdef int BOARD_WIDTH = 15
cdef int WIN_REQUIRE = 5
cdef int BOARD_SIZE = BOARD_WIDTH ** 2

# the state is a 2d list
# this function returns a list of lists
# each list is a coordinate of an empty space
# valid action == a space that has at least one of the eight neighboring spaces occupied
cpdef list get_valid_actions(list state, int distance=1):
    cdef list occupied_spaces = []

    cdef int state_c[15][15]
    cdef int row
    cdef int col
    cdef (int, int) pos

    # indexes
    cdef int i = 0
    cdef int j = 0

    for i in range(15):
        for j in range(15):
            state_c[i][j] = state[i][j]

    for row in range(15):
        for col in range(15):
            if state_c[row][col] != 0:
                pos = (row, col)
                occupied_spaces.append(pos)

    if len(occupied_spaces) == 0:
        return [(7, 7)]

    cdef list valid_actions = []
    # check 8 directions for every pos
    # check directions: up, down, left, right, up left, up right, down left, down right
    # directions = [[1, 0], [-1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]

    cdef int directions[8][2]
    directions[0] = [1, 0]
    directions[1] = [-1, 0]
    directions[2] = [0, -1]
    directions[3] = [0, 1]
    directions[4] = [-1, -1]
    directions[5] = [-1, 1]
    directions[6] = [1, -1]
    directions[7] = [1, 1]

    cdef (int, int) check_pos

    for occupied_pos in occupied_spaces:
        for direction in directions:
            check_pos = occupied_pos
            for _ in range(distance):
                check_pos = (check_pos[0] + direction[0], check_pos[1] + direction[1])
                # if out of bounds
                if (check_pos[0] < 0 or check_pos[0] >= BOARD_WIDTH) or (
                        check_pos[1] < 0 or check_pos[1] >= BOARD_WIDTH):
                    break
                if state_c[check_pos[0]][check_pos[1]] == 0 and (check_pos[0], check_pos[1]) not in valid_actions:
                    valid_actions.append((check_pos[0], check_pos[1]))
    return valid_actions

def get_valid_actions_1d(list state, int distance=1):
    return [pos_to_index(a) for a in get_valid_actions(state, distance)]

cpdef tuple index_to_pos(int num):
    qr = divmod(num + 1, 15)
    # if remainder is 0
    if qr[1] == 0:
        return qr[0] - 1, 14
    else:
        return qr[0], qr[1] - 1

cpdef int pos_to_index(tuple pos):
    return pos[0] * 15 + pos[1]

# 1 if win, -1 if lose, else 0
def get_reward(list state, int player_num):
    enemy_num = 2 if player_num == 1 else 1
    if detect_win(state, player_num):
        return 1
    elif detect_win(state, enemy_num):
        return -1
    else:
        return 0

cpdef list get_valid_actions_all(list state):
    valid_actions = []
    cdef int state_c[15][15]
    cdef int i = 0
    cdef int j = 0

    for i in range(15):
        for j in range(15):
            state_c[i][j] = state[i][j]

    for i in range(BOARD_WIDTH):
        for j in range(BOARD_WIDTH):
            if state_c[i][j] == 0:
                valid_actions.append((i, j))

    if len(valid_actions) == BOARD_SIZE:
        return [(7, 7)]

    return valid_actions

cpdef bool detect_win(list state, int player_num):
    cdef int state_c[15][15]
    cdef int len_pattern = 5
    cdef int BOARD_WIDTH = 15
    cdef int WIN_REQUIRE = 5

    # indexes
    cdef int i = 0
    cdef int j = 0

    for i in range(15):
        for j in range(15):
            state_c[i][j] = state[i][j]

    if checkVertical(state_c, BOARD_WIDTH, WIN_REQUIRE, player_num) + \
            checkHorizontal(state_c, BOARD_WIDTH, WIN_REQUIRE, player_num) + \
            checkUpLeftToDownRight(state_c, BOARD_WIDTH, WIN_REQUIRE, player_num) + \
            check_up_right_to_down_left(state_c, BOARD_WIDTH, WIN_REQUIRE, player_num) > 0:
        return True
    else:
        return False

cdef int checkVertical(int state2D[15][15], int gameBoardWidth, int winRequire, int player):
    cdef int inARow = 0
    cdef int rowIndex
    cdef int row
    cdef int col

    row = 1
    for row in range(gameBoardWidth - winRequire + 2):
        col = 1
        for col in range(gameBoardWidth + 1):
            if state2D[row][col] == player:
                rowIndex = row
                while True:
                    if inARow >= winRequire: return 1
                    if state2D[rowIndex][col] == player:
                        inARow += 1
                        rowIndex += 1
                    else:
                        inARow = 0
                        break
    return 0

cdef int checkHorizontal(int state2D[15][15], int gameBoardWidth, int winRequire, int player):
    cdef int inARow = 0
    cdef int colIndex
    cdef int row
    cdef int col

    row = 1
    for row in range(gameBoardWidth + 1):
        col = 1
        for col in range(gameBoardWidth - winRequire + 2):
            if state2D[row][col] == player:
                colIndex = col
                while True:
                    if inARow >= winRequire: return 1
                    if state2D[row][colIndex] == player:
                        inARow += 1
                        colIndex += 1
                    else:
                        inARow = 0
                        break

    return 0

cdef int checkUpLeftToDownRight(int state2D[15][15], int gameBoardWidth, int winRequire, int player):
    cdef int inARow = 0
    cdef int rowIndex
    cdef int colIndex
    cdef int row
    cdef int col

    row = 1
    for row in range(gameBoardWidth - winRequire + 2):
        col = 1
        for col in range(gameBoardWidth - winRequire + 2):
            if state2D[row][col] == player:
                colIndex = col
                rowIndex = row
                while True:
                    if inARow >= winRequire: return 1
                    if state2D[rowIndex][colIndex] == player:
                        inARow += 1
                        colIndex += 1
                        rowIndex += 1
                    else:
                        inARow = 0
                        break

    return 0

cdef int check_up_right_to_down_left(int state2D[15][15], int gameBoardWidth, int winRequire, int player):
    cdef int inARow = 0
    cdef int rowIndex
    cdef int colIndex
    cdef int row
    cdef int col

    row = 1
    for row in range(gameBoardWidth - winRequire + 2):
        col = winRequire
        for col in range(gameBoardWidth + 1):
            if state2D[row][col] == player:
                colIndex = col
                rowIndex = row
                while True:
                    if inARow >= winRequire: return 1
                    if state2D[rowIndex][colIndex] == player:
                        inARow += 1
                        colIndex -= 1
                        rowIndex += 1
                    else:
                        inARow = 0
                        break

    return 0
