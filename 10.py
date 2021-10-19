from numpy import *
from matplotlib.pyplot import *
from brian2 import *


start_scope()
eqs = '''
dv/dt = (0.04*v**2 + 5*v + 140 - u + I)/ms : 1 
du/dt = a*((b*v) - u)/ms : 1
a = 0.02: 1
b = 0.2: 1
c = -65: 1
d = 8: 1
I : 1
'''
reset = '''
v = c
u = u + d
'''
#Reset koşulu da dışarıda tanımlanabilir. 
G = NeuronGroup(1, eqs, method='euler', threshold = 'v>30',reset = reset)

stm = StateMonitor(G, 'v', record = 0)

G.I = 10
run(300*ms)

figure()
plot(stm.t/ms, stm.v[0])
