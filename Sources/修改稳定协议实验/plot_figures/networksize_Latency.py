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
y1 = [0.2162, 0.22078, 0.228775, 0.238285, 0.25468, 0.27585, 0.319615, 0.372035, 0.4694, 0.4777, 0.653795, 0.724875]
y2 = [0.420995, 0.426195, 0.434505, 0.44362, 0.46088, 0.48419, 0.516175, 0.583305, 0.63343, 0.75854, 0.868285, 0.919025]
y3 = [0.83036, 0.83531, 0.84129, 0.85235, 0.86711, 0.89434, 0.93308, 1.000105, 1.07747, 1.11665, 1.289905, 1.55807]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='0.5MB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='1MB', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='2MB', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Network Sizes',fontsize=10)
ax1.set_ylabel('Average Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()