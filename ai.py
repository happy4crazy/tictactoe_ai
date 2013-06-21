# ai.py
# James Wang, 13 Jun 2013

"""Simple AI for TicTacToe Game"""

import math
import copy
import sys


class LeanComputerPlayer(object):
    """ai.LeanComputerPlayer:: LeanComputerPlayer(List(Int), Int, Int)

    AI player for tictactoe game. Takes Int list (-1: empty, 0: O, 1: X)
    representing a tictactoe board (e.g. 0-2 is first row, 3-5 is second, 6-8
    is third for a 3x3 board, the size of the board as an Int (e.g. 3 for 3x3)
    and an Int that is 0 if computer player is O and 1 if computer player is X.

    Can only play on a board with an odd number of cells.

    """
    _board = []
    _max_row = 0
    _max_col = 0
    _to_win = 0
    XO = 0  # 0 for O, 1 for X

    # weighting for wins and losses
    _win_value = 1
    _loss_value = -1
    _draw_value = 0

    def __init__(self, board, board_size, XO):
        self._board = board
        self.XO = XO

        self._max_row = board_size
        self._max_col = self._max_row
        self._to_win = self._max_row

    def update_board(self, board):
        """ai.LeanComputerPlayer.update_board:: update_board(List(Int))

        Updates LeanComputerPlayer's internal board state. Takes Int list
        representing board.

        """
        self._board = board

    def next_move(self):
        """ai.LeanComputerPlayer.next_move:: next_move()

        Returns the best next move as index of Int list board representation.

        """
        pos_moves = self._pos_moves(self._board)
        outcome_val = {self.XO: self._win_value,
                       1 if self.XO == 0 else 0: self._loss_value}

        if len(pos_moves) == self._max_row**2:
            return (self._max_row**2 - 1) / 2  # return center

        def flip(player):
            return 1 if player == 0 else 0

        def descendents(moves, board, player):
            def copy_ret(brd, mv, plyr):
                new_board = copy.copy(board)
                new_board[mv] = plyr
                return new_board

            return [solve_tree(copy_ret(board, mv, player), flip(player), mv)
                    for mv in moves]

        def solve_tree(board, player, move=None):
            moves = self._pos_moves(board)
            winner = self._winner(board)
            if moves == [] or winner is not False:
                if winner is not False:
                    return (outcome_val[winner], move)
                else:
                    return (self._draw_value, move)
            else:
                results = descendents(moves, board, player)
                min_or_max = max if player == self.XO else min
                result = min_or_max(results)
                return (result[0], move if move is not None else result[1])

        return solve_tree(self._board, self.XO)[1]

    def move(self):
        """ai.LeanComputerPlayer.move:: move()

        Finds best move, updates internal representation, and returns move as
        index of Int list board representation

        """
        the_move = self.next_move()
        self._board[the_move] = self.XO
        return the_move

    def _winner(self, board):
        num_win = self._to_win

        # maxes only work for x's in first row/column/row respectively
        # these are all + 1 higher than true target to work with range func
        v_max = lambda x: x + num_win * (num_win - 1) + 1
        h_max = lambda x: x + self._max_row
        d_max = lambda x: num_win * num_win - x

        v_step = lambda x: self._max_row
        h_step = lambda x: 1
        d_step = lambda x: self._max_row + 1 - x

        def win_cond(x, max_func, step_func):
            for element in range(x, max_func(x), step_func(x)):
                if board[element] == -1 or board[element] != board[x]:
                    return False
            return board[x]  # return winner

        def test_range(range_to_test, test_step, max_func, step_func):
            for x in range(0, range_to_test, test_step):
                winner = win_cond(x, max_func, step_func)
                if winner is not False:
                    return winner
            return False

        # only test first row, first column, and top two diag cells
        # since that's all that's needed to determine the winner
        h_win = test_range(v_max(0), v_step(0), h_max, h_step)
        v_win = test_range(h_max(0), h_step(0), v_max, v_step)
        d_win = test_range(self._max_row, self._max_row - 1, d_max, d_step)

        for winner in (h_win, v_win, d_win):
            if winner is not False:  # 0 also returns, so can't do if winner:
                return winner

        return False

    def _pos_moves(self, board):
        moves = []
        cells = len(board)
        [moves.append(i) for i in range(cells) if board[i] == -1]
        return moves


