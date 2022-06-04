import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = np.arange(50, 501, 50)
y1 = [0.11191, 0.117395, 0.12083, 0.12958, 0.14211, 0.16849, 0.20054, 0.27228, 0.33995, 0.44485]
y2 = [0.21576, 0.21791, 0.22697, 0.233635, 0.24779, 0.27316, 0.297455, 0.35207, 0.450215, 0.56476]
y3 = [0.419855, 0.427385, 0.43315, 0.4382, 0.45084, 0.46994, 0.512715, 0.57672, 0.674305, 0.836775]

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