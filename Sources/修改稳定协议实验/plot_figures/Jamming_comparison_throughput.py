import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = np.arange(0.1, 1.1, 0.1)
y1 = [535, 1028, 1586, 1777, 2131, 2894, 2596, 3371, 3686, 3948]
y2 = [3929, 3936, 3775, 4135, 3707, 3938, 3778, 3903, 4044, 4407]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=4, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='Perpetual', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()