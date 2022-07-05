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

y1 = [5.248675, 3.02318, 2.1719, 1.696375, 1.309455, 1.10186, 1.057095, 0.946115, 0.83568, 0.754075]
y2 = [0.721575, 0.766155, 0.78104, 0.793475, 0.78754, 0.779275, 0.78785, 0.71262, 0.71631, 0.70784]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='Consecutive', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Consensus Latency(s)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()