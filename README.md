TicTacToe AI
============
AI for TicTacToe that uses an exhaustive search to find best move.
Use LeanComputerPlayer vs. ComputerPlayer (the latter is unfinished).

Algorithm
----------
Essentially a minimax algorithm (though I sort of backed into it
accidently).

Creates a tree of every possible move and every possible countermove.
At the end, find the proportion of times a specific next move causes
the AI to lose, and the proportion of times that move causes the AI
to win. 

The AI minimizes the proportion of times it loses and then tiebreaks
by maximizing the proportion of times it wins.

Board Representation
---------
Flat list (implicitly loops around for next row).

- Empty Space: -1
- O: 0
- X: 1