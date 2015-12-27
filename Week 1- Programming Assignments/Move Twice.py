#Modify the move function to accommodate the added 
#probabilities of overshooting or undershooting 
#the intended destination.

p=[0, 1, 0, 0, 0]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q


def move(p, U):
    q = []
    nCells= len(p)
    for i in range(len(p)):
        #three ways to get to a spot
        #undershoot
        #exact
        #overshoot
        #
        ###exact (cyclic subtraction)
        iExact = (i-U)% nCells
        possExact= p[iExact] * pExact
        ###overshoot (cyclic subtraction-1**)
        iOvershoot= (iExact-1) % nCells
        possOvershoot= p[iOvershoot] * pOvershoot
        ###undershoot (cyclic subtraction+1***)
        iUndershoot = (iExact+1) % nCells
        possUndershoot= p[iUndershoot] * pUndershoot
        
        totalPoss= possExact + possUndershoot + possOvershoot
        q.append(totalPoss)
        
    return q

#def move(p, U):
#    q=[]
#    for 

p= move(move(p,1), 1)
print p
