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
# Sybil not send
# y1 = [0.424315, 0.42377, 0.426475, 0.42543, 0.42567, 0.424775, 0.42584, 0.42567, 0.43017, 0.43138]
# y2 = [0.47288, 0.472185, 0.468245, 0.459615, 0.457845, 0.453375, 0.451295, 0.449445, 0.449345, 0.451125]
# y3 = [0.72998, 0.689595, 0.643065, 0.61195, 0.592415, 0.54729, 0.528175, 0.51742, 0.49611, 0.48979]
# Sybil send
y1 = [0.424515, 0.42401, 0.42486, 0.42544, 0.42425, 0.42591, 0.427175, 0.429535, 0.43304, 0.437775]
y2 = [0.48055, 0.474275, 0.471805, 0.4658, 0.4645, 0.46608, 0.465265, 0.46273, 0.46797, 0.46898]
y3 = [0.775125, 0.71136, 0.66155, 0.626495, 0.63776, 0.613435, 0.58212, 0.55756, 0.54991, 0.553395]

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