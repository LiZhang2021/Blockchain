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
# y1 = [0.1167, 0.222515, 0.32069, 0.424165, 0.528185, 0.627535, 0.732425, 0.83374, 0.93467, 1.037325]
# y2 = [0.16358, 0.26951, 0.371725, 0.474475, 0.57222, 0.68039, 0.780355, 0.88072, 0.98085, 1.088475]
# y3 = [0.45889, 0.641045, 0.66045, 0.78052, 0.902685, 1.01543, 1.116145, 1.22234, 1.29809, 1.42348]

y1 = [0.11632, 0.21955, 0.319585, 0.42341, 0.525735, 0.6283, 0.731445, 0.833075, 0.933845, 1.03961]
y2 = [0.168535, 0.271395, 0.371395, 0.473885, 0.571935, 0.67568, 0.780925, 0.881665, 0.98029, 1.08508]
y3 = [0.45232, 0.58194, 0.709795, 0.80221, 0.891385, 1.05161, 1.15682, 1.200355, 1.35357, 1.488765]


fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='100 Nodes', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='300 Nodes', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='500 Nodes', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Block Sizes(MB)',fontsize=10)
ax1.set_ylabel('Average Latency(sec.)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()