from brian2 import *
#prefs.codegen.cpp.compiler = 'gcc'
#set_device('cpp_standalone')

N = 36
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

eqs = """
dv/dt = (gL*(EL - v) + gL*DeltaT*exp((v - VT)/DeltaT) + I - w)/C : volt
dw/dt = (a*(v - EL) - w)/tauw : amp
I : amp
"""

input = PoissonGroup(N, rates=F)
neurons = NeuronGroup(1, eqs_neurons, threshold='v>vt', reset='v = vr')
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

run(1*second, report='text')
#device.build(directory='STDP_standalone', compile=True, run=True, debug=True)

subplot(411)
plot(S.w / gmax, '.k')
ylabel('Weight / gmax')
xlabel('Synapse index')
subplot(412)
hist(S.w / gmax, 20)
xlabel('Weight / gmax')
subplot(413)
plot(mon.t/second, mon.w.T/gmax)
xlabel('Time (s)')
ylabel('Weight / gmax')
tight_layout()
subplot(414)
plot(s_mon.t/ms, s_mon.i, '.k')

show()