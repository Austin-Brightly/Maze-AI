import os
import random
import sys

# Randomly selects a border wall to become the exit wall
# TODO: Create more elegant solution/ fix problem of multiple walls
def create_end_tile(maze, rows, columns, position):
    # POSITION: top=1, bottom=2, left=3, right=any other number
    if position == 1:
        end_created = False
        top_index = 1
        while not end_created and top_index in range(1, columns - 1):
            if maze[1][top_index-1] == -1:
                maze[0][top_index-1] = 2
                end_created = True
            top_index += 1
    elif position == 2:
        end_created = False
        top_index = 1
        while not end_created and top_index in range(1, columns - 1):
            if maze[rows-2][top_index] == -1:
                maze[rows-1][top_index] = 2
                end_created = True
            top_index += 1
    elif position == 3:
        end_created = False
        top_index = 1
        while not end_created and top_index in range(1, columns - 1):
            if maze[top_index-1][1] == -1:
                maze[top_index-1][0] = 2
                end_created = True
            top_index += 1
    else:
        end_created = False
        top_index = 1
        while not end_created and top_index in range(1, rows - 1):
            #print(f"top_index:{top_index}, columns:{columns}")
            if maze[top_index-1][columns-2] == -1:
                maze[top_index-1][columns-1] = 2
                end_created = True
            top_index += 1
    return maze

# Returns tile coordinates with a distance of the variable ('distance')'s tiles
def nearby_tiles(x, y, rows, cols, dist):
    cardinal_tiles = [[x - dist, y], [x, y - dist], [x + dist, y], [x, y + dist]]
    wall_list = list(filter(lambda tile: tile[0] in range(1, cols) and tile[1] in range(1, rows), cardinal_tiles))
    #wall_list = [coord for coord in cardinal_tiles if coord[0]<rows and coord[1]<cols]
    return wall_list


# Based on prims algorithm provided by https://www.youtube.com/watch?v=ZXF9-KX4DIQ
# TODO: Fix extra walls on certain size mazes, or account for them
def generate_maze_prim(rows, columns):
    # Initialize maze to all walls, create frontier set
    maze = [[0] * columns for i in range(rows)]
    frontier_set = []

    # Select random cell in maze, mark as passage.
    #x = random.randint(1, columns-2)
    #y = random.randint(1, rows-2)
    x = int(columns/2)
    y = int(rows/2)
    maze[y][x] = -1

    # Compute frontier
    frontier_set = nearby_tiles(x=x, y=y, rows=rows-1, cols=columns-1, dist=2)

    # While frontier not empty: pick a frontier cell, set inbetween as passage, add middle's frontiers to list
    count = 0
    while len(frontier_set) > 0:
        if len(frontier_set) < 2:
            choice = frontier_set.pop(0)
        else:
            choice = frontier_set.pop(random.randrange(0, len(frontier_set) - 1))

        tiles_near_choice = (list(filter(lambda tile: maze[tile[1]][tile[0]] == -1, nearby_tiles(x=choice[0], y=choice[1], rows=rows, cols=columns, dist=2))))
        filtered_near_tiles = list(filter(lambda tile: tile not in frontier_set and tile[0] in range(columns-1) and tile[1] in range(rows-1), tiles_near_choice))[0]
        middle_cell = [int((filtered_near_tiles[0]+choice[0])/2), int((filtered_near_tiles[1]+choice[1])/2)]
        maze[middle_cell[1]][middle_cell[0]] = -1
        maze[choice[1]][choice[0]] = -1
        if [choice[0],choice[1]] in frontier_set:
            frontier_set.remove([choice[0],choice[1]])
        if [middle_cell[0],middle_cell[1]] in frontier_set:
            frontier_set.remove([middle_cell[0],middle_cell[1]])
        choice_frontier = nearby_tiles(x=choice[0], y=choice[1], rows=rows, cols=columns, dist=2)
        filtered_middle = list(filter(lambda tile: tile not in frontier_set and maze[tile[1]][tile[0]] != -1 and tile[0] in range(columns-1) and tile[1] in range(rows-1), choice_frontier))
        frontier_set.extend(filtered_middle)
        #maze_to_image(maze, str(count))
        count +=1
    #create start
    maze[y][x] = 4

    #create end and return
    return (create_end_tile(maze, rows, columns, 4), [x,y])

     #create end bottom


    return maze

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
            if tile == 0:
                print(u"\u25A1", end="")
            else:
                print(u"\u25A0", end="")
        print()
def maze_to_p1(maze, name):
    # create ppm image from array
    rows = len(maze)
    cols = len(maze[0])
    os.makedirs("images", exist_ok=True)
    with open(f"images/{name}.pbm", "w") as image_file:
        image_file.write(f"P1\n{cols} {rows}\n")
        for row in maze:
            for tile in row:
                if tile == 0:
                    image_file.write("1")
                else:
                    image_file.write("0")
            image_file.write("\n")
def maze_to_p3(maze, name):
    # Define some colors
    black = "0 0 0 "
    white = "255 255 255 "
    red = "0 255 0 "
    green = "0 0 255 "
    yellow = "255 255 0 "

    # create ppm image from array
    rows = len(maze)
    cols = len(maze[0])
    os.makedirs("images", exist_ok=True)
    with open(f"images/{name}.ppm", "w") as image_file:
        image_file.write(f"P3\n{cols} {rows}\n255\n")
        for row in maze:
            line = ""
            for tile in row:
                if tile == 0:
                    line += black
                elif tile == 1:
                    line += yellow
                elif tile == 2:
                    line += green
                elif tile == 3:
                    line += black
                elif tile == 4:
                    line += red
                else:
                    line += white
            image_file.write(line.strip()+"\n")

if __name__ == '__main__':
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    new_maze = generate_maze_prim(rows, cols)
    print_maze(new_maze[0])
    maze_to_p3(new_maze, "maze")
    

    #generate_maze_kruskal(5,5)

