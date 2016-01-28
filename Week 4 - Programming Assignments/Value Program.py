# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 1, 0],
#         [0, 0, 0, 0, 1, 0]]
        
        
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']


#pos = [0, goal[0], goal[1]]

looper = True

def compute_value(grid,goal,cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    
    value = [[99 for j in grid[0]] for i in grid]
    open = []
    open.append([0, goal[0], goal[1]])
    value[goal[0]][goal[1]] = 0
    
    while(looper):
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
                        value[x2][y2] = value[x][y] + cost
                        g2 = g + 1 
                        open.append([g2, x2, y2])                    
   
    #print corners
    
    
    # make sure your function returns a grid of values as 
    # demonstrated in the previous video.
    return value 

result = compute_value(grid,goal,cost)

for i in range(len(result)):
    print result[i]
