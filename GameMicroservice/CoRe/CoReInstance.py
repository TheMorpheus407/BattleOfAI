from GameMicroservice.DomainModel.GameInstance import GameInstance


class CoReInstance(GameInstance):
    GAME_NAME = "Core"
    AMOUNT_PLAYERS = 2

    def initialize_board(self):
        board = []
        for x in range(8):
            board.append([])
            for y in range(8):
                board[x].append('#')
        return board

    def turn(self, vars):
        symbol = 'XO'[self.active_player]
        pos_x = vars[1]
        pos_y = vars[0]
        self.board[pos_y][pos_x] = symbol
        self.flip_the_shit_out_of_it(self.board, pos_x, pos_y, player=symbol, other='OX'[self.active_player])

    def valid(self, vars):
        try:
            if len(vars) == 2 and type(vars[0]) == int and vars[0] >= 0 and vars[0] < 8 and type(vars[1]) == int and vars[1] >= 0 and vars[1] < 8:
                pass
            else:
                return False
        except:
            pass
        pos_x = vars[1]
        pos_y = vars[0]
        if not self.board[pos_y][pos_x] == '#':
            return False
        return True

    def won_check(self):
        if not self.board_is_full(self.board):
            return False

        score_p1, score_p2 = self.score(self.board)
        if score_p1 > score_p2:
            self.won(0)
        elif score_p2 > score_p1:
            self.won(1)
        return True

    def board_is_full(self, board):
        for line in board:
            for item in line:
                if item == '#': return False
        return True

    def score(self, board):
        player_1 = 0
        player_2 = 0
        for line in board:
            for item in line:
                if item == 'X': player_1 += 1
                if item == 'O': player_2 += 1
        return (player_1, player_2)

    def flip_the_shit_out_of_it(self, board, x, y, player, other):
        # corner kill
        if x == 1 and y == 1 and board[0][0] == other: board[0][0] = player
        if x == 1 and y == 6 and board[7][0] == other: board[7][0] = player
        if x == 6 and y == 1 and board[0][7] == other: board[0][7] = player
        if x == 6 and y == 6 and board[7][7] == other: board[7][7] = player
        # right side of it
        found = False
        for i in range(x + 1, 8):
            if board[y][i] == player: found = True
        if found:
            flipped = False
            for i in range(x + 1, 8):
                if board[y][i] == player:
                    break
                elif board[y][i] == other:
                    flipped = True
                    board[y][i] = player
        # left side of it
        found = False
        for i in range(x)[::-1]:
            if board[y][i] == player: found = True
        if found:
            flipped = False
            for i in range(x)[::-1]:
                if board[y][i] == player:
                    break
                elif board[y][i] == other:
                    flipped = True
                    board[y][i] = player
        # bottom side of it
        found = False
        for i in range(y + 1, 8):
            if board[i][x] == player: found = True
        if found:
            flipped = False
            for i in range(y + 1, 8):
                if board[i][x] == player:
                    break
                elif board[i][x] == other:
                    flipped = True
                    board[i][x] = player
        # upper side of it
        found = False
        for i in range(y)[::-1]:
            if board[i][x] == player: found = True
        if found:
            flipped = False
            for i in range(y)[::-1]:
                if board[i][x] == player:
                    break
                elif board[i][x] == other:
                    flipped = True
                    board[i][x] = player

