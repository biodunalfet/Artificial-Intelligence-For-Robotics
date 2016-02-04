# -------------
# User Instructions
#
# Here you will be implementing a cyclic smoothing
# algorithm. This algorithm should not fix the end
# points (as you did in the unit quizzes). You  
# should use the gradient descent equations that
# you used previously.
#
# Your function should return the newpath that it
# calculates.
#
# Feel free to use the provided solution_check function
# to test your code. You can find it at the bottom.
#
# --------------
# Testing Instructions
# 
# To test your code, call the solution_check function with
# two arguments. The first argument should be the result of your
# smooth function. The second should be the corresponding answer.
# For example, calling
#
# solution_check(smooth(testpath1), answer1)
#
# should return True if your answer is correct and False if
# it is not.

from math import *
from copy import deepcopy
import matplotlib.pyplot as plt

# Do not modify path inside your function.
path=[[0, 0], 
      [1, 0],
      [2, 0],
      [3, 0],
      [4, 0],
      [5, 0],
      [6, 0],
      [6, 1],
      [6, 2],
      [6, 3],
      [5, 3],
      [4, 3],
      [3, 3],
      [2, 3],
      [1, 3],
      [0, 3],
      [0, 2],
      [0, 1]]

############# ONLY ENTER CODE BELOW THIS LINE ##########

# ------------------------------------------------
# smooth coordinates
# If your code is timing out, make the tolerance parameter
# larger to decrease run time.
#

def smooth(path, weight_data = 0.1, weight_smooth = 0.1, tolerance = 0.00001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)
    plt.show()
    plt.axis([-1, 7, -1, 7])
    plt.plot([x[0] for x in path] , [y[1] for y in path], 'g-')
    plt.pause(1)
    # 
    # Enter code here
    #
    cumm_error = 0
    while True:
        
        for i in range(0, len(path)):
            for j in range(0, len(path[0])):   
            
                temp = newpath[i][j]
                newpath[i][j] += weight_data * (path[i][j] - newpath[i][j]) + \
                 weight_smooth * (newpath[(i-1)% len(path)][j] + newpath[(i+1) % len(path)][j] - 2.0 * newpath[i][j])

                cumm_error += abs(temp - newpath[i][j])
                              
                #newpath[i][j] = newpath[i][j] 
        #break
        if (cumm_error < tolerance):
            print newpath
            plt.axis([-1, 7, -1, 7])
            plt.plot([x[0] for x in newpath] , [y[1] for y in newpath], 'ro')
            plt.pause(0.1)
            #plt.show()
            break
        else:
            cumm_error = 0
    
    return newpath

# thank you - EnTerr - for posting this on our discussion forum

#newpath = smooth(path)
#for i in range(len(path)):
#    print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'


##### TESTING ######

# --------------------------------------------------
# check if two numbers are 'close enough,'used in
# solution_check function.
#
def close_enough(user_answer, true_answer, epsilon = 0.001):
    if abs(user_answer - true_answer) > epsilon:
        return False
    return True

# --------------------------------------------------
# check your solution against our reference solution for
# a variety of test cases (given below)
#
def solution_check(newpath, answer):
    if type(newpath) != type(answer):
        print "Error. You do not return a list."
        return False
    if len(newpath) != len(answer):
        print 'Error. Your newpath is not the correct length.'
        return False
    if len(newpath[0]) != len(answer[0]):
        print 'Error. Your entries do not contain an (x, y) coordinate pair.'
        return False
    for i in range(len(newpath)): 
        for j in range(len(newpath[0])):
            if not close_enough(newpath[i][j], answer[i][j]):
                print 'Error, at least one of your entries is not correct.'
                return False
    print "Test case correct!"
    return True

# --------------
# Testing Instructions
# 
# To test your code, call the solution_check function with
# two arguments. The first argument should be the result of your
# smooth function. The second should be the corresponding answer.
# For example, calling
#
# solution_check(smooth(testpath1), answer1)
#
# should return True if your answer is correct and False if
# it is not.
    
testpath1 = [[0, 0],
             [1, 0],
             [2, 0],
             [3, 0],
             [4, 0],
             [5, 0],
             [6, 0],
             [6, 1],
             [6, 2],
             [6, 3],
             [5, 3],
             [4, 3],
             [3, 3],
             [2, 3],
             [1, 3],
             [0, 3],
             [0, 2],
             [0, 1]]

#[[0, 0], 
# [0.9967235121445233, 0.002931680909966322], 
# [1.9901686095672608, 0.008795534796866572], 
# [2.9737789287970426, 0.023455665866683056], 
# [3.931163610447162, 0.061572211054109066], 
# [4.819706485694734, 0.1612614592435749], 
# [5.527949954343564, 0.4222121646394302], 
# [5.764137414827135, 1.105374362637527], 
# [5.7644566583387995, 1.8939094936108294], 
# [5.529227609685471, 2.576351944260887], 
# [4.823222155072526, 2.8351435330888615], 
# [3.9404358964718758, 2.9290754126202225], 
# [2.9980836093886136, 2.9520792809106386], 
# [2.053813889569799, 2.9271591072564], 
# [1.163357661115749, 2.829395094246875], 
# [0.4362590704642022, 2.5610238383275243], 
# [0.1454196622565017, 1.8536748544580561], 
# [0, 1]]

answer1 = [[0.4705860385182691, 0.4235279620576893], 
           [1.1764695730296597, 0.16470408411716733], 
           [2.058823799247812, 0.07058633859438503], 
           [3.000001503542886, 0.04705708651959327], 
           [3.9411790099468273, 0.07058689299792453], 
           [4.8235326678889345, 0.16470511854183797], 
           [5.529415336860586, 0.4235293374365447], 
           [5.76470933698621, 1.1058829941330384], 
           [5.764708805535902, 1.8941189433780983], 
           [5.5294138118186265, 2.5764724018811056], 
           [4.823530348360371, 2.835296251305122], 
           [3.941176199414957, 2.929413985845729],
           [2.9999985709076413, 2.952943245204772], 
           [2.0588211310939526, 2.9294134622132018], 
           [1.1764675231284938, 2.8352952720424938], 
           [0.4705848811030855, 2.5764710948028178], 
           [0.23529088056307781, 1.8941174802285707], 
           [0.23529138316655338, 1.1058815684272394]]

testpath2 = [[1, 0], # Move in the shape of a plus sign
             [2, 0],
             [2, 1],
             [3, 1],
             [3, 2],
             [2, 2],
             [2, 3],
             [1, 3],
             [1, 2],
             [0, 2], 
             [0, 1],
             [1, 1]]

answer2 = [[1.2222234770374059, 0.4444422843711052],
           [1.7777807251383388, 0.4444432993123497], 
           [2.111114925633848, 0.8888894279539462], 
           [2.5555592020540376, 1.2222246475393077], 
           [2.5555580686154244, 1.7777817817879298], 
           [2.111111849558437, 2.1111159707965514], 
           [1.7777765871460525, 2.55556033483712], 
           [1.2222194640861452, 2.5555593592828543], 
           [0.8888853322565222, 2.111113321684573], 
           [0.44444105139827167, 1.777778212019149], 
           [0.44444210978390364, 1.2222211690821811], 
           [0.8888882042812255, 0.8888870211766268]]

solution_check(smooth(testpath1), answer1)
# solution_check(smooth(testpath2), answer2)
plt.axis([-1, 7, -1, 7])
plt.plot([x[0] for x in answer1] , [y[1] for y in answer1], 'mo')
plt.pause(0.1)
plt.show()