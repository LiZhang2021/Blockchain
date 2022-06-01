import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


N = 100
p_hard = 0.33
# N = np.arange(100, 1501, 50)
x = np.arange(0.5, 5.1, 0.5)
y1 = [8766, 9199, 9576, 9654, 9691, 9789, 9785, 9824, 9859, 9870]
y2 = [6253, 7595, 8261, 8630, 8945, 9028, 9184, 9300, 9394, 9406]
y3 = [2229, 3193, 4649, 5246, 5670, 6049, 6421, 6701, 7098, 7192]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='100 Nodes', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='300 Nodes', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='500 Nodes', linewidth=1)
plt.legend(loc=4, ncol = 1, mode='None')
ax1.set_xlabel('Block Sizes(MB)',fontsize=10)
ax1.set_ylabel('Average Throughput(TPS)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()