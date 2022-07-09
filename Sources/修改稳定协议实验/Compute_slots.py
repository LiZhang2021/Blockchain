import random
import numpy as np
from scipy.special import perm, comb
import matplotlib.pyplot as plt
import matplotlib.pylab as mp
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

PL = 20*np.log10(0.125/(4*np.pi))
beta = 10
Pt = 100
Pn=pow(10, -9)
p=0.005
N=500
p = 1/N
sigma = 0.95
xi = 0.95
p_comp = N*p*pow(1-p,N-1)/(1-pow(1-p,N))
d = 143
expont = pow(10, 0.1 *PL)*beta*Pn*pow(d, 5)/Pt
print("exponent=",expont)
m_epsilon = 1-pow(np.e, -expont)
## 给定目标竞争成功概率和目标传输成功概率
p_suc = sigma*xi
p_comm = 0
x = []
y1=[]
for N in range(100,500, 50):
    x.append(N)
    for f in range(int(N/2+1),N-1):
        p_comm = p_comm + comb(N-1, f)* pow(1-p_suc,f)*pow(p_suc, N-1-f)
    p_cp = p_suc * (1-p_comm) * p_suc
    print("p_consensus = ", p_cp)
    y1.append(p_cp)
# plt.plot(x, y, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.show()

x = []
y=[]
p_comm = 0
for N in range(100,500, 50):
    p = 1/N
    p_c = N*p*pow(1-p,N-1)/(1-pow(1-p,N))
    print("p_c = ", p_c)
    expont = pow(10, 0.1 *PL)*beta*Pn*pow(d, 3)/Pt
    print("exponent=",expont)
    epsilon = 1-pow(np.e, -expont)
    p_suc= p_c*(1-epsilon)
    print("max epsilon=", epsilon)
    x.append(N)
    for f in range(int(N/2+1),N-1):
        p_comm = p_comm + comb(N-1, f)* pow(1-p_suc,f)*pow(p_suc, N-1-f)
    p_cp = p_suc * (1-p_comm) * p_suc
    print("p_consensus = ", p_cp)
    y.append(p_cp)
# plt.plot(x, y, 'o--', c='red', label ='SWIB', linewidth=1)
# plt.plot(x, y1, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.show()


# N = np.arange(100, 1501, 50)
P=np.arange(0.01, 0.61, 0.01)
n=100
x_comp = np.log(1-sigma)/np.log(1-p_comp)
print("p_comp = ", p_comp)
print("x_comp = ", round(x_comp))
x = []
y = []
for p in P:
    x.append(p)
    p_comp = n*p*pow(1-p,n-1)/(1-pow(1-p,n))
    y.append(p_comp)
# plt.plot(x, y, 'o-', c='orange', label ='SWIB', linewidth=1)
# plt.show()
x = []
y=[]
N = 100
Xis = np.arange(0.1, 1.1, 0.1)
m_epsilon = 0.0005
for xi in Xis:
    x.append(xi)
    x_trans = np.log(1-pow(xi,N))/np.log(m_epsilon)
    y.append(x_trans)
plt.plot(x, y, 'o-', c='orange', label ='SWIB', linewidth=1)
plt.show()
# print("max epsilon=", m_epsilon)
# print("x_trans=", x_trans)
# print("x_trans=", round(x_trans))


