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
y1 = [0.214325, 0.21828, 0.22472, 0.23073, 0.249815, 0.273545, 0.31252, 0.37097, 0.43859, 0.56358]
y2 = [0.222495, 0.23114, 0.24471, 0.262395, 0.29102, 0.33395, 0.394755, 0.509945, 0.71289, 1.000745]


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