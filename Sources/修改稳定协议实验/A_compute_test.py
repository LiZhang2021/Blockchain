import numpy as np
PL = 20*np.log10(0.125/(4*np.pi))
print('PL=', PL)
beta = 2
Pt = 100
Pn=pow(10, 9)
d_max = 142
ev = pow(10, int(PL/10))*beta*Pn*Pt*pow(d_max, -3)
epsilon = 1-pow(np.e,-ev)
print('epsilon=', epsilon)