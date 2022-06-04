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
y1 = [9473, 8541, 8472, 7520, 7440, 6470, 6405, 5477, 5401, 5248]
y2 = [7296, 6894, 5992, 5802, 5900, 5130, 4993, 4222, 4163, 3454]
y3 = [3615, 3768, 3859, 3126, 3222, 2837, 2509, 2412, 2398, 2598]

# y1 = [9501, 9460, 9475, 9297, 9402, 8964, 9026, 9163, 8894, 8396]
# y2 = [7435, 7832, 7415, 7785, 7795, 7604, 6875, 7557, 7950, 7436]
# y3 = [3745, 4076, 4515, 4908, 4697, 3638, 5227, 5271, 4996, 5052]

# y1 = [9516, 9393, 9415, 9265, 9283, 9087, 8967, 8741, 8598, 8389]
# y2 = [7729, 7510, 7552, 7670, 7900, 7587, 7711, 7316, 7374, 6839]
# y3 = [3912, 4102, 4931, 4565, 4943, 6037, 5416, 5205, 5612, 5238]

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