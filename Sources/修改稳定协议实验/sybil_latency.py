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
# y1 = [0.214965, 0.215655, 0.19636, 0.217775, 0.217125, 0.15878, 0.18031, 0.201845, 0.10572, 0.210755]
# y2 = [0.26729, 0.26161, 0.22318, 0.25583, 0.23627, 0.23238, 0.214695, 0.214685, 0.21554, 0.218045]
# y3 = [0.58152, 0.476725, 0.466345, 0.42336, 0.39809, 0.383925, 0.370145, 0.31024, 0.303465, 0.265285]

y1 = [0.21545, 0.216365, 0.21604, 0.19814, 0.217705, 0.159845, 0.181425, 0.201045, 0.184115, 0.170655]
y2 = [0.24776, 0.261335, 0.22083, 0.236635, 0.236325, 0.21536, 0.178645, 0.21668, 0.23172, 0.2202]
y3 = [0.546585, 0.50216, 0.453375, 0.41701, 0.39222, 0.337535, 0.35245, 0.310665, 0.286795, 0.283625]

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