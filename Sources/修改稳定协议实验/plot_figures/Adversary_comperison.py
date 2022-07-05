import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x1 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.5, 0.5, 0.5, 0.5]
x2 = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.33,0.35, 0.35, 0.35, 0.35]
y1 = [0.839355, 0.78334, 0.84219, 0.81093, 0.874765, 0.849735, 0.9265, 0.911715, 0.99778, 1, 1.5, 2, 2.5, 3]
y2 = [1.12686, 1.029315, 0.98776, 0.925825, 0.95962, 0.934395, 1, 1.5, 2, 2.5, 3]
fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x1, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x2, y2, 'o-', c='blue', label ='PBFT', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Adversary Power',fontsize=10)
ax1.set_ylabel('Aversage Consensus Latency(s)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()