
from brian2 import *
import time

RATEIN = 1
iE = []
tE = []


# Parameters
#C = 281 * pF
#gL = 30 * nS
#taum = C / gL
#EL = -70.6 * mV
#VT = -50.4 * mV
#DeltaT = 2 * mV
#Vcut = VT + 5 * DeltaT

taum = 10*ms

Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms


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



NE = 10          # Number of excitatory cells



#taum, taue, taui = 10*ms, 2*ms, 25*ms

# Pick an electrophysiological behaviour
#tauw, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

#eqs = """
#dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - VT)/DeltaT) + I)/C : volt
#backgroundCurrent: amp
#rates : Hz  # each neuron's input has a different rate
#I = 1*sin(rates*t)*nA : amp
#"""

tau = 10*ms
eqs = '''
dvm/dt = (1-vm + I) /tau : 1 (unless refractory)
rates : Hz  # each neuron's input has a different rate
I = 1*sin(rates*t) : 1
'''

Pe = NeuronGroup(4, eqs, threshold='vm>0.8', reset='vm = 0', refractory=5*ms)



#Pe = NeuronGroup(10, model=eqs, threshold='vm>Vcut', refractory=5*ms,
#                     reset="vm=Vr")

#Pe = NeuronGroup(10, eqs_neurons, threshold='v>vt', reset='v = vr')

#==============================================


#P = PoissonInput(Pe[:1], 'vm', 1, 20*Hz, weight=60*mV)



Pe.rates[0] = 1*Hz
Pe.rates[1] = 10*Hz
Pe.rates[2] = 50*Hz
Pe.rates[3] = 100*Hz





#Pe.size = '(100-i)/100. + 0.1'



# ACCESS THE VALUES BEING RECORDED AND STIM
@network_operation(dt=100*ms)
def update_active():
    global RATEIN
    global iE, tE
    #Pe.rates = 'RATEIN*Hz'
    #Pe.rates = 'RATEIN*Hz + i*Hz'
    #print RATEIN
    # THE AIM WAS TOC CHANGE THE RATE ON THE 
    #iE, tE = spikesE.it

    #print iE

    

spikesE = SpikeMonitor(Pe)
M = StateMonitor(Pe, 'vm', record=True)


    
   
run(250 *ms)  
    

    
figure()  

ax2 = subplot(211) 
iE, tE = spikesE.it
plot(tE/ms, iE, 'b.') #ms=0.25
# overlay inhib 
ax2.set_ylim([-1, 5])

ax1 = subplot(212)    
#plot(traceE.t / ms, vmE / mV,'k')
# overlay inhib  
#plot(traceI.t / ms, vmI / mV,'r')

plot(M.t/ms, M.vm[0]/mV, '-c', label='1 Hz')
plot(M.t/ms, M.vm[1]/mV, '-y', lw=2, label='10 Hz')
plot(M.t/ms, M.vm[2]/mV, '-b', lw=2, label='50 Hz')
plot(M.t/ms, M.vm[3]/mV, '-r', lw=2, label='100 Hz')


     
#ax1.set_ylim([-80, -50])
#ax1.set_xlim([0, 1000])

xlabel('time (ms)')
ylabel('membrane ptential (mV)')
legend(loc='best')

show()



    
    
