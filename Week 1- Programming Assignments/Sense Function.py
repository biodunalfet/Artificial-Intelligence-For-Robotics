p= [0.2]*5
pHit= 0.6
pMiss= 0.2
world = ['green', 'red', 'red', 'green', 'green']
Z= 'red'

#print sum(p)
        
def sense(p, Z):
    for i in range(0,len(p)):
        if (world[i]== 'red'):
            p[i]*=pHit
        else:
            p[i]*=pMiss
    return p

print sense(p, Z)
