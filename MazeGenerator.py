import os
import random

# class Tile():
#     def __init__(self, x, y, neighbors):
#         self.x = x
#         self.y = y
#         self.is_wall = True
#         self.visited = False
#         self.neighbors = neighbors
#         self.walls = neighbors
#
#
#     # def __repr__(self):
#     #     return f"x:{self.x}, y: {self.y}, is_wall: {self.is_wall}, visited: {self.visited}"
#     def __repr__(self):
#         if self.is_wall:
#             return "0"
#         if self.visited:
#             return "1"
#         return "-1"

def nearby_tiles(x, y, rows, cols, dist):
    cardinal_tiles = [[x - dist, y], [x, y - dist], [x + dist, y], [x, y + dist]]
    wall_list = list(filter(lambda tile: tile[0] in range(0, cols) and tile[1] in range(0, rows), cardinal_tiles))
    #wall_list = [coord for coord in cardinal_tiles if coord[0]<rows and coord[1]<cols]
    return wall_list
#
# def distinct_sets(divided_cells, sets):
#     return True


# Based on prims aglorithm provided by https://www.youtube.com/watch?v=ZXF9-KX4DIQ
def generate_maze_yt(rows, columns):
    maze = [[0] * columns for i in range(rows)]
    frontier_set = []

    # Select random cell in maze, mark as passage.
    x = random.randint(0, columns-1)
    y = random.randint(0, rows-1)
    #x = 4
    #y = 6
    maze[y][x] = -1

    # Compute frontier
    frontier_set = nearby_tiles(x=x, y=y, rows=rows, cols=columns, dist=2)

    #While frontier not empty: pick a frontier cell, set inbetween as passage, add middle's fronteirs to list
    count = 0
    while len(frontier_set) > 0:
        if len(frontier_set) < 2:
            choice = frontier_set.pop(0)
        else:
            choice = frontier_set.pop(random.randrange(0, len(frontier_set) - 1))

        choice_near = (list(filter(lambda tile: maze[tile[1]][tile[0]] == -1, nearby_tiles(x=choice[0], y=choice[1], rows=rows, cols=columns, dist=2))))[0]
        middle_cell = [int((choice_near[0]+choice[0])/2), int((choice_near[1]+choice[1])/2)]
        maze[middle_cell[1]][middle_cell[0]] = -1
        maze[choice[1]][choice[0]] = -1
        if [choice[0],choice[1]] in frontier_set:
            frontier_set.remove([choice[0],choice[1]])
        if [middle_cell[0],middle_cell[1]] in frontier_set:
            frontier_set.remove([middle_cell[0],middle_cell[1]])
        choice_frontier = nearby_tiles(x=choice[0], y=choice[1], rows=rows, cols=columns, dist=2)
        filtered_middle = list(filter(lambda tile: tile not in frontier_set and maze[tile[1]][tile[0]] != -1, choice_frontier))
        frontier_set.extend(filtered_middle)
        # for row in maze:
        #     print(row)
        # print()
        # for row in maze:
        #     for tile in row:
        #         if tile == -1:
        #             print(u"\u25A0", end="")
        #         else:
        #             print(u"\u25A1", end="")
        #     print()
        # print("end")
        #print_maze(maze)
        #print("end")
        maze_to_image(maze, str(count))
        count +=1
    return maze

