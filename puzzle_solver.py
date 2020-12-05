import timeit
from pysat.solvers import Glucose3


level3 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0]]
level2 = [[0,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,0,0,1,0,0]]
level1 = [[0,0,1],[0,0,0],[1,0,0]]
level4 = [
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
  [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
#takes input of [[],[],[],...] where each smaller array is the row, starting from the top of the level. Each smaller [] is a sequence
# of 0s and 1s, where 1 is a boulder and 0 is an unused step.

#takes a level encoding and returns the number of rows and columns. Assumes that the level is a rectangle and is encoded properly 
def get_dimensions(level):
    rows = len(level)
    columns = len(level[0])
    return rows, columns

#takes a level encoding and returns array of tiles and array of boulders, numbered from  top left to bottom right
def get_tile_types(level):
    tiles = []
    boulders = []
    tile_counter = 1
    for a in level:
        for i in a:
            if i == 0:
                tiles.append(tile_counter)
            if i == 1:
                boulders.append(tile_counter)
            tile_counter += 1
    return tiles, boulders

#takes a level, starting tile #, and ending tile # and returns a large array of CNF clauses encoding the level and puzzle rules
def create_cnf_rules(level, starting_tile, ending_tile):
    rows, columns = get_dimensions(level)
    tiles, boulders = get_tile_types(level)
    num_of_blocks = rows * columns
    num_of_tiles = len(tiles)
    #clauses is an array of arrays
    clauses = []

    #Must start at this tile:
    for i in tiles:
        if i == starting_tile:
            clauses.append([i])
        else:
            clauses.append([-i])

    #Must end at this tile:
    for i in tiles:
        if i == ending_tile:
            clauses.append([i + (num_of_tiles-1)*num_of_blocks])
        else:
            clauses.append([-(i + (num_of_tiles-1)*num_of_blocks)])

    #Boulders:
    for i in boulders:
        for j in range(num_of_tiles):
            clauses.append([-(i + (num_of_blocks * j))])

    #At least one tile per step:
    for j in range(1, num_of_tiles):
        clauses.append([i + j*num_of_blocks for i in tiles])

    #At most one tile per step:
    for i in tiles:
        for j in tiles:
            if j > i:
                for k in range(num_of_tiles):
                    clauses.append([-(i+num_of_blocks*k),-(j+num_of_blocks*k)])

    #Each tile is used at least once by the end of the path:
    for i in tiles:
        dummy = []
        for j in range(num_of_tiles):
            dummy.append(i + num_of_blocks * j)
        clauses.append(dummy)

    #Each tile is used at most once by the end of the path:
    for i in tiles:
        dummy = [i + num_of_blocks * j for j in range(num_of_tiles)]
        for j in dummy:
            for k in dummy:
                if k > j:
                    clauses.append([-j,-k])
    
    #Path must be continuous (no skipping tiles): This works for only the first step, now need to extend to further steps. 
    for i in tiles:
        if i <= columns:
            if i % columns == 1:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i + k*num_of_blocks), i + k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            elif i % columns == 0:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks),i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            else:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i +k*num_of_blocks + 1 + num_of_blocks, i +k*num_of_blocks - 1 + num_of_blocks, i +k*num_of_blocks + columns + num_of_blocks])
        elif i >= 1 + (rows-1)*columns:
            if i % columns == 1:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks - columns + num_of_blocks])
            elif i % columns == 0:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks - columns + num_of_blocks])
            else:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks - columns + num_of_blocks])
        else:
            if i % columns == 1:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - columns + num_of_blocks, i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            elif i % columns == 0:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - columns + num_of_blocks, i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            else:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - columns + num_of_blocks, i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
    return clauses
    


def solve_puzzle(level, starting_tile, ending_tile):
    rows, columns = get_dimensions(level)
    blocks = rows * columns
    clauses = create_cnf_rules(level, starting_tile, ending_tile)
    solver = Glucose3()
    for i in clauses:
        solver.add_clause(i)
    if solver.solve() == False:
        print("No solution!")
        return
    else:
        solutions = []
        for i in solver.get_model():
            if i > 0:
                while i > blocks:
                    i -= blocks
                solutions.append(i)
        return solutions


