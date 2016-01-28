# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 

# forward, forward_name, action, and action_name
# grid = [[1, 1, 1, 0, 0, 0],
#         [1, 1, 1, 0, 1, 0],
#         [0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 0, 1, 1],
#         [1, 1, 1, 0, 1, 1]]

# init = [4, 3, 0] # given in the form [row,col,direction]
#                  # direction = 0: up
#                  #             1: left
#                  #             2: down
#                  #             3: right
                
# goal = [2, 0] # given in the form [row,col]

# cost = [2, 1, 20] # cost has 3 values, corresponding to making 
#                   # a right turn, no turn, and a left turn


#cost = [0, 0, 0, 0]
#path_show = 0
#cost = 0                 

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

# def pathOptions(grid,goal,cost):
#     # ----------------------------------------
#     # modify code below
#     # ----------------------------------------
#     value = [[999 for j in grid[0]] for i in grid]
#     open = []
#     open.append([0, goal[0], goal[1]])
#     value[goal[0]][goal[1]] = 0
#     looper = True
    
#     while looper:
#         if (len(open) == 0):
#             break
#         else:
#             open.sort()
#             open.reverse()
#             pos = open.pop()
#             for i in range(len(forward)):
#                 x = pos[1]
#                 y = pos[2]
#                 g = pos[0]
#                 x2 = x + forward[i][0]
#                 y2 = y + forward[i][1]
#                 if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
#                     if value[x2][y2] == 99 and grid[x2][y2] == 0:
#                         value[x2][y2] = value[x][y] + 1
#                         g2 = g + 1 
#                         open.append([g2, x2, y2])       

#     return value

def optimum_policy2D(grid,init,goal,cost):

    value_i = [[99 for j in grid[0]] for i in grid]
    open = []
    open.append([0, goal[0], goal[1]])
    value_i[goal[0]][goal[1]] = 0
    looper = True
    
    while looper:
        if (len(open) == 0):
            break
        else:
            open.sort()
            open.reverse()
            pos = open.pop()
            for i in range(len(forward)):
                x = pos[1]
                y = pos[2]
                g = pos[0]
                x2 = x + forward[i][0]
                y2 = y + forward[i][1]
                if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                    if value_i[x2][y2] == 99 and grid[x2][y2] == 0:
                        value_i[x2][y2] = value_i[x][y] + 1
                        g2 = g + 1 
                        open.append([g2, x2, y2])       

    map = value_i
    
    # for i in range(len(map)):
    #     print map[i]
        
    #print map
    print " "
    
    looper = True
    policy = [[" " for j in grid[0]] for i in grid]
    policy[goal[0]][goal[1]] = "*"
    pos = init
    policy[pos[0]][pos[1]] = "#"
    
    # print "You're pointing to the " + str(forward_name[pos[2]]) + " postion. Goodluck!"
    # print " "
    db = 0
    
    while looper:
        
        db += 1
        
        # if (db == 13):
        #     break
        
        if (pos[0] == goal[0] and pos[1] == goal[1]):
            policy[pos[0]][pos[1]] = "*"
            #print "Congrats you're at the goal"
            break
        else:            
            x = pos[0]
            y = pos[1]
            h = pos[2]
            #print h
            #print "car is facing " + forward_name[h] + " at " + str(x) + " " + str(y)
           
            actions_len = len(action)
            fs = [999] * actions_len
            actions_in_order = [0] * actions_len
            
            for i in range(actions_len):
            
                if action_name[i] == "R":
                    p_action = forward[(h + 3) % 4]
                elif action_name[i] == "#":
                    p_action = forward[h % 4]
                else:
                    p_action = forward[(h + 1) % 4]    
                    
                actions_in_order[i] = p_action
                x2 = x + p_action[0]
                y2 = y + p_action[1]
                
                if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                    #print str(i) + " " + str(x2) + " " + str(y2) + " " +str(map[x2][y2])
                    fs[i] = cost[i] + map[x2][y2]
            
            index_of_cheapest = fs.index(min(fs))
            
            if pos[2] == forward.index(actions_in_order[index_of_cheapest]):
                #print "You're in the right direction"
                map[pos[0]][pos[1]] = 50
                pos[0] += forward[h][0]
                pos[1] += forward[h][1]
                policy[pos[0]][pos[1]] = "#"
            else:                
                #print index_of_cheapest
                #print "You gotta turn " + action_name[index_of_cheapest] + " bruh"
                pos[2] = forward.index(actions_in_order[index_of_cheapest])
                #print pos[2]
                policy[pos[0]][pos[1]] = action_name[index_of_cheapest]                     

            #print fs
            #print "car is facing " + forward_name[pos[2]] + " at " + str(pos[0]) + " " + str(pos[1])
            #print " "
            
    return policy

    
grid = [[0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 0],
[0, 1, 0, 0, 0, 1, 0],
[0, 1, 0, 1, 0, 1, 0],
[0, 1, 0, 1, 0, 0, 0],
[0, 1, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0]]
init = [0, 0, 3]
goal = [4, 2]
cost = [10, 40, 65]    

# grid = [[1, 1, 1, 0, 0, 0],
#         [1, 1, 1, 0, 1, 0],
#         [0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 0, 1, 1],
#         [1, 1, 1, 0, 1, 1]]
# init = [4, 3, 0]
# goal = [2, 0]
# cost = [2, 1, 20]

result = optimum_policy2D(grid,init,goal,cost)

print result
for i in range(len(result)):
    print result[i]



