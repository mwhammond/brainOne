from brian2 import *

# Parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -60 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

# Pick an electrophysiological behaviour
tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking
tau = 5*ms
eqsG = '''
dv/dt = (1-v)/tau : volt
'''

eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
I : amp
"""

G = NeuronGroup(36, eqs, threshold='v>0.8', reset='v = 0', refractory=15*ms)


neuron = NeuronGroup(10, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")
neuron.vm = EL


#run(20 * ms)
#neuron.I = 1*nA
#run(100 * ms)
#neuron.I = 0*nA




#G.rates = '30*Hz'
#G.size = '0.5*nA'

#P = PoissonGroup(100, np.arange(100)*Hz + 100*Hz)

#S = Synapses(inputGroup, hidden1Group, pre='V += -J')

#convergence = inputNeurons/hidden1Neurons
#for i in range(0, inputNeurons, convergence):
#    S1.connect(list(range(i,i+convergence)),i/convergence) 
spikemon2 = SpikeMonitor(G)
trace = StateMonitor(G, 'v', record=0)
spikemon = SpikeMonitor(neuron)
    
S = Synapses(G, neuron, pre='vm+=0.15*mV')
S.connect(True, p=0.7)

run(1000 * ms)

# We draw nicer spikes
v = trace[0].v[:]
for t in spikemon.t:
    i = int(t / defaultclock.dt)
    v[i] = 20*mV
    

figure()
subplot(221)
plot(spikemon.t/ms, spikemon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')


subplot(222)
plot(spikemon2.t/ms, spikemon2.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(223)
plot(trace.t / ms, v / mV)
xlabel('time (ms)')
ylabel('membrane potential (mV)')

#plot(trace.t/ms, trace[0].vm/mV)
#plot(trace.t/ms, trace[4].v/mV)
#plot(trace.t/ms, trace[7].v/mV)
#xlabel('t (ms)')
#ylabel('v (mV)')
show()