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
y1 = [8415, 8414, 8385, 8373, 7288, 7269, 6232, 6217, 8175, 6018]
y2 = [6730, 7079, 7120, 6354, 6409, 7502, 7559, 4817, 6674, 6649]
y3 = [3854, 4015, 4692, 4354, 5144, 4301, 5310, 6184, 5690, 5778]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='100 Nodes', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='300 Nodes', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='500 Nodes', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Percentage of Sybil Nodes',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()