class ComputerPlayer(object):
    """ai.ComputerPlayer:: ComputerPlayer(tictactoe.Grid, String)

    Creates an AI player for tictactoe game. Takes a Grid, a String value of
    either 'X' or 'O' depending on what player the AI is meant to represent,
    and a String value for the difficulty ('easy', 'medium', or 'hard').

    NOT FINISHED. DOES NOT CURRENTLY WORK.

    """
    _grid = None
    _max_row = 0
    _max_col = 0
    _XO = ""
    _multiplier = 1  # player is O if positive, X if negative
    difficulty = ""

    def __init__(self, grid, x_or_o, difficulty):
        self._grid = grid  # Reference, not copy!

        self._max_col = len(grid.cells)
        self._max_row = len(grid.cells[0])

        self._XO = x_or_o

        if x_or_o == "O":
            self._multiplier = 1
        elif x_or_o == "X":
            self._multiplier = -1
        else:
            raise ValueError("ComputerPlayer must be passed a string with " +
                             "a value of 'X' or 'O'.")

        self.difficulty = difficulty

    def next_move(self):
        # !!! Assumes that it is actually the comp player's turn
        # Recursively find the move with fewest possible losses
        # Breadth or depth search doesn't matter -- try all possible moves
        # Breadth-first may allow me to set difficulties though
        num_open = len(self._open_cells(self._grid.cells))
        move_depth = {'easy': 3, 'medium': num_open/2, 'hard': num_open - 1}

        def traverse(grid, depth, XO, move_acc):
            open_cells = self._open_cells(grid.cells)
            dig_outcomes = []
            for cell in open_cells:
                dig_outcomes.append(dig(cell, grid, depth - 1, XO, move_acc))
            solution = max(dig_outcomes, key=lambda x: x[0])
            print(solution)
            print(depth)
            return solution

        def dig(move, grid, depth, XO, move_acc):
            if depth == 0 or grid.winner():
                win_flag = 0

                if grid.winner() == self._XO:
                    win_flag = sys.maxint - len(move_acc)  # short wins best
                elif grid.winner() == self._flip_player(self._XO):
                    win_flag = -1  # losses are worst

                # remember that victory_routes are centered around 0
                adj_victory_route = map(lambda x: x * self._multiplier,
                                        grid._victory_routes)
                opponent_closeness = min(adj_victory_route)
                opponent_ways = adj_victory_route.count(opponent_closeness)
                player_closeness = max(adj_victory_route)
                player_ways = adj_victory_route.count(player_closeness)
                diff = (player_closeness * player_ways +
                        opponent_closeness * opponent_ways)

                return ((win_flag, diff), move_acc)
            else:
                new_grid = copy.deepcopy(grid)
                new_moves = copy.deepcopy(move_acc)
                r, c = move
                new_grid.fill_cell(r, c, XO)
                new_moves.append(move)
                return traverse(new_grid, depth, self._flip_player(XO),
                                new_moves)

        satisfice_solution = traverse(self._grid, move_depth[self.difficulty],
                                      self._XO, [])
        return satisfice_solution[1][0]  # return next move (head of move_acc)

    def _score(self, grid):
        # ways * closeness to winning - ways * closeness of opponent to win
        pass

    def _flip_player(self, XO):
        return 'X' if XO == 'O' else 'O'

    def _open_cells(self, cells):
        return list((row, col) for row in range(self._max_row)
                    for col in range(self._max_col)
                    if cells[row][col] == '-')

    def _possible_moves(self, board):
        return math.factorial(self._num_open_cells(board))
