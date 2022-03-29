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

P =beta[0]
print("P", P)

Disk = [0]
sum_p = 0
for p in beta:
    sum_p = sum_p + p
    Disk.append(sum_p)
print(beta)
print(Disk)


p1 = random.random()
print("random", p1)
p2 = random.randint(0, 300)
print("randint", p2)
p3 = random.uniform(0, 300)
print("uniform", p3)