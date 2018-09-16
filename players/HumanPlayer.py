class HumanPlayer:

    @staticmethod
    def choose_action(state):
        while True:
            while True:
                x = input('x:')
                if x.isdecimal() and (0 <= int(x) <= 14):
                    break
            while True:
                y = input('y:')
                if y.isdecimal() and (0 <= int(y) <= 14):
                    break
            x, y = int(x), int(y)

            if state[x][y] == 0:
                break

        return x, y
