from brian2 import *

start_scope()



# Parameters
#neuron parameters
Vthr = 30 * mvolt       # threshold value for Izhikevich neuron
EL = -75 * mV           # initial value of membrane potentials

# cortex with excitatory and inhibitory neuron populations.
number_of_neurons_in_pyramid = 900
number_of_neurons_in_crtx_in = 100


#synaptic parameters
tau_s = 1 * ms          # time constant for synatic dynamics
we = 0.1 *amp/mV        # weights for excitatory synapses
wi = 0.1 *amp/mV        # weights for inhibitory synapses
Vi = -90 * mV           # resting potential for inhibitory synaptic currents.
Ve = 0 * mV             # resting potential for excitatory synaptic currents.
dly=(3+rand())*ms       # axonal and synaptic delay 

    
print('Equations')

eqs_dyn = """
dv/dt=(0.04/ms/mV)*v**2+(5/ms)*v+140*mV/ms-u/ms+I*mV/(amp*ms)+Is*mV/(amp*ms) : volt
du/dt=a*(b*v-u)/ms                                           : volt
I : amp
Is=ge*(Ve-v)+gi*(Vi-v) :  amp
dge/dt=-ge/tau_e	: amp/volt
dgi/dt=-gi/tau_i	: amp/volt
a : 1
b : 1
c : volt
d : volt
tau_e : second
tau_i : second
"""


# reset condition for Izhikevich neuron.
eqs_reset = '''
v = c
u = u+d
'''

pyramid = NeuronGroup(number_of_neurons_in_pyramid, model=eqs_dyn, method='rk4', threshold='v>Vthr', reset=eqs_reset)


for i in range(number_of_neurons_in_pyramid):
    pyramid.a[i] = 0.02
    pyramid.b[i] = 0.2
    pyramid.c[i] = -65 * mvolt        
    pyramid.d[i] = 8 * mvolt 
    pyramid.v[i] = EL
    pyramid.u[i] = -14.5 * mvolt
pyramid.tau_e = tau_s
pyramid.tau_i = tau_s





crtx_in = NeuronGroup(number_of_neurons_in_crtx_in, model=eqs_dyn, method='rk4', threshold='v>Vthr', reset=eqs_reset)


for i in range(number_of_neurons_in_crtx_in):
    crtx_in.a[i] = 0.01
    crtx_in.b[i] = 0.2
    crtx_in.c[i] = -65 * mvolt        
    crtx_in.d[i] = 2 * mvolt 
    crtx_in.v[i] = EL
    crtx_in.u[i] = -14.5 * mV
crtx_in.tau_e = tau_s
crtx_in.tau_i = tau_s




pyramid.I = 4*amp
crtx_in.I = 10*amp





###### Synapses #############
#############################
print('Synapses')
# The synaptic connection between and within neural structures are defined with “synapse”  of BRIAN2 is used.Each structure is coded with a number for example code of cortex is 1, pyramidal neuron population in cortex is coded with 11 and connection between pyramidal neurons and cortex IN is coded with 1112.



# 1  cortex
## 11 Pyramid


S1211 = Synapses(crtx_in, pyramid,  delay=dly, on_pre='gi += wi')
S1211.connect(True, p = 0.50)



# 12 IN

S1112 = Synapses(pyramid, crtx_in, delay=dly, on_pre='ge += we')
S1112.connect(True, p = 0.25)




###### Monitors ###########
###########################
print('Monitors')
# “StateMonitor” and "SpikeMonitor" commands of BRIAN are used to follow the behavior of  neurons during simulation.


trace_pyramid = StateMonitor(pyramid, 'v', record=True)
monge_pyramid = StateMonitor(pyramid, 'ge', record=True)
mongi_pyramid = StateMonitor(pyramid, 'gi', record=True)
spikes_pyramid = SpikeMonitor(pyramid)


trace_crtx_in = StateMonitor(crtx_in, 'v', record=True)
monge_crtx_in = StateMonitor(crtx_in, 'ge', record=True)
mongi_crtx_in = StateMonitor(crtx_in, 'gi', record=True)
spikes_crtx_in = SpikeMonitor(crtx_in)


import time
init_time=time.time()

run(1000*ms,report='text')

final_time=time.time()
print("Simulation Time:",str(final_time-init_time))

print("Pyramid : "+str(spikes_pyramid.num_spikes)+"  ---->  : " +str(spikes_pyramid.num_spikes/number_of_neurons_in_pyramid))
print("Crtx IN : "+str(spikes_crtx_in.num_spikes)+"  ---->  : " +str(spikes_crtx_in.num_spikes/number_of_neurons_in_crtx_in))


#########################################
############# --- Figures --- #########
#########################################
print('Figures')
#To see the results single neuron behavior figures are obtained.

figure()
subplot(411)
plot(trace_pyramid.t / ms, trace_pyramid[9].v / mV)
ylabel('v, mV (p)')

subplot(412)
plot(spikes_pyramid.t/ms, spikes_pyramid.i, '.k')

ylabel('Pyr');

subplot(413)
plot(trace_crtx_in.t / ms, trace_crtx_in[9].v / mV)
ylabel('v, mv (in)')

subplot(414)
plot(spikes_crtx_in.t/ms, spikes_crtx_in.i, '.k')
ylabel('IN')
xlabel('time, ms')



