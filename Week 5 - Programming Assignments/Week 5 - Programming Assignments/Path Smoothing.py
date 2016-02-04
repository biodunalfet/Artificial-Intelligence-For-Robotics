# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and 
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite 
# correct).
# -----------

from copy import deepcopy
import matplotlib.pyplot as plt
#from matplotlib.pyplot import plot, ion, show


# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def selectColor(x):
    colors = "roygbv"
    return colors[x%len(colors)]

def smooth(path, weight_data = 0.9, weight_smooth = 0.3, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    #######################
    ### ENTER CODE HERE ###
    #######################
    
    cumm_error = 0
    cfc = 0
    plt.show()
    plt.axis([-1, 5, -1, 5])
    plt.plot([x[0] for x in path] , [y[1] for y in path], 'g-')
    plt.pause(1)
    
    while True:
        
        for i in range(1, len(path) -1):
            for j in range(0, len(path[0])):   
            
                temp = newpath[i][j]
                #y_i_minus = newpath[i - 1][j]
                #y_i_plus = newpath[i + 1][j]
                #y_i = newpath[i][j]
                #x_i = path[i][j]
            
            
                #y_i += (weight_data * (x_i - y_i))  
                #y_i += (weight_smooth * (y_i_minus + y_i_plus - (2 * y_i)))
                newpath[i][j] += weight_data * (path[i][j] - newpath[i][j]) + \
                 weight_smooth * (newpath[i-1][j] + newpath[i+1][j] - 2.0 * newpath[i][j])

                cumm_error += abs(temp - newpath[i][j])
                              
                #newpath[i][j] = newpath[i][j] 
        #break
        if (cumm_error < tolerance):
            plt.axis([-1, 5, -1, 5])
            plt.plot([x[0] for x in newpath] , [y[1] for y in newpath], 'ro')
            break
        else:
            cumm_error = 0
    
        
    return newpath # Leave this line for the grader!

#plt.show()
printpaths(path,smooth(path))
plt.show()
