p= [0.2]*5
pHit= 0.6
pMiss= 0.2

for i in range(0,5):
    if ((i== 1)or(i==2)):
        p[i]*=pHit
    else:
        p[i]*=pMiss

print sum(p)
        
