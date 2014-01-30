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

grid = [[0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
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

# Nachbarn, die noch nicht besucht und innerhalb des Koordsystems liegen
def get_adjacent_cells(distance, x, y, min_dist_grid):
    result = []
    for i in range(len(delta)):
        x2 = x + delta[i][0]
        y2 = y + delta[i][1]
        if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
            if grid[x2][y2] == 0 and min_dist_grid[x2][y2] > distance:
                result.append((x2, y2))
    return result


def compute_value2(distance, x, y, min_dist_grid):
    cells = get_adjacent_cells(distance, x, y, min_dist_grid)
    for (xx, yy) in cells:
        min_dist_grid[xx][yy] = distance + cost_step
    for (xx, yy) in cells:
        compute_value2(distance+1, xx, yy, min_dist_grid)


def compute_value():
    result = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    #print result
    result[goal[0]][goal[1]] = 0
    compute_value2(0, goal[0], goal[1], result)
    return result

r = compute_value()
for l in r:
    print l
