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

gmax = .01 * siemens
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
dge/dt = -ge / taue : 1
I : amp
"""
#

#eqs = '''
#dvm/dt = (ge*(EL - vm) + ge*DeltaT*exp((vm - VT)/DeltaT)) : volt
#dge/dt = -ge / taue : 1
#'''


##### GROUP CREATION #####
layer1 = NeuronGroup(36, model=eqs, threshold='vm>Vcut', reset="vm=Vr; wa+=b")

#layer1 = NeuronGroup(36, eqs, threshold='vm>vt', reset='vm = vr')
#layer2 = NeuronGroup(12, eqs, threshold='vm>vt', reset='vm = vr')

layer2 = NeuronGroup(12, model=eqs, threshold='vm>Vcut', reset="vm=Vr; wa+=b")

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
    layer1.I = CURRENT*nA # SET TO SPECIFIC CELLS

    
    

    

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
#plot(statemonHidden.t/ms, statemonHidden.vm[0])

    
v = statemonHidden[0].vm[:]
for t in spikesHidden.t:
    i = int(t / defaultclock.dt)
    v[i] = 20*mV
plot(statemonHidden.t / ms, v / mV)
show()

#subplot(222)

    


