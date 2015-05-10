from brian2 import *
import math

# Parameters
C = 281 * pF # Membrane capacitance
gL = 30 * nS # Leak conductanc
er = -80*mV # Inhibitory reversal potential
#taum = C / gL

VT = -50.4 * mV # Spiking threshold
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT
bgcurrent = 0*pA #200*pA   # External current
propInhib = 0.2 # proportion of inhbitory cells
NE = 50          # Number of excitatory cells
NI = int(math.ceil(NE*propInhib))         # Number of inhibitory cells
print NE
print "excitatory neurons"
print NI
print "inhibitory neurons"
tau_ampa = 5.0*ms   # Glutamatergic synaptic time constant
tau_gaba = 10.0*ms  # GABAergic synaptic time constant
epsilon = 0.02      # Sparseness of synaptic connections
tau_stdp = 20*ms    # STDP time constant

simtime = 10*second # Simulation time
we = 6*nS  # excitatory synaptic weight
wi = 67*nS  # inhibitory synaptic weight
taue = 5*ms # inhibitory time constant
taui = 10*ms # excitatory time constant

gl = 10.0*nsiemens   # Leak conductance
el = -60*mV          # Resting potential
er = -80*mV          # Inhibitory reversal potential
vt = -50.*mV         # Spiking threshold

gmax = .01
taupre = 20*ms
taupost = taupre
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax


Ee = 0*mV
vr = -60*mV
El = -74*mV # Resting potential
vt = -54*mV
vr = -60*mV
taum = 10*ms

###################
##### MODEL #######
###################

# Pick an electrophysiological behaviour
tauw1, a, b, Vr = 144*ms, 4*nS, 0.0805*nA, -70.6*mV # Regular spiking (as in the paper)
#tauw1,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw1,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

#eqs = """
#dv/dt = ((gl+ge+gi)*(el - v) + gl*DeltaT*exp((v - VT)/DeltaT) + bgcurrent + I - w1)/C : volt
#dw1/dt = (a*(v - el) - w1)/tauw1 : amp
#dge/dt = -ge*(1./taue) : siemens
#dgi/dt = -gi*(1./taui) : siemens
#I : amp
#"""
#dv/dt=(-gl*(v-el)-(ge*v+gi*(v-er)) + gL*DeltaT*exp((v - VT)/DeltaT) + bgcurrent + I - w1)/C : volt
#dv/dt = (gL*(ge+gi+EL - v) + gL*DeltaT*exp((v - VT)/DeltaT) + bgcurrent + I - w)/C : volt

eqs = '''
dv/dt = (ge * (Ee-vr) + El - v) + I / taum : volt
dge/dt = -ge / taue : 1
I : 1
'''


#dg_ampa/dt = -g_ampa/tau_ampa : siemens
#dg_gaba/dt = -g_gaba/tau_gaba : siemens

####################
##### NETWORK ######
####################



P = NeuronGroup(NE, model=eqs, threshold='v>vt',reset="v=vr", refractory=5*ms)
#P = NeuronGroup(NE+NI, model=eqs, threshold='v>Vcut',reset="v=Vr; w1+=b", refractory=5*ms)
#neurons = NeuronGroup(NE+NI, model=eqs_neurons, threshold='v > vt',reset='v=el', refractory=5*ms)


####################
##### SYNAPSES #####
####################

Pe = P[:NE] # set all to excitatory
Pi = P[NE-NI:] # everything after is inhibitory


Ce = Synapses(Pe, P,
              '''w : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''ge += w
                    Apre += dApre
                    w = clip(w + Apost, 0, gmax)''',
             post='''Apost += dApost
                     w = clip(w + Apre, 0, gmax)''',
              connect=True)


#Ci = Synapses(Pi, P,
#              '''w : 1
#                dApre/dt = -Apre / taupre : 1 (event-driven)
#                dApost/dt = -Apost / taupost : 1 (event-driven)''',
#             pre='''gi += w
#                    Apre += dApre
#                    w = clip(w + Apost, 0, gmax)''',
#             post='''Apost += dApost
#                     w = clip(w + Apre, 0, gmax)''',
#              connect=True)



# w was ns  

#Ci = Synapses(Pi, P, pre='gi+=wi', connect='rand()<0.1')

# initalise

#P.v = 'el + (randn() * 5 - 5)*mV'
#P.ge = '(randn() * 1.5 + 4) * 10.*nS'
#P.gi = '(randn() * 12 + 20) * 10.*nS'
Ce.w = 'rand() * gmax'
#Ci.w = 'rand() * gmax'


#####################
##### INPUT ######
#####################


@network_operation(dt=100*ms)
def update_active():
    #print defaultclock.t
    #global INPUT
    #global OUTPUT
    # SET INPUT ACCORDING TO BOARD PIXEL VALUE
    #print "Printing INPUT from braincore: {}".format(INPUT)
    #print "Printing INPUT from braincore: {}".format(INPUT[0,0])
    for i in range (0,4):
        P.I_[i] = 100
        #P.bgcurrent_[i] = 10*INPUT[i,0]*pA


#####################
##### PLOTTING ######
#####################


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


# Record a few traces
trace = StateMonitor(P, 'v', record=[0, 1, 4])
spikes = SpikeMonitor(P)
mon = StateMonitor(Ce, 'w', record=[0, 1, 4])
visualise_connectivity(Ce)

run(2 * second, report='text')



figure()
i, t = spikes.it
subplot(411)
plot(t/ms, i, 'k.') #ms=0.25

subplot(412)
plot(trace.t/ms, trace[0].v /mV)
plot(trace.t/ms, trace[1].v /mV)
plot(trace.t/ms, trace[4].v /mV)
xlabel('t (ms)')
ylabel('v (mV)')

#subplot(323)
#plot(Ce.w / gmax, '.k')
#ylabel('Weight / gmax')
#xlabel('Synapse index')



subplot(413)
plot(mon.t/second, mon.w.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
tight_layout()

subplot(414)
hist(Ce.w / gmax, 20)
xlabel('Weight / gmax')





    
show()
