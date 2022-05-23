import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

N = 100
epsilons = np.arange(0.1, 0.61, 0.01)
p_hard = 0.1
# epsilon = 0.5
# N = np.arange(100, 1501, 50)
x = []
y = []
for epsilon in epsilons:
    x.append(epsilon)
    p_comm = 0
    for f in range(int(N/3+1),N):
        p_comm = p_comm + comb(N-1, f)* pow(epsilon,f)*pow(1-epsilon, N-1-f)
    p_cp = p_cp = p_hard + p_comm - p_hard*p_comm
    y.append(p_cp)
    # print("p_comm=", p_comm)
    # print("p_cp = ", pow(p_sum, N))
print(x)
print(y)
# y = savgol_filter(y,15, 3,  mode= 'nearest')
plt.plot(x, y)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('Probability of Communication Interruption',fontsize=14)
plt.ylabel('Probability of Consensus Interruption',fontsize=14)
plt.show()