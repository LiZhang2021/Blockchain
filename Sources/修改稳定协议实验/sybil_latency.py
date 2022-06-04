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
y1 = [0.216085, 0.215685, 0.217455, 0.21774, 0.22008, 0.221435, 0.223715, 0.224245, 0.227375, 0.234025]
y2 = [0.280545, 0.267225, 0.27328, 0.282245, 0.277545, 0.279315, 0.286935, 0.29084, 0.29498, 0.296245]
y3 = [0.566245, 0.543145, 0.5304, 0.589335, 0.635185, 0.577035, 0.65259, 0.593865, 0.597335, 0.63011]

# y1 = [0.21545, 0.216365, 0.21604, 0.19814, 0.217705, 0.159845, 0.181425, 0.201045, 0.184115, 0.170655]
# y2 = [0.24776, 0.261335, 0.22083, 0.236635, 0.236325, 0.21536, 0.178645, 0.21668, 0.23172, 0.2202]
# y3 = [0.546585, 0.50216, 0.453375, 0.41701, 0.39222, 0.337535, 0.35245, 0.310665, 0.286795, 0.283625]

# y1 = [0.21509, 0.196115, 0.19566, 0.17674, 0.176405, 0.15767, 0.15979, 0.140495, 0.142845, 0.14639]
# y2 = [0.264815, 0.24529, 0.216835, 0.213495, 0.20729, 0.188855, 0.18581, 0.167875, 0.16655, 0.149645]
# y3 = [0.523165, 0.449015, 0.41511, 0.35871, 0.331255, 0.33905, 0.264555, 0.235965, 0.218815, 0.19539]

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