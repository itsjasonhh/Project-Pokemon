class Node:
    def __init__(self, value):
        self.value = value
        self.edges = ()
        self.visited = False
#edges in a dictionary: each tile is a key, the value of each key is a list of ints for which other tiles are accessible
def get_dimensions(level):
    rows = len(level)
    columns = len(level[0])
    return rows, columns

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


def create_list_of_edges(level):
    rows, columns = get_dimensions(level)
    tiles, boulders = get_tile_types(level)
    edges = {}
    for tile in tiles:
        if tile <= columns:
            if tile % columns == 1:
                edges[tile] = (tile + 1, tile + columns)
            elif tile % columns == 0:
                edges[tile] = (tile - 1, tile + columns)
            else:
                edges[tile] = (tile - 1, tile + 1, tile + columns)
        elif tile >= 1 + (rows - 1) * columns:
            if tile % columns == 1:
                edges[tile] = (tile - columns, tile + 1)
            elif tile & columns == 0:
                edges[tile] = (tile - columns, tile - 1)
            else:
                edges[tile] = (tile - columns, tile - 1, tile + 1)
        else:
            if tile % columns == 1:
                edges[tile] = (tile - columns, tile + 1, tile + columns)
            elif tile & columns == 0:
                edges[tile] = (tile - columns, tile - 1, tile + columns)
            else:
                edges[tile] = (tile - columns, tile - 1, tile + 1, tile + columns)
    return edges



level3 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0]]
level2 = [[0,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,0,0,1,0,0]]
level1 = [[0,0,1],[0,0,0],[1,0,0]]