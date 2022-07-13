import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0
# N = np.arange(100, 1501, 50)
x = []
y1 = []
y2 = []
epsilons = np.arange(0.0, 1.1, 0.05)
for epsilon in epsilons:
    x.append(1-epsilon)
    p_comm1 = 0
    for f in range(int(N/2+1),N):
        p_comm1 = p_comm1 + comb(N-1, f)* pow(epsilon,f)*pow(1-epsilon, N-1-f)
    p_cp1 = pow(p_comm1, int(N))
    y1.append(1-p_cp1)
    p_comm2 = 0
    for f in range(int((N+1)/3),N):
        p_comm2 = p_comm2 + comb(N-1, f)* pow(epsilon,f)*pow(1-epsilon, N-1-f)
    p_cp = p_cp = p_hard + p_comm2 - p_hard*p_comm2
    # p_cp2 = pow(p_comm2, int(2*N/3))
    # p_cp2 = pow(p_comm2, int(N))
    # p_cp = p_hard +  p_cp2 - p_hard* p_cp2
    y2.append(1-p_cp)
    
# print(x)
# print(y)
# y = savgol_filter(y,15, 3,  mode= 'nearest')
# plt.plot(x, y2)
# #设置横纵坐标字体大小
# plt.xticks(fontsize=10)
# plt.yticks(fontsize=10)
# #标签设置字体大小设置
# plt.xlabel('Probability of Communication Interruption',fontsize=14)
# plt.ylabel('Probability of Consensus Interruption',fontsize=14)
# plt.show()
fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o-', c='blue', label ='PBFT', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Transmission Success Probability',fontsize=10)
ax1.set_ylabel('Consensus Success Probability',fontsize=10)
# ax2.set_ylabel('Probability of Consensus Interruption(PBFT)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()