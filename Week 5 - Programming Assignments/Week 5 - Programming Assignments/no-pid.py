import matplotlib.pylab as plt

def cruiseControllerNoPID(n, req_speed, initial_speed = 0, accelerate_step = 1):
    speeds = []
    current_speed = initial_speed
    ns = []
    x = 0
    acc = []
    
    while x < n + 1:
        x += 1

        #print current_speed
        
        #plt.axis([-10, n + 10 , -10, req_speed + 10])
        plt.axis([-10, n + 10 , -1.5, 0.75])
        speeds.append(current_speed)
        
        
        acc.append(speeds[x - 1] - speeds[x - 2])
        ns.append(x)
        #plt.plot(ns, speeds, 'g-',label = "speed")
        plt.plot(ns, acc, 'r-', label = "input (force applied to pedal)")
        
        if (x == 1):
            plt.legend()

        plt.xlabel("time")
        plt.ylabel("Input (Force applied to pedal)")
        
        
        plt.pause(0.000001)


        if (current_speed < req_speed):
            #accelerate
            current_speed += accelerate_step
            
        elif (current_speed > req_speed):
            #apply brakes
            current_speed -= accelerate_step

        else:
            #speed reduction when pedal isn't pressed
            current_speed -= 1

        if (current_speed < 0):
            current_speed = 0

        #print current_speed


def PController(n, req_speed, initial_speed = 0, accelerate_step = 1):
    speeds = []
    current_speed = initial_speed
    ns = []
    x = 0
    acc = []
    req_speeds = []
    
    while x < n + 1:
        x += 1
        #print current_speed
        
        plt.axis([-10, n + 10 , -10, req_speed + 10])
        #plt.axis([-10, n + 10 , -1.5, 0.75])
        speeds.append(current_speed)
        req_speeds.append(req_speed)
        acc.append(speeds[x - 1] - speeds[x - 2])
        ns.append(x)
        plt.plot(ns, speeds, 'g-',label = "speed")
        plt.plot(ns, req_speeds, 'r--', label = "required speed")
        #plt.plot(ns, acc, 'r-', label = "input (force applied to pedal)")
        
        if (x == 1):
            plt.legend()

        plt.xlabel("time")
        plt.ylabel("Car's speed")
        
        
        plt.pause(0.000001)

        Kp = 0.2
        e = req_speed - current_speed
        drag = 0.03 
        current_speed += e * Kp - drag * current_speed

        print current_speed

def PIController(n, req_speed, initial_speed = 0, accelerate_step = 1):
    speeds = []
    current_speed = initial_speed
    ns = []
    x = 0
    acc = []
    req_speeds = []
    accumulated_e = 0
    
    while x < n + 1:
        x += 1
        #print current_speed
        
        plt.axis([-10, n + 10 , -10, req_speed + 10])
        #plt.axis([-10, n + 10 , -1.5, 0.75])
        speeds.append(current_speed)
        req_speeds.append(req_speed)
        acc.append(speeds[x - 1] - speeds[x - 2])
        ns.append(x)
        plt.plot(ns, speeds, 'g-',label = "speed")
        plt.plot(ns, req_speeds, 'r--', label = "required speed")
        #plt.plot(ns, acc, 'r-', label = "input (force applied to pedal)")
        
        if (x == 1):
            plt.legend()

        plt.xlabel("time")
        plt.ylabel("Car's speed")
        
        
        plt.pause(0.000001)

        Kp = 0.2
        e = req_speed - current_speed
        drag = 0.03 
        KI = 0.007
        accumulated_e += e

        current_speed += (e * Kp - drag * current_speed) + (KI * accumulated_e)

        print current_speed

def PIDController(n, req_speed, initial_speed = 0, accelerate_step = 1):
    speeds = []
    current_speed = initial_speed
    ns = []
    x = 0
    acc = []
    req_speeds = []
    accumulated_e = 0
    
    while x < n + 1:
        x += 1
        #print current_speed
        
        plt.axis([-10, n + 10 , -10, req_speed + 10])
        #plt.axis([-10, n + 10 , -1.5, 0.75])
        speeds.append(current_speed)
        req_speeds.append(req_speed)
        acc.append(speeds[x - 1] - speeds[x - 2])
        ns.append(x)
        plt.plot(ns, speeds, 'g-',label = "speed")
        plt.plot(ns, req_speeds, 'r--', label = "required speed")
        #plt.plot(ns, acc, 'r-', label = "input (force applied to pedal)")
        
        if (x == 1):
            plt.legend()

        plt.xlabel("time")
        plt.ylabel("Car's speed")
        
        
        plt.pause(0.000001)

        drag = 0.03 
        e = req_speed - current_speed
       
        KI = 0.07
        Kd = 0.1
        Kp = 0.1

        accumulated_e += e
        diff_e = speeds[x - 1] - speeds[x - 2]

        current_speed += (e * Kp - drag * current_speed) + (Kp * accumulated_e) + (Kd * diff_e) 

        print current_speed


#cruiseControllerNoPID(100, initial_speed = 0, req_speed = 20, accelerate_step = 0.5)
PIController(100, initial_speed = 10, req_speed = 20, accelerate_step = 0.5)
plt.show()

