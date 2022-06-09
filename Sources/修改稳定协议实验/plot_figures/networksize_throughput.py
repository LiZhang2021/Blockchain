import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = np.arange(50, 601, 50)
y1 = [4731, 4633, 4471, 4293, 4016, 3708, 3200, 2749, 2179, 2141, 1564, 1411]
y2 = [4862, 4802, 4711, 4614, 4441, 4227, 3965, 3509, 3231, 2698, 2357, 2227]
y3 = [4931, 4902, 4867, 4804, 4722, 4578, 4388, 4094, 3800, 3667, 3174, 2628]

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