# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

# Nachbarn, die noch nicht besucht und innerhalb des Koordsystems liegen
def get_adjacent_cells(distance, x, y, direction, min_dist_grid):
    result = []
    for i in range(len(action)):
        (dx, dy) = forward[direction]
        x2 = x - dx
        y2 = y - dy
        direction2 = (direction - action[i]) % len(forward)
        if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
            if grid[x2][y2] == 0 and (min_dist_grid[x2][y2][direction2] + cost[i]) > distance:
                result.append((x2, y2, direction2, i))
    return result


def compute_min_dist_grid(distance, x, y, direction, min_dist_grid):
    cells = get_adjacent_cells(distance, x, y, direction, min_dist_grid)
    for (xx, yy, dd, i) in cells:
        min_dist_grid[xx][yy][dd] = distance + cost[i]
    for (xx, yy, dd, i) in cells:
        compute_min_dist_grid(distance + cost[i], xx, yy, dd, min_dist_grid)


def create_policy_matrix_3d(min_dist_grid):
    policy = [[[99 for direction in range(len(forward))] for row in range(len(grid[0]))] for col in range(len(grid))]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for direction in range(len(forward)):
                for i in range(len(action)):
                    direction2 = (direction + action[i]) % len(forward)
                    (dx, dy) = forward[direction2]
                    x2 = x + dx
                    y2 = y + dy
                    if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                        #print (x, y, x2, y2)
                        if min_dist_grid[x2][y2][direction2] < min_dist_grid[x][y][direction] and min_dist_grid[x][y][direction] < 999:
                            policy[x][y][direction] = i
                            break
    #
    return policy


def optimum_policy2D():
    min_dist_grid = [[[999 for direction in range(len(forward))] for row in range(len(grid[0]))] for col in range(len(grid))]

    min_dist_grid[goal[0]][goal[1]][1] = 0
    compute_min_dist_grid(0, goal[0], goal[1], 1, min_dist_grid)

    print min_dist_grid[goal[0]][goal[1]]

    for i in range(len(forward)):
        print forward_name[i]
        for row in min_dist_grid:
            print [x[i] for x in row]


    policy3D = create_policy_matrix_3d(min_dist_grid)
    policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    c = init
    while c[0] != goal[0] or c[1] != goal[1]:
        a = policy3D[c[0]][c[1]][c[2]]
        policy2D[c[0]][c[1]] = action_name[a]
        new_direction = (c[2] + action[a]) % len(forward)
        c = (c[0] + forward[new_direction][0], c[1] + forward[new_direction][1], new_direction)

    policy2D[goal[0]][goal[1]] = '*'
    return policy2D # Make sure your function returns the expected grid.


o = optimum_policy2D()
for row in o:
    print row

# for i in range(len(forward)):
#     print forward_name[i]
#     for row in o:
#         print [x[i] for x in row]

