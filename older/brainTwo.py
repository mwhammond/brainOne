from brian2 import *

# Neuron parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

# Pick an electrophysiological behaviour
#tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

# Define low spiking unit

eqs = """
dv/dt = (gL*(EL - v) + gL*DeltaT*exp((v - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(v - EL) - w)/tauw : amp
I : amp
"""

hidden1 = NeuronGroup(10, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")
hidden1.v = EL

#hidden1 = NeuronGroup(10, eqs, threshold='v> -60*mV', reset='v = -70*mV', refractory=2*ms, #method='euler', name='hidden1')

spikemon = SpikeMonitor(hidden1)
trace = StateMonitor(hidden1, 'v', record=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])



# Define single synapse
# Define two groups
# Define poisson input

P = PoissonGroup(100, np.arange(100)*Hz + 100*Hz)

#S = Synapses(inputGroup, hidden1Group, pre='V += -J')

#convergence = inputNeurons/hidden1Neurons
#for i in range(0, inputNeurons, convergence):
#    S1.connect(list(range(i,i+convergence)),i/convergence) 
    
    
S = Synapses(P, hidden1, pre='v+=0.2*mV')
S.connect(True, p=0.7)

# Define custom input
# Expand to multiple groups
hidden1.I = 1*nA
run(500*ms)


figure()
subplot(121)
plot(spikemon.t/ms, spikemon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(122)
plot(trace.t/ms, trace[0].v/mV)
plot(trace.t/ms, trace[4].v/mV)
#plot(trace.t/ms, trace[7].v/mV)
xlabel('t (ms)')
ylabel('v (mV)')

#visualise_connectivity(S1)
#visualise_connectivity(S2)
#visualise_connectivity(S3)
show(block=True)