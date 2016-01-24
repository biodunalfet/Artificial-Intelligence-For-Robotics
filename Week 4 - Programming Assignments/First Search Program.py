# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
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
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0]]
        
# grid = [[0, 1],
#         [0, 0]]
        
        
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

open_cells = []
closed_cells = []
smallest = 0


# def getSmallestGValue(open_cells):
    
#     if (len(open_cells) == 0):
#         return -1
#     else:
#         #get list of g-Values
#         gValue_list = [item[0] for item in open_cells]
#         #get the index of the smallest g-Value
#         index_smallest_cell = gValue_list.index(min(gValue_list))
#         #get the smallest cell (g-Value) and delete from list of open cells
#         smallest_cell = open_cells.pop(index_smallest_cell)
#         #add cell to closed closed_cells
#         closed_cells.append(smallest_cell)
#         #print smallest_cell
#         #print "picked " + str(smallest_cell)
#         return smallest_cell
    
# def createExpansion(cell):
#     row = cell[1][0]
#     col = cell[1][1]
#     gValue = cell[0]
    
#     postionClosedCells = [item[1] for item in closed_cells]
#     maxrow = len(grid) - 1
#     maxcol = len(grid[0]) - 1
    
#     for i in range(0, len(delta)):
#         x_new = row + delta[i][0]
#         y_new = col + delta[i][1]
        
        
#         #valid position
#         if ((x_new >= 0 and x_new <= maxrow) and (y_new >= 0 and y_new <= maxcol)):
#             #check if closed/open
#             #print x_new
#             #print y_new
#             if ([x_new, y_new] not in postionClosedCells): 
#                 if ((grid[x_new][y_new] == 0)):
#                     open_cells.append([gValue + 1, [x_new, y_new]])
    

def search():
    # ----------------------------------------
    # insert code here
    # ----------------------------------------
    
    loopOn = True
    init_GValue =  0
    open_cells.append([init_GValue, init])
    
    while(loopOn):
        cell = 0
        
        if (len(open_cells) == 0):
            cell = -1
        else:
            gValue_list = [item[0] for item in open_cells]
            index_smallest_cell = gValue_list.index(min(gValue_list))
            smallest_cell = open_cells.pop(index_smallest_cell)
            closed_cells.append(smallest_cell)
            cell = smallest_cell
        
        if (cell == -1):
            path = "fail"
            break
        
        if (cell[1][0] == goal[0] and cell[1][1] == goal[1]):
            result = []
            result.append(cell[0] * cost)
            result.append(cell[1][0])
            result.append(cell[1][1])
            path = result
            break
            
        row = cell[1][0]
        col = cell[1][1]
        gValue = cell[0]
        
        postionClosedCells = [item[1] for item in closed_cells]
        maxrow = len(grid) - 1
        maxcol = len(grid[0]) - 1
        
        for i in range(0, len(delta)):
            x_new = row + delta[i][0]
            y_new = col + delta[i][1]
            
            if ((x_new >= 0 and x_new <= maxrow) and (y_new >= 0 and y_new <= maxcol)):
                if ([x_new, y_new] not in postionClosedCells): 
                    if ((grid[x_new][y_new] == 0)):
                        open_cells.append([gValue + 1, [x_new, y_new]])
          
    return path
 
print search()
