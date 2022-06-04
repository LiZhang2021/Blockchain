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
y1 = [9141, 8714, 8466, 7894, 7198, 6071, 5101, 3757, 3009, 2299]
y2 = [9487, 9393, 9018, 8761, 8261, 7493, 6881, 5814, 4546, 3624]
y3 = [9753, 9581, 9453, 9345, 9083, 8713, 7986, 7100, 6072, 4893]

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