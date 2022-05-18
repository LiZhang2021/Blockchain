import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 1000
C = np.arange(10, 181, 10)
f = N/3-1
print("f = ", f)
x = []
y = []
for c in C:
    x.append(c)
    print("c = ", c)
    B = np.arange(c/2 +1, c)
    Ps = 0
    # b = c/2+1
    # # print("b=", b)
    # a = c- b
    # Pb = (float)(comb(N-f,a)*comb(f,b)/comb(N,c))
    for b in B:
        if b > f:
            b = f
        # print("b=", b)
        a = c-b
        Ps += (float)(comb(N-f,a)*comb(f,b)/comb(N,c))
        # print("Pb = ", comb(N-f,a)*comb(f,b)/comb(N,c))
    print("Ps = ", Ps)
    y.append(Ps)

plt.plot(x, y)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('committee size(N = 1000)',fontsize=14)
plt.ylabel('probability of failue',fontsize=14)
plt.show()
    