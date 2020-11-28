from pysat.solvers import Glucose3

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
    
    #Must start at this tile and end at this future tile:
    # for i in range(1, num_of_blocks+1):
    #     if i == starting_tile:
    #         clauses.append([i])
    #     else:
    #         clauses.append([-i])

    # #Must end at this tile, can combine with the above for better efficiency but i don't like the code:
    # for i in range(1 + num_of_blocks * (num_of_tiles - 1), num_of_blocks + num_of_blocks * (num_of_tiles - 1)+1):
    #     if i % num_of_blocks == ending_tile % num_of_blocks:
    #         clauses.append([i])
    #     else:
    #         clauses.append([-i])

    # #Boulders:
    # for i in boulders:
    #     for j in range(num_of_tiles):
    #         clauses.append([-(i + (num_of_blocks * j))])

    # #At least one tile per step:
    # for j in range(1, num_of_tiles):
    #     clauses.append([i + j*num_of_blocks for i in tiles])

    #At most one tile per step:
    # for i in tiles:
    #     for j in tiles:
    #         if j > i:
    #             for k in range(num_of_tiles):
    #                 clauses.append([-(i+num_of_blocks*k),-(j+num_of_blocks*k)])

    #Each tile is used at least once by the end of the path:
    # for i in tiles:
    #     dummy = []
    #     for j in range(num_of_tiles):
    #         dummy.append(i + num_of_blocks * j)
    #     clauses.append(dummy)

    #Each tile is used at most once by the end of the path:
    for i in tiles:
        dummy = [i + num_of_blocks * j for j in range(num_of_tiles)]
        for j in dummy:
            for k in dummy:
                if k > j:
                    clauses.append([-j,-k])
    
    #Path must be continuous (no skipping tiles):






    print(clauses)
    




level = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0]]
level2 = [[0,0,1],[0,0,0],[1,0,0]]
#print(get_tile_types(level))
#don't need to put 0 at the end of each clause, but also generates unused variables 1-10 (since i'm starting with 11)
#How to number variables??? If there are x tiles, then 1,2,...,x = tile on step 1, x+1,...,2x = tile on step 
# g = Glucose3()
# g.add_clause([0,2])
# g.add_clause([-2,5])
# print((g.solve()))
# print(g.get_model())

#test for the 3x3 puzzle (level 1):
create_cnf_rules(level2,8,2)
