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
y1 = [0.215435, 0.21806, 0.222925, 0.23291, 0.246645, 0.26896, 0.305145, 0.356705, 0.446395, 0.49506, 0.62967, 0.694655]
y2 = [0.22312, 0.23148, 0.244625, 0.261555, 0.28932, 0.329235, 0.403545, 0.52163, 0.705705, 1.01761, 1.51931, 2.416515]


fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o-', c='blue', label ='PBFT', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Network Sizes',fontsize=10)
ax1.set_ylabel('Average Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()