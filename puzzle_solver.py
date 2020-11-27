from pysat.solvers import Glucose3

#takes input of [[],[],[],...] where each smaller array is the row, starting from the top of the level. Each smaller [] is a sequence
# of 0s and 1s, where 1 is a boulder and 0 is an unused step.

#takes a level encoding and returns rows, columns. Assumes that the level is a rectangle and is encoded properly 
def get_dimensions(level):
    rows = len(level)
    columns = len(level[0])
    return rows, columns

#takes a level encoding and returns array of tiles and array of boulders
def get_tile_types(level):
    tiles = []
    boulders = []
    tile_counter = 1
    for a in reversed(level):
        for i in a:
            if i == 0:
                tiles.append(tile_counter)
            if i == 1:
                boulders.append(tile_counter)
            tile_counter += 1
    return tiles, boulders

def create_cnf_rules(level):
    rows, columns = get_dimensions(level)
    tiles, boulders = get_tile_types(level)
    num_of_blocks = rows * columns
    num_of_tiles = len(tiles)
    




level = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0]]
#print(get_tile_types(level))

create_cnf_rules(level)
#don't need to put 0 at the end of each clause, but also generates unused variables 1-10 (since i'm starting with 11)
#How to number variables??? If there are x tiles, then 1,2,...,x = tile on step 1, x+1,...,2x = tile on step 
# g = Glucose3()
# g.add_clause([0,2])
# g.add_clause([-2,5])
# print((g.solve()))
# print(g.get_model())

