# cython: language_level=3
def detect_win(list state, int player_num):
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
            checkUpRightToDownLeft(state_c, BOARD_WIDTH, WIN_REQUIRE, player_num) > 0:
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

cdef int checkUpRightToDownLeft(int state2D[15][15], int gameBoardWidth, int winRequire, int player):
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
