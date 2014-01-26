# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.
print goal

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1


def pick_shortest(list):
    k = 0
    for i in range(len(list)):
        if list[i][0] < list[k][0]:
                k = i
    return list[k]

def search():
    # ----------------------------------------
    # insert code here and make sure it returns the appropriate result
    # ----------------------------------------
    expand = [[-1*grid[col][row] for row in range(len(grid[0]))] for col in range(len(grid))]
    print expand
    visited = []
    open = [[0, init[0], init[1]]]

    while True:
        if len(open) == 0:
            return "fail"

        # pick coordinates with shortest path
        k = 0
        for i in range(len(open)):
            if open[i][0] < open[k][0]:
                k = i

        node_cost, y, x = min_node = open[k]
        open.remove(min_node)

        if [y, x] == goal:
            return min_node
        else:
            visited.append([x, y])
            for d in delta:
                xd, yd = x + d[0], y + d[1]
                if xd < 0 or xd > len(grid[0])-1:
                    continue
                if yd < 0 or yd > len(grid)-1:
                    continue
                if [xd, yd] in visited:
                    continue
                if grid[yd][xd] == 1:
                    continue
                new_node = [node_cost+cost, yd, xd]
                if not new_node in open:
                    open.append(new_node)
        print open

    #return path # you should RETURN your result

print search()

