from brian2 import *
import time

print "creating network"

OUTPUT = np.zeros((4,1))
INPUT = np.zeros((36,1))


theta = 5*mV
Vr = 10*mV
tau = 20*ms
muext = 25*mV
sigmaext = 1*mV
we = 2*mV


C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT
duration = 50000*ms

# Pick an electrophysiological behaviour
#tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dv/dt = (gL*(EL - v) + gL*DeltaT*exp((v - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(v - EL) - w)/tauw : amp
I : amp
"""


#  I = sin(2*pi*rate*t) : 1

##### GROUP CREATION #####
G = NeuronGroup(36, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")

# Multiple groups because spike tracking can't be cleared so use single count variable
output1Group = NeuronGroup(1, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")

output2Group = NeuronGroup(1, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")

output3Group = NeuronGroup(1, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")

output4Group = NeuronGroup(1, model=eqs, threshold='v>Vcut',
                     reset="v=Vr; w+=b")


##### GROUP CREATION #####



##### CREATE CONNECTIONS ######

S1 = Synapses(G, output1Group, model='w:volt', pre='v_post += we')
S1.connect('i!=j')
S1.w = 'rand()*mV'

S2 = Synapses(G, output2Group, model='w:volt', pre='v_post += we')
S2.connect('i!=j')
S2.w = 'rand()*mV'

S3 = Synapses(G, output3Group, model='w:volt', pre='v_post += we')
S3.connect('i!=j')
S3.w = 'rand()*mV'

S4 = Synapses(G, output4Group, model='w:volt', pre='v_post += we')
S4.connect('i!=j')
S4.w = 'rand()*mV'

##### CREATE CONNECTIONS ######




##### MONITORING #####

#statemon0 = StateMonitor(G, 'v', record=True)
#statemon1 = StateMonitor(output1Group, 'v', record=True)


#inputSpikes = SpikeMonitor(G, rec) 
out1Spikes = SpikeMonitor(output1Group, record=False)
out2Spikes = SpikeMonitor(output2Group, record=False)
out3Spikes = SpikeMonitor(output3Group, record=False)
out4Spikes = SpikeMonitor(output4Group, record=False)

#out1Rate = PopulationRateMonitor(output1Group)

#def printHello():
#    print "hello" 

##### MONITORING #####



@network_operation(dt=500*ms)
def update_active():
    #print defaultclock.t
    global INPUT
    global OUTPUT

    
    # SET INPUT ACCORDING TO BOARD PIXEL VALUE
    #print "Printing INPUT from braincore: {}".format(INPUT)
    #print "Printing INPUT from braincore: {}".format(INPUT[0,0])
    for i in range (0,35):
        G.I_[i] = 10*INPUT[i,0]*nA
 

    # GET OUTPUT AND SEND TO WORLD TO DECIDE ON MOVE
    #print out1Spikes.i
    
    OUTPUT[0,0] = out1Spikes.count
    OUTPUT[1,0] = out2Spikes.count
    OUTPUT[2,0] = out3Spikes.count
    OUTPUT[3,0] = out4Spikes.count

    
    #OUTPUT[1,0] = len(np.equal(out1Spikes.i, 1))
    #OUTPUT[2,0] = len(np.equal(out1Spikes.i, 2))
    #OUTPUT[3,0] = len(np.equal(out1Spikes.i, 3))
    
    #out1Spikes.reinit() # clears recorded spikes
    
    #print "Printing MOVE from braincore: {}".format(OUTPUT)
    #print "Spike count on onput 1: {}".format(out1Spikes.num_spikes)
    #print INPUT
    #print OUTPUT
    
    # PROBLEMS
    # NOT ACTUALLY DOING MOVE
    # OUTPUT SEEM TO JUST BE COUNT OF SPIKE, IDENTICAL ON ALL - because it needs indexing see e.g.
    # SEEMS TO STOP AFTER A FEW MINUTES
    # 2s BEING FLATTENED TO 1S
    
    
    
def runit():
    run(duration)



##### PLOTTING ####


#def visualise_connectivity(S):
#    Ns = len(S.source)
#    Nt = len(S.target)
#    figure(figsize=(10, 4))
#    subplot(121)
#    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
#    plot(ones(Nt), arange(Nt), 'ok', ms=10)
#    for i, j in zip(S.i, S.j):
#        plot([0, 1], [i, j], '-k')
#    xticks([0, 1], ['Source', 'Target'])
#    ylabel('Neuron index')
#    xlim(-0.1, 1.1)
#    ylim(-1, max(Ns, Nt))
#    subplot(122)
#    plot(S.i, S.j, 'ok')
 #   xlim(-1, Ns)
#    ylim(-1, Nt)
#    xlabel('Source neuron index')
#    ylabel('Target neuron index')
    


#figure()
#subplot(221)
#plot(inputSpikes.t/ms, inputSpikes.i, '.k')
#title('input')
#xlabel('Time (ms)')
#ylabel('Neuron index')

#subplot(222)
#v = statemon0[4].v[:]
#for t in inputSpikes.t:
#    i = int(t / defaultclock.dt)
#    v[i] = 20*mV

#plot(statemon0.t / ms, v / mV)
    
#plot(statemon0.t/ms, statemon0.v[0])



#for t in inputSpikes.t:
#    axvline(t/ms, ls='--', c='r', lw=3)
#axhline(G.threshold_[0], ls=':', c='g', lw=3)
#xlabel('Time (ms)')
#ylabel('v')
#print "Spike times:", spikemon.t[8]

#subplot(223)
#window = 100*ms
#plot(out1Spikes.t/ms, out1Spikes.i, '.k')
#title('output spike times')
#xlabel('Time (ms)')
#ylabel('Rate / Hz')

#subplot(224)
#v = statemon1[1].v[:]
#for t in out1Spikes.t:
#    i = int(t / defaultclock.dt)
#    v[i] = 20*mV

#plot(statemon0.t / ms, v / mV)



#visualise_connectivity(S1)


#show()