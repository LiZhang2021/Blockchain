import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49]
# Sybil not send
# y1 = [4824, 4347, 4319, 3849, 3847, 3373, 3364, 2885, 2855, 2847]
# y2 = [4328, 3901, 3497, 3562, 3576, 3160, 3175, 2732, 2733, 2268]
# y3 = [2523, 2671, 2546, 2676, 2418, 2618, 2325, 2373, 2063, 2089]
# Sybil send
y1 = [9528, 9516, 9502, 9287, 9442, 9416, 8393, 8531, 8061, 7510]
y2 = [8769, 8750, 8709, 8104, 8425, 7074, 8093, 7231, 6970, 7640]
y3 = [8111, 7921, 8082, 7678, 8000, 7420, 7184, 6763, 6633, 5781]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='100 Nodes', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='300 Nodes', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='500 Nodes', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Percentage of Sybil Nodes',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()