import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = np.arange(50, 501, 50)
y1 = [18291, 17436, 16941, 15797, 14404, 12149, 10207, 7517, 6021, 4601]
y2 = [9487, 9393, 9018, 8761, 8261, 7493, 6881, 5814, 4546, 3624]
y3 = [4875, 4789, 4725, 4671, 4540, 4355, 3992, 3549, 3035, 2446]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='0.5MB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='1MB', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='2MB', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Network Sizes',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()