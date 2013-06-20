# tests.py
# James Wang, 17 Jun 2013

"""Test suite for tictactoe AI"""

import tictactoe
import ai
import copy
import unittest


class TestAIFunctionality(unittest.TestCase):

    def setUp(self):
        self.empty_grid = tictactoe.Grid(3, 3)
        self.one_to_win_grid = tictactoe.Grid(3, 3)

        self.one_to_win_grid.fill_cell(1, 1, 'O')
        self.one_to_win_grid.fill_cell(0, 0, 'X')
        self.one_to_win_grid.fill_cell(1, 0, 'O')
        self.one_to_win_grid.fill_cell(0, 1, 'X')
        # O's turn, one to win (2, 0)

        self.lean_empty_grid = [-1 for i in range(9)]
        self.lean_one_to_win_grid = [1, 1, -1,
                                     0, 0, -1,
                                     -1, -1, -1]
        self.lean_simple_to_win_grid = [1, 1, -1,
                                        0, 0, -1,
                                        1, 0, 1]
        self.center_filled_grid = [-1, -1, -1,
                                   -1, 0, -1,
                                   -1, -1, -1]

        self.comp1 = ai.LeanComputerPlayer(self.lean_empty_grid, 3, 0)
        self.comp2 = ai.LeanComputerPlayer(self.lean_one_to_win_grid, 3, 0)
        self.comp3 = ai.LeanComputerPlayer(self.lean_simple_to_win_grid,
                                           3, 0)
        self.comp4 = ai.LeanComputerPlayer(self.center_filled_grid, 3, 1)

    # def testGrid(self):
    #     new_grid = copy.deepcopy(self.one_to_win_grid)
    #     self.assertEqual(False, new_grid.winner())

    #     new_grid.fill_cell(1, 2, 'O')  # (1, 2) provides 'O' with victory
    #     self.assertEqual('O', new_grid.winner())

    # def testMove(self):
    #     comp1 = ai.ComputerPlayer(self.empty_grid, 'O', 'hard')
    #     comp2 = ai.ComputerPlayer(self.one_to_win_grid, 'O', 'hard')
    #     self.assertEqual((1, 2), comp2.next_move())
    #     self.assertEqual((1, 1), comp1.next_move())

    def test_win_cond(self):
        no_win1 = [1, 1, 0,
                   0, 0, -1,
                   -1, -1, -1]
        O_wins = [1, 1, -1,
                  0, 0, 0,
                  -1, -1, -1]
        no_win2 = [1, 1, 0,
                   0, 0, 1,
                   1, 0, 0]

        self.assertEqual(self.comp1._winner(self.lean_empty_grid), False)
        self.assertEqual(self.comp1._winner(no_win1), False)
        self.assertEqual(self.comp1._winner(O_wins), 0)
        self.assertEqual(self.comp1._winner(no_win2), False)

    def test_lean(self):
        self.assertEqual(4, self.comp1.next_move())
        self.assertEqual(5, self.comp2.next_move())
        self.assertEqual(5, self.comp3.next_move())
        print(self.comp4.next_move())

if __name__ == '__main__':
    unittest.main()
