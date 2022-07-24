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

y1 = [2.177899, 1.15579, 0.791203, 0.600025, 0.486209, 0.408014, 0.353558, 0.309256, 0.276497, 0.252218]
y2 = [0.252331, 0.251838, 0.252073, 0.252339, 0.251917, 0.252579, 0.252388, 0.252327, 0.251586, 0.252352]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='Random', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, '+-', c='blue', label ='Consecutive', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Jamming Bound(Delta)',fontsize=10)
ax1.set_ylabel('Average Consensus Latency(s)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()