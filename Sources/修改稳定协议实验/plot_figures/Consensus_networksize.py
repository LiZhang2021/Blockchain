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
# epsilons = np.arange(0.0, 1.01, 0.01)
# sigma = 0.9
# F=45
# N=1000
# for epsilon in epsilons:
#     x.append(epsilon)
#     p_comm1 = 0
#     p_suc = epsilon
#     for f in range(int(N/2+1)-F,N-F):
#         p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
#     p_cp1 = 1-pow(p_comm1, int(N-F))
#     y1.append(p_cp1)
# plt.plot(x, y1, 'o-', c='red', label ='SWIB', linewidth=1)
# #设置横纵坐标字体大小
# plt.xticks(fontsize=10)
# plt.yticks(fontsize=10)
# #标签设置字体大小设置
# plt.xlabel('Transmission Success Probability',fontsize=10)
# plt.ylabel('Consensus Success Probability',fontsize=10)
# plt.show()

# # 共识成功概率与节点数量的关系
# x = []
# y1 = []
# Nodes = np.arange(10, 1001, 5)
# F=0
# epsilon = 0.7
# for N in Nodes:
#     x.append(N)
#     p_comm1 = 0
#     p_suc = epsilon
#     for f in range(int(N/2+1)-F,N-F):
#         p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
#     p_cp1 = 1-pow(p_comm1, int(N-F))
#     y1.append(p_cp1)
# plt.plot(x, y1, 'o-', c='red', label ='SWIB', linewidth=1)
# #设置横纵坐标字体大小
# plt.xticks(fontsize=10)
# plt.yticks(fontsize=10)
# #标签设置字体大小设置
# plt.xlabel('Network Size',fontsize=10)
# plt.ylabel('Consensus Success Probability',fontsize=10)
# plt.show()

# 共识成功概率与故障节点数量的关系
x = []
y1 = []
N=500
ratio = np.arange(0.0, 0.49, 0.01)
epsilon = 0.7
for r in ratio:
    F = int(N*r)
    x.append(r)
    p_comm1 = 0
    p_suc = epsilon
    for f in range(int(N/2+1)-F,N-F):
        p_comm1 += comb(N-F-1, f)* pow(1-p_suc,f)*pow(p_suc, N-F-1-f)
    p_cp1 = 1-pow(p_comm1, int(N-F))
    y1.append(p_cp1)
plt.plot(x, y1, 'o-', c='red', label ='SWIB', linewidth=1)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('Malicious Nodes Ratio',fontsize=10)
plt.ylabel('Consensus Success Probability',fontsize=10)
plt.show()

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