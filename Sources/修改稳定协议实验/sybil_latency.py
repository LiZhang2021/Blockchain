import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(0.5, 5.1, 0.5)
x = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49]
y1 = [0.218925, 0.218935, 0.21971, 0.220015, 0.22467, 0.225285, 0.229915, 0.23045, 0.225335, 0.23807]
y2 = [0.273715, 0.260235, 0.258745, 0.25769, 0.25551, 0.245565, 0.2437, 0.25495, 0.24537, 0.246275]
y3 = [0.47799, 0.458765, 0.392565, 0.42305, 0.358085, 0.333095, 0.308375, 0.297875, 0.2878, 0.2834]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='100 Nodes', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='300 Nodes', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='500 Nodes', linewidth=1)
plt.legend(loc=1, ncol = 1, mode='None')
ax1.set_xlabel('Percentage of Sybil Nodes',fontsize=10)
ax1.set_ylabel('Average Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()