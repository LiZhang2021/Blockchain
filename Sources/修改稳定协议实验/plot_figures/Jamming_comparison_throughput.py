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
y1 = [939, 1771, 2587, 3411, 4210, 5016, 5789, 6619, 7403, 8115]
y2 = [8112, 8128, 8120, 8112, 8125, 8104, 8110, 8112, 8136, 8111]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=4, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='Consecutive', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()