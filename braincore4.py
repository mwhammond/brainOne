from brian2 import *

# Parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

gmax = 2
taupre = 20*ms
taupost = taupre
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

propInhib = 0.2 # proportion of inhbitory cells
NE = 20          # Number of excitatory cells
NI = int(math.ceil(NE*propInhib))         # Number of inhibitory cells
print NE
print "excitatory neurons"
print NI
print "inhibitory neurons"

# Pick an electrophysiological behaviour
tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
I : amp
"""


neuron2 = NeuronGroup(NE, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")


#neuron2.vm =  'rand() * EL'



Pe = neuron2[:NE] # set all to excitatory
Pi = neuron2[NE-NI:] # everything after is inhibitory

traceE = StateMonitor(Pe, 'vm', record=[0,5,10])
spikesE = SpikeMonitor(Pe)

traceI = StateMonitor(Pi, 'vm', record=[0,1])
spikesI = SpikeMonitor(Pi)

# THEN ADD WEIGHT TRACE FOR INHIB


#run(20 * ms)

#run(100 * ms)
#neuron1.I = 0*nA
#run(20 * ms)

#S = Synapses(neuron1, neuron2, model='we : volt', pre='vm += we')
#S.connect([0,1],0)
#S.we = 2 *mV

Se = Synapses(Pe, neuron2,
              '''we : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''vm += we * mV
                    Apre += dApre
                    we = clip(we + Apost, 0, gmax)''',
             post='''Apost += dApost
                     we = clip(we + Apre, 0, gmax)''')

Se.connect('i!=j', p=0.8)
Se.we = 'rand() * gmax'


Si = Synapses(Pi, neuron2,
              '''wi : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''vm -= wi * mV
                    Apre += dApre
                    wi = clip(wi + Apost, 0, gmax)''',
             post='''Apost += dApost
                     wi = clip(wi + Apre, 0, gmax)''')

Si.connect('i!=j', p=0.2)
Si.wi = 'rand() * gmax'











mon = StateMonitor(Se, 'we', record=[0, 1])
spikesE = SpikeMonitor(Pe)
spikesI = SpikeMonitor(Pi)


#@network_operation(dt=100*ms)
#def update_active():
#    print("inject")
    #print defaultclock.t
    #global INPUT
    #global OUTPUT
    # SET INPUT ACCORDING TO BOARD PIXEL VALUE
    #print "Printing INPUT from braincore: {}".format(INPUT)
    #print "Printing INPUT from braincore: {}".format(INPUT[0,0])
    #Pe.I = 1*nA
 #   for i in range (0,4):
  #      Pe.I_[i] = 1*nA
        
        
# NEXT STEPS #############################
#SET A STATIC CURRENT TO SEPERATE SPIKING TYPE FROM CURRENT TIME
#COMBINE SPIKES OF EXCITATORY AND INHIB ON SAME RASTER
#ADD GRAPH OF INHIB WEIGHTS
#FIX BLOODY AXIS
        
        
        
#neuron2.I = 1*nA  
neuron2.I = 'rand() *nA'
run(500 *ms)        


### TRACES #####
# We draw nicer spikes
    
vmE = traceE[0].vm[:]
for t in spikesE.t:
    i = int(t / defaultclock.dt)
    vmE[i] = 20*mV
    
vmI = traceI[0].vm[:]
for t in spikesI.t:
    i = int(t / defaultclock.dt)
    vmI[i] = 20*mV
    
################


figure()  

subplot(311) 
iE, tE = spikesE.it
plot(tE/ms, iE, 'k.') #ms=0.25
# overlay inhib 
iI, tI = spikesI.it
plot(tI/ms, iI, 'r.') #ms=0.25

subplot(312)    
plot(traceE.t / ms, vmE / mV,'k')
# overlay inhib  
plot(traceI.t / ms, vmI / mV,'r')
xlabel('time (ms)')
ylabel('membrane potential (mV)')

subplot(313) 
plot(mon.t/second, mon.we.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
tight_layout()






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

visualise_connectivity(Se)

show()