import random
import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

PL = 20*np.log10(0.125/(4*np.pi))
beta = 10
Pt = pow(10, -2)
Pn=pow(10, -9)
p=0.005
N=500
p = 1/N
sigma = 0.9999
p_comp = N*p*pow(1-p,N-1)/(1-pow(1-p,N))
x_comp = np.log(1-sigma)/np.log(1-p_comp)
print("p_comp = ", p_comp)
print("x_comp = ", round(x_comp))
d = 143
expont = pow(10, 0.1 *PL)*beta*Pt*Pn*pow(d, 5)
print("exponent=",expont)
m_epsilon = 1-pow(2.7, -expont)
# m_epsilon = 0.0005
xi = 0.9999
x_trans = np.log(1-pow(xi,N))/np.log(m_epsilon)
print("max epsilon=", m_epsilon)
print("x_trans=", x_trans)
print("x_trans=", round(x_trans))
# N = np.arange(100, 1501, 50)
P=np.arange(0.01, 0.61, 0.01)
n=100
x = []
y = []
for p in P:
    x.append(p)
    p_comp = n*p*pow(1-p,n-1)/(1-pow(1-p,n))
    y.append(p_comp)
# plt.plot(x, y, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.show()
