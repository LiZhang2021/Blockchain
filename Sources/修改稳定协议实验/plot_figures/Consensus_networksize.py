import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

x = []
y1 = []
y2 = []
# F = 0
# # F = int(N/2)-1
# Nodes = np.arange(10, 1001, 1)
# epsilons = np.arange(0.0, 1.01, 0.01)
# sigma = 0.9
# epsilon = 0.5
# p_suc = sigma*epsilon
# for N in Nodes:
#     x.append(N)
#     p_sum = 0
#     for f in range(int(N/2+1)-F,N-F-1):
#         p_sum = p_sum + comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
#     p_full = 1-pow(p_sum, N-F)
#     p_cons = p_full
#     y1.append(p_cons)

# plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.xticks(fontsize=10)
# plt.yticks(fontsize=10)
# #标签设置字体大小设置
# plt.xlabel('Network Size',fontsize=10)
# plt.ylabel('Consensus Success Probability',fontsize=10)
# plt.show()


# for N in Nodes:
#     x.append(N)
#     p_sum = 0
#     for f in range(int(N/2+1),N):
#         p_sum = p_sum + comb(N-1, f)* pow(1-p_suc,f)*pow(p_suc, N-1-f)
#     p_full = 1-pow(p_sum, N)
#     p_cons = p_suc*p_full*p_suc
#     y1.append(p_cons)
# p = 1/N
# p_BG = p*pow(1-p,N-1)/(1-pow(1-p, N))
x = []
y1 = []
y2 = []
epsilons = np.arange(0.0, 1.01, 0.01)
sigma = 0.9
F=45
N=100
for epsilon in epsilons:
    x.append(epsilon)
    p_comm1 = 0
    p_suc = epsilon
    for f in range(int(N/2+1)-F,N-F):
        p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
    p_cp1 = 1-pow(p_comm1, int(N-F))
    y1.append(p_cp1)
# for epsilon in epsilons:
#     x.append(epsilon)
#     N = 100
#     p_sum = 0
#     p_suc = epsilon
#     for f in range(int(N/2+1),N-1):
#         p_sum += comb(N-1, f)*pow(1-epsilon,f)*pow(epsilon, N-1-f)
#     p_cons = 1-pow(p_sum, int(N))    
#     y2.append(p_cons)
plt.plot(x, y1, 'o-', c='red', label ='SWIB', linewidth=1)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('Network Size',fontsize=10)
plt.ylabel('Consensus Success Probability',fontsize=10)
plt.show()