
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
tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(vm - EL) - w)/tauw : amp
backgroundCurrent: amp
rates : Hz  # each neuron's input has a different rate
I = 1*sin(rates*t)*nA : amp
"""


Pe = NeuronGroup(100, model=eqs, threshold='vm>Vcut',
                     reset="vm=Vr; w+=b")

#==============================================


#P = PoissonInput(Pe[:1], 'vm', 1, 20*Hz, weight=60*mV)



Pe.rates = '1*Hz + i*Hz'
#Pe.size = '(100-i)/100. + 0.1'


traceE = StateMonitor(Pe, 'vm', record=[15])
spikesE = SpikeMonitor(Pe)


@network_operation(dt=1000*ms)
def update_active():
    Pe.rates = '1*Hz + i*Hz'
    print "switch"


run(10000 *ms)  
    
figure()  

subplot(211) 
iE, tE = spikesE.it
plot(tE/ms, iE, 'k.') #ms=0.25


subplot(212)    
plot(traceE.t / ms, traceE[15].vm / mV,'k')
xlabel('time (ms)')
ylabel('membrane potential (mV)')


tight_layout()

show()