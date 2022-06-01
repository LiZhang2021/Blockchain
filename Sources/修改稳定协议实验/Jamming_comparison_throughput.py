import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49]
y1 = [308, 502, 639, 900, 1037, 1260, 1480, 1612, 1709, 2040]
y2 = [6900, 6909, 6935, 6904, 6962, 6918, 6929, 6909, 6903, 6866]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='Bursty', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()