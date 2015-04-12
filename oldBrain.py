from brian2 import *

theta = 5*mV
Vr = 10*mV
tau = 20*ms
muext = 25*mV
sigmaext = 1*mV
we = 1*mV
duration = 100*ms

C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

# Pick an electrophysiological behaviour
#tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dv/dt = (gL*(EL - v) + gL*DeltaT*exp((v - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(v - EL) - w)/tauw : amp
I : amp
"""

StimEqs = '''dv/dt = (-v + rate)/(10*ms) : 1
                       rate : 1  # each neuron's input has a different rate
                       active : 1  # will be set in the network function'''

Standardeqs = """
dv/dt = (-v+muext + sigmaext * sqrt(tau) * xi)/tau : volt
"""

#  I = sin(2*pi*rate*t) : 1

##### GROUP CREATION #####
G = NeuronGroup(10, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")


output1Group = NeuronGroup(4, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")


##### GROUP CREATION #####



##### CREATE CONNECTIONS ######

S1 = Synapses(G, output1Group, pre='v_post += we')
S1.connect('i!=j')

##### CREATE CONNECTIONS ######




##### MONITORING #####

statemon0 = StateMonitor(G, 'v', record=True)
statemon1 = StateMonitor(output1Group, 'v', record=True)


inputSpikes = SpikeMonitor(G, rec) 
out1Spikes = SpikeMonitor(output1Group, rec)

#out1Rate = PopulationRateMonitor(output1Group)


##### MONITORING #####


@network_operation(dt=20*ms)
def update_active():
    print defaultclock.t
    G.I_[0] = 5*nA
    G.I_[1] = 5*nA
    G.I_[2] = 0*nA
    G.I_[3] = 0*nA
    G.I_[4] = 5*nA
    G.I_[5] = 10*nA
    G.I_[6] = 0*nA
    G.I_[7] = 0*nA
    G.I_[8] = 5*nA
    G.I_[9] = 5*nA
    printHello()
    
    print out1Spikes.num_spikes
    

def printHello():
    print "Hello!"
 
#@network_operation(dt=100*ms)
#def find_active():
#    print spikemon.count
   # if  G.v_[0] > 0.1:
    #reint() clears all spikes
    #    print "Go right!"
    #if  G.v_[2] > 0.1:
     #   print "Go left!"
    
    #index = np.random.randint(10)  # index for the active neuron
    #G.active_ = 0  # the underscore switches off unit checking
    #G.active_[0] = 1

   

run(duration)

##### PLOTTING ####


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
    


figure()
subplot(221)
plot(inputSpikes.t/ms, inputSpikes.i, '.k')
title('input')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(222)
v = statemon0[4].v[:]
for t in inputSpikes.t:
    i = int(t / defaultclock.dt)
    v[i] = 20*mV

plot(statemon0.t / ms, v / mV)
    
#plot(statemon0.t/ms, statemon0.v[0])



#for t in inputSpikes.t:
#    axvline(t/ms, ls='--', c='r', lw=3)
#axhline(G.threshold_[0], ls=':', c='g', lw=3)
xlabel('Time (ms)')
ylabel('v')
#print "Spike times:", spikemon.t[8]

subplot(223)
window = 100*ms
plot(out1Spikes.t/ms, out1Spikes.i, '.k')
title('output spike times')
xlabel('Time (ms)')
ylabel('Rate / Hz')

subplot(224)
v = statemon1[1].v[:]
for t in out1Spikes.t:
    i = int(t / defaultclock.dt)
    v[i] = 20*mV

plot(statemon0.t / ms, v / mV)



visualise_connectivity(S1)


show()