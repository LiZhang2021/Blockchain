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
y1 = [0.894441, 1.013594, 1.021473, 1.11347, 1.240722, 1.321944, 1.325152, 1.463664, 1.528732, 1.79757]
y2 = [0.696391, 0.773161, 0.910062, 0.911144, 0.938167, 0.969302, 1.017247, 1.162423, 1.262502, 1.444638]
y3 = [0.49794, 0.578208, 0.65221, 0.676112, 0.682336, 0.748049, 0.771418, 0.880671, 0.984171, 1.167806]

fig, ax1 = mp.subplots()
# ax2= ax1.twinx()
plt.plot(x, y1, 'o-', c='orange', label ='0.7', linewidth=1)
# plt.legend(loc=2, ncol = 1, mode='None')
plt.plot(x, y2, 'o--', c='blue', label ='0.8', linewidth=1)
plt.plot(x, y3, '+-', c='green', label ='0.9', linewidth=1)
plt.legend(loc=2, ncol = 1, mode='None')
ax1.set_xlabel('Network Size',fontsize=10)
ax1.set_ylabel('Average Consensus Latency(s)',fontsize=10)
plt.gcf().autofmt_xdate()
plt.show()