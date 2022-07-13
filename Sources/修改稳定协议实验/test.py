import random
import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

# sigmas = np.arange(0.05, 1, 0.05)
# x = []
# y1 = []
# y2 = []
# y21 = []
# y3 = 0
# Nodes = np.arange(5, 1001, 5)
# n = 100
# vars = 0.7
# for n in Nodes:
#     x.append(n)
#     p = 1/n
#     # p = 0.0125
#     p_comp = n*p*pow(1-p,n-1)/(1-pow(1-p,n))
#     # print("p_comp=", p_comp)
#     # print("np.log(1-vars)=",np.log(1-vars))
#     # print("np.log(1-p_comp)=",np.log(1-p_comp))
#     x_comp = np.log(1-vars)/np.log(1-p_comp)
#     y1.append(x_comp)
#     y2.append(np.log(1-vars)/np.log(1-(1/(np.e-1))))
#     # y2.append(-np.e/np.log(1-p))
#     # y21.append(n) 
#     # if p_comp+np.e/np.log(1-p) >=0:
#     #     y3 += 1
# # print("y3 = ", y3)
#     if x_comp - np.log(1-vars)/np.log(1-(1/(np.e-1))) >=0:
#         y3 += 1
# print("y3 = ", y3)
#     # y2.append(1/(1-vars)*pow(np.e,-1))
# plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.plot(x, y2, 'o-', c='red', label ='SWIB', linewidth=1)
# # plt.plot(x, y21, 'o-', c='green', label ='SWIB', linewidth=1)
# plt.show()

x = []
y1= []
y2 = []
y4 = []
y3 = 0
N = 100
Nodes = np.arange(5, 1001, 15)
Xis = np.arange(0.05, 1, 0.05)
m_epsilon = 0.1
xi = 0.9
for N in Nodes:
    x.append(N)
    x_trans = np.log(1-pow(xi,1/N))/np.log(m_epsilon)
    y1.append(x_trans)
    y2.append(np.log(-np.log(xi)/(N-np.log(xi)))/np.log(m_epsilon))
    if (np.log(1-N/(N-np.log(xi)))/np.log(m_epsilon)) -x_trans<=0:
        y3 +=1
    y4.append(-3*np.log(N)/np.log(m_epsilon))
print("y3 = ", y3)
plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.plot(x, y2, 'o', c='red', label ='SWIB', linewidth=1)
plt.plot(x, y4, 'o--', c='green', label ='SWIB', linewidth=1)
plt.show()