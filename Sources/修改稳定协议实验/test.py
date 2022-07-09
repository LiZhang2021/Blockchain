import random
import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

# sigmas = np.arange(0.05, 1, 0.05)
# x = []
# y = []
# n = 100
# p = 1/n
# p_comp = n*p*pow(1-p,n-1)/(1-pow(1-p,n))
# print("p_comp=", p_comp)
# for vars in sigmas:
#     x.append(vars)
#     # print("np.log(1-vars)=",np.log(1-vars))
#     # print("np.log(1-p_comp)=",np.log(1-p_comp))
#     x_comp = np.log(1-vars)/np.log(1-p_comp)
#     y.append(round(x_comp)+1)
# plt.plot(x, y, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.show()

x = []
y=[]
N = 100
Xis = np.arange(0.05, 1, 0.05)
m_epsilon = 0.005
for xi in Xis:
    x.append(xi)
    x_trans = np.log(1-pow(xi,1/N))/np.log(m_epsilon)
    y.append(x_trans)
    # y.append(round(x_trans)+1)
plt.plot(x, y, 'o-', c='orange', label ='SWIB', linewidth=1)
plt.show()