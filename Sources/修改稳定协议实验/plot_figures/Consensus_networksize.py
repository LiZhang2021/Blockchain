from matplotlib import projections
import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

# # 共识成功概率与消息接收成功概率的关系
# x = []
# y1 = []
# epsilons = np.arange(0.0, 1.01, 0.05)
# sigma = 0.9
# F=0
# N=100
# for epsilon in epsilons:
#     x.append(epsilon)
#     p_comm1 = 0
#     p_suc = epsilon
#     for f in range(int(N/2+1)-F,N-F):
#         p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
#     p_cp1 = 1-pow(p_comm1, int(N-F))
#     y1.append(p_cp1)
# y2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.8, 0.87, 0.88, 0.94, 0.95, 0.99, 1]

# fig, ax1 = mp.subplots()
# plt.plot(x, y1, 'o-', c='orange', label ='Theory', linewidth=1)
# # plt.legend(loc=2, ncol = 1, mode='None')
# plt.plot(x, y2, '+-', c='blue', label ='Simulation', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
# ax1.set_xlabel('Transmission Success Probability',fontsize=10)
# ax1.set_ylabel('Consensus Success Probability',fontsize=10)
# # ax2.set_ylabel('Probability of Consensus Interruption(PBFT)',fontsize=10)
# plt.gcf().autofmt_xdate()
# plt.show()

# 共识成功概率与重传次数的关系
x = []
y1 = []
N = 100
F = 0
epsilon = 0.2
Retransis = np.arange(1, 21, 1)
for retrans in Retransis:
    x.append(retrans)
    p_comm1 = 0
    p_suc = 1-pow(1-epsilon,retrans)
    for f in range(int(N/2+1)-F,N-F):
        p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
    p_cp1 = 1-pow(p_comm1, int(N-F))
    y1.append(p_cp1)
y2 = [0, 0, 0, 0, 0.63, 0.82, 0.92, 0.88, 0.91, 0.96, 0.95, 0.95, 0.98, 0.97, 0.96, 1, 0.98, 0.99, 1, 1]

fig, ax1 = mp.subplots()
plt.plot(x, y1, 'o-', c='orange', label ='Theory', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, '+--', c='blue', label ='Simulation', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Retransmission Times',fontsize=10)
ax1.set_ylabel('Consensus Success Probability',fontsize=10)
# ax2.set_ylabel('Probability of Consensus Interruption(PBFT)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()

# # 共识成功概率与故障节点数量的关系
# x = []
# y1 = []
# N=100
# ratio = np.arange(0.0, 0.49, 0.03)
# epsilon = 0.8
# for r in ratio:
#     F = int(N*r)
#     x.append(r)
#     p_comm1 = 0
#     p_suc = epsilon
#     for f in range(int(N/2+1)-F,N-F):
#         p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
#     p_cp1 = 1-pow(p_comm1, int(N-F))
#     y1.append(p_cp1)
# y2 = [0.9, 0.88, 0.87, 0.88, 0.86, 0.86, 0.86, 0.83, 0.77, 0.59, 0.37, 0.16, 0.04, 0, 0, 0, 0]
# fig, ax1 = mp.subplots()
# plt.plot(x, y1, 'o-', c='orange', label ='Theory', linewidth=1)
# # plt.legend(loc=2, ncol = 1, mode='None')
# plt.plot(x, y2, '+-', c='red', label ='Simulation', linewidth=1)
# plt.legend(loc=3, ncol = 1, mode='None')
# #标签设置字体大小设置
# plt.xlabel('Malicious Nodes Ratio',fontsize=10)
# plt.ylabel('Consensus Success Probability',fontsize=10)
# plt.show()

# # 绘制三维图
# fig = plt.figure()
# ax3 = plt.axes(projection='3d')
# N=100
# x1 = np.arange(0.0, 1.01, 0.01)
# x2 = N*np.arange(0.0, 0.49, 0.01)
# p_suc, F = np.meshgrid(x1, x2)
# y1 = 7*p_suc + 9*F
# ax3.plot_surface(p_suc, F, y1, cmap='rainbow')
# plt.show()