# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def test_adjacent(x, y, result, callback):
    for i in range(len(delta)):
        x2 = x + delta[i][0]
        y2 = y + delta[i][1]
        if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
            if grid[x2][y2] == 0 and result[x2][y2] == 99:
                callback(x2, y2)

def compute_value2(distance, current_cell, result):
    test_adjacent(current_cell[0], current_cell[1], result, lambda x2, y2: result[x2][y2]=distance+1)

    return value #make sure your function returns a grid of values as demonstrated in the previous video.

def compute_value():
    result = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    current_cell = goal
    return compute_value2(0, current_cell, result)



