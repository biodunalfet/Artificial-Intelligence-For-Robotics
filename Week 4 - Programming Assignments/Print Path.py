# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. Note that the 'v' should be 
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0
    e = 0

    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand[0][0] = 0

    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            e += 1
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
                            expand[x2][y2] = e
                            
    start = True
    sPos = goal

    f = 0

    pathCoordinates = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    while (start):
        motion_temp = []
        gVgoal = expand[goal[0]][goal[1]] + 1
        val = [gVgoal for i in delta]
        store = [[0, 0] for i in delta]
        
        motion = []
        for i in range(len(delta)):
            x2 = sPos[0] + delta[i][0]
            y2 = sPos[1] + delta[i][1]
            
            if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]) and expand[x2][y2] != -1:
            
                store[i] = [x2, y2]
                val[i] = expand[x2][y2]
                motion.append(i)
        
        p = val.index(min(val))
        sPos = [store[p][0], store[p][1]]
        pathCoordinates[sPos[0]][sPos[1]] = delta_name[(p + 2) % 4]
        
        if (sPos == [0, 0]):
            break
    pathCoordinates[goal[0]][goal[1]]= "*"
    return pathCoordinates



print search(grid,init,goal,cost)


        

 
# for i in range(len(pathCoordinates)):
#     print pathCoordinates[i]
    
