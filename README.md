# Project-Pokemon

This repository contains a program to solve the puzzles found in Sootopolis City Gym, from the games Pokemon Ruby and Pokemon Emerald. In the puzzle, the player must step on every tile on a level before the ladder appears. Thus, the player must start at the bottom center of each level, step on every tile, and end on the top center of the level. 

To solve the problem, the level is encoded as an array of 0s and 1s, where 1 represents boulders and 0 represents a possible step. After reading in the layout of the level, the function "create_cnf_rules" creates an encoding of the rules specific to the level. Then, the rules are run through a SAT solver to solve the puzzle.

More details to come.
