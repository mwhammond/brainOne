from brian2 import *
import time
import matplotlib.pyplot as plt
#1 neuron
#1 input
# connect second

# monitor waveform
CURRENT = 5


theta = 5*mV
Vr = 10*mV
tau = 20*ms
muext = 25*mV
sigmaext = 1*mV
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT
duration = 500*ms
we = 2*mV

# vars from synaptic model

taum = 10*ms
taupre = 20*ms
taupost = taupre
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms

# synapse variables

gmax = .01
dApre = .01
taupre = 20*ms
taupost = taupre
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax
taue = 5*ms


# ========================================================

# Pick an electrophysiological behaviour

tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking


eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + I - wa)/C : volt
dwa/dt = (a*(vm - EL) - wa)/tauw : amp
dge/dt = -ge / taue : siemens
I : amp
"""

eqs_neurons = '''
dvm/dt = (ge * (Ee-vr) + El - vm + I) / taum : volt
dge/dt = -ge / taue : 1
I : amp
'''

eqs_LIF = '''
dv/dt = (-g_l*(v-E_l) + I_syn_e) / C : volt
dg_e/dt = -g_e/tau_syn_e : siemens
I_syn_e = g_e*(E_syn_e - v) : amp
C : farad
g_l : siemens
E_l : volt
I_inject : amp
v_t : volt
v_r : volt
tau_syn_e : second
E_syn_e : volt
'''

#

#eqs = '''
#dvm/dt = (ge*(EL - vm) + ge*DeltaT*exp((vm - VT)/DeltaT)) : volt
#dge/dt = -ge / taue : 1
#'''


##### GROUP CREATION #####
layer1 = NeuronGroup(36, model=eqs_neurons, threshold='vm>Vcut', reset="vm=Vr")

#layer1 = NeuronGroup(36, eqs, threshold='vm>vt', reset='vm = vr')
#layer2 = NeuronGroup(12, eqs, threshold='vm>vt', reset='vm = vr')

layer2 = NeuronGroup(12, model=eqs_neurons, threshold='vm>Vcut', reset="vm=Vr")

#layer3 = NeuronGroup(12, model=eqs, threshold='vm>Vcut',
#                     reset="vm=Vr; w+=b")

#layer4 = NeuronGroup(4, model=eqs, threshold='vm>Vcut',
#                     reset="vm=Vr; w+=b")




### SYNAPSE FROM INPUT #######


S = Synapses(layer1, layer2,
             '''w : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''ge += w
                    Apre += dApre
                    w = clip(w + Apost, 0, gmax)''',
             post='''Apost += dApost
                     w = clip(w + Apre, 0, gmax)''',
             connect=True,
             )
                     
S.w = 'rand() * gmax'



# without STDP

#S1 = Synapses(stimulation, hidden, pre='v_post += we')
#S1.connect('i!=j')
#S1.w = 1

# with STDP





### STIMULATING #######

@network_operation(dt=100*ms)
def update_active():
    layer1.I = CURRENT*pA # SET TO SPECIFIC CELLS

    
    

    

#stimulation = NeuronGroup(1, 'dx/dt = 300*Hz : 1', threshold='x>1', reset='x=0')





### MONITORING ########
        

#statemonStim = StateMonitor(stimulation, 'v', record=True)
#spikesStim = SpikeMonitor(stimulation, record=True)

statemonHidden = StateMonitor(layer2, 'vm', record=True)
spikesHidden = SpikeMonitor(layer2, record=True)


#def runit():

run(duration, report='text')
print "running"

#subplot(221)
#plot(statemonHidden.t/ms, statemonHidden.vm[1])

figure()    
#v = statemonHidden[0].vm[:]
#for t in spikesHidden.t:
#    i = int(t / defaultclock.dt)
#    v[i] = 20*mV
#plot(statemonHidden.t / ms, v / mV)
plot(statemonHidden.t/ms, statemonHidden.vm[1])


#subplot(222)


def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')

#visualise_connectivity(S)
show()    



