import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(0.5, 5.1, 0.5)
x = np.arange(0.1, 1.1, 0.1)
y1 = [3.822835, 1.99029, 1.29058, 1.15162, 0.96018, 0.707125, 0.788425, 0.60711, 0.555275, 0.5184]
y2 = [3.629115, 2.41995, 1.546545, 1.372185, 0.93966, 0.925965, 0.815275, 0.62792, 0.610165, 0.579555]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='Perpetual', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()