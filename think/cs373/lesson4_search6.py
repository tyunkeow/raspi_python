# ----------
# User Instructions:
# 
# Create a function optimum_policy() that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell.
# 
# un-navigable cells must contain an empty string
# WITH a space, as shown in the previous video.
# Don't forget to mark the goal with a '*'

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
# modify code below
# ----------------------------------------

def get_adjacent_cells(x, y, min_dist_grid):
    result = []
    for i in range(len(delta)):
        x2 = x + delta[i][0]
        y2 = y + delta[i][1]
        if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
            if grid[x2][y2] == 0 and min_dist_grid[x2][y2] < 99:
                result.append((x2, y2))
    return result

def optimum_policy():
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost_step

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2

    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                    print (x, y, x2, y2)
                    if value[x2][y2] < value[x][y] and value[x][y] < 99:
                        policy[x][y] = delta_name[i]
                        break
    policy[goal[0]][goal[1]] = '*'
    return policy # Make sure your function returns the expected grid.

pol = optimum_policy()
for p in pol:
    print p
