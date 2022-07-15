from matplotlib import projections
import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

# 共识成功概率与消息接收成功概率的关系
x = []
y1 = []
epsilons = np.arange(0.0, 1.01, 0.01)
sigma = 0.9
F=45
N=1000
for epsilon in epsilons:
    x.append(epsilon)
    p_comm1 = 0
    p_suc = epsilon
    for f in range(int(N/2+1)-F,N-F):
        p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
    p_cp1 = 1-pow(p_comm1, int(N-F))
    y1.append(p_suc*p_cp1)
plt.plot(x, y1, 'o-', c='red', label ='SWIB', linewidth=1)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('Transmission Success Probability',fontsize=10)
plt.ylabel('Consensus Success Probability',fontsize=10)
plt.show()
    
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