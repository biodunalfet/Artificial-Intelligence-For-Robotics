p= [0.2]*5
pHit= 0.6
pMiss= 0.2
world = ['green', 'red', 'red', 'green', 'green']
Z= 'red'

#print sum(p)
        
def sense(p, Z):
    q= list(p)
    for i in range(0,len(q)):
        if (world[i]== Z):
            q[i]*=pHit
        else:
            q[i]*=pMiss
    list_sum = sum(q)
    return [j/list_sum for j in q]

print sense(p, Z)
