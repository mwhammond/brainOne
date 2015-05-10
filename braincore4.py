from brian2 import *

# Parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

gmax = 10
taupre = 20*ms
taupost = taupre
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

# Pick an electrophysiological behaviour
tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
I : amp
"""

neuron1 = NeuronGroup(10, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")

neuron2 = NeuronGroup(5, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")

neuron1.vm = EL
trace1 = StateMonitor(neuron1, 'vm', record=0)
spikes1 = SpikeMonitor(neuron1)

neuron2.vm = EL
trace2 = StateMonitor(neuron2, 'vm', record=0)
spikes2 = SpikeMonitor(neuron2)



#run(20 * ms)
#neuron1.I = 1*nA
#run(100 * ms)
#neuron1.I = 0*nA
#run(20 * ms)

#S = Synapses(neuron1, neuron2, model='we : volt', pre='vm += we')
#S.connect([0,1],0)
#S.we = 2 *mV

S = Synapses(neuron1, neuron2,
              '''we : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''vm += we * mV
                    Apre += dApre
                    we = clip(we + Apost, 0, gmax)''',
             post='''Apost += dApost
                     we = clip(we + Apre, 0, gmax)''',
              connect=True)

S.we = 'rand() * gmax'

mon = StateMonitor(S, 'we', record=[0, 1])
spikes = SpikeMonitor(neuron2)


@network_operation(dt=100*ms)
def update_active():
    print("inject")
    #print defaultclock.t
    #global INPUT
    #global OUTPUT
    # SET INPUT ACCORDING TO BOARD PIXEL VALUE
    #print "Printing INPUT from braincore: {}".format(INPUT)
    #print "Printing INPUT from braincore: {}".format(INPUT[0,0])
    neuron1.I = 1*nA
    #for i in range (0,4):
     #   neuron1.I_[i] = 2*nA
        
        

        
        
        
        
run(500 *ms)        

# We draw nicer spikes
vm1 = trace1[0].vm[:]
for t in spikes1.t:
    i = int(t / defaultclock.dt)
    vm1[i] = 20*mV
    
vm2 = trace2[0].vm[:]
for t in spikes2.t:
    i = int(t / defaultclock.dt)
    vm2[i] = 20*mV

figure()    
subplot(411)    
plot(trace1.t / ms, vm1 / mV)
xlabel('time (ms)')
ylabel('membrane potential (mV)')

subplot(412)    
plot(trace1.t / ms, vm2 / mV)
xlabel('time (ms)')
ylabel('membrane potential (mV)')


subplot(413) 
plot(mon.t/second, mon.we.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
tight_layout()

subplot(414) 
i, t = spikes.it
plot(t/ms, i, 'k.') #ms=0.25



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

visualise_connectivity(S)

show()