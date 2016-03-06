# ----------
# Part Three
#
# Now you'll actually track down and recover the runaway Traxbot. 
# In this step, your speed will be about twice as fast the runaway bot,
# which means that your bot's distance parameter will be about twice that
# of the runaway. You can move less than this parameter if you'd 
# like to slow down your bot near the end of the chase. 
#
# ----------
# YOUR JOB
#
# Complete the next_move function. This function will give you access to 
# the position and heading of your bot (the hunter); the most recent 
# measurement received from the runaway bot (the target), the max distance
# your bot can move in a given timestep, and another variable, called 
# OTHER, which you can use to keep track of information.
# 
# Your function will return the amount you want your bot to turn, the 
# distance you want your bot to move, and the OTHER variable, with any
# information you want to keep track of.
# 
# ----------
# GRADING
# 
# We will make repeated calls to your next_move function. After
# each call, we will move the hunter bot according to your instructions
# and compare its position to the target bot's true position
# As soon as the hunter is within 0.01 stepsizes of the target,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot. 
#
# As an added challenge, try to get to the target bot as quickly as 
# possible. 

from robot import *
from math import *
from matrix import *
import random
#import turtle

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

            #print radius
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


def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    if OTHER == None:
        #1 for centre
        #2 for radius
        #3 for mode(trap or centre)
        
        OTHER = [[target_measurement], [], [], "centre", []]
        turning = 0
        distance = 0
        
    else:
        OTHER[0].append(target_measurement)
        measurements = OTHER[0]
        centre = OTHER[1]
        radii = OTHER[2]
        mode = OTHER[3]
        trap_from = OTHER[4]

        if len(OTHER[0]) < 5:
            turning = 0
            distance = 0
        else:
            # initializes matrix
            #lmatrix = np.mat('[0. 0. 0.;0. 0. 0.;0. 0. 0.]')
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
            
            lmatrix_inverse = lmatrix.inverse()
            
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

            OTHER[1] = [cx, cy]

            radius = sqrt((4*resultl[2][0])+resultl[0][0]**2+resultl[1][0]**2)/2
            radii.append(radius)
            OTHER[2] = radii
            
            #get the vector that links the centre to the bots current position
            vec_centre_hunter = cx - hunter_position[0], cy - hunter_position[1]


            if mode == "centre":
                #print "centre"
                turning = atan2(vec_centre_hunter[1], vec_centre_hunter[0]) - hunter_heading
                dist_to_goal = distance_between(hunter_position, (cx, cy))

                if (dist_to_goal > max_distance):
                    distance = max_distance
                else:
                    distance = dist_to_goal

                if distance_between(hunter_position, (cx, cy)) <= 0.05:
                    mode = "trap"
                    trap_from = [target_measurement]
                    heading_centre_to_measurement = atan2((cx - target_measurement[0]), 
                                                          (cy - target_measurement[1])) 
                    
                    heading_to_current_measurement = get_heading(hunter_position, trap_from[0])
                    #print "heading to current measurement " + str(heading_to_current_measurement)
                    turning = heading_centre_to_measurement + radians(90) - hunter_heading
                    #turning = hunter_heading - 90
                    OTHER[4] = trap_from
                    #print turning

                    if abs(distance_between(hunter_position, (cx, cy)) - mean(radii)) > max_distance:
                        distance = max_distance
                    else:
                        distance =  mean(radii) - distance_between(hunter_position, (cx, cy))



            else:
                #print "trap"
                #trap_from = [target_measurement]
                #print hunter_heading

                heading_centre_to_measurement = atan2((cx - trap_from[0][0]), 
                                                        (cy - trap_from[0][1]))
                    
                heading_to_current_measurement = get_heading(hunter_position, trap_from[0])
                #turning = heading_centre_to_measurement - hunter_heading
                #turning = -hunter_heading
                turning = 0
                if abs(distance_between(hunter_position, (cx, cy)) - mean(radii)) > max_distance:
                    distance = max_distance
                else:
                    distance =  mean(radii) - distance_between(hunter_position, (cx, cy))

                if distance_between(hunter_position, target_measurement) < 0.3:
                    mode = "centre"
                    #turning = hunter_heading + 90
                
            OTHER[3] = mode
    return turning, distance, OTHER

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 1.94 * target_bot.distance # 1.94 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        

        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught

#def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
#    """Returns True if your next_move_fcn successfully guides the hunter_bot
#    to the target_bot. This function is here to help you understand how we 
#    will grade your submission."""
#    max_distance = 1.94 * target_bot.distance # 1.94 is an example. It will change.
#    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
#    caught = False
#    ctr = 0
#    #For Visualization
#    import turtle
#    window = turtle.Screen()
#    window.bgcolor('white')
#    chaser_robot = turtle.Turtle()
#    chaser_robot.shape('arrow')
#    chaser_robot.color('blue')
#    chaser_robot.resizemode('user')
#    chaser_robot.shapesize(0.3, 0.3, 0.3)
#    broken_robot = turtle.Turtle()
#    broken_robot.shape('turtle')
#    broken_robot.color('green')
#    broken_robot.resizemode('user')
#    broken_robot.shapesize(0.3, 0.3, 0.3)
#    size_multiplier = 15.0 #change Size of animation
#    chaser_robot.hideturtle()
#    chaser_robot.penup()
#    chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
#    chaser_robot.showturtle()
#    broken_robot.hideturtle()
#    broken_robot.penup()
#    broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
#    broken_robot.showturtle()
#    measuredbroken_robot = turtle.Turtle()
#    measuredbroken_robot.shape('circle')
#    measuredbroken_robot.color('red')
#    measuredbroken_robot.penup()
#    measuredbroken_robot.resizemode('user')
#    measuredbroken_robot.shapesize(0.1, 0.1, 0.1)
#    broken_robot.pendown()
#    chaser_robot.pendown()
#    #End of Visualization
#    # We will use your next_move_fcn until we catch the target or time expires.
#    while not caught and ctr < 1000:
#        # Check to see if the hunter has caught the target.
#        hunter_position = (hunter_bot.x, hunter_bot.y)
#        target_position = (target_bot.x, target_bot.y)
#        separation = distance_between(hunter_position, target_position)

#        #print "seperation " + str(separation)
#        #print "seperation tolerance " + str(separation_tolerance)
#        if separation < separation_tolerance:
#            print "You got it right! It took you ", ctr, " steps to catch the target."
#            caught = True

#        # The target broadcasts its noisy measurement
#        target_measurement = target_bot.sense()

#        # This is where YOUR function will be called.
#        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)

#        # Don't try to move faster than allowed!
#        if distance > max_distance:
#            distance = max_distance

#        # We move the hunter according to your instructions
#        hunter_bot.move(turning, distance)

#        # The target continues its (nearly) circular motion.
#        target_bot.move_in_circle()
#        #Visualize it
#        measuredbroken_robot.setheading(target_bot.heading*180/pi)
#        measuredbroken_robot.goto(target_measurement[0]*size_multiplier, target_measurement[1]*size_multiplier-100)
#        measuredbroken_robot.stamp()
#        broken_robot.setheading(target_bot.heading*180/pi)
#        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
#        chaser_robot.setheading(hunter_bot.heading*180/pi)
#        chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
#        #End of visualization
#        ctr += 1            
#        if ctr >= 1000:
#            print "It took too many steps to catch the target."
#    return caught

def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!

    print max_distance
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
measurement_noise = .05*target.distance
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

print demo_grading(hunter, target, next_move)





