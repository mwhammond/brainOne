
from brian2 import *
import time

INPUT = np.zeros(4)
OUTPUT = np.zeros(4)
iE = []
tE = []

group1Cells = 100

propInhib = 0.2 # proportion of inhbitory cells
NE = group1Cells # Number of excitatory cells
NI = int(math.ceil(NE*propInhib))        
print "%d excitatory neurons" % NE
print "%d inhibitory neurons" % NI

eeE = NE-NI
inputElectrodes = [0,1,2,3]
#outputElectrodes = [0,1,2,3]
outputElectrodes = [eeE-4, eeE-3, eeE-2, eeE-1]

print inputElectrodes
print outputElectrodes





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





taum, taue, taui = 10*ms, 2*ms, 25*ms

# Pick an electrophysiological behaviour
#tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + backgroundCurrent + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
backgroundCurrent: amp
rates : Hz  # each neuron's input has a different rate
I = 1*sin(rates*t)*nA : amp
"""


group1 = NeuronGroup(group1Cells, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")

group1.backgroundCurrent = 'rand()/10*pA' # add level of bg noise

Pe = group1[:NE] # set all to excitatory
Pi = group1[NE-NI:] # everything after is inhibitory

#==============================================



Se = Synapses(Pe, group1,
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

Se.connect(True, p=0.7)
Se.we = 'rand()'
#Se.Dopamine = 0


# LINK THE DOPAMINE ACROSS ALL SYNAPSES IN TIME


Si = Synapses(Pi, group1,
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









############################################


#P = PoissonInput(Pe[:1], 'vm', 1, 20*Hz, weight=60*mV)



#Pe.rates = '1*Hz + i*Hz'
#Pe.size = '(100-i)/100. + 0.1'


traceE = StateMonitor(Pe, 'vm', record=[15])
spikesE = SpikeMonitor(Pe)


# ACCESS THE VALUES BEING RECORDED AND STIM
@network_operation(dt=100*ms)
def update_active(): 
    global RATEIN
    global OUTPUT
    global iE, tE

    # SET INPUT
    loops = 0
    for i in inputElectrodes:
        Pe.rates[i] = INPUT[loops]*Hz
        loops +=1    
    
    print "input electrodes:"
    print INPUT
    

    #READ OUTPUT
    iE, tE = spikesE.it
    # get all of the indexes in last 100ms
    #print 'dt: ', Pe.clock.t
    lastPeriodSpikes = iE[tE>Pe.clock.t-100*ms]
    # find how many times each channel fired
    unique, counts = np.unique(lastPeriodSpikes, return_counts=True)
    countsArray = np.asarray((unique, counts))
    # just uses neurons 0-3 at the moment, might want to define sequence later
    loops = 0
    for i in outputElectrodes:
        val = countsArray[1,np.nonzero(countsArray[0,:] == i)]
        if val > 1:
            OUTPUT[loops] = np.asscalar(val[0])
        else:
            OUTPUT[loops] = 0
        loops +=1
    
    print "output electrodes:"
    print OUTPUT        

    
def runit():    
    run(4000 *ms)  
    

    
#if __name__ == '__main__':
 #   runit()
    
#    figure()  

#    subplot(211) 
#    iE, tE = spikesE.it
#    plot(tE/ms, iE, 'k.') #ms=0.25

#    subplot(212)    
#    plot(traceE.t / ms, traceE[15].vm / mV,'k')
#    xlabel('time (ms)')
#    ylabel('membrane potential (mV)')
#    tight_layout()
#    show()  



    
    
