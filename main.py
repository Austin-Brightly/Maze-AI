import copy
import math
import MazeGenerator
#import numpy as np
#import tkinter as tk

class BoardState:
    """
    Boardstate is a class which represents a maze\
    4 = start
    2 = goal tile
    1 = explored space
    0 = wall
    -1 = unexplored space
    """
    def __init__(self, depth=0, last_tile=[0,0], board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
        self.board = board
        self.cols = len(board)
        self.rows = len(board[0])
        self.depth = depth
        self.last_tile = last_tile
        self.goal_tile = self.find_goal()
        self.is_goal_state = int((math.dist(last_tile, self.goal_tile)) < 2) # Doesn't account for diagonals
        self.h_value = self.find_h()

    def __repr__(self):
        return_str = ""
        for item in self.board:
            return_str+=str(item)
            return_str+="\n"
        return return_str

    def print_board(self):
        for row in self.board:
            print(row)
        print()
    # Heuristic function to estimate distance of board to goal-state
    def find_h(self):
        # Depth + distance of tile to goal
        return int(math.dist(self.last_tile, self.goal_tile)) + self.depth

    # Return [x,y] coordinate location of goal tile
    def find_goal(self):
        x = 0
        y = 0

        # Search board for goal tile
        while x < self.cols:
            while y < self.rows:
                if self.board[x][y] == 2:
                    return [x,y]
                y += 1
            y = 0
            x += 1

        # No goal found in maze
        return [0,0]

    # Generate all mutations of self and return as a list. Up to 4 directionals.
    def get_children(self):
        x = self.last_tile[0]
        y = self.last_tile[1]
        new_boards = []  # fill with all possible child boards
        check_coordinates = [[x-1,y],[x,y-1],[x+1,y],[x,y+1]]
        for pair in check_coordinates:
            if pair[0] in range(0,self.cols) and pair[1] in range(0,self.rows):
                if (self.board[pair[0]][pair[1]] not in [2,0]):
                    new_child = copy.deepcopy(self.board)
                    new_child[pair[0]][pair[1]] = 1
                    new_boards.append(BoardState(board=new_child, last_tile=pair, depth=self.depth + 1))
        # for x in range(4)
        #     if self.board[x][y] == 0:
        #         # create child board, modify it with new player action. (ex: new board with x at [0,1])
        #         new_child = copy.deepcopy(self.board)
        #         new_child[x][y] = player
        #         new_boards.append(BoardState(board=new_child, last_tile=[x,y], depth=self.depth+1))
        return new_boards


# Search for the goal tile
def a_star(start):
    # open is sorted by hueristic value
    open = [start]
    closed = []

    # while boardstates are on open, search for goal.
    while len(open) > 0:
        #open.sort(reverse=True, key=lambda x: x.h_value)
        current_item = open.pop(open.index(min(open, key=lambda x: x.h_value)))
        #current_item = open.pop(0)

        closed.append(current_item)
        current_children = current_item.get_children()
        not_duplicate_children = []
        for child in current_children:
            duplicate = False
            for closed_tile in closed:
                if child.board == closed_tile.board:
                    duplicate = True
            if not duplicate:
                not_duplicate_children.append(child)

        for item in not_duplicate_children:
            open.insert(0, item)
            # If goal board found, return success == 1
            if item.is_goal_state:
                return [item, True]
    # no solution, return success==0
    return [closed, False]


if __name__ == '__main__':
    print("A* Search")
    print(a_star(BoardState(board=[[1,-1,-1],[-1,-1,2]], last_tile=[0,0])))
    print("Getting MazeGenerator Board")
    maze_gen_board = MazeGenerator.generate_maze_prim(rows=7, columns=7)
    MazeGenerator.print_maze(maze_gen_board[0])
    print("Getting Board Solution")
    board_solution = a_star(BoardState(board=maze_gen_board[0], last_tile=maze_gen_board[1]))
    print(board_solution[0].board)
    MazeGenerator.print_maze(board_solution[0].board)
    MazeGenerator.maze_to_p3(board_solution[0].board, 'solved_board')
