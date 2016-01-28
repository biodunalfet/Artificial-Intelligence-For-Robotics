# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def optimum_policy(grid,goal,cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    value = [[99 for j in grid[0]] for i in grid]
    open = []
    open.append([0, goal[0], goal[1]])
    value[goal[0]][goal[1]] = 0
    looper = True
    policy = [[" " for j in grid[0]] for i in grid]
    policy[goal[0]][goal[1]] = "*"
    
    while looper:
        if (len(open) == 0):
            break
        else:
            open.sort()
            open.reverse()
            pos = open.pop()
            for i in range(len(delta)):
                x = pos[1]
                y = pos[2]
                g = pos[0]
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                    if value[x2][y2] == 99 and grid[x2][y2] == 0:
                        policy[x2][y2] = delta_name[(i + 2) % 4]
                        value[x2][y2] = value[x][y] + cost
                        g2 = g + 1 
                        open.append([g2, x2, y2])       

    return policy

result = optimum_policy(grid,goal,cost)

for i in range(len(result)):
    print result[i]