print(timeit.timeit(
    """from pysat.solvers import Glucose3


level3 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0]]
level2 = [[0,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,0,0,1,0,0]]
level1 = [[0,0,1],[0,0,0],[1,0,0]]
level4 = [
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
  [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
#takes input of [[],[],[],...] where each smaller array is the row, starting from the top of the level. Each smaller [] is a sequence
# of 0s and 1s, where 1 is a boulder and 0 is an unused step.

#takes a level encoding and returns the number of rows and columns. Assumes that the level is a rectangle and is encoded properly 
def get_dimensions(level):
    rows = len(level)
    columns = len(level[0])
    return rows, columns

#takes a level encoding and returns array of tiles and array of boulders, numbered from  top left to bottom right
def get_tile_types(level):
    tiles = []
    boulders = []
    tile_counter = 1
    for a in level:
        for i in a:
            if i == 0:
                tiles.append(tile_counter)
            if i == 1:
                boulders.append(tile_counter)
            tile_counter += 1
    return tiles, boulders

#takes a level, starting tile #, and ending tile # and returns a large array of CNF clauses encoding the level and puzzle rules
def create_cnf_rules(level, starting_tile, ending_tile):
    rows, columns = get_dimensions(level)
    tiles, boulders = get_tile_types(level)
    num_of_blocks = rows * columns
    num_of_tiles = len(tiles)
    #clauses is an array of arrays
    clauses = []

    #Must start at this tile:
    for i in tiles:
        if i == starting_tile:
            clauses.append([i])
        else:
            clauses.append([-i])

    #Must end at this tile:
    for i in tiles:
        if i == ending_tile:
            clauses.append([i + (num_of_tiles-1)*num_of_blocks])
        else:
            clauses.append([-(i + (num_of_tiles-1)*num_of_blocks)])

    #Boulders:
    for i in boulders:
        for j in range(num_of_tiles):
            clauses.append([-(i + (num_of_blocks * j))])

    #At least one tile per step:
    for j in range(1, num_of_tiles):
        clauses.append([i + j*num_of_blocks for i in tiles])

    #At most one tile per step:
    for i in tiles:
        for j in tiles:
            if j > i:
                for k in range(num_of_tiles):
                    clauses.append([-(i+num_of_blocks*k),-(j+num_of_blocks*k)])

    #Each tile is used at least once by the end of the path:
    for i in tiles:
        dummy = []
        for j in range(num_of_tiles):
            dummy.append(i + num_of_blocks * j)
        clauses.append(dummy)

    #Each tile is used at most once by the end of the path:
    for i in tiles:
        dummy = [i + num_of_blocks * j for j in range(num_of_tiles)]
        for j in dummy:
            for k in dummy:
                if k > j:
                    clauses.append([-j,-k])
    
    #Path must be continuous (no skipping tiles): This works for only the first step, now need to extend to further steps. 
    for i in tiles:
        if i <= columns:
            if i % columns == 1:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i + k*num_of_blocks), i + k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            elif i % columns == 0:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks),i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            else:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i +k*num_of_blocks + 1 + num_of_blocks, i +k*num_of_blocks - 1 + num_of_blocks, i +k*num_of_blocks + columns + num_of_blocks])
        elif i >= 1 + (rows-1)*columns:
            if i % columns == 1:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks - columns + num_of_blocks])
            elif i % columns == 0:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks - columns + num_of_blocks])
            else:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks - columns + num_of_blocks])
        else:
            if i % columns == 1:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - columns + num_of_blocks, i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            elif i % columns == 0:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - columns + num_of_blocks, i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
            else:
                for k in range(num_of_tiles-1):
                    clauses.append([-(i+k*num_of_blocks), i+k*num_of_blocks - columns + num_of_blocks, i+k*num_of_blocks + 1 + num_of_blocks, i+k*num_of_blocks - 1 + num_of_blocks, i+k*num_of_blocks + columns + num_of_blocks])
    return clauses
    


def solve_puzzle(level, starting_tile, ending_tile):
    rows, columns = get_dimensions(level)
    blocks = rows * columns
    clauses = create_cnf_rules(level, starting_tile, ending_tile)
    solver = Glucose3()
    for i in clauses:
        solver.add_clause(i)
    if solver.solve() == False:
        print("No solution!")
        return
    else:
        solutions = []
        for i in solver.get_model():
            if i > 0:
                while i > blocks:
                    i -= blocks
                solutions.append(i)
        return solutions

solve_puzzle(level3,39,6)""", 
        number=1
))

