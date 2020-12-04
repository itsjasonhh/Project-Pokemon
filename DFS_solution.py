level3 = [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0]]
level2 = [[0,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,0,0,1,0,0]]
level1 = [[0,0,1],[0,0,0],[1,0,0]]
level4 = [
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
  [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]


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
            elif tile % columns == 0:
                edges[tile] = (tile - columns, tile - 1)
            else:
                edges[tile] = (tile - columns, tile - 1, tile + 1)
        else:
            if tile % columns == 1:
                edges[tile] = (tile - columns, tile + 1, tile + columns)
            elif tile % columns == 0:
                edges[tile] = (tile - columns, tile - 1, tile + columns)
            else:
                edges[tile] = (tile - columns, tile - 1, tile + 1, tile + columns)
    for tile in boulders:
        edges[tile] = ()
    return edges


def solve_by_dfs(level, start, end):
    edges = create_list_of_edges(level)
    rows, columns = get_dimensions(level)
    tiles, boulders = get_tile_types(level)
    unvisited = tiles.copy()
    solution = []
    return traverse(unvisited,start,end,[],edges)


#board updates per recursive call, so maybe have each call generate its own copy of board to modify and path update
# so if it's not a solution, we don't have to backtrack and undo any changes made 

#Need to fix: prints out correctly, but returns None.

#unvisited is an array of positive ints, e.g. [1,3,4,5]
#start is an int in unvisited, e.g. 4
#end is an int in unvisited, e.g. 5
#edges is a dictionary, each key is an int in unvisited, each value is a list of connected nodes
#edges looks like {1: (4,5), 3: (1), 4: (1,3,5), 5: (1,4)}
#Goal is to use DFS to go from start to end while visiting all unvisited nodes, and return the path
#e.g. 4 -> 3 -> 1 -> 5 
def traverse(unvisited, start, end, path, edges,sol):
    copy_unvisited = unvisited.copy()
    copy_path = path.copy()
    current = start
    copy_unvisited.remove(current)
    copy_path.append(current)
    if current == end and len(copy_unvisited)==0:
        if len(sol) == 0:
            for i in copy_path:
                sol.append(i)
    for i in edges[current]:
        if i in copy_unvisited:
            traverse(copy_unvisited, i, end, copy_path, edges,sol)
    return sol


edges1 = create_list_of_edges(level1)
print(traverse([1,2,4,5,6,8,9], 8, 2, [], edges1, []))
edges2 = create_list_of_edges(level2)
tiles,boulders = get_tile_types(level2)
print(traverse(tiles,18,4,[],edges2,[]))
edges3 = create_list_of_edges(level3)
tiles2, boulders2 = get_tile_types(level3)
print(traverse(tiles2,39,6,[],edges3,[]))
edges4 = create_list_of_edges(level4)
tiles4, boulders4 = get_tile_types(level4)
print(traverse(tiles4,39,6,[],edges4,[]))

