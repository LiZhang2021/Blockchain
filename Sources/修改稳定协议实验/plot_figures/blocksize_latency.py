import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(0.5, 5.1, 0.5)
x = np.arange(0.5, 5.1, 0.5)
y1 = [0.22089, 0.42765, 0.631445, 0.834715, 1.04151, 1.24461, 1.45258, 1.65496, 1.86174, 2.065645]
y2 = [0.27899, 0.479915, 0.691975, 0.890145, 1.090425, 1.299245, 1.504055, 1.70748, 1.915645, 2.116665]
y3 = [0.57744, 0.74509, 1.074285, 1.194955, 1.3592, 1.64897, 1.817745, 2.059735, 2.299515, 2.46613]



fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='100 Nodes', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='300 Nodes', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='500 Nodes', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Block Size(MB)',fontsize=10)
ax1.set_ylabel('Average Consensus Latency(s)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()