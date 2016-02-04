import matplotlib.pyplot as plt
import numpy as np

plt.show()
#plt.plot([1,2,3,4], [1,4,9,16], 'ro')
#plt.pause(2)
#plt.plot([-1, -2, -3, -4], [ 2, 4, 6, 8], 'g-')
#plt.pause(2)


index = [0]
sqrd = [0]
for i in range(0, 20, 2):
    plt.axis([-50, 20, -50, 320])
    plt.plot(index, sqrd , 'ro')
    plt.pause(1)
    index.append(i)
    sqrd.append(i**2)

plt.show()
#plt.axis([0, 6, 0, 20])


# evenly sampled time at 200ms intervals
#t = np.arange(0., 5., 0.2)

## red dashes, blue squares and green triangles
#plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
#plt.show()