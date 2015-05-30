from brian2 import *
import time


# Parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -70.4 * mV # manually changed this
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT
print "threshold"
print Vcut

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
NE = 50          # Number of excitatory cells
NI = int(math.ceil(NE*propInhib))         # Number of inhibitory cells
print NE
print "excitatory neurons"
print NI
print "inhibitory neurons"

taum, taue, taui = 10*ms, 2*ms, 25*ms

# Pick an electrophysiological behaviour
tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

# STIM GROUP IS A MORE BASIC CELL WITH NO ADAPTION TO ENABLE A LINEAR RELATIONSHIP WITH SPIKING

taus = 100*ms


eqsStim = '''
dvm/dt = (1-vm) / taus : 1 (unless refractory)
taus : second
'''

#dv/dt = (1-v)/tau : 1
    

stimGroup = NeuronGroup(10, eqsStim, threshold='vm>0.8', reset='vm = 0', refractory=5*ms)

# STILL NOT SURE THAT THIS BASIC STIM IS ANY DIFFERENT USESING THE SAME UNITS AS THE OTHER - THE PROFILE LOOKS THE SAME?!
# NEXT CONNECT THE STIM GROUP TO A SUBSET OF NEURONS!




eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + backgroundCurrent + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
backgroundCurrent: amp
rates : Hz  # each neuron's input has a different rate
I = 1*sin(rates*t)*nA : amp
"""


neuron2 = NeuronGroup(NE, model=eqs, threshold='vm>Vcut', refractory=1*ms,
                     reset="vm=Vr; w+=b")


neuron2.backgroundCurrent = 'rand()/10*nA' # add level of bg noise

Pe = neuron2[:NE] # set all to excitatory
Pi = neuron2[NE-NI:] # everything after is inhibitory
InputGroup = neuron2[:9]


#   LEFT AT WTF IS GOING ON WITH THE SYNAPSE PROPOGATION AND THRESHOLD?????
##################################
##################################
# INPUT ALL SET UP, COPY OVER FROM HERE ONCE WORK THIS OUT


S = Synapses(stimGroup, InputGroup, pre='vm += 0.3 * mV')
S.connect('i!=j', p=1.0)




Se = Synapses(Pe, neuron2,
              '''we : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)
                dDopamine/dt = -Dopamine/dopTime : 1
                ''',
             pre='''vm += we * mV
                    Apre += dApre
                    we = clip(we + Apost, 0, EPSPmax)*1''',
             post='''Apost += dApost
                     we = clip(we + Apre, 0, EPSPmax)*1''')

Se.connect('i!=j', p=0.3)
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




Si.connect('i!=j', p=0.3)
Si.wi = 'rand()'







#################################################
########### NETWORK UPDATES #####################




@network_operation(dt=1000*ms)
def update_active():
    print("stim")

    
    stimGroup.taus[0] = 10 * ms
    stimGroup.taus[1] = 15 * ms
    stimGroup.taus[2] = 10 * ms
    stimGroup.taus[3] = 10 * ms

    stimGroup.taus[4] = 1 * ms
    stimGroup.taus[5] = 10 * ms
    stimGroup.taus[6] = 10 * ms
    stimGroup.taus[7] = 15 * ms

    stimGroup.taus[8] = 10 * ms
    stimGroup.taus[9] = 10 * ms

    
    Se.Dopamine = clip(Se.Dopamine + dopAmount, 0, dopMax)
    
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

#traceE = StateMonitor(neuron2, 'vm', record=[60])
spikesE = SpikeMonitor(Pe)
spikesStim = SpikeMonitor(stimGroup)
spikesInput = SpikeMonitor(InputGroup)
spikesI = SpikeMonitor(Pi)

monE = StateMonitor(Pe, 'vm', record=[15])
monI = StateMonitor(Pi, 'vm', record=[0])


monInputs = StateMonitor(InputGroup, 'vm', record=[2])

monEW = StateMonitor(Se, 'we', record=[0,1])
monIW = StateMonitor(Si, 'wi', record=[0,1])

monD = StateMonitor(Se, 'Dopamine', record=[0,1])



####################################################
    
    
run(3000 *ms)    


### TRACES ######################################

    


figure()  

subplot(211) 
iE, tE = spikesE.it
plot(tE/ms, iE, 'k.') #ms=0.25
# overlay inhib 

iI, tI = spikesI.it
plot(tI/ms, iI, 'r.') #ms=0.25

iS, tS = spikesStim.it
plot(tS/ms, iS, 'g.') #ms=0.25


iIn, tIn = spikesInput.it
plot(tIn/ms, iIn, 'y.') #ms=0.25





ax1 = subplot(212)    
#plot(traceE.t / ms, vmE / mV,'k')
# overlay inhib  
#plot(traceI.t / ms, vmI / mV,'r')

plot(monE.t/ms, monE[15].vm/mV, '-k', label='e')

plot(monI.t/ms, monI[0].vm/mV, '-r', label='i')

plot(monInputs.t/ms, monInputs[2].vm/mV, '-y', label='inputs')

     
     
ax1.set_ylim([-80, -50])
#ax1.set_xlim([0, 1000])

xlabel('time (ms)')
ylabel('membrane ptential (mV)')
legend(loc='best')



figure()

subplot(311) 
plot(monEW.t/second, monEW.we.T/EPSPmax,'k')
plot(monIW.t/second, monIW.wi.T/IPSPmax,'r')
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