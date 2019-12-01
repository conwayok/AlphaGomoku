# Stronger ai player, used for testing

import random


class Player:
    edge = 15
    W_on_score_board = -2
    B_on_score_board = -1
    direction = [(0, 1), (1, 1), (1, 0), (1, -1)]

    def __init__(self, color):  # d means defending
        self.score1 = 542
        self.score2 = 963
        self.score3 = 1888
        self.score4 = 2097152
        self.d_score1 = 1
        self.d_score2 = 1195
        self.d_score3 = 1928
        self.d_score4 = 262144
        self.debuff_rate = 0.520002840838485
        self.color = -1 * color

    @staticmethod
    def isnt_out(i, j):
        if 0 <= i < Player.edge and 0 <= j < Player.edge:
            return True
        else:
            return False

    @staticmethod
    def enemy(WB):
        if WB == Player.W_on_score_board:
            return Player.B_on_score_board
        else:
            return Player.W_on_score_board

    def max_position(self):
        row_max = []
        max_list = []
        for row in self.score_board:
            row_max.append(max(row))
        _max = max(row_max)
        for i in range(Player.edge):
            for j in range(Player.edge):
                if self.score_board[i][j] == _max:
                    max_list.append((i, j))
        return random.choice(max_list)

    def connected(self, WB, num_chess, i, j, step_x, step_y):  # 專心處理是否有機會可以贏
        chance_to_win = True
        connected = 1 + num_chess
        while self.isnt_out(i + step_x, j + step_y) and self.score_board[i + step_x][j + step_y] != self.enemy(
                WB) and connected < 5:
            i += step_x
            j += step_y
            connected += 1
        if connected < 5:
            chance_to_win = False
        return chance_to_win

    def get_score(self, WB, num_chess, i, j, step_x, step_y, both_open):
        chance_to_win = self.connected(WB, num_chess, i, j, step_x, step_y)
        both_close = False
        if chance_to_win:
            # debuff_square=0
            if self.isnt_out(i + step_x, j + step_y):
                if self.score_board[i + step_x][j + step_y] == WB:
                    # debuff_square=connected-1
                    while self.isnt_out(i + step_x, j + step_y) and self.score_board[i + step_x][j + step_y] == WB:
                        num_chess += 1
                        i += step_x
                        j += step_y
                    if self.isnt_out(i + step_x, j + step_y) == False or self.score_board[i + step_x][
                        j + step_y] == self.enemy(WB):
                        if both_open:
                            both_open = False
                        else:
                            both_close = True
                # elif self.score_board[i+step_x][j+step_y] == 0:
                #     connected+=1
                elif self.isnt_out(i + step_x, j + step_y) == False and self.score_board[i + step_x][
                    j + step_y] == self.enemy(WB):
                    if both_open:
                        both_open = False
                    else:
                        both_close = True
            # chess_to_win=connected+num_chess
            # if chess_to_win < 5:
            #     return 0
            if num_chess < 4 and both_close:
                return 0
            elif not both_open:
                if WB == self.color:
                    if num_chess == 1:
                        return self.score1 * self.debuff_rate
                    elif num_chess == 2:
                        return self.score2 * self.debuff_rate
                    elif num_chess == 3:
                        return self.score3 * self.debuff_rate
                    elif num_chess >= 4:
                        return self.score4 * self.debuff_rate


                else:
                    if num_chess == 1:
                        return self.d_score1 * self.debuff_rate
                    elif num_chess == 2:
                        return self.d_score2 * self.debuff_rate
                    elif num_chess == 3:
                        return self.d_score3 * self.debuff_rate
                    elif num_chess >= 4:
                        return self.d_score4 * self.debuff_rate
            elif both_open:
                if WB == self.color:
                    if num_chess == 1:
                        return self.score1
                    elif num_chess == 2:
                        return self.score2
                    elif num_chess == 3:
                        return self.score3
                    elif num_chess >= 4:
                        return self.score4


                else:
                    if num_chess == 1:
                        return self.d_score1
                    elif num_chess == 2:
                        return self.d_score2
                    elif num_chess == 3:
                        return self.d_score3
                    elif num_chess >= 4:
                        return self.d_score4

        else:
            return 0

    def set_score(self, state, WB, i, j, hrz_step, ver_step):  # WB means black or white on board
        inverse_hrz = (-1) * hrz_step
        inverse_ver = (-1) * ver_step
        front_i, front_j, back_i, back_j = i + hrz_step, j + ver_step, i + inverse_hrz, j + inverse_ver
        return_list = []
        both_open = False
        num_chess = 1
        if self.isnt_out(front_i, front_j) and self.isnt_out(back_i, back_j):  # 判斷是否超過棋盤
            if (state[front_i][front_j] == WB and state[back_i][back_j] == WB) or (
                    state[front_i][front_j] == self.enemy(WB) and state[back_i][back_j] == self.enemy(WB)):
                pass
            else:
                while self.isnt_out(front_i, front_j) and self.score_board[front_i][front_j] == WB:
                    num_chess += 1
                    front_i += hrz_step
                    front_j += ver_step
                while self.isnt_out(back_i, back_j) and self.score_board[back_i][back_j] == WB:
                    num_chess += 1
                    back_i += inverse_hrz
                    back_j += inverse_ver
                if self.isnt_out(front_i, front_j) and self.isnt_out(back_i, back_j):
                    if state[front_i][front_j] == 0 and state[back_i][back_j] == 0:
                        both_open = True
                    if state[front_i][front_j] == 0:
                        score = self.get_score(WB, num_chess, front_i, front_j, hrz_step, ver_step, both_open) / 2
                        return_list.append([front_i, front_j, score])
                    if state[back_i][back_j] == 0:
                        score = self.get_score(WB, num_chess, back_i, back_j, inverse_hrz, inverse_ver, both_open) / 2
                        return_list.append([back_i, back_j, score])
        if len(return_list) != 0:
            return return_list
        else:
            return False

        # 測試在往前下有沒有機會連五科  如果還沒連到就撞壁or碰到他棋 給一個debuff_rate

    def initialize_score_board(self):
        self.score_board = [[0 for i in range(Player.edge)] for j in range(Player.edge)]
        for i in range(Player.edge):
            for j in range(Player.edge):
                self.score_board[i][j] = self.state[i][j] * (-1)

    def choose_action(self, state):
        self.state = state
        num_zero = 0
        self.initialize_score_board()
        # to_win=False #我方已經有四顆 差一顆棋就贏 優先度最高
        # danger=False #敵方已經有四棵 差一顆就輸 第二優先
        for i in range(Player.edge):
            for j in range(Player.edge):
                if self.score_board[i][j] == Player.W_on_score_board or self.score_board[i][
                    j] == Player.B_on_score_board:
                    for direc in Player.direction:
                        dir_x, dir_y = direc
                        score_update = self.set_score(self.state, self.score_board[i][j], i, j, dir_x, dir_y)
                        if score_update == False:
                            pass
                        else:
                            for t in range(len(score_update)):
                                x, y, score = score_update[t]
                                # if score == -5:
                                #     to_win=True
                                #     return x,y
                                # elif score == -10:
                                #     danger=True
                                #     return x,y
                                self.score_board[x][y] += score
                else:
                    num_zero += 1
        # if to_win or danger:
        # pass
        # else:
        if num_zero == Player.edge ** 2:
            return 7, 7  # 如果沒有棋 下最中間
        else:
            return self.max_position()

# if __name__=='__main__':
