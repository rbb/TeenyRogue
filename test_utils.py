import numpy as np
import utils

N = 100

for n in range(N):
    m = utils.randint(n)
    if m != 0 and m > n - 1:
        print(f"{m=} {n=}")
    if m < 0:
        print(f"{m=} {n=}")

M = np.zeros(N)
for n in range(N):
    m = utils.randint(N)
    if m != 0 and m > N - 1:
        print(f"{m=} {n=}")
    if m < 0:
        print(f"{m=} {n=}")
    M[n] = m
print("mean = " + str(np.mean(M)))
