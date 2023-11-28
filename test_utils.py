import numpy as np
#import utils 
from utils import *

N = 100

for n in range(N):
    #m = utils.randint(n)
    m = randint(n)
    if m != 0 and m > n-1:
        print("m = " +str(m) +" n = " +str(n))
    if m < 0:
        print("m = " +str(m) +" n = " +str(n))

M = np.zeros(N)    
for n in range(N):
    m = randint(N)
    if m != 0 and m > N-1:
        print("m = " +str(m) +" n = " +str(n))
    if m < 0:
        print("m = " +str(m) +" n = " +str(n))
    M[n] = m
print("mean = " +str(np.mean(M)) )
