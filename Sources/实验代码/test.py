import random
import numpy as np

a = [1,2,3]
c = 7
for i in range(4):
    k = sum(a[:i])
    print(k)
for i in range(4):
    low = sum(a[:i])
    high = sum(a[:i+1])
    if c>=low and c<high:
        print(i)

p = random.random()
print(p)

alphas = range(1,10)
print(alphas)
beta = np.arange(0, 16, 2)
print(beta)
K = random.choice(beta)
print(K)
print(beta)

beta = [1, 2, 6, 9, 11]
m = np.mean(beta)
print(m)
n = np.median(beta)
print(n)

bmax = max(beta)
print(bmax)