# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# takes no input and RETURNS two grids. The
# first grid, value, should contain the computed
# value of each cell as shown in the video. The
# second grid, policy, should contain the optimum
# policy for each cell.
#
# Stay tuned for a homework help video! This should
# be available by Thursday and will be visible
# in the course content tab.
#
# Good luck! Keep learning!
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
#
# NOTE: Please do not modify the values of grid,
# success_prob, collision_cost, or cost_step inside
# your function. Doing so could result in your
# submission being inappropriately marked as incorrect.

# -------------
# GLOBAL VARIABLES
#
# You may modify these variables for testing
# purposes, but you should only modify them here.
# Do NOT modify them inside your stochastic_value
# function.

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
       
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
cost_step = 1        
                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.

def get_adjacent_cells(distance, x, y, min_dist_grid):
    result = []
    for i in range(len(delta)):
        x2 = x - delta[i][0]
        y2 = y - delta[i][1]
        if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]) and grid[x2][y2] == 0:
            #if grid[x2][y2] == 0 and min_dist_grid[x2][y2] > distance + cost_step:
            result.append((x2, y2, i))
    return result


def compute_min_dist_grid(distance, x, y, min_dist_grid):
    cells = get_adjacent_cells(distance, x, y, min_dist_grid)
    for (xx, yy) in cells:
        min_dist_grid[xx][yy] = distance + cost_step
    for (xx, yy) in cells:
        compute_min_dist_grid(distance+1, xx, yy, min_dist_grid)


def compute_policy(min_dist_grid):
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                    #print (x, y, x2, y2)
                    if min_dist_grid[x2][y2] < min_dist_grid[x][y] and min_dist_grid[x][y] < 99:
                        policy[x][y] = delta_name[i]
                        break
    policy[goal[0]][goal[1]] = '*'
    return policy


def stochastic_value():
    min_dist_grid = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    #policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    min_dist_grid[goal[0]][goal[1]] = 0
    compute_min_dist_grid(0, goal[0], goal[1], min_dist_grid)
    policy = compute_policy(min_dist_grid)
    return min_dist_grid, policy



m, p = stochastic_value()
for row in m:
    print row
for row in p:
    print row