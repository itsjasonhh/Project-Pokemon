# Project-Pokemon

This repository contains a program to solve the puzzles found in Sootopolis City Gym, from the games Pokemon Ruby and Pokemon Emerald. In the puzzle, the player must step on every tile on a level before the ladder appears. Thus, the player must start at the bottom center of each level, step on every tile, and end on the top center of the level. 

![Sootpolis Gym Puzzle](RS_Sootopolis_Gym.png)

To solve the problem, the level is encoded as an array of 0s and 1s, where 1 represents boulders and 0 represents a possible step. After reading in the layout of the level, the function "create_cnf_rules" creates an encoding of the rules specific to the level. Then, the rules are run through a SAT solver to solve the puzzle.

For the encoding, the tiles are numbered from top left corner, left to right, top to bottom FOR EACH STEP. For example, in the bottom-level puzzle, for the first step, the tiles are labeled from 1 to 9, with tiles 3 and 7 being boulders. The player starts on tile 8. For the second step, the tiles are labeled from 10 to 18, and so on for the 7 total steps. Thus, the player needs to end on tile 56, which is the same tile as tile 2, except tile 56 represents the 7th (last) step, while tile 2 represents the first step. In this example then, there are 63 total Boolean variables created, each representing a tile at a particular step.

These rules are encoded into the SAT Solver: 

1. The player must start on the given "start" tile.
2. The player must end on the given "end" tile.
3. For each step, at least one tile must be true.
4. For each step, at most one tile must be true. (Together with 3, this means only one tile is true at each step. This makes sense since the character may occupy only one tile at a time).
5. Each tile is used at least once by the end of the path.
6. Each tile is used at most once by the end of the path. (Together with 5, this means each tile is used exactly once by the end of the path, a necessary condition for the puzzle).
7. The path must be continuous (the player cannot jump between two disconnected tiles).




Also in this repo is a DFS solution to finding the correct path. In each of puzzle_solver.py and DFS_solution.py, there is code for using the TimeIt module. The SAT-Solver solution is generally quicker than the DFS solution, although the results may be biased due to how the puzzles are oriented. 
