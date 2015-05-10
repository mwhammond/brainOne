from brian2 import *

N = 20
taum = 10*ms
taupre = 20*ms
taupost = taupre
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms
F = 15*Hz
gmax = .01
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

input = NeuronGroup(10, eqs_neurons, threshold='v>vt', reset='v = vr')

neurons = NeuronGroup(10, eqs_neurons, threshold='v>vt', reset='v = vr')


S = Synapses(input, neurons,
             '''w : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             pre='''ge += w
                    Apre += dApre
                    w = clip(w + Apost, 0, gmax)''',
             post='''Apost += dApost
                     w = clip(w + Apre, 0, gmax)''',
             connect=True,
             )
S.w = 'rand() * gmax'
mon = StateMonitor(S, 'w', record=[0, 1])
s_mon = SpikeMonitor(input)
r_mon = PopulationRateMonitor(input)

trace = StateMonitor(input, 'v', record=[0, 1, 4])

run(10*second, report='text')


@network_operation(dt=100*ms)
def update_active():
    #print defaultclock.t
    #global INPUT
    #global OUTPUT
    # SET INPUT ACCORDING TO BOARD PIXEL VALUE
    #print "Printing INPUT from braincore: {}".format(INPUT)
    #print "Printing INPUT from braincore: {}".format(INPUT[0,0])
    for i in range (0,4):
        input.I_[i] = 100
        #P.bgcurrent_[i] = 10*INPUT[i,0]*pA

subplot(411)
plot(trace.t/ms, trace[0].v /mV)
plot(trace.t/ms, trace[1].v /mV)
plot(trace.t/ms, trace[4].v /mV)
xlabel('t (ms)')
ylabel('v (mV)')

subplot(412)
plot(S.w / gmax, '.k')
ylabel('Weight / gmax')
xlabel('Synapse index')
subplot(413)
hist(S.w / gmax, 20)
xlabel('Weight / gmax')
subplot(414)
plot(mon.t/second, mon.w.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
tight_layout()
show()