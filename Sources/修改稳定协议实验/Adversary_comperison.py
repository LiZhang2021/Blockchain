import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x1 = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.5, 0.5, 0.5, 0.5]
x2 = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35,0.35, 0.35, 0.35, 0.35]
y1 = [0.64179, 0.576735, 0.63481, 0.65252, 0.695415, 0.758285, 0.803575, 0.86821, 0.93147,  0.99648, 1, 1.5, 2, 2.5, 3]
y2 = [0.873105, 0.738983, 0.76793, 0.783715, 0.810735, 0.861835, 0.925255, 1, 1.5, 2, 2.5, 3]


fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x1, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x2, y2, 'o-', c='blue', label ='PBFT', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Adversary Power',fontsize=10)
ax1.set_ylabel('Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()