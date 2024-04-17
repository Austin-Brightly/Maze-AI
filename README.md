# Maze-AI
An AI to find a solution to any given maze. Uses the A* algorithm to find a solution to a given maze.

# Running Maze-AI
You can randomly generate a maze and it's solution by running main with parameters rows and columns
'''
python (number of rows) (number of columns)
'''
The output of the program is a PPM file, and can be found in /images folder.

Example output:
![Image of a solved maze.](/images/example_solved)

# How it works
Main.py starts by calling MazeGenerator.py. MazeGenerator creates a random maze using [Prims Algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm). It gives the maze a start and exit, then returns the maze to main. Main then solves the maze using the [A* algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm), and saves the result to a PPM file.