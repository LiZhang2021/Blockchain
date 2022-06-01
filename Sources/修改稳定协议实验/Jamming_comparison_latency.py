import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(0.5, 5.1, 0.5)
x = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49]
y1 = [6.625825, 4.073615, 3.200745, 2.273245, 1.973015, 1.624325, 1.382645, 1.269835, 1.19725, 1.00319]
y2 = [0.29663, 0.296275, 0.295155, 0.296455, 0.29402, 0.29586, 0.29542, 0.29625, 0.296535, 0.2981]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='Bursty', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()