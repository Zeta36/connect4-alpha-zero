import enum
import numpy as np

from logging import getLogger

logger = getLogger(__name__)

# noinspection PyArgumentList
Winner = enum.Enum("Winner", "black white draw")

# noinspection PyArgumentList
Player = enum.Enum("Player", "black white")


class Connect4Env:
    def __init__(self):
        self.board = None
        self.turn = 0
        self.done = False
        self.winner = None  # type: Winner
        self.resigned = False

    def reset(self):
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')
        self.turn = 0
        self.done = False
        self.winner = None
        self.resigned = False
        return self

    def update(self, board):
        self.board = np.copy(board)
        self.turn = self.turn_n()
        self.done = False
        self.winner = None
        self.resigned = False
        return self

    def turn_n(self):
        turn = 0
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    turn += 1

        return turn

    def player_turn(self):
        if self.turn % 2 == 0:
            return Player.white
        else:
            return Player.black

    def step(self, action):
        if action is None:
            self._resigned()
            return self.board, {}

        for i in range(6):
            if self.board[i][action] == ' ':
                self.board[i][action] = ('X' if self.player_turn() == Player.white else 'O')
                break

        self.turn += 1

        self.check_for_fours()

        if self.turn > 42:
            self.done = True
            if self.winner is None:
                self.winner = Winner.draw

        return self.board, {}

    def legal_moves(self):
        legal = [0, 0, 0, 0, 0, 0, 0]
        for j in range(7):
            for i in range(6):
                if self.board[i][j] == ' ':
                    legal[j] = 1
                    break

        return legal

    def check_for_fours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.vertical_check(i, j):
                        self.done = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontal_check(i, j):
                        self.done = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    diag_fours = self.diagonal_check(i, j)
                    if diag_fours:
                        self.done = True
                        return

    def vertical_check(self, row, col):
        # print("checking vert")
        four_in_a_row = False
        consecutive_count = 0

        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count >= 4:
            four_in_a_row = True
            if 'x' == self.board[row][col].lower():
                self.winner = Winner.white
            else:
                self.winner = Winner.black

        return four_in_a_row

    def horizontal_check(self, row, col):
        four_in_a_row = False
        consecutive_count = 0

        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count >= 4:
            four_in_a_row = True
            if 'x' == self.board[row][col].lower():
                self.winner = Winner.white
            else:
                self.winner = Winner.black

        return four_in_a_row

    def diagonal_check(self, row, col):
        four_in_a_row = False
        count = 0

        consecutive_count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1

        if consecutive_count >= 4:
            count += 1
            if 'x' == self.board[row][col].lower():
                self.winner = Winner.white
            else:
                self.winner = Winner.black

        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1

        if consecutive_count >= 4:
            count += 1
            if 'x' == self.board[row][col].lower():
                self.winner = Winner.white
            else:
                self.winner = Winner.black

        if count > 0:
            four_in_a_row = True

        return four_in_a_row

    def _resigned(self):
        if self.player_turn() == Player.white:
            self.winner = Winner.white
        else:
            self.winner = Winner.black
        self.done = True
        self.resigned = True

    def black_and_white_plane(self):
        board_white = np.copy(self.board)
        board_black = np.copy(self.board)
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == ' ':
                    board_white[i][j] = 0
                    board_black[i][j] = 0
                elif self.board[i][j] == 'X':
                    board_white[i][j] = 1
                    board_black[i][j] = 0
                else:
                    board_white[i][j] = 0
                    board_black[i][j] = 1

        return np.array(board_white), np.array(board_black)

    def render(self):
        print("\nRound: " + str(self.turn))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.done:
            print("Game Over!")
            if self.winner == Winner.white:
                print("X is the winner")
            elif self.winner == Winner.black:
                print("O is the winner")
            else:
                print("Game was a draw")

    @property
    def observation(self):
        return ''.join(''.join(x for x in y) for y in self.board)