# Iterative randomized Prim's algorithm (without stack, without sets)
def generate_maze(rows, columns):
    """
    https://en.wikipedia.org/wiki/Maze_generation_algorithm
    This algorithm is a randomized version of Prim's algorithm.

    Start with a grid full of walls.
    Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
    While there are walls in the list:
        Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
            Make the wall a passage and mark the unvisited cell as part of the maze.
            Add the neighboring walls of the cell to the wall list.
        Remove the wall from the list.

    Note that simply running classical Prim's on a graph with random edge weights would create mazes stylistically identical to Kruskal's,
    because they are both minimal spanning tree algorithms.
    Instead, this algorithm introduces stylistic variation because the edges closer to the starting point have a lower effective weight.

        Boardstate is a class which represents a maze
        2 = goal tile
        1 = explored space
        0 = wall
        -1 = unexplored space
    """
    maze = [[0]*columns for i in range(rows)]
    x = random.randint(0, rows-1)
    y = random.randint(0, columns-1)
    maze[x][y] = -1
    #nearby_tiles = [[x-1,y],[x,y-1],[x+1,y],[x,y+1]]
    wall_list = nearby_tiles(x=x, y=y, rows=rows, cols=columns, dist=2)
    # Filter out invalid tile numbers
    #wall_list = list(filter(lambda tile: tile[0] in range(0,rows) and tile[1] in range(0, columns), nearby_tiles))
    while len(wall_list) > 0:
        selected_wall = random.choice(wall_list)
        nearby_selected = list(filter(lambda tile: tile[0] in range(0, rows) and tile[1] in range(0, columns), [[selected_wall[0] - 1, selected_wall[1]], [selected_wall[0], selected_wall[1] - 1], [selected_wall[0] + 1, selected_wall[1]], [selected_wall[0], selected_wall[1] + 1]]))
        nearby_unoccupied_tiles = 0
        for tile in nearby_selected:
            if maze[tile[0]][tile[1]] == -1:
                nearby_unoccupied_tiles+=1
        if(nearby_unoccupied_tiles==1):
            maze[selected_wall[0]][selected_wall[1]] = -1
            #get neighboring walls
           # selected_wall
            #add_tiles = list(filter(lambda tile: tile[0] in range(0, rows) and tile[1] in range(0, columns), se))
           # nearby_selected.extend()

        wall_list.remove(selected_wall)
    return maze

# def generate_maze_kruskal(rows, columns):
#     #maze = [[0] * columns for i in range(rows)]
#     #maze = [[1,2,3],[4,5,6],[7,8,9]]
#
#     #new = {maze[x][y]: item for item in maze}
#     tile_locations = [Tile(x,y,nearby_tiles(x, y, rows, columns)) for x in range(columns) for y in range(rows)]
#     tile_sets = [[x,y] for x in range(columns) for y in range(rows)]
#     print("mylist")
#     print(tile_locations)
#     for tile in sorted(tile_locations, key=lambda _: random.random()):
#         near_tiles = nearby_tiles(x=tile.x, y=tile.y, rows=rows, cols=columns)
#         # if len(list(filter(lambda f: (each_tile in f for each_tile in near_tiles), tile_sets))):
#         #     print(len(list(filter(lambda f: (each_tile in f for each_tile in near_tiles), tile_sets))))
#
#         # for set_tile in tile_sets:
#         #     found = True
#         #     for tile_near in near_tiles:
#         #         if tile_near not in set_tile:
#         #             found = False
#         #     if found:
#         #         print("found")
#
#         # all_seperate_sets = True
#         # joined_list = []
#         # for nearby_tile in near_tiles:
#         #     if nearby_tile not in tile_sets:
#         #         all_seperate_sets = False
#         # if all_seperate_sets:
#         #     for nearby_tile in near_tiles:
#         #         joined_list.append(tile_sets.pop())
#         #     tile_sets.append(joined_list)
#         #     tile.is_wall = False
#
#         all_seperate_sets = distinct_sets(near_tiles, tile_sets)

    print(str(tile_locations))
    print()
    for x in range(columns):
        for y in range(rows):
            print(tile_locations[x+y], end="")
        print()
    return 1
def print_maze(maze):
    for row in maze:
        for tile in row:
            if tile == -1:
                print(u"\u25A0", end="")
            else:
                print(u"\u25A1", end="")
        print()
def maze_to_image(maze, name):
    # create ppm image from array
    rows = len(maze)
    cols = len(maze[0])
    os.makedirs("images", exist_ok=True)
    with open(f"images/{name}.pbm", "w") as image_file:
        image_file.write(f"P1\n{cols} {rows}\n")
        for row in maze:
            for tile in row:
                if tile == -1:
                    image_file.write("0")
                else:
                    image_file.write("1")
            image_file.write("\n")
def cool_func():
    rows = 60
    cols = 49
    new_maze = generate_maze_yt(rows, cols)
    print_maze(new_maze)
    

    #generate_maze_kruskal(5,5)



cool_func()
