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
y1 = [2288, 2019, 2003, 1838, 1649, 1548, 1544, 1398, 1339, 1138]
y2 = [2939, 2647, 2249, 2246, 2181, 2111, 2012, 1760, 1621, 1416]
y3 = [4110, 3540, 3138, 3027, 2999, 2736, 2653, 2324, 2079, 1752]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='0.7', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='0.8', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='0.9', linewidth=1)
# plt.plot(x, y3, '+-', c='green', label ='2MB', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Network Sizes',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()