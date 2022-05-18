import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

P = pow(10,-6)
# N = 400
N = np.arange(100, 1501, 50)
# print("f = ", f)
x = []
y = []
for n in N:
    print("N=", n)
    x.append(n)
    f = n/3-1
    C = np.arange(50, 251, 1)
    for c in C:
        B = np.arange(c/2 +1, c)
        Ps = 0
        for b in B:
            if b > f:
                b = f
            # print("b=", b)
            a = c-b
            Ps += (float)(comb(n-f,a)*comb(f,b)/comb(n,c))
        if Ps < P:
            print("c = ", c)
            y.append(c)
            print("Ps = ", Ps)
            break
    
print(x)
print(y)
# y = savgol_filter(y,15, 3,  mode= 'nearest')
plt.plot(x, y)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('Number of Nodes',fontsize=14)
plt.ylabel('Committee Size',fontsize=14)
plt.show()