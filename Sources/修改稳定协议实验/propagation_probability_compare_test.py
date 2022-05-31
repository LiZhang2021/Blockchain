import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = np.arange(0, 1.01, 0.05)
y1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.14, 0.93, 1, 1, 1, 1, 1, 1, 1, 1]
y2 = [0, 0.87, 0.98, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o-', c='blue', label ='PBFT', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Probability of Communication Interruption',fontsize=10)
ax1.set_ylabel('Probability of Consensus Interruption',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()