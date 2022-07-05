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
y1 = [0.420995, 0.426195, 0.434505, 0.44362, 0.46088, 0.48419, 0.516175, 0.583305, 0.63343, 0.75854, 0.868285, 0.919025]
y2 = [0.430685, 0.44282, 0.458665, 0.481355, 0.51188, 0.560395, 0.63006, 0.744415, 0.943125, 1.24534, 1.770565, 2.649845]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o-', c='blue', label ='PBFT', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Network Size',fontsize=10)
ax1.set_ylabel('Average Consensus Latency(s)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()