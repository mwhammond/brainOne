import numpy as np

longboard = np.zeros((36,0))

a = np.zeros((6,6))
a[1,1] = 1
a[1,2] = 2
a[1,3] = 3
a[1,4] = 4
a[2,3] = -1

print a

longboard = np.reshape(a,(36,1))

print longboard
# flatten to one value
longboard[np.greater(longboard, 1)] = 1
longboard[np.less(longboard, 0)] = 2


print longboard