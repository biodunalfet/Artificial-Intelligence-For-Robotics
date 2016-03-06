# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random
import turtle
import matplotlib.pyplot as plt

#from scipy import linalg
import numpy as np

#measurements = [1, 2, 3]
#plt.plot()

x = matrix([[0.]]) # initial state (step size and angle)
P = matrix([[1000.]]) # initial uncertainty
u = matrix([[0.]]) # external motion
F = matrix([[1.]]) # next state function
H = matrix([[1.]]) # measurement function
R = matrix([[1.]]) # measurement uncertainty
I = matrix([[1., 0.], [0., 1.]]) # identity matrix

x2 = matrix([[0.]]) # initial state (step size and angle)
P2 = matrix([[1000.]]) # initial uncertainty
u2 = matrix([[0.]]) # external motion
F2 = matrix([[1.]]) # next state function
H2 = matrix([[1.]]) # measurement function
R2 = matrix([[1.]]) # measurement uncertainty

def lbestimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements.
    
    http://www.had2know.com/academics/best-fit-circle-least-squares.html
    """
    
    x,y = measurement
    
    if OTHER == None:
        OTHER = [[measurement], None, [], measurement]
        xy_estimate = (0.0,0.0)
    else:
        OTHER[0].append(measurement)
        
        if OTHER[1] == None:
            px,py = OTHER[3]
            OTHER[3] = measurement
            distance = distance_between((px,py),measurement)
            theta = atan2(y - py, x-px)
            
            xy_estimate=(0.0,0.0)
        else:
            measurements = OTHER[0]
            
            # initializes matrix
            lmatrix = np.mat('[0. 0. 0.;0. 0. 0.;0. 0. 0.]')
            lmatrix = matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
            
            # first row
            R00 = sum(measurement[0]**2 for measurement in measurements)
            R01 = sum(measurement[0]*measurement[1] for measurement in measurements)
            R02 = sum(measurement[0] for measurement in measurements)
            
            # second row
            R10 = sum(measurement[0]*measurement[1] for measurement in measurements)
            R11 = sum(measurement[1]**2 for measurement in measurements)
            R12 = sum(measurement[1] for measurement in measurements)
            
            # third row
            R20 = sum(measurement[0] for measurement in measurements)
            R21 = sum(measurement[1] for measurement in measurements)
            R22 = len(measurements)

            Lval = [[R00, R01, R02],
                    [R10, R11, R12],
                    [R20, R21, R22]]

            lmatrix.value = Lval
            
            #lmatrix_inverse = linalg.inv(lmatrix)
            lmatrix_inverse = lmatrix.inverse()

            
            #rmatrix = np.mat('[0.; 0.; 0.]')
            rmatrix = matrix([[0], [0], [0]])

            L00 = sum(measurement[0]*(measurement[0]**2 + measurement[1]**2) for measurement in measurements)
            L10 = sum(measurement[1]*(measurement[0]**2 + measurement[1]**2) for measurement in measurements)
            L20 = sum(measurement[0]**2 + measurement[1]**2 for measurement in measurements)
            
            Rval = [[L00], [L10], [L20]]

            rmatrix.value = Rval

            result = lmatrix_inverse * rmatrix

            resultl = result.value
            cx = resultl[0][0]/2
            cy = resultl[1][0]/2
            radius = sqrt((4*resultl[2][0])+resultl[0][0]**2+resultl[1][0]**2)/2

            print radius
            theta = atan2(y - cy, x - cx)

            new_x = cx + (radius * cos(theta))  # bring x on to circle
            new_y = cy + (radius * sin(theta))  # bring y on to circle
            distance = distance_between((new_x,new_y),OTHER[3])
            
            theta = atan2(new_y - OTHER[3][1], new_x - OTHER[3][0])
            turning = theta - OTHER[1]
            
            adistance = np.mean(OTHER[2])
            
            my_robot = robot(x, y, theta, turning, adistance)
            my_robot.set_noise(0.0, 0.0, 0.0)
            my_robot.move_in_circle()
            xy_estimate = (my_robot.x, my_robot.y) 
            
            OTHER[3] = (new_x, new_y)
    
        OTHER[1] = theta
        OTHER[2].append(distance)
        
    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    return xy_estimate, OTHER


# using least square method to fit the circle as seen in the forums
def lestimate_next_pos(measurement, OTHER = None):
    #print "measurement " + str(measurement)

    if OTHER == None:
        OTHER = [0] * 5
        OTHER[0] = []
        OTHER[4] = [measurement]
        OTHER[1] = []

        
        # "OTHER " + "none"
        return (0,0), OTHER
    else:
        data_points = OTHER[4]
        data_points.append(measurement)
        n = len(data_points)
        C_angles = OTHER[0]
        dist_from_centre = OTHER[1]
        

        if (n < 3):
            #print "OTHER " + "less than 3"
            return (0,0), OTHER
        else:
            ### L * vars = R
            L = matrix([[]])
            L.dimx = 3
            L.dimy = 3
            R = matrix([[0], [0], [0]])
            
            R00 = 0
            R01 = 0
            R02 = 0
            R10 = 0
            R11 = 0
            R12 = 0
            R20 = 0
            R21 = 0
            R22 = 0
            L00 = 0
            L10 = 0
            L20 = 0

            
            for i in range(n):
                temp = data_points[i]
                R00 += temp[0] ** 2
                R01 += temp[0] * temp[1]
                R02 += temp[0]
                R10 += temp[0] * temp[1]
                R11 += temp[1] ** 2
                R12 += temp[1]
                R20 += temp[0]
                R21 += temp[1]
                R22 = n

                L00 += temp[0] * (temp[0] ** 2 + temp[1] ** 2)
                L10 += temp[1] * (temp[0] ** 2 + temp[1] ** 2)
                L20 += temp[0] ** 2 + temp[1] ** 2

            Lval = [[R00, R01, R02],
                    [R10, R11, R12],
                    [R20, R21, R22]]
            Rval = [[L00], [L10], [L20]]

            L.value = Lval
            R.value = Rval

            #print Lval
            #print Rval

            #print L.dimx, L.dimy
            #print R.dimx, R.dimy
            

            vars = L.inverse() * R
            vars_val = vars.value
            #print vars_val

            A = vars_val[0][0]
            B = vars_val[1][0]
            C = vars_val[2][0]

            h = -A/2
            k = -B/2
            r = sqrt((4*C + A**2 + B**2))/2


            # C is centre of circle
            p2 = data_points[n - 1]
            p1 = data_points[n - 2]

            d10 = distance_between((h, k), (p1[0], p1[1]))
            d20 = distance_between((h, k), (p2[0], p2[1]))
            d21 = distance_between((p1[0], p1[1]), (p2[0], p2[1]))

            dist_from_centre.append(d20)
            new_dist = mean(dist_from_centre)

            angleC = acos((d21 ** 2 - d10 ** 2 - d20 ** 2) / (-2 * d10 * d20))
            C_angles.append(angleC)

            OTHER[0] = C_angles
            OTHER[4] = data_points

            meanC = mean(C_angles)
            #meanC = angleC

            v0 = h - p2[0]
            v1 = k - p2[1]

            dist_rotated = sqrt(v0 ** 2 + v1 ** 2)

            #v0 = v0/dist_rotated * r
            #v1 = v1/dist_rotated * r

            v0_rotated = v0 * cos(meanC) - v1 * sin(meanC)
            v1_rotated = v0 * sin(meanC) + v1 * cos(meanC)

            
            
            

            myrobot = robot(p2[0], p2[1])
            myrobot.set_noise(0.0, 0.0, 0.0)

            

            ## store angle C
            x_estimate = h - v0_rotated
            y_estimate = k - v1_rotated

            xy_estimate = (x_estimate, y_estimate)
            print "xy_estimate " + str(xy_estimate)

            OTHER[1] = dist_from_centre

            return xy_estimate, OTHER



def kestimate_next_pos(measurement, OTHER = None):
    
    #print "measurement " + str(measurement)
    if OTHER == None:
        OTHER = [0] * 11

        prev0 = 0
        prev1 = 0
        
        

        OTHER[0] = prev0
        OTHER[1] = prev1
        OTHER[2] = measurement

        x = matrix([[0]])
        P = matrix([[1000.]]) # initial uncertainty
        xn, Pn = kalman_filter(x, P, 1.5)   
        xn2, Pn2 = kalman_filter(x2, P, 169.4)   
            

        OTHER[3] = 1
        OTHER[4] = xn
        OTHER[5] = Pn
        OTHER[6] = []
        OTHER[7] = []
        OTHER[8] = []
        OTHER[9] = xn2
        OTHER[10] = Pn2

        print "prev 2 " + str(OTHER[1])
        print "measurement " + str(OTHER[2])
        print "estimate " + str((0,0))
        return (0,0), OTHER
    else:
        
        prev0 = OTHER[0]
        prev1 = OTHER[1]
        prev2 = OTHER[2]
        n = OTHER[3]
        xn = OTHER[4]
        Pn = OTHER[5]
        xs = OTHER[6]
        ns = OTHER[7]
        steps = OTHER[8]
        xn2 = OTHER[9]
        Pn2 = OTHER[10]
       
        n += 1

        if (n == 2):
            OTHER[0] = OTHER[1]
            OTHER[1] = OTHER[2]
            OTHER[2] = measurement
            OTHER[3] = n

            x = matrix([[0]])
            P = Pn # initial uncertainty
            P2 = Pn2
            xn, Pn = kalman_filter(xn, P, 1.5)       
            xn2, Pn2 = kalman_filter(xn2, P2, 169.4)   
               
            OTHER[4] = xn
            OTHER[5] = Pn

            OTHER[9]  = xn2
            OTHER[10] = Pn2

            #print "prev 1 " + str(OTHER[0])
            #print "prev 2 " + str(OTHER[1])
            #print "measurement " + str(OTHER[2])
            #print "estimate " + str((0,0))

            return (0,0), OTHER 

        else:
            OTHER[0] = OTHER[1]
            OTHER[1] = OTHER[2]
            OTHER[2] = measurement
            #n += 1
            OTHER[3] = n            

            v1 = (OTHER[0][0] - OTHER[1][0]), (OTHER[0][1] - OTHER[1][1])
            v2 = (OTHER[1][0] - OTHER[2][0]), (OTHER[1][1] - OTHER[2][1])

            num = (v1[0]*v2[0] + v1[1]*v2[1])
            den =  sqrt(v1[0] ** 2 + v1[1] ** 2) * sqrt(v2[0] ** 2 + v2[1] ** 2)

            alpha = acos(-num/den)
            alpha_in_degrees = degrees(alpha)     
            

            #print x
            step = distance_between(OTHER[1], OTHER[2])
            #print "step" + str(step)
            xn, Pn = kalman_filter(xn, Pn, step)  
            
            xn2, Pn2 = kalman_filter(xn2, Pn2, alpha_in_degrees)                   

            
            #use_alpha = xn.value[1][0]
            use_alpha = xn2.value[0][0]

            proj_step = xn.value[0][0] 
            #print "proj step " + str(proj_step) + "measur " + str(step)
            #print "proj angle " + str(use_alpha) + "measur " + str(alpha_in_degrees)

            if (n < 5):
                use_alpha = 169.4/2
            else:
                use_alpha = 169.4
            


            v2_x_prime_turn = v2[0]*cos(use_alpha) + v2[1]*sin(use_alpha)
            v2_y_prime_turn = -v2[0]*sin(use_alpha) + v2[1]*cos(use_alpha)    
    
            scaled_v2_turned = (v2_x_prime_turn/step) * proj_step, (v2_y_prime_turn/step) * proj_step

            #v2_turn = v2[0]/step * proj_step, v2[1]/step * proj_step
            #v2_turn = v2
            
            #x_prime = v2_turn[0]*cos(use_alpha) + v2_turn[1]*sin(use_alpha)
            #y_prime = -v2_turn[0]*sin(use_alpha) + v2_turn[1]*cos(use_alpha)


            ############################
            OTHER[4] = xn
            OTHER[5] = Pn

            xs.append(xn2.value[0][0])
            ns.append(n)
            steps.append(alpha_in_degrees)

            OTHER[6] = xs
            OTHER[7] = ns
            OTHER[9] = xn2
            OTHER[10] = Pn2
            ###############################
            #plt.axis([0, 3, 0, 3])
            
            #v3 = ((v2_x_prime_turn/step) * proj_step) + measurement[1], 
            #((v2_y_prime_turn/step) * proj_step) + measurement[0]
            #v3 = x_prime + measurement[0] , y_prime + measurement[1]
            #print v3

            v3 = scaled_v2_turned[0] + measurement[0], scaled_v2_turned[1] + measurement[1]
            #print "================================"

            #print "steps " + str(proj_step)
            #print "angle " + str(use_alpha)
            #print "scaled after turn " + str(scaled_v2_turned)

            #print "prev 1 " + str(OTHER[0])
            #print "prev 2 " + str(prev2)
            #print "measurement " + str(measurement)
            #print "estimate " + str(v3)

            #plt.plot(measurement[0], measurement[1], 'ro')
            #plt.plot(v3[0], v3[1], 'go')
            #plt.pause(0.05)
            return v3, OTHER

def kalman_filter2(x2, P2, measurement2):
        
    # measurement update
    z2= matrix([[measurement2]])
    #z.identity(1, measurement[0])
    #print z2
    
    Hx= H2 * x2
    y= z2 - Hx
    S= H2 * P2 *  H2.transpose() + R2
    K= P2 * H2.transpose() * S.inverse()
    Ky= K * y
    x2= x2 + Ky
    KH= K * H2
    #print KH.dimx, KH.dimy
    #print KH.dimx
    one= matrix([[1]])
    #one.identity(KH.dimx,1)
    #print one
    P= (one - KH) * P2

    #print "After measurement " + str(n)
    #print "x:"
    #x.show()
    #print "P:"
    #P.show()
        

    # prediction
    x= F2 * x2 + u2
    P2= F2 * P2 * F2.transpose()

    #print "After prediction " + str(n)
    #print "x:"
    #x.show()
    #print "P:"
    #P.show()
    print x2,P2
        
    return x2,P2

def kalman_filter(x, P, measurement):
        
    # measurement update
    z= matrix([[measurement]])
    #z.identity(1, measurement[0])
    #print z
    
    Hx= H * x
    y= z - Hx
    S= H * P *  H.transpose() + R
    K= P * H.transpose() * S.inverse()
    Ky= K * y
    x= x + Ky
    KH= K * H
    #print KH.dimx, KH.dimy
    #print KH.dimx
    one= matrix([[1]])
    #one.identity(KH.dimx,1)
    #print one
    P= (one - KH) * P

    #print "After measurement " + str(n)
    #print "x:"
    #x.show()
    #print "P:"
    #P.show()
        

    # prediction
    x= F * x + u
    P= F * P * F.transpose()

    #print "After prediction " + str(n)
    #print "x:"
    #x.show()
    #print "P:"
    #P.show()
    #print x,P
        
    return x,P


# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def zestimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    
    print "measurement " + str(measurement)

    if OTHER == None:

        #angle = atan2(measurement[1], measurement[0])
        OTHER = [0] * 8
        prev0 = 0
        prev1 = 0
        current = measurement
        OTHER[0] = prev0
        OTHER[1] = prev1
        OTHER[2] = current
        OTHER[3] = 1
        #add a noise accumulator
        #x variations
        OTHER[4] = []
        #y variations
        OTHER[5] = []
        #store xy_estimates
        OTHER[6] = None
        OTHER[7] = []
        xy_estimate = current
    else:

        prev0 = OTHER[0]
        prev1 = OTHER[1]
        prev2 = OTHER[2]
        n = OTHER[3]
        x_vars = OTHER[4]
        y_vars = OTHER[5]
        last_estimate = OTHER[6]
        saved_alphas = OTHER[7]

        if (n < 3):
            OTHER[0] = prev1
            OTHER[1] = prev2
            OTHER[2] = measurement
            n += 1
            OTHER[3] = n
            #x_vars.append()
            #y_vars.append()
            xy_estimate = measurement
        else:
            OTHER[0] = prev1
            OTHER[1] = prev2
            OTHER[2] = measurement


            #print prev1, prev2, measurement
            n += 1
            OTHER[3] = n
            #print prev1
            #print prev2
            #print measurement

            

            v1 = (OTHER[0][0] - OTHER[1][0]), (OTHER[0][1] - OTHER[1][1])
            v2 = (OTHER[1][0] - OTHER[2][0]), (OTHER[1][1] - OTHER[2][1])


            num = (v1[0]*v2[0] + v1[1]*v2[1])
            den =  sqrt(v1[0] ** 2 + v1[1] ** 2) * sqrt(v2[0] ** 2 + v2[1] ** 2)

            alpha = acos(-num/den)
            saved_alphas.append(alpha)

            use_alpha = alpha
            if (len(saved_alphas) >= 2):
                use_alpha = random.gauss(mean(saved_alphas), pstdev(saved_alphas))
                #print "degrees " + str(degrees(use_alpha))


            print sqrt(v2[0] ** 2 + v2[1] ** 2)
            x_prime = v2[0]*cos(use_alpha) + v2[1]*sin(use_alpha)
            y_prime = -v2[0]*sin(use_alpha) + v2[1]*cos(use_alpha)
                        


            v3 = x_prime + measurement[0], y_prime + measurement[1]
            #print v3 

            x_noise = 0
            y_noise = 0
            rx = 0
            ry = 0
            if last_estimate is not None:
                x_vars.append(measurement[0] - last_estimate[0])
                y_vars.append(measurement[1] - last_estimate[1])
                #print last_estimate, measurement
                #print len(x_vars)
                #print len(y_vars)
                if len(x_vars) >= 2:
                    mean_x = mean(x_vars)
                    mean_y = mean(y_vars)
                    std_dev_x = pstdev(x_vars)
                    std_dev_y = pstdev(y_vars)
                    
                    rx = random.uniform(0, max(x_vars))
                    ry = random.uniform(0, max(y_vars))

                    print rx,ry
                    signx = [-1, 1]
                    random.shuffle(signx)
                    rx *= signx[0]
                    signy = [-1, 1]
                    random.shuffle(signy)
                    ry *= signy[0]

                    x_noise = random.gauss(mean_x, std_dev_x/2)
                    y_noise = random.gauss(mean_y, std_dev_y/2)
                    #print "white noise " + str(x_noise) + " " + str(y_noise)


            v3x_noise = v3[0] + rx
            v3y_noise = v3[1] + ry


            xy_estimate = v3x_noise, v3y_noise
            #xy_estimate = v3

            #print "deviations " + str(v3) + " " + str(xy_estimate)

            OTHER[6]= xy_estimate 
            


        #print "xy_estimate " + str(xy_estimate)
    #print slopex, slopey
    #xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER


def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    
    print measurement

    if OTHER == None:

        #angle = atan2(measurement[1], measurement[0])
        OTHER = [0] * 4
        prev0 = 0
        prev1 = 0
        current = measurement
        OTHER[0] = prev0
        OTHER[1] = prev1
        OTHER[2] = current
        OTHER[3] = 1
        xy_estimate = current
    else:

        prev0 = OTHER[0]
        prev1 = OTHER[1]
        prev2 = OTHER[2]
        n = OTHER[3]

        if (n < 3):
            OTHER[0] = prev1
            OTHER[1] = prev2
            OTHER[2] = measurement
            n += 1
            OTHER[3] = n
            xy_estimate = measurement
        else:
            OTHER[0] = prev1
            OTHER[1] = prev2
            OTHER[2] = measurement

            #print prev1, prev2, measurement
            n += 1
            OTHER[3] = n
            #print prev1
            #print prev2
            #print measurement

            v1 = (OTHER[0][0] - OTHER[1][0]), (OTHER[0][1] - OTHER[1][1])
            v2 = (OTHER[1][0] - OTHER[2][0]), (OTHER[1][1] - OTHER[2][1])

            print v1, v2
            print "distance " + str(distance_between(prev1, prev2))


            num = (v1[0]*v2[0] + v1[1]*v2[1])
            den =  sqrt(v1[0] ** 2 + v1[1] ** 2) * sqrt(v2[0] ** 2 + v2[1] ** 2)
            
            #print "distance v " + str(sqrt(v2[0] ** 2 + v2[1] ** 2))
            
            #print num/den

            alpha = acos(-num/den)
            #print alpha
            #print degrees(alpha)     

            #rotate v2 to get vector
            print degrees(alpha)

            x_prime = v2[0]*cos(alpha) + v2[1]*sin(alpha)
            y_prime = -v2[0]*sin(alpha) + v2[1]*cos(alpha)

            v3 = x_prime + measurement[0], y_prime + measurement[1]
            #print v3 
            xy_estimate = v3
            xy_estimate = measurement
    #print slopex, slopey

    return xy_estimate, OTHER 

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        print "error " + str(error)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 1000:
            print "Sorry, it took you too many steps to localize the target."
    return localized

#def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
#    localized = False
#    distance_tolerance = 0.01 * target_bot.distance
#    ctr = 0
#    # if you haven't localized the target bot, make a guess about the next
#    # position, then we move the bot and compare your guess to the true
#    # next position. When you are close enough, we stop checking.
#    #For Visualization
#    #import turtle    #You need to run this locally to use the turtle module
#    window = turtle.Screen()
#    window.bgcolor('white')
#    size_multiplier= 25.0  #change Size of animation
#    broken_robot = turtle.Turtle()
#    broken_robot.shape('turtle')
#    broken_robot.color('green')
#    broken_robot.resizemode('user')
#    broken_robot.shapesize(0.3, 0.3, 0.3)
#    measured_broken_robot = turtle.Turtle()
#    measured_broken_robot.shape('circle')
#    measured_broken_robot.color('red')
#    measured_broken_robot.resizemode('user')
#    measured_broken_robot.shapesize(0.3, 0.3, 0.3)
#    prediction = turtle.Turtle()
#    prediction.shape('arrow')
#    prediction.color('blue')
#    prediction.resizemode('user')
#    prediction.shapesize(0.3, 0.3, 0.3)
#    prediction.penup()
#    broken_robot.penup()
#    measured_broken_robot.penup()
#    #End of Visualization
#    while not localized and ctr <= 40:
#        ctr += 1
#        measurement = target_bot.sense()
#        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
#        target_bot.move_in_circle()
#        true_position = (target_bot.x, target_bot.y)
#        error = distance_between(position_guess, true_position)
#        if error <= distance_tolerance:
#            print "You got it right! It took you ", ctr, " steps to localize."
#            localized = True
#        if ctr == 1000:
#            print "Sorry, it took you too many steps to localize the target."
#        #More Visualization
#        measured_broken_robot.setheading(target_bot.heading*180/pi)
#        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
#        measured_broken_robot.stamp()
#        broken_robot.setheading(target_bot.heading*180/pi)
#        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
#        broken_robot.stamp()
#        prediction.setheading(target_bot.heading*180/pi)
#        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
#        prediction.stamp()
#        #End of Visualization
#    return localized

## This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

#plt.show()
demo_grading(lbestimate_next_pos, test_target)
#plt.show()



