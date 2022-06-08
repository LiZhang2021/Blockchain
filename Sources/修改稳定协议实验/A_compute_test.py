import numpy as np
# 参考路径丢失
PL = 20*np.log10(0.125/(4*np.pi))
print('PL=', PL)
beta = 10
Pt = pow(10, -2)
Pn=pow(10, -10)
d_max = 143
M = 1024
B = 20*pow(10,6)
ev = pow(10, int(PL/10))*beta*Pn*Pt*pow(d_max, 3)
epsilon = 1-pow(np.e,-ev)
print('epsilon=', epsilon)
p_suc = 1 - epsilon
print('p_suc=', p_suc)
tau_o = M/(B*np.log10(1+beta))
print("tau_o = ", tau_o)
tau_1 = M/(B*np.log10(1+2*beta))
print("tau_1 = ", tau_1)
t = [1, 2, 4]
y1 = [0.11632, 0.21955, 0.319585, 0.42341, 0.525735, 0.6283, 0.731445, 0.833075, 0.933845, 1.03961]
print("y1 = ",y1)
y = np.multiply(2,y1)
print("y = ",y)