import math

f= [0.6, 1.2, 2.4, 0.6, 1.2]
fsum= sum(f)
wf=[]
for i in range(len(f)):
	wf.append(f[i]/fsum)
    
print(1-math.pow(1 - wf[2],5))