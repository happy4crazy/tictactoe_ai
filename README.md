TicTacToe AI
============
AI for TicTacToe that uses an exhaustive search to find best move.
Use LeanComputerPlayer vs. ComputerPlayer (the latter is unfinished).

Algorithm
----------
Uses minimax. Assumes opponent always chooses the best path (for it),
and then makes decisions with that assumption.

Creates a tree of every possible move and every possible countermove.
Assuming that the opponent choses best path each time, AI chooses path
that maximizes outcomes for itself.

Board Representation
---------
Flat list (implicitly loops around for next row).

- Empty Space: -1
- O: 0
- X: 1