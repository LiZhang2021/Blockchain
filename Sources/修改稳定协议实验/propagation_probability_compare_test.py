import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

N = 100
# epsilon = 0.5
x = np.arange(0, 1.1, 0.1)
y1 = [0, 0, 0, 0, 0.03, 0.6, 0.83, ]
y2 = []

# y = savgol_filter(y,15, 3,  mode= 'nearest')
plt.plot(x, y)
#设置横纵坐标字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#标签设置字体大小设置
plt.xlabel('Probability of Communication Interruption',fontsize=14)
plt.ylabel('Probability of Consensus Interruption',fontsize=14)
plt.show()