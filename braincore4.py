from brian2 import *
import time

# Parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

EPSPmax = 1
IPSPmax = 1

taupre = 20*ms
taupost = taupre

dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= EPSPmax
dApre *= EPSPmax


dopTime = 200*ms
dDopamine = 0
dopMax = 2
dopAmount = 0.2



propInhib = 0.2 # proportion of inhbitory cells
NE = 20          # Number of excitatory cells
NI = int(math.ceil(NE*propInhib))         # Number of inhibitory cells
print NE
print "excitatory neurons"
print NI
print "inhibitory neurons"

taum, taue, taui = 10*ms, 2*ms, 25*ms

# Pick an electrophysiological behaviour
#tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + backgroundCurrent + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
I : amp
backgroundCurrent: amp
Dopamine : 1
"""


neuron2 = NeuronGroup(NE, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")


neuron2.backgroundCurrent = 'rand()/10*nA' # add level of bg noise
Pe = neuron2[:NE] # set all to excitatory
Pi = neuron2[NE-NI:] # everything after is inhibitory


#                


Se = Synapses(Pe, neuron2,
              '''we : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)
                ''',
             pre='''vm += we * mV
                    Apre += dApre
                    we = clip(we + Apost, 0, EPSPmax)*Dopamine''',
             post='''Apost += dApost
                     we = clip(we + Apre, 0, EPSPmax)*Dopamine''')

Se.connect(True, p=0.7)
Se.we = 'rand()'
#Se.Dopamine = 0


# LINK THE DOPAMINE ACROSS ALL SYNAPSES IN TIME


Si = Synapses(Pi, neuron2,
              '''wi : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''vm -= wi * mV
                    Apre += dApre
                    wi = clip(wi + Apost, 0, IPSPmax)''',
             post='''Apost += dApost
                     wi = clip(wi + Apre, 0, IPSPmax)''')




Si.connect(True, p=0.7)
Si.wi = 'rand()'


dop_updater = neuron2.custom_operation('''dDopamine/dt = -Dopamine/dopTime : 1''',dt=50*ms)




#################################################
########### NETWORK UPDATES #####################


@network_operation(dt=100*ms)
def update_active():
    Pe.vm[0] += 50 * mV 
    Pe.vm[1] += 50 * mV 
    Pe.vm[5] += 50 * mV 
    Pe.vm[10] += 50 * mV 
    Pe.vm[15] += 50 * mV 
    
    print("reward")
    neuron2.Dopamine = clip(neuron2.Dopamine + dopAmount, 0, dopMax)

    
    #print defaultclock.t
    #global INPUT
    #global OUTPUT
    # SET INPUT ACCORDING TO BOARD PIXEL VALUE
    #print "Printing INPUT from braincore: {}".format(INPUT)
    #print "Printing INPUT from braincore: {}".format(INPUT[0,0])
    #Pe.I = 1*nA
    #for i in range (0,4):
    # Pe.I[15] = 5 * nA # EITHER USE V OR DEGRADE CURRENT OVER TIME!
    # NEXT GET THIS TO WORK FOR MULTIPLE INPUTS AND TURN ON AND OFF
#    time.sleep(0.1)
 #   

################################################

    


################# MONITORING ######################

traceE = StateMonitor(Pe, 'vm', record=[0])
spikesE = SpikeMonitor(Pe)

traceI = StateMonitor(Pi, 'vm', record=[0])
spikesI = SpikeMonitor(Pi)

monE = StateMonitor(Se, 'we', record=[0,1])
monI = StateMonitor(Si, 'wi', record=[0,1])
monD = StateMonitor(neuron2, 'Dopamine', record=[0,1])

spikesE = SpikeMonitor(Pe)
spikesI = SpikeMonitor(Pi)

####################################################
    
    
run(1000 *ms)    


### TRACES ######################################

    
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

subplot(211) 
iE, tE = spikesE.it
plot(tE/ms, iE, 'k.') #ms=0.25
# overlay inhib 
iI, tI = spikesI.it
plot(tI/ms, iI, 'r.') #ms=0.25

subplot(212)    
plot(traceE.t / ms, vmE / mV,'k')
# overlay inhib  
#plot(traceI.t / ms, vmI / mV,'r')
xlabel('time (ms)')
ylabel('membrane potential (mV)')


figure()

subplot(311) 
plot(monE.t/second, monE.we.T/EPSPmax,'k')
plot(monI.t/second, monI.wi.T/IPSPmax,'r')
xlabel('Time (s)')
ylabel('Weight / gmax')



subplot(312)
hist(Se.we / EPSPmax, 20)
hist(Si.wi / IPSPmax, 20)
xlabel('Weight / gmax')


subplot(313) 
plot(monD.t/second, monD.Dopamine.T,'k')
xlabel('Time (s)')
ylabel('Dopamine level')

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

#visualise_connectivity(Se)

